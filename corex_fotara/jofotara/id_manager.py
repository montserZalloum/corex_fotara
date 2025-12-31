# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
JoFotara ID Manager - Concurrency-safe counter generation.

Uses database-level locking (SELECT ... FOR UPDATE) to prevent race conditions
in high-concurrency scenarios (e.g., multiple cashiers submitting simultaneously).

All dates use Asia/Amman timezone to prevent date-shifting issues.
"""

import uuid
from datetime import datetime

import pytz
import frappe
from frappe import _


# Jordan timezone
JORDAN_TZ = pytz.timezone("Asia/Amman")


def get_jordan_date() -> datetime:
	"""Get current date/time in Jordan timezone."""
	return datetime.now(JORDAN_TZ)


def get_jordan_date_str() -> str:
	"""Get current date as string in YYYY-MM-DD format (Jordan timezone)."""
	return get_jordan_date().strftime("%Y-%m-%d")


class JoFotaraIDManager:
	"""
	Manages the generation of JoFotara identifiers with database-level locking
	to prevent race conditions in high-concurrency scenarios.

	Pattern: SELECT ... FOR UPDATE on Company row for serialized access.
	"""

	def __init__(self, company_name: str):
		self.company_name = company_name

	def generate_identifiers(self, invoice_doc) -> dict:
		"""
		Generate all required JoFotara identifiers atomically.

		This method MUST be called within a transaction and acquires a row-level
		lock on the Company record to prevent duplicate counters.

		If IDs already exist on the invoice (retry scenario), they are reused
		to prevent gaps in the ICV sequence.

		Args:
			invoice_doc: The Sales Invoice document

		Returns:
			dict with: jofotara_id, jofotara_uuid, jofotara_icv
		"""
		# Check if IDs already exist (retry scenario - e.g., network failure)
		if invoice_doc.get("custom_jofotara_id"):
			return {
				"jofotara_id": invoice_doc.custom_jofotara_id,
				"jofotara_uuid": invoice_doc.custom_jofotara_uuid,
				"jofotara_icv": invoice_doc.custom_jofotara_icv,
			}

		# Acquire lock by fetching Company with FOR UPDATE
		# This serializes concurrent requests - one must wait for the other
		company_data = frappe.db.sql(
			"""
			SELECT
				name, abbr,
				custom_starter_icv,
				custom_latest_sent_icv,
				custom_last_daily_seq_date,
				custom_last_daily_seq_no
			FROM `tabCompany`
			WHERE name = %s
			FOR UPDATE
			""",
			(self.company_name,),
			as_dict=True,
		)

		if not company_data:
			frappe.throw(_("Company {0} not found").format(self.company_name))

		company = company_data[0]

		# Get current date in Jordan timezone
		jordan_now = get_jordan_date()
		current_date = jordan_now.date()
		date_str = jordan_now.strftime("%Y-%m-%d")

		# Calculate new ICV (sequential counter)
		starter_icv = company.custom_starter_icv or 0
		latest_icv = company.custom_latest_sent_icv or 0
		new_icv = max(starter_icv, latest_icv) + 1

		# Calculate daily sequence
		# Reset sequence if date changed
		last_seq_date = company.custom_last_daily_seq_date
		if last_seq_date and last_seq_date == current_date:
			new_daily_seq = (company.custom_last_daily_seq_no or 0) + 1
		else:
			new_daily_seq = 1

		# Generate UUID4
		new_uuid = str(uuid.uuid4())

		# Format JoFotara ID: [Abbr]-[YYYY-MM-DD]-[Seq]
		jofotara_id = f"{company.abbr}-{date_str}-{new_daily_seq:05d}"

		# Update Company counters (still within the lock)
		frappe.db.sql(
			"""
			UPDATE `tabCompany`
			SET
				custom_latest_sent_icv = %s,
				custom_last_daily_seq_date = %s,
				custom_last_daily_seq_no = %s
			WHERE name = %s
			""",
			(new_icv, current_date, new_daily_seq, self.company_name),
		)

		# Update Invoice fields
		frappe.db.set_value(
			"Sales Invoice",
			invoice_doc.name,
			{
				"custom_jofotara_id": jofotara_id,
				"custom_jofotara_uuid": new_uuid,
				"custom_jofotara_icv": new_icv,
				"custom_jofotara_status": "Queued",
			},
			update_modified=False,
		)

		return {
			"jofotara_id": jofotara_id,
			"jofotara_uuid": new_uuid,
			"jofotara_icv": new_icv,
		}
