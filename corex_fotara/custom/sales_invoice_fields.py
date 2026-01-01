# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def add_sales_invoice_jofotara_fields():
	"""Add JoFotara tracking fields to Sales Invoice doctype."""
	custom_fields = {
		"Sales Invoice": [
			{
                "fieldname": "custom_jofotara_enabled",
                "fieldtype": "Check",
                "label": "JoFotara Enabled",
                "fetch_from": "company.custom_enable_jofotara", # Format: link_field.field_name
                "read_only": 1,
                "hidden": 1,
                "insert_after": "amended_from",
            },
			{
				"fieldname": "custom_jofotara_vat_registered",
				"fieldtype": "Check",
				"fetch_from": "company.custom_jofotara_vat_registered", # Pulls from Company
				"hidden": 1,
				"read_only": 1,
				"insert_after": "custom_jofotara_enabled",
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
				"fieldname": "custom_jofotara_payment_type",
				"fieldtype": "Select",
				"label": "JoFotara Payment Type",
				"insert_after": "jofotara_section",
				"options": "Cash\nCredit\nAuto",
				"default": "Cash",
				"description": "",
			},
			# QR Code Section
			{
				"fieldname": "custom_jofotara_qr",
				"fieldtype": "Long Text",
				"label": "JoFotara QR Data",
				"insert_after": "custom_jofotara_payment_type",
				"read_only": 1,
				"hidden":1,
			},
			{
				"fieldname": "custom_qr_preview",
				"fieldtype": "HTML",
				"label": "QR Preview",
				"insert_after": "custom_jofotara_qr",
				"read_only": 1,
				"depends_on": "eval:doc.custom_jofotara_qr",
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
			},
			
			{
				"fieldname": "custom_jofotara_uuid",
				"fieldtype": "Data",
				"label": "JoFotara UUID",
				"insert_after": "custom_jofotara_status",
				"hidden":1,
				"read_only": 1,
			},
			{
				"fieldname": "custom_jofotara_icv",
				"fieldtype": "Int",
				"label": "JoFotara ICV",
				"insert_after": "custom_jofotara_uuid",
				"read_only": 1,
				"hidden":1,
				"description": "Sequential audit counter",
			},

			{
				"fieldname": "custom_jofotara_id",
				"fieldtype": "Data",
				"label": "JoFotara ID",
				"insert_after": "custom_jofotara_icv",
				"read_only": 1,
				"hidden":1,
				"description": "Format: [Abbr]-[Date]-[Seq]",
			},
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
