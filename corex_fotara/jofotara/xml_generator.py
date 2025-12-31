# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
JoFotara XML Generator - UBL 2.1 compliant invoice generation.

Uses 9 decimal precision for all calculations as per government requirements.
Tax category (S/Z/O) is determined automatically based on:
- Tax Rate > 0% → S (Standard)
- Tax Rate == 0% + Jordan customer → Z (Exempt)
- Tax Rate == 0% + Non-Jordan customer → O (Out of Scope)
"""

import re
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import frappe
from frappe import _

from corex_fotara.jofotara.id_manager import get_jordan_date_str


class JoFotaraXMLGenerator:
	"""
	Generates UBL 2.1 compliant XML for JoFotara submission.
	Uses 9 decimal precision for all calculations as per government requirements.
	"""

	# 9 decimal places as required by JoFotara
	PRECISION = Decimal("0.000000001")

	def __init__(self, invoice_doc, company_doc):
		self.invoice = invoice_doc
		self.company = company_doc
		self.uom_mapping = self._build_uom_mapping()
		self._customer_country = None  # Cache for customer country

	def _build_uom_mapping(self) -> dict:
		"""Build UOM to JoFotara code mapping from Company settings."""
		# Default mappings
		mapping = {
			"Nos": "PCE",
			"Unit": "PCE",
			"Kg": "KGM",
			"Litre": "LTR",
			"Meter": "MTR",
		}
		# Override with company-specific mappings
		for row in self.company.get("custom_uom_mapping", []):
			mapping[row.uom] = row.jofotara_code
		return mapping

	def _to_decimal(self, value) -> Decimal:
		"""Convert value to Decimal with 9 decimal precision."""
		if value is None:
			return Decimal("0")
		return Decimal(str(value)).quantize(self.PRECISION, rounding=ROUND_HALF_UP)

	def _format_amount(self, value) -> str:
		"""Format decimal for XML output (9 decimal places as required by JoFotara)."""
		d = self._to_decimal(value)
		# Quantize to 9 decimal places
		quantized = d.quantize(Decimal("0.000000001"), rounding=ROUND_HALF_UP)
		# Format as fixed-point string (avoid scientific notation like 0E-9)
		result = format(quantized, 'f')
		# Ensure it has exactly 9 decimal places
		if '.' in result:
			integer_part, decimal_part = result.split('.')
			decimal_part = decimal_part.ljust(9, '0')[:9]
			return f"{integer_part}.{decimal_part}"
		else:
			return f"{result}.000000000"

	def _minify_xml(self, xml_string: str) -> str:
		"""
		Minify XML using the exact specification:
		1. Flatten (remove newlines/tabs)
		2. Collapse whitespace between tags
		"""
		# Flatten: Remove newlines, carriage returns, and tabs
		flat_xml = xml_string.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
		# Minify: Remove whitespace between tags
		minified_xml = re.sub(r'>\s+<', '><', flat_xml).strip()
		return minified_xml

	def generate(self) -> str:
		"""Generate the complete UBL 2.1 XML invoice."""
		context = self._build_context()

		# Load template from file
		template = frappe.get_template("corex_fotara/templates/xml/invoice.xml")
		xml_content = template.render(**context)

		# Minify XML using exact specification
		return self._minify_xml(xml_content)

	def _get_jordan_time(self) -> str:
		"""Get current time in Jordan timezone (Asia/Amman) in HH:MM:SS format."""
		try:
			from pytz import timezone
			jordan_tz = timezone('Asia/Amman')
			now = datetime.now(jordan_tz)
			return now.strftime('%H:%M:%S')
		except ImportError:
			# Fallback if pytz is not available
			return datetime.now().strftime('%H:%M:%S')

	def _build_context(self) -> dict:
		"""Build the complete context for XML template rendering."""
		return {
			"invoice": self.invoice,
			"issue_date": get_jordan_date_str(),
			"issue_time": self._get_jordan_time(),
			"invoice_type_code": self._get_invoice_type_code(),
			"invoice_type_name": self._get_invoice_type_name(),
			"billing_reference": self._get_billing_reference(),
			"seller": self._get_seller_info(),
			"buyer": self._get_buyer_info(),
			"income_source_sequence": self.company.custom_income_source_sequence or "",
			"is_return": self.invoice.is_return,
			"line_items": self._process_line_items(),
			"tax_subtotals": self._calculate_tax_subtotals(),
			"totals": self._calculate_totals(),
		}

	def _get_invoice_type_code(self) -> str:
		"""Return 388 for Sales, 381 for Returns."""
		return "381" if self.invoice.is_return else "388"

	def _get_invoice_type_name(self) -> str:
		"""
		Determine invoice subtype code (3 digits).
		Format: XYZ where:
		  X: 0=Local, 1=Export
		  Y: 1=Cash, 2=Credit
		  Z: 1=Income, 2=Sales, 3=Special

		Logic:
		- Cash -> "011" or "012"
		- Credit -> "021" or "022"
		"""
		# Determine if export based on customer country
		customer_country = self._get_customer_country()
		is_export = "1" if customer_country != "Jordan" else "0"

		# Determine payment type from custom field
		payment_type = self.invoice.get("custom_jofotara_payment_type") or "Cash"

		if payment_type == "Auto":
			# Auto: Check is_pos field (POS = Cash, Non-POS = Credit)
			is_credit = "1" if self.invoice.is_pos else "2"
		elif payment_type == "Credit":
			is_credit = "2"
		else:  # Cash (default)
			is_credit = "1"

		# Determine tax type based on VAT registration status
		# If VAT registered → "2" (Sales), otherwise → "1" (Income)
		vat_registered = self.company.get("custom_jofotara_vat_registered")
		tax_type = "2" if vat_registered else "1"

		return f"{is_export}{is_credit}{tax_type}"

	def _get_customer_country(self) -> str:
		"""Get customer's country from their address (cached)."""
		if self._customer_country is not None:
			return self._customer_country

		self._customer_country = "Jordan"  # Default

		if self.invoice.customer_address:
			country = frappe.db.get_value("Address", self.invoice.customer_address, "country")
			if country:
				self._customer_country = country

		return self._customer_country

	def _get_billing_reference(self) -> dict | None:
		"""Get billing reference for return invoices."""
		if not self.invoice.is_return or not self.invoice.return_against:
			return None

		original = frappe.get_doc("Sales Invoice", self.invoice.return_against)

		if not original.custom_jofotara_uuid:
			frappe.throw(
				_("Original invoice {0} has not been sent to JoFotara. Please send the original invoice first.").format(
					self.invoice.return_against
				)
			)

		total_formatted = self._format_amount(abs(original.grand_total))

		return {
			"id": original.custom_jofotara_id,
			"uuid": original.custom_jofotara_uuid,
			"total": total_formatted,
			"original_total": total_formatted,  # Required for originalInvoiceTotal reference
		}

	def _get_seller_info(self) -> dict:
		"""Extract seller (Company) information."""
		# Try to get company address
		postal_code = ""
		city_code = self.company.custom_default_city_code or "JO-AM"

		company_address = frappe.db.get_value(
			"Dynamic Link",
			{"link_doctype": "Company", "link_name": self.company.name, "parenttype": "Address"},
			"parent",
		)

		if company_address:
			address_doc = frappe.get_doc("Address", company_address)
			postal_code = address_doc.pincode or ""
			if address_doc.custom_jofotara_city_code:
				city_code = address_doc.custom_jofotara_city_code

		return {
			"name": self.company.company_name,
			"tax_id": self.company.tax_id or "",
			"postal_code": postal_code,
			"city_code": city_code,
		}

	def _get_buyer_info(self) -> dict:
		"""Extract buyer (Customer) information with address."""
		customer = frappe.get_doc("Customer", self.invoice.customer)

		# Get identification type and value
		id_scheme = "NIN"  # Default: National ID
		id_value = customer.tax_id or ""

		# For cash sales without tax ID, use None (do not send identification)
		if not id_value:
			# Determine payment type to check if this is a cash sale
			payment_type = self.invoice.get("custom_jofotara_payment_type") or "Cash"
			is_cash = payment_type == "Cash" or (payment_type == "Auto" and self.invoice.is_pos)

			if is_cash:
				# Use None for cash B2C sales - template will skip PartyIdentification
				id_value = None
				id_scheme = "NIN"

		# If we have an ID, determine the scheme
		if id_value:
			id_type = customer.get("custom_identification_type")
			if id_type == "Tax ID":
				id_scheme = "TN"
			elif id_type == "Passport":
				id_scheme = "PN"
			# else: NIN (National ID) is default

		# Get address info with fallbacks
		city_code = self.company.custom_default_city_code or "JO-AM"
		country_code = "JO"
		postal_code = ""
		phone = ""

		if self.invoice.customer_address:
			address = frappe.get_doc("Address", self.invoice.customer_address)
			if address.custom_jofotara_city_code:
				city_code = address.custom_jofotara_city_code
			if address.country and address.country != "Jordan":
				# Get 2-letter country code
				country_code = frappe.db.get_value("Country", address.country, "code") or "JO"
			postal_code = address.pincode or ""
			phone = address.phone or ""

		return {
			"name": self.invoice.customer_name,
			"id_scheme": id_scheme,
			"id_value": id_value,  # Can be None for cash sales
			"city_code": city_code,
			"country_code": country_code.upper()[:2],
			"postal_code": postal_code,
			"phone": phone,
		}

	def _calculate_line_extension_amount(self, quantity, unit_price, discount=0.0) -> Decimal:
		"""
		Formula: ROUND((quantity * unitPrice) - discount, 9)
		Use absolute values to ensure positive amounts.
		"""
		qty_dec = self._to_decimal(abs(quantity))
		price_dec = self._to_decimal(abs(unit_price))
		disc_dec = self._to_decimal(abs(discount))
		result = (qty_dec * price_dec) - disc_dec
		# Ensure positive result
		return abs(result.quantize(self.PRECISION, rounding=ROUND_HALF_UP))

	def _calculate_tax_amount(self, taxable_amount, tax_percent) -> Decimal:
		"""Formula: ROUND(taxableAmount * (taxPercent / 100), 9)"""
		amount_dec = self._to_decimal(taxable_amount)
		percent_dec = self._to_decimal(tax_percent) / Decimal("100")
		result = amount_dec * percent_dec
		return result.quantize(self.PRECISION, rounding=ROUND_HALF_UP)

	def _calculate_rounding_amount(self, taxable_amount, tax_amount) -> Decimal:
		"""Formula: ROUND(taxableAmount + taxAmount, 9)"""
		base_dec = self._to_decimal(taxable_amount)
		tax_dec = self._to_decimal(tax_amount)
		result = base_dec + tax_dec
		return result.quantize(self.PRECISION, rounding=ROUND_HALF_UP)

	def _get_item_tax_rate(self, item) -> float:
		"""Get the effective tax rate for an item."""
		# First check item tax template
		if item.item_tax_template:
			template = frappe.get_doc("Item Tax Template", item.item_tax_template)
			for tax in template.taxes:
				return float(tax.tax_rate or 0)

		# Fallback: Calculate from invoice taxes
		if self.invoice.taxes:
			# Get total tax percentage from invoice taxes
			total_tax_rate = 0
			for tax in self.invoice.taxes:
				if tax.rate:
					total_tax_rate += float(tax.rate)
			return total_tax_rate

		return 0

	def _get_tax_category(self, tax_rate: float) -> str:
		"""
		Determine JoFotara tax category code based on tax rate and customer country.

		Tax Heuristic (No Map):
		- If Rate > 0 → Code "S" (Standard)
		- If Rate == 0 & Customer in Jordan → Code "Z" (Exempt)
		- If Rate == 0 & Customer NOT in Jordan → Code "O" (Out of Scope)
		"""
		if tax_rate > 0:
			return "S"

		# Zero tax rate - check customer country
		customer_country = self._get_customer_country()
		if customer_country == "Jordan":
			return "Z"  # Exempt (local zero-rated)
		else:
			return "O"  # Out of Scope (export/non-Jordan)

	def _process_line_items(self) -> list:
		"""Process invoice items with 9 decimal precision calculations."""
		items = []

		for idx, item in enumerate(self.invoice.items, 1):
			qty = abs(item.qty)
			rate = abs(item.rate)
			discount = abs(item.discount_amount or 0)

			# Calculate line extension using exact formula
			line_extension = self._calculate_line_extension_amount(qty, rate, discount)

			# Get tax info
			tax_rate = self._get_item_tax_rate(item)
			tax_category = self._get_tax_category(tax_rate)

			# Calculate tax amount using exact formula
			tax_amount = self._calculate_tax_amount(line_extension, tax_rate)

			# Calculate rounding amount using exact formula
			rounding_amount = self._calculate_rounding_amount(line_extension, tax_amount)

			items.append(
				{
					"idx": idx,
					"name": item.item_name,
					"qty": self._format_amount(qty),
					"uom_code": self.uom_mapping.get(item.uom, "PCE"),
					"unit_price": self._format_amount(rate),
					"line_extension": self._format_amount(line_extension),
					"tax_amount": self._format_amount(tax_amount),
					"rounding_amount": self._format_amount(rounding_amount),
					"tax_category": tax_category,
					"tax_percent": str(tax_rate),
					# Store raw values for totals calculation
					"_line_extension": line_extension,
					"_tax_amount": tax_amount,
				}
			)

		return items

	def _calculate_tax_subtotals(self) -> list:
		"""Group taxes by category code for TaxSubtotal elements."""
		tax_groups = {}
		line_items = self._process_line_items()

		for item in line_items:
			category = item["tax_category"]
			if category not in tax_groups:
				tax_groups[category] = {
					"category_code": category,
					"taxable_amount": Decimal("0"),
					"tax_amount": Decimal("0"),
					"percent": item["tax_percent"],
				}

			tax_groups[category]["taxable_amount"] += item["_line_extension"]
			tax_groups[category]["tax_amount"] += item["_tax_amount"]

		return [
			{
				"category_code": g["category_code"],
				"taxable_amount": self._format_amount(g["taxable_amount"]),
				"tax_amount": self._format_amount(g["tax_amount"]),
				"percent": g["percent"],
			}
			for g in tax_groups.values()
		]

	def _calculate_totals(self) -> dict:
		"""Calculate monetary totals with precision."""
		tax_exclusive = Decimal("0")
		total_tax = Decimal("0")

		for item in self._process_line_items():
			tax_exclusive += item["_line_extension"]
			total_tax += item["_tax_amount"]

		tax_inclusive = tax_exclusive + total_tax

		# Use absolute value for allowance/discount total
		allowance_total = abs(self._to_decimal(self.invoice.discount_amount or 0))

		# Payable amount (ensure positive)
		payable = abs(tax_inclusive - allowance_total)

		return {
			"tax_exclusive": self._format_amount(tax_exclusive),
			"tax_inclusive": self._format_amount(tax_inclusive),
			"total_tax": self._format_amount(total_tax),
			"allowance_total": self._format_amount(allowance_total),
			"discount_amount": self._format_amount(allowance_total),  # Same as allowance_total
			"payable": self._format_amount(payable),
			# Raw numeric values for template comparisons
			"_discount_amount_raw": float(allowance_total),
		}
