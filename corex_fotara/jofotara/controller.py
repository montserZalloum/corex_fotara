# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
JoFotara Controller - Main business logic and document hooks.

Handles:
- on_submit: Triggers JoFotara submission flow
- before_cancel: Blocks cancellation of successfully submitted invoices
- Manual send via whitelist method
"""

import json
import traceback

import frappe
from frappe import _
from frappe.utils import flt, now_datetime

from corex_fotara.jofotara.api import JoFotaraAPIClient
from corex_fotara.jofotara.id_manager import JoFotaraIDManager
from corex_fotara.jofotara.xml_generator import JoFotaraXMLGenerator


def on_sales_invoice_submit(doc, method):
	"""
	Hook called on Sales Invoice submit.
	If auto-send is enabled, triggers the JoFotara submission flow.
	"""
	company = frappe.get_cached_doc("Company", doc.company)

	# Check if JoFotara is enabled for this company
	if not company.custom_enable_jofotara:
		return

	# Check if auto-send is enabled
	if not company.custom_jofotara_auto_send:
		return

	# Trigger the send process
	send_to_jofotara(doc.name)


def on_sales_invoice_cancel(doc, method):
	"""
	Hook called before Sales Invoice cancel.
	Blocks cancellation if invoice was successfully submitted to JoFotara.
	"""
	if doc.custom_jofotara_status == "Success":
		frappe.throw(
			_(
				"This invoice has been submitted to JoFotara and cannot be cancelled. "
				"Please create a Return Invoice (Credit Note) instead to maintain consistency "
				"with the government backend."
			),
			title=_("Cannot Cancel JoFotara Invoice"),
		)


@frappe.whitelist()
def send_to_jofotara(invoice_name: str):
	"""
	Main entry point for sending invoice to JoFotara.

	Phase A: Synchronous ID generation with DB locking
	Phase B: Async XML generation and API call

	Args:
		invoice_name: The name of the Sales Invoice to send
	"""
	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	company = frappe.get_cached_doc("Company", invoice.company)

	# Validation: Check if JoFotara is enabled
	if not company.custom_enable_jofotara:
		frappe.throw(_("JoFotara is not enabled for company {0}").format(invoice.company))

	# Validation: Invoice must be submitted
	if invoice.docstatus != 1:
		frappe.throw(_("Invoice must be submitted before sending to JoFotara"))

	# Validation: Already successfully sent
	if invoice.custom_jofotara_status == "Success":
		frappe.throw(_("This invoice has already been successfully sent to JoFotara"))

	# Phase A: Generate IDs (synchronous, with DB lock)
	id_manager = JoFotaraIDManager(invoice.company)
	identifiers = id_manager.generate_identifiers(invoice)

	# Commit to release the lock before async phase
	frappe.db.commit()

	current_user = frappe.session.user

	# Phase B: Enqueue async processing
	frappe.enqueue(
		"corex_fotara.jofotara.controller.process_jofotara_submission",
		queue="default",
		invoice_name=invoice_name,
		identifiers=identifiers,
		triggering_user=current_user,
		now=frappe.flags.in_test,  # Run synchronously in tests
	)

	frappe.msgprint(
		_("Invoice {0} sent to JoFotara").format(invoice_name),
		indicator="blue",
		alert=True
	)


def process_jofotara_submission(invoice_name: str, identifiers: dict, triggering_user: str = None):
	"""
	Async worker for XML generation and API submission.
	Creates JoFotara Log on completion/error.

	Args:
		invoice_name: The name of the Sales Invoice
		identifiers: Dict with jofotara_id, jofotara_uuid, jofotara_icv
	"""
	invoice = frappe.get_doc("Sales Invoice", invoice_name)
	company = frappe.get_cached_doc("Company", invoice.company)

	xml_content = None

	try:
		# Pre-submission validations
		_validate_before_submission(invoice, company)

		# Generate XML
		generator = JoFotaraXMLGenerator(invoice, company)
		xml_content = generator.generate()

		# Get secret key
		secret_key = company.get_password("custom_jofotara_secret_key")

		# Send to API
		client = JoFotaraAPIClient(
			client_id=company.custom_jofotara_client_id,
			secret_key=secret_key,
		)

		result = client.send_invoice(xml_content)

		if result["success"]:
			# Extract QR code from response (if available)
			qr_code = result["response"].get("EINV_QR") or ""

			# Update invoice status
			frappe.db.set_value(
				"Sales Invoice",
				invoice_name,
				{
					"custom_jofotara_status": "Success",
					"custom_jofotara_qr": qr_code,
				},
				update_modified=False,
			)

			# Create success log
			_create_jofotara_log(
				invoice_name=invoice_name,
				company=invoice.company,
				status="Success",
				xml=xml_content,
				response=result["response"],
			)
		else:
			# Update invoice status to Error
			frappe.db.set_value(
				"Sales Invoice",
				invoice_name,
				{"custom_jofotara_status": "Error"},
				update_modified=False,
			)

			# Create error log
			_create_jofotara_log(
				invoice_name=invoice_name,
				company=invoice.company,
				status="Error",
				xml=xml_content,
				response=result["response"],
				error=result.get("error", "Unknown error"),
			)

		frappe.db.commit()

		if triggering_user:
			frappe.publish_realtime(
				event="jofotara_submission_complete",
				message={
					"invoice_name": invoice_name,
					"status": "Success" if result["success"] else "Error"
				},
				user=triggering_user
			)

	except Exception as e:
		# Update invoice status to Error
		frappe.db.set_value(
			"Sales Invoice",
			invoice_name,
			{"custom_jofotara_status": "Error"},
			update_modified=False,
		)

		# Create error log with traceback
		_create_jofotara_log(
			invoice_name=invoice_name,
			company=invoice.company,
			status="Error",
			xml=xml_content,
			response={},
			error=traceback.format_exc(),
		)

		# Log to error log
		frappe.log_error(
			message=traceback.format_exc(),
			title=f"JoFotara Error: {invoice_name}",
		)

		frappe.db.commit() # Ensure error logs are committed

		if triggering_user:
			frappe.publish_realtime(
				event="jofotara_submission_complete",
				message={
					"invoice_name": invoice_name,
					"status": "Error"
				},
				user=triggering_user
			)
	


def _validate_before_submission(invoice, company):
	"""
	Pre-submission validations.

	Raises:
		frappe.ValidationError: If validation fails
	"""
	# Validation for return invoices
	if invoice.is_return:
		if not invoice.return_against:
			frappe.throw(_("Return invoice must have a reference to original invoice"))

		original = frappe.get_doc("Sales Invoice", invoice.return_against)
		if not original.custom_jofotara_uuid:
			frappe.throw(
				_("Original invoice {0} has not been sent to JoFotara. Please send the original invoice first.").format(
					invoice.return_against
				)
			)

	# Get payment type
	payment_type = invoice.get("custom_jofotara_payment_type") or "Cash"

	# Determine if this is effectively a credit invoice
	is_credit_invoice = False
	if payment_type == "Credit":
		is_credit_invoice = True
	elif payment_type == "Auto" and not invoice.is_pos:
		is_credit_invoice = True

	# Validation for credit sales or high value invoices
	grand_total = flt(abs(invoice.grand_total))

	if is_credit_invoice or grand_total > 10000:
		customer = frappe.get_doc("Customer", invoice.customer)
		if not customer.tax_id:
			frappe.throw(
				_(
					"Customer Tax ID is required for credit sales or invoices over 10,000 JOD. "
					"Please update the customer record."
				)
			)


def _create_jofotara_log(
	invoice_name: str,
	company: str,
	status: str,
	xml: str = None,
	response: dict = None,
	error: str = None,
):
	"""Create a JoFotara Log entry."""
	log = frappe.new_doc("JoFotara Log")
	log.invoice = invoice_name
	log.company = company
	log.status = status
	log.creation_time = now_datetime()
	log.generated_xml = xml or ""
	log.response_body = json.dumps(response or {}, indent=2, ensure_ascii=False)
	log.error_traceback = error or ""
	log.insert(ignore_permissions=True)
	return log
