# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def add_sales_invoice_jofotara_fields():
	"""Add JoFotara tracking fields to Sales Invoice doctype."""
	custom_fields = {
		"Sales Invoice": [
			# JoFotara Section
			{
				"fieldname": "jofotara_section",
				"fieldtype": "Section Break",
				"label": "JoFotara Integration",
				"insert_after": "amended_from",
				"collapsible": 1,
			},
			{
				"fieldname": "custom_jofotara_payment_type",
				"fieldtype": "Select",
				"label": "JoFotara Payment Type",
				"insert_after": "jofotara_section",
				"options": "Cash\nCredit\nAuto",
				"default": "Cash",
				"description": "Cash: 011/012, Credit: 021/022 (enforces Tax ID), Auto: Uses is_pos field",
			},
			{
				"fieldname": "custom_jofotara_status",
				"fieldtype": "Select",
				"label": "JoFotara Status",
				"insert_after": "custom_jofotara_payment_type",
				"options": "\nPending\nQueued\nSuccess\nError",
				"read_only": 1,
				"in_list_view": 1,
				"in_standard_filter": 1,
			},
			{
				"fieldname": "jofotara_cb1",
				"fieldtype": "Column Break",
				"insert_after": "custom_jofotara_status",
			},
			{
				"fieldname": "custom_jofotara_id",
				"fieldtype": "Data",
				"label": "JoFotara ID",
				"insert_after": "jofotara_cb1",
				"read_only": 1,
				"description": "Format: [Abbr]-[Date]-[Seq]",
			},
			{
				"fieldname": "custom_jofotara_uuid",
				"fieldtype": "Data",
				"label": "JoFotara UUID",
				"insert_after": "custom_jofotara_id",
				"read_only": 1,
			},
			{
				"fieldname": "custom_jofotara_icv",
				"fieldtype": "Int",
				"label": "JoFotara ICV",
				"insert_after": "custom_jofotara_uuid",
				"read_only": 1,
				"description": "Sequential audit counter",
			},
			# QR Code Section
			{
				"fieldname": "jofotara_qr_section",
				"fieldtype": "Section Break",
				"label": "QR Code",
				"insert_after": "custom_jofotara_icv",
				"collapsible": 1,
				"depends_on": "eval:doc.custom_jofotara_qr",
			},
			{
				"fieldname": "custom_jofotara_qr",
				"fieldtype": "Long Text",
				"label": "JoFotara QR Data",
				"insert_after": "jofotara_qr_section",
				"read_only": 1,
			},
			{
				"fieldname": "custom_qr_preview",
				"fieldtype": "HTML",
				"label": "QR Preview",
				"insert_after": "custom_jofotara_qr",
				"read_only": 1,
			},
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
