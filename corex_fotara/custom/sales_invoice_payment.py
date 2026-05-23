# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
Is Cash checkbox handling on Sales Invoice.

- validate: syncs custom_jofotara_payment_type with custom_is_cash.
- on_submit: creates and submits a Cash Payment Entry when custom_is_cash is set.
"""

import frappe
from frappe import _
from frappe.utils import flt


def sync_payment_type_from_is_cash(doc, method=None):
	"""Keep custom_jofotara_payment_type aligned with the Is Cash checkbox."""
	doc.custom_jofotara_payment_type = "Cash" if doc.custom_is_cash else "Credit"


def create_cash_payment_entry(doc, method=None):
	"""Auto-create and submit a Payment Entry when Is Cash is checked."""
	if not doc.custom_is_cash:
		return

	if flt(doc.outstanding_amount) == 0:
		return

	if _payment_entry_exists(doc.name):
		return

	from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

	pe = get_payment_entry("Sales Invoice", doc.name)
	_apply_cash_mode_of_payment(pe, doc.company)
	pe.reference_no = doc.name
	pe.reference_date = doc.posting_date
	pe.flags.ignore_permissions = True
	pe.insert()
	pe.submit()

	frappe.msgprint(
		_("Cash Payment Entry {0} created for this invoice.").format(
			frappe.utils.get_link_to_form("Payment Entry", pe.name)
		),
		indicator="green",
		alert=True,
	)


def _payment_entry_exists(invoice_name: str) -> bool:
	return bool(
		frappe.db.exists(
			"Payment Entry Reference",
			{
				"reference_doctype": "Sales Invoice",
				"reference_name": invoice_name,
				"docstatus": ["<", 2],
			},
		)
	)


def _apply_cash_mode_of_payment(pe, company: str):
	"""Force the Payment Entry to use the Cash Mode of Payment account for the company."""
	cash_account = _resolve_cash_account(company)

	pe.mode_of_payment = "Cash"

	account_currency = frappe.db.get_value("Account", cash_account, "account_currency")
	account_type = frappe.db.get_value("Account", cash_account, "account_type")

	if pe.payment_type == "Receive":
		pe.paid_to = cash_account
		pe.paid_to_account_currency = account_currency
		pe.paid_to_account_type = account_type
	else:
		pe.paid_from = cash_account
		pe.paid_from_account_currency = account_currency
		pe.paid_from_account_type = account_type


def _resolve_cash_account(company: str) -> str:
	"""Resolve the Cash account: Mode of Payment 'Cash' account for the company, else Company default."""
	from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account

	account = get_default_bank_cash_account(company, "Cash", mode_of_payment="Cash").get("account")

	if not account:
		account = frappe.get_cached_value("Company", company, "default_cash_account")

	if not account:
		frappe.throw(
			_(
				"No Cash account configured for company {0}. "
				"Please set the account on the 'Cash' Mode of Payment or as the company's Default Cash Account."
			).format(company),
			title=_("Cash Account Missing"),
		)

	return account
