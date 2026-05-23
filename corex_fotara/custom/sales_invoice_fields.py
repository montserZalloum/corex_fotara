# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def add_sales_invoice_jofotara_fields():
	"""Add JoFotara tracking fields to Sales Invoice doctype."""
	custom_fields = {
		"Sales Invoice": [
			{
				"fieldname": "custom_is_cash",
				"fieldtype": "Check",
				"label": "Is Cash",
				"insert_after": "company_tax_id",
				"default": "1",
				"description": "If checked, payment type is Cash and a Payment Entry is auto-created on submit. Otherwise, payment type is Credit.",
			},
			{
                "fieldname": "custom_jofotara_enabled",
                "fieldtype": "Check",
                "label": "JoFotara Enabled",
                "fetch_from": "company.custom_enable_jofotara", # Format: link_field.field_name
                "read_only": 1,
                "hidden": 1,
                "insert_after": "amended_from",
            },
			# JoFotara Section
			{
				"fieldname": "jofotara_section",
				"fieldtype": "Section Break",
				"label": "JoFotara Integration",
				"insert_after": "custom_jofotara_enabled",
				"collapsible": 1,
				"depends_on": "eval:doc.custom_jofotara_enabled == 1"
			},
			{
				"fieldname": "custom_jofotara_taxpayer_type",
				"fieldtype": "Select",
				"label": "Taxpayer Type",
				"insert_after": "jofotara_section",
				"options": "Income\nGeneral Sales\nSpecial Sales",
				"fetch_from": "company.custom_jofotara_taxpayer_type",
				"hidden": 1,
				"description": "Defaults from Company. Override per invoice only if this transaction falls under a different taxpayer category.",
			},
			{
				"fieldname": "custom_jofotara_payment_type",
				"fieldtype": "Select",
				"label": "JoFotara Payment Type",
				"insert_after": "custom_jofotara_taxpayer_type",
				"options": "Cash\nCredit",
				"default": "Cash",
				"read_only": 1,
				"description": "Driven by the 'Is Cash' checkbox.",
			},
			# QR Code Section
			{
				"fieldname": "custom_jofotara_qr",
				"fieldtype": "Long Text",
				"label": "JoFotara QR Data",
				"insert_after": "custom_jofotara_payment_type",
				"read_only": 1,
				"hidden":1,
				"no_copy": 1,
			},
			{
				"fieldname": "custom_qr_preview",
				"fieldtype": "HTML",
				"label": "QR Preview",
				"insert_after": "custom_jofotara_qr",
				"read_only": 1,
				"depends_on": "eval:doc.custom_jofotara_qr",
				"no_copy": 1,
			},
			{
				"fieldname": "custom_jofotara_cb", # Unique name for the break
				"fieldtype": "Column Break",
				"insert_after": "custom_jofotara_qr", # Place it after the first field
			},
			
			{
				"fieldname": "custom_jofotara_status",
				"fieldtype": "Select",
				"label": "JoFotara Status",
				"insert_after": "custom_jofotara_cb",
				"options": "\nPending\nQueued\nSuccess\nError",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1,
				"no_copy": 1,
			},
			
			{
				"fieldname": "custom_jofotara_uuid",
				"fieldtype": "Data",
				"label": "JoFotara UUID",
				"insert_after": "custom_jofotara_status",
				"hidden":1,
				"read_only": 1,
				"no_copy": 1,
			},
			{
				"fieldname": "custom_jofotara_icv",
				"fieldtype": "Int",
				"label": "JoFotara ICV",
				"insert_after": "custom_jofotara_uuid",
				"read_only": 1,
				"hidden":1,
				"description": "Sequential audit counter",
				"no_copy": 1,
			},

			{
				"fieldname": "custom_jofotara_id",
				"fieldtype": "Data",
				"label": "JoFotara ID",
				"insert_after": "custom_jofotara_icv",
				"read_only": 1,
				"hidden":1,
				"description": "Format: [Abbr]-[Date]-[Seq]",
				"no_copy": 1,
			},
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
