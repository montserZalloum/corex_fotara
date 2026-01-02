// Copyright (c) 2024, Corex and contributors
// For license information, please see license.txt
frappe.ui.form.on("Sales Invoice", {
	refresh: function (frm) {
		const is_enabled = frm.doc.custom_jofotara_enabled;
		const is_historical_success = frm.doc.custom_jofotara_status === "Success";

		if (is_enabled || is_historical_success) {
			// 1. Clear previous indicators to prevent stacking
			frm.dashboard.clear_comment_count && frm.dashboard.clear_indicators(); 
			
			add_jofotara_indicator(frm);
			render_qr_preview(frm);
			
			if (frm.doc.docstatus === 1 && is_enabled) {
				add_send_button(frm);
			}
		}
		
	},

	validate: function (frm) {
		if (!validate_currency_for_jofotara(frm)) return false;
		return validate_vat_registration_and_taxes(frm);
	},

	before_submit: function (frm) {
		if (!validate_currency_for_jofotara(frm)) return false;
		return validate_vat_registration_and_taxes(frm);
	},
});

function add_jofotara_indicator(frm) {
	const status = frm.doc.custom_jofotara_status;
	if (!status) return;

	const colors = {
		Success: "green",
		Error: "red",
		Queued: "blue",
		Pending: "orange",
	};

	frm.dashboard.add_indicator(__(`JoFotara: ${status}`), colors[status] || "gray");
}

function add_send_button(frm) {
	const status = frm.doc.custom_jofotara_status;

	if (status !== "Success" && status !== "Queued") {
		const button_label = status === "Error" ? __("Retry JoFotara") : __("Send to JoFotara");

		// remove_custom_button ensures we don't have duplicate buttons if refresh is called twice
		frm.remove_custom_button(button_label, __("Actions"));
		
		frm.add_custom_button(
			button_label,
			function () {
				frappe.call({
					method: "corex_fotara.jofotara.controller.send_to_jofotara",
					args: { invoice_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Sending to JoFotara..."),
					callback: function (r) {
						if(!r.exc) frm.reload_doc();
					},
				});
			},
			__("Actions")
		);
	}
}

function render_qr_preview(frm) {
	const qr_data = frm.doc.custom_jofotara_qr;
	const field = frm.fields_dict.custom_qr_preview;

	if (!field || !field.$wrapper) return;

	// PERFORMANCE OPTIMIZATION: 
	// If the QR is already rendered and data hasn't changed, do nothing.
	if (field.$wrapper.attr('data-rendered-qr') === qr_data) {
		return; 
	}

	field.$wrapper.empty();

	if (!qr_data) {
		field.$wrapper.html(
			`<div class="text-muted" style="padding: 15px; border: 1px dashed #d1d8dd; text-align: center; border-radius: 4px;">
				${__("QR code will appear here after successful submission")}
			</div>`
		);
		return;
	}

	// Create a unique container for this specific rendering
	const container_id = `qr-container-${frm.doc.name}`;
	field.$wrapper.append(`<div id="${container_id}" style="display: flex; flex-direction: column; align-items: center; padding: 10px;"></div>`);

	if (typeof QRCode !== "undefined") {
		new QRCode(document.getElementById(container_id), {
			text: qr_data,
			width: 160,
			height: 160,
			correctLevel: QRCode.CorrectLevel.M,
		});
		field.$wrapper.append(`<div class="text-center text-muted mt-2" style="font-size: 11px;">${__("JoFotara Verified")}</div>`);
		
		// Mark as rendered to prevent flicker on next refresh
		field.$wrapper.attr('data-rendered-qr', qr_data);
	} else {
		field.$wrapper.html(`<div class="alert alert-light"><code>${qr_data}</code></div>`);
	}
}

function validate_currency_for_jofotara(frm) {
	if (!frm.doc.custom_jofotara_enabled) return true;

	const currency = frm.doc.currency;
	if (currency !== "JOD") {
		frappe.msgprint({
			title: __("JoFotara Requirement"),
			indicator: "red",
			message: __("JoFotara is enabled for this invoice. The currency must be 'JOD' (Jordanian Dinar) to proceed."),
		});
		frappe.validated = false;
		return false;
	}
	return true;
}

function validate_vat_registration_and_taxes(frm) {
	if (!frm.doc.custom_jofotara_enabled) return true;

	const has_taxes = frm.doc.taxes && frm.doc.taxes.length > 0;
	const is_vat_registered = frm.doc.custom_jofotara_vat_registered;

	if (has_taxes && !is_vat_registered) {
		frappe.msgprint({
			title: __("JoFotara Compliance"),
			indicator: "red",
			message: __("This company is not marked as VAT Registered. Please remove taxes or enable VAT Registration in Company settings."),
		});
		frappe.validated = false;
		return false;
	}
	return true;
}

frappe.realtime.off("jofotara_submission_complete"); // Clear any stale listeners from previous file loads
frappe.realtime.on("jofotara_submission_complete", function(data) {
    // 1. Check if a Form is currently open
    if (!cur_frm || cur_frm.doctype !== "Sales Invoice") return;

    // 2. Check if the open Form is the one that was just processed
    if (cur_frm.doc.name === data.invoice_name) {
        
        // Show Alert
        frappe.show_alert({
            message: __("JoFotara Response: " + data.status),
            indicator: data.status === "Success" ? "green" : "red"
        });

        // Reload
        cur_frm.reload_doc();
    }
});