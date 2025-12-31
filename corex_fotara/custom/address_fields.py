# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# Jordan city codes based on ISO 3166-2:JO
JORDAN_CITY_CODES = """
JO-AM
JO-AQ
JO-AT
JO-AZ
JO-BA
JO-IR
JO-JA
JO-KA
JO-MA
JO-MD
JO-MN
"""


def add_address_jofotara_fields():
	"""Add JoFotara city code field to Address doctype."""
	custom_fields = {
		"Address": [
			{
				"fieldname": "custom_jofotara_city_code",
				"fieldtype": "Select",
				"label": "JoFotara City Code",
				"insert_after": "country",
				"options": JORDAN_CITY_CODES,
				"depends_on": "eval:doc.country=='Jordan'",
				"description": "Jordan city code for JoFotara compliance",
			}
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
