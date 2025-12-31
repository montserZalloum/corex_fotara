// Copyright (c) 2024, Corex and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Invoice", {
	refresh: function (frm) {
		// Only process for submitted invoices
		if (frm.doc.docstatus !== 1) return;

		// Check if JoFotara is enabled for the company
		frappe.db
			.get_value("Company", frm.doc.company, "custom_enable_jofotara")
			.then((r) => {
				if (!r.message || !r.message.custom_enable_jofotara) return;

				// Add status indicator
				add_jofotara_indicator(frm);

				// Add "Send to JoFotara" button if needed
				add_send_button(frm);

				// Render QR code preview if available
				render_qr_preview(frm);
			});
	},
});

function add_jofotara_indicator(frm) {
	const status = frm.doc.custom_jofotara_status;

	if (status === "Success") {
		frm.dashboard.add_indicator(__("JoFotara: Sent"), "green");
	} else if (status === "Error") {
		frm.dashboard.add_indicator(__("JoFotara: Error"), "red");
	} else if (status === "Queued") {
		frm.dashboard.add_indicator(__("JoFotara: Processing"), "blue");
	} else if (status === "Pending") {
		frm.dashboard.add_indicator(__("JoFotara: Pending"), "orange");
	}
}

function add_send_button(frm) {
	const status = frm.doc.custom_jofotara_status;

	// Show button for Pending, Error, or no status
	if (!status || status === "Pending" || status === "Error") {
		const button_label = status === "Error" ? __("Retry JoFotara") : __("Send to JoFotara");

		frm.add_custom_button(
			button_label,
			function () {
				frappe.call({
					method: "corex_fotara.jofotara.controller.send_to_jofotara",
					args: {
						invoice_name: frm.doc.name,
					},
					freeze: true,
					freeze_message: __("Sending to JoFotara..."),
					callback: function (r) {
						frm.reload_doc();
					},
					error: function (r) {
						frappe.msgprint({
							title: __("Error"),
							indicator: "red",
							message: __("Failed to send invoice to JoFotara. Please check the error log."),
						});
						frm.reload_doc();
					},
				});
			},
			__("Actions")
		);
	}

	// Add link to view logs
	if (status) {
		frm.add_custom_button(
			__("View JoFotara Logs"),
			function () {
				frappe.set_route("List", "JoFotara Log", { invoice: frm.doc.name });
			},
			__("Actions")
		);
	}
}

function render_qr_preview(frm) {
	const qr_data = frm.doc.custom_jofotara_qr;
	const qr_wrapper = frm.fields_dict.custom_qr_preview;

	if (!qr_wrapper || !qr_wrapper.$wrapper) return;

	// Clear existing content
	qr_wrapper.$wrapper.empty();

	if (!qr_data) {
		qr_wrapper.$wrapper.html('<div class="text-muted">' + __("QR code will appear here after successful submission") + "</div>");
		return;
	}

	// Create container for QR code
	const container = $('<div id="jofotara-qr-container" style="text-align: center; padding: 10px;"></div>');
	qr_wrapper.$wrapper.append(container);

	// Generate QR code using qrcode.js library
	try {
		if (typeof QRCode !== "undefined") {
			new QRCode(document.getElementById("jofotara-qr-container"), {
				text: qr_data,
				width: 200,
				height: 200,
				colorDark: "#000000",
				colorLight: "#ffffff",
				correctLevel: QRCode.CorrectLevel.M,
			});

			// Add label
			container.append('<div class="text-muted mt-2" style="font-size: 12px;">' + __("Scan this QR code to verify the invoice") + "</div>");
		} else {
			// Fallback if QRCode library not loaded
			container.html(
				'<div class="alert alert-warning">' + __("QR code library not loaded. QR Data:") + "<br><code>" + frappe.utils.escape_html(qr_data) + "</code></div>"
			);
		}
	} catch (e) {
		console.error("Error generating QR code:", e);
		container.html('<div class="alert alert-danger">' + __("Error generating QR code") + "</div>");
	}
}
