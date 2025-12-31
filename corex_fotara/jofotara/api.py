# Copyright (c) 2024, Corex and contributors
# For license information, please see license.txt

"""
JoFotara API Client - HTTP client for government API.

Handles encoding, request sending, and response parsing.
"""

import base64
import json

import requests

import frappe
from frappe import _


# JoFotara API endpoint
JOFOTARA_API_ENDPOINT = "https://backend.jofotara.gov.jo/core/invoices/"


class JoFotaraAPIClient:
	"""HTTP client for JoFotara government API."""

	def __init__(self, client_id: str, secret_key: str):
		self.client_id = client_id
		self.secret_key = secret_key
		self.timeout = 30  # seconds

	def send_invoice(self, xml_content: str) -> dict:
		"""
		Send invoice XML to JoFotara API.

		Args:
			xml_content: Raw XML string (not Base64 encoded)

		Returns:
			dict with:
				- success: bool
				- response: dict (API response body)
				- status_code: int (HTTP status code, if available)
				- error: str (error message, if any)
		"""
		# Validate credentials
		if not self.client_id or not self.secret_key:
			return {
				"success": False,
				"error": _("JoFotara API credentials are not configured"),
				"response": {},
			}

		# Encode XML to Base64
		xml_bytes = xml_content.encode("utf-8")
		base64_xml = base64.b64encode(xml_bytes).decode("utf-8")

		# Prepare request
		headers = {
			"Client-Id": self.client_id,
			"Secret-Key": self.secret_key,
			"Content-Type": "application/json",
		}

		payload = {"invoice": base64_xml}

		try:
			response = requests.post(
				JOFOTARA_API_ENDPOINT,
				headers=headers,
				json=payload,
				timeout=self.timeout,
			)

			# Try to parse response as JSON
			try:
				response_data = response.json() if response.text else {}
			except json.JSONDecodeError:
				response_data = {"raw_response": response.text}

			if response.status_code == 200:
				return {
					"success": True,
					"response": response_data,
					"status_code": response.status_code,
				}
			else:
				error_msg = response_data.get("message") or response_data.get("error") or f"API returned status {response.status_code}"
				return {
					"success": False,
					"response": response_data,
					"status_code": response.status_code,
					"error": error_msg,
				}

		except requests.Timeout:
			return {
				"success": False,
				"error": _("Request timed out after {0} seconds").format(self.timeout),
				"response": {},
			}
		except requests.ConnectionError:
			return {
				"success": False,
				"error": _("Failed to connect to JoFotara API. Please check your internet connection."),
				"response": {},
			}
		except requests.RequestException as e:
			return {
				"success": False,
				"error": str(e),
				"response": {},
			}
