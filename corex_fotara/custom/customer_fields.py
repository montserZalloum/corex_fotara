# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def add_customer_jofotara_fields():
	"""Add JoFotara identification type field to Customer doctype."""
	custom_fields = {
		"Customer": [
			{
				"fieldname": "custom_identification_type",
				"fieldtype": "Select",
				"label": "Identification Type",
				"insert_after": "tax_id",
				"options": "\nNational ID\nTax ID\nPassport",
				"description": "Required for Credit Sales or invoices over 10,000 JOD",
			}
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
