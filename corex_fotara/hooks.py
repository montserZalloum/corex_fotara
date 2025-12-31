app_name = "corex_fotara"
app_title = "Corex Fotara"
app_publisher = "Corex"
app_description = "JoFotara E-Invoicing Integration for Jordan"
app_email = "dev@corex.com"
app_license = "mit"

# Required Apps
# ------------------
required_apps = ["erpnext"]

# Includes in <head>
# ------------------

# Include qrcode.js library for QR visualization
app_include_js = "/assets/corex_fotara/js/qrcode.min.js"

# Include js in doctype views
doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"on_submit": "corex_fotara.jofotara.controller.on_sales_invoice_submit",
		"before_cancel": "corex_fotara.jofotara.controller.on_sales_invoice_cancel",
	}
}

# After Migrate - Create Custom Fields
# ------------------------------------

after_migrate = [
	"corex_fotara.custom.company_fields.add_company_jofotara_fields",
	"corex_fotara.custom.sales_invoice_fields.add_sales_invoice_jofotara_fields",
	"corex_fotara.custom.address_fields.add_address_jofotara_fields",
	"corex_fotara.custom.customer_fields.add_customer_jofotara_fields",
]

# Log Clearing
# ------------
# Retain JoFotara logs for 90 days
default_log_clearing_doctypes = {
	"JoFotara Log": 90,
}
