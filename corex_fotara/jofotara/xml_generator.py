# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
JoFotara XML Generator - UBL 2.1 compliant invoice generation.
"""

import re
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import frappe
from frappe import _
from frappe.utils import flt

# تأكد من استدعاء دالة التاريخ بشكل صحيح حسب مشروعك
from corex_fotara.jofotara.id_manager import get_jordan_date_str


class JoFotaraXMLGenerator:
    """
    Generates UBL 2.1 compliant XML for JoFotara submission.
    Uses 9 decimal precision for all calculations.
    """

    # 9 decimal places as required by JoFotara
    PRECISION = Decimal("0.000000001")

    def __init__(self, invoice_doc, company_doc):
        self.invoice = invoice_doc
        self.company = company_doc
        self.uom_mapping = self._build_uom_mapping()
        self._customer_country = None
        
        # Cache for processed lines to avoid re-calculation
        self._cached_items = None 

    def _build_uom_mapping(self) -> dict:
        mapping = {
            "Nos": "PCE", "Unit": "PCE", "Kg": "KGM", 
            "Litre": "LTR", "Meter": "MTR", "Box": "BX"
        }
        for row in self.company.get("custom_uom_mapping", []):
            mapping[row.uom] = row.jofotara_code
        return mapping

    def _to_decimal(self, value) -> Decimal:
        if value is None:
            return Decimal("0")
        return Decimal(str(value)).quantize(self.PRECISION, rounding=ROUND_HALF_UP)

    def _format_amount(self, value) -> str:
        """Format decimal for XML output (Exactly 9 decimal places)."""
        d = self._to_decimal(value)
        result = format(d, 'f')
        if '.' in result:
            integer_part, decimal_part = result.split('.')
            decimal_part = decimal_part.ljust(9, '0')[:9]
            return f"{integer_part}.{decimal_part}"
        else:
            return f"{result}.000000000"

    def _minify_xml(self, xml_string: str) -> str:
        # Flatten and remove whitespace between tags
        flat_xml = xml_string.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
        return re.sub(r'>\s+<', '><', flat_xml).strip()

    def generate(self) -> str:
        # 1. Process items first and cache them
        self._cached_items = self._process_line_items()
        
        context = self._build_context()
        template = frappe.get_template("corex_fotara/templates/xml/invoice.xml")
        xml_content = template.render(**context)
        return self._minify_xml(xml_content)

    def _get_jordan_time(self) -> str:
        try:
            from pytz import timezone
            jordan_tz = timezone('Asia/Amman')
            now = datetime.now(jordan_tz)
            return now.strftime('%H:%M:%S')
        except ImportError:
            return datetime.now().strftime('%H:%M:%S')

    def _build_context(self) -> dict:
        return {
            "invoice": self.invoice,
            "issue_date": get_jordan_date_str(),
            "issue_time": self._get_jordan_time(),
            "invoice_type_code": "381" if self.invoice.is_return else "388",
            "invoice_type_name": self._get_invoice_type_name(),
            "billing_reference": self._get_billing_reference(),
            "seller": self._get_seller_info(),
            "buyer": self._get_buyer_info(),
            "income_source_sequence": self.company.custom_income_source_sequence or "",
            "is_return": self.invoice.is_return,
            
            # Use cached items
            "line_items": self._cached_items,
            "tax_subtotals": self._calculate_tax_subtotals(),
            "totals": self._calculate_totals(),
        }

    def _get_invoice_type_name(self) -> str:
        # 1st Digit: Export (1) vs Local (0)
        is_export = "1" if self._get_customer_country() != "Jordan" else "0"

        # 2nd Digit: Payment (Cash=1, Credit=2)
        payment_type = self.invoice.get("custom_jofotara_payment_type") or "Cash"
        if payment_type == "Auto":
            is_credit = "1" if self.invoice.is_pos else "2"
        elif payment_type == "Credit":
            is_credit = "2"
        else:
            is_credit = "1"

        # 3rd Digit: Taxpayer Type (Sales=2, Income=1)
        vat_registered = self.company.get("custom_jofotara_vat_registered")
        tax_type = "2" if vat_registered else "1"

        return f"{is_export}{is_credit}{tax_type}"

    def _get_customer_country(self) -> str:
        if self._customer_country is not None:
            return self._customer_country
        self._customer_country = "Jordan"
        if self.invoice.customer_address:
            country = frappe.db.get_value("Address", self.invoice.customer_address, "country")
            if country:
                self._customer_country = country
        return self._customer_country

    def _get_billing_reference(self) -> dict | None:
        if not self.invoice.is_return or not self.invoice.return_against:
            return None
        
        original_inv_name = self.invoice.return_against
        original_data = frappe.db.get_value(
            "Sales Invoice", original_inv_name,
            ["custom_jofotara_uuid", "custom_jofotara_id", "grand_total"], 
            as_dict=True
        )

        if not original_data or not original_data.custom_jofotara_uuid:
            # Fallback check: If original invoice wasn't synced, we can't sync the return
            # But for flexibility, maybe return minimal data or throw error
            frappe.throw(_("Original invoice {0} has no UUID. Cannot generate return XML.").format(original_inv_name))

        total_formatted = self._format_amount(abs(original_data.grand_total))
        return {
            "id": original_data.custom_jofotara_id or original_inv_name,
            "uuid": original_data.custom_jofotara_uuid,
            "total": total_formatted,
            "original_total": total_formatted, 
        }

    def _get_seller_info(self) -> dict:
        postal_code = ""
        city_code = self.company.custom_default_city_code or "JO-AM"
        
        # Optimized: Fetch needed fields directly
        company_address_name = frappe.db.get_value("Dynamic Link", 
            {"link_doctype": "Company", "link_name": self.company.name, "parenttype": "Address"}, 
            "parent"
        )
        
        if company_address_name:
            addr = frappe.db.get_value("Address", company_address_name, 
                ["pincode", "custom_jofotara_city_code"], as_dict=True)
            if addr:
                postal_code = addr.pincode or ""
                if addr.custom_jofotara_city_code:
                    city_code = addr.custom_jofotara_city_code

        return {
            "name": self.company.company_name,
            "tax_id": self.company.tax_id or "",
            "postal_code": postal_code,
            "city_code": city_code,
        }

    def _get_buyer_info(self) -> dict:
        # Optimized fetching
        customer_data = frappe.db.get_value("Customer", self.invoice.customer, 
            ["tax_id", "customer_name", "custom_identification_type"], as_dict=True)
        
        id_value = customer_data.tax_id or ""
        id_scheme = "NIN" # Default

        # Logic for Cash Sales (Hidden ID)
        payment_type = self.invoice.get("custom_jofotara_payment_type") or "Cash"
        is_cash = payment_type == "Cash" or (payment_type == "Auto" and self.invoice.is_pos)
        
        if is_cash and not id_value:
             id_value = None # Template will skip ID tag
        
        if id_value:
            id_type = customer_data.custom_identification_type
            if id_type == "Tax ID": id_scheme = "TN"
            elif id_type == "Passport": id_scheme = "PN"

        # Address Info
        city_code = self.company.custom_default_city_code or "JO-AM"
        country_code = "JO"
        postal_code = ""
        phone = ""

        if self.invoice.customer_address:
            addr = frappe.db.get_value("Address", self.invoice.customer_address, 
                ["custom_jofotara_city_code", "country", "pincode", "phone"], as_dict=True)
            if addr:
                if addr.custom_jofotara_city_code: city_code = addr.custom_jofotara_city_code
                if addr.country and addr.country != "Jordan":
                    c_code = frappe.db.get_value("Country", addr.country, "code")
                    country_code = c_code if c_code else "JO"
                postal_code = addr.pincode or ""
                phone = addr.phone or ""

        return {
            "name": customer_data.customer_name,
            "id_scheme": id_scheme,
            "id_value": id_value,
            "city_code": city_code,
            "country_code": country_code.upper()[:2],
            "postal_code": postal_code,
            "phone": phone,
        }

    # --- Calculations ---

    def _calculate_line_extension(self, qty_dec, price_dec, disc_dec) -> Decimal:
        """ (Qty * Price) - Discount """
        res = (qty_dec * price_dec) - disc_dec
        return abs(res.quantize(self.PRECISION, rounding=ROUND_HALF_UP))

    def _calculate_tax(self, amount_dec, rate_float) -> Decimal:
        """ Amount * (Rate/100) """
        rate_dec = self._to_decimal(rate_float) / Decimal("100")
        res = amount_dec * rate_dec
        return res.quantize(self.PRECISION, rounding=ROUND_HALF_UP)

    def _get_item_tax_rate(self, item) -> float:
        # 1. Item Tax Template
        if item.item_tax_template:
            # Assuming simple template with one tax for simplicity, or sum them up
            template = frappe.get_doc("Item Tax Template", item.item_tax_template)
            return sum([float(t.tax_rate) for t in template.taxes])
        
        # 2. Invoice Taxes (Fallback - approximate)
        # This is tricky if multiple items have different taxes. 
        # Ideally, ERPNext stores item_tax_rate in the item table JSON.
        # For now, we use the method that loops invoice taxes if no template.
        if self.invoice.taxes:
            return sum([float(t.rate) for t in self.invoice.taxes if t.rate])
            
        return 0.0

    def _process_line_items(self) -> list:
        """
        Process items using NET PRICE logic to avoid validation errors.
        We send the Price After Discount as the Unit Price, and skip the AllowanceCharge tag.
        """
        items = []
        for idx, item in enumerate(self.invoice.items, 1):
            qty = abs(flt(item.qty))
            qty_dec = self._to_decimal(qty)

            # --- LOGIC CHANGE: USE NET PRICE ---
            # Instead of sending Gross Price + Discount, we send Net Price directly.
            # Net Amount = (Qty * Price) - Discount
            # In ERPNext: item.amount is usually the Net Amount (Tax Exclusive)
            
            line_extension_dec = self._to_decimal(abs(flt(item.amount)))
            
            # Calculate Net Unit Price (Price after discount)
            if qty > 0:
                unit_price_dec = line_extension_dec / qty_dec
            else:
                unit_price_dec = Decimal("0")
                
            # Quantize the price to 9 decimals
            unit_price_dec = unit_price_dec.quantize(self.PRECISION, rounding=ROUND_HALF_UP)
            
            # Recalculate Line Extension from the rounded Net Price to ensure match
            # This ensures (Qty * NetPrice) == LineExtension exactly
            line_extension_dec = (qty_dec * unit_price_dec).quantize(self.PRECISION, rounding=ROUND_HALF_UP)

            # Tax Calculation
            tax_rate = self._get_item_tax_rate(item)
            tax_category = "S" if tax_rate > 0 else ("Z" if self._get_customer_country() == "Jordan" else "O")
            
            tax_amount_dec = self._calculate_tax(line_extension_dec, tax_rate)
            rounding_amount_dec = line_extension_dec + tax_amount_dec

            items.append({
                "idx": idx,
                "name": item.item_name,
                "qty": self._format_amount(qty_dec),
                "uom_code": self.uom_mapping.get(item.uom, "PCE"),
                
                # Send NET PRICE here
                "unit_price": self._format_amount(unit_price_dec),
                
                # Zero out discount fields so XML template doesn't generate AllowanceCharge
                "discount_amount": self._format_amount(0),
                "gross_amount": self._format_amount(0),
                "discount_factor": self._format_amount(0),
                "_discount_amount_raw": 0, 

                "line_extension": self._format_amount(line_extension_dec),
                "tax_amount": self._format_amount(tax_amount_dec),
                "rounding_amount": self._format_amount(rounding_amount_dec),
                "tax_category": tax_category,
                "tax_percent": str(tax_rate),
                
                "_line_extension": line_extension_dec,
                "_tax_amount": tax_amount_dec,
            })
        return items

    def _calculate_tax_subtotals(self) -> list:
        # Use Cached items
        tax_groups = {}
        for item in self._cached_items:
            cat = item["tax_category"]
            if cat not in tax_groups:
                tax_groups[cat] = {
                    "category_code": cat,
                    "taxable_amount": Decimal("0"),
                    "tax_amount": Decimal("0"),
                    "percent": item["tax_percent"],
                }
            tax_groups[cat]["taxable_amount"] += item["_line_extension"]
            tax_groups[cat]["tax_amount"] += item["_tax_amount"]

        return [{
            "category_code": g["category_code"],
            "taxable_amount": self._format_amount(g["taxable_amount"]),
            "tax_amount": self._format_amount(g["tax_amount"]),
            "percent": g["percent"],
        } for g in tax_groups.values()]

    def _calculate_totals(self) -> dict:
        tax_exclusive = Decimal("0")
        total_tax = Decimal("0")
        
        # Sum from lines (Bottom-up accuracy)
        for item in self._cached_items:
            tax_exclusive += item["_line_extension"]
            total_tax += item["_tax_amount"]

        tax_inclusive = tax_exclusive + total_tax

        # GLOBAL DISCOUNT LOGIC:
        # In ERPNext, invoice.discount_amount usually refers to "Additional Discount" 
        # applied on the Grand Total (Net or Gross).
        # We must NOT include line-level discounts here again.
        
        # NOTE: Verify if `discount_amount` in your ERPNext setup is "Additional" only.
        # If it sums up line discounts, you should set this to 0 or use `additional_discount_percentage` logic.
        allowance_total = abs(self._to_decimal(self.invoice.discount_amount or 0))

        # Payable = Inclusive - Global Discount
        payable = tax_inclusive - allowance_total
        
        # Sanity check against negative
        if payable < 0: payable = Decimal("0")

        return {
            "tax_exclusive": self._format_amount(tax_exclusive),
            "tax_inclusive": self._format_amount(tax_inclusive),
            "total_tax": self._format_amount(total_tax),
            "allowance_total": self._format_amount(allowance_total),
            "discount_amount": self._format_amount(allowance_total),
            "payable": self._format_amount(payable),
            "_discount_amount_raw": float(allowance_total),
        }