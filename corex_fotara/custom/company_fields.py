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


def add_company_jofotara_fields():
	"""Add JoFotara settings tab and fields to Company doctype."""
	custom_fields = {
		"Company": [
			# Tab Break for JoFotara Settings
			{
				"fieldname": "jofotara_settings_tab",
				"fieldtype": "Tab Break",
				"label": "JoFotara Settings",
				"insert_after": "default_holiday_list",
			},
			# Basic Settings Section
			{
				"fieldname": "jofotara_basic_section",
				"fieldtype": "Section Break",
				"label": "Basic Settings",
				"insert_after": "jofotara_settings_tab",
			},
			{
				"fieldname": "custom_enable_jofotara",
				"fieldtype": "Check",
				"label": "Enable JoFotara",
				"insert_after": "jofotara_basic_section",
				"description": "Master switch. If OFF, all JoFotara logic is bypassed.",
			},
			{
				"fieldname": "custom_jofotara_auto_send",
				"fieldtype": "Check",
				"label": "Auto-Send on Submit",
				"insert_after": "custom_enable_jofotara",
				"depends_on": "eval:doc.custom_enable_jofotara",
				"description": "Automatically send invoice to JoFotara when submitted.",
			},
			# API Credentials Section
			{
				"fieldname": "jofotara_credentials_section",
				"fieldtype": "Section Break",
				"label": "API Credentials",
				"insert_after": "custom_jofotara_auto_send",
				"depends_on": "eval:doc.custom_enable_jofotara",
			},
			{
				"fieldname": "custom_jofotara_client_id",
				"fieldtype": "Data",
				"label": "Client ID",
				"insert_after": "jofotara_credentials_section",
				"description": "Client ID from JoFotara portal",
			},
			{
				"fieldname": "custom_jofotara_secret_key",
				"fieldtype": "Password",
				"label": "Secret Key",
				"insert_after": "custom_jofotara_client_id",
				"description": "Secret Key from JoFotara portal",
				"length": 500
			},
			{
				"fieldname": "jofotara_cb1",
				"fieldtype": "Column Break",
				"insert_after": "custom_jofotara_secret_key",
			},
			{
				"fieldname": "custom_income_source_sequence",
				"fieldtype": "Data",
				"label": "Income Source Sequence",
				"insert_after": "jofotara_cb1",
				"description": "Branch ID from JoFotara portal (تسلسل مصدر الدخل)",
			},
			{
				"fieldname": "custom_default_city_code",
				"fieldtype": "Select",
				"label": "Default City Code",
				"insert_after": "custom_income_source_sequence",
				"options": JORDAN_CITY_CODES,
				"description": "Fallback city code if customer address is missing",
			},
			# Counter Settings Section
			{
				"fieldname": "jofotara_counter_section",
				"fieldtype": "Section Break",
				"label": "Counter Settings",
				"insert_after": "custom_default_city_code",
				"depends_on": "eval:doc.custom_enable_jofotara",
			},
			{
				"fieldname": "custom_starter_icv",
				"fieldtype": "Int",
				"label": "Starter ICV",
				"insert_after": "jofotara_counter_section",
				"default": "0",
				"description": "Starting point for the ICV counter",
			},
			{
				"fieldname": "custom_latest_sent_icv",
				"fieldtype": "Int",
				"label": "Latest Sent ICV",
				"insert_after": "custom_starter_icv",
				"read_only": 1,
				"description": "Last used ICV counter (updated automatically)",
			},
			{
				"fieldname": "jofotara_cb2",
				"fieldtype": "Column Break",
				"insert_after": "custom_latest_sent_icv",
			},
			{
				"fieldname": "custom_last_daily_seq_date",
				"fieldtype": "Date",
				"label": "Last Daily Seq Date",
				"insert_after": "jofotara_cb2",
				"hidden": 1,
				"read_only": 1,
			},
			{
				"fieldname": "custom_last_daily_seq_no",
				"fieldtype": "Int",
				"label": "Last Daily Seq No",
				"insert_after": "custom_last_daily_seq_date",
				"hidden": 1,
				"read_only": 1,
			},
			# UOM Mapping Section
			{
				"fieldname": "jofotara_uom_section",
				"fieldtype": "Section Break",
				"label": "UOM Mapping",
				"insert_after": "custom_last_daily_seq_no",
				"depends_on": "eval:doc.custom_enable_jofotara",
				"description": "Map ERPNext UOMs to JoFotara UBL codes (e.g., Nos → PCE, Kg → KGM)",
			},
			{
				"fieldname": "custom_uom_mapping",
				"fieldtype": "Table",
				"label": "UOM Mapping",
				"insert_after": "jofotara_uom_section",
				"options": "JoFotara UOM Map",
			},
		]
	}
	create_custom_fields(custom_fields)
	frappe.db.commit()
