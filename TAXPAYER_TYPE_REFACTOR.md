# Taxpayer Type Refactor — Change Log

Replaced the legacy `custom_jofotara_vat_registered` boolean with a 3-way `custom_jofotara_taxpayer_type` Select so the `InvoiceTypeCode/@name` 3rd digit can produce `1` (Income), `2` (General Sales), or `3` (Special Sales). Previously only `1` or `2` were reachable.

Use this document to review/revert the behavioral surface area when diagnosing an API submission.

> **Not included in this document:** the cleanup patch (`patches/remove_vat_registered_field.py`) and its registration in `patches.txt`. Excluded intentionally.

---

## 1. `corex_fotara/custom/company_fields.py`

**Before:**
```python
{
    "fieldname": "custom_jofotara_vat_registered",
    "fieldtype": "Check",
    "label": "Registered for Sales Tax (VAT)",
    "insert_after": "custom_jofotara_auto_send",
    "depends_on": "eval:doc.custom_enable_jofotara",
    "description": "You are authorized to collect 16%, 4%, or 0% Sales Tax",
},
{
    "fieldname": "custom_jofotara_save_logs",
    ...
    "insert_after": "custom_jofotara_vat_registered",
    ...
},
```

**After:**
```python
{
    "fieldname": "custom_jofotara_taxpayer_type",
    "fieldtype": "Select",
    "label": "Taxpayer Type",
    "insert_after": "custom_jofotara_auto_send",
    "options": "Income\nGeneral Sales\nSpecial Sales",
    "default": "General Sales",
    "depends_on": "eval:doc.custom_enable_jofotara",
    "mandatory_depends_on": "eval:doc.custom_enable_jofotara",
    "description": "Income = not registered for sales tax; General Sales = VAT registered (16%/4%/0%); Special Sales = subject to special sales tax",
},
{
    "fieldname": "custom_jofotara_save_logs",
    ...
    "insert_after": "custom_jofotara_taxpayer_type",
    ...
},
```

**Effect on XML:** none directly — this just defines the Company form field. Becomes relevant through the XML generator (change #3).

---

## 2. `corex_fotara/custom/sales_invoice_fields.py`

**Before:** the Sales Invoice had a hidden, read-only mirror of the old boolean, inserted before the JoFotara section.
```python
{
    "fieldname": "custom_jofotara_vat_registered",
    "fieldtype": "Check",
    "fetch_from": "company.custom_jofotara_vat_registered",
    "hidden": 1,
    "read_only": 1,
    "insert_after": "custom_jofotara_enabled",
},
# JoFotara Section
{
    "fieldname": "jofotara_section",
    ...
},
{
    "fieldname": "custom_jofotara_payment_type",
    "fieldtype": "Select",
    ...
    "insert_after": "jofotara_section",
    ...
},
```

**After:** the hidden mirror is removed. A new user-editable Select lives inside the JoFotara section, fetched from the company default:
```python
# JoFotara Section
{
    "fieldname": "jofotara_section",
    ...
},
{
    "fieldname": "custom_jofotara_taxpayer_type",
    "fieldtype": "Select",
    "label": "Taxpayer Type",
    "insert_after": "jofotara_section",
    "options": "Income\nGeneral Sales\nSpecial Sales",
    "fetch_from": "company.custom_jofotara_taxpayer_type",
    "description": "Defaults from Company. Override per invoice only if this transaction falls under a different taxpayer category.",
},
{
    "fieldname": "custom_jofotara_payment_type",
    ...
    "insert_after": "custom_jofotara_taxpayer_type",
    ...
},
```

**Effect on XML:** none directly. The invoice field feeds the XML generator (change #3).

---

## 3. `corex_fotara/jofotara/xml_generator.py` — `_get_invoice_type_name()`

**This is the only change that directly affects XML output.**

**Before** (lines ~118–120):
```python
# 3rd Digit: Taxpayer Type (Sales=2, Income=1)
vat_registered = self.company.get("custom_jofotara_vat_registered")
tax_type = "2" if vat_registered else "1"

return f"{is_export}{is_credit}{tax_type}"
```

**After:**
```python
# 3rd Digit: Taxpayer Type (Income=1, General Sales=2, Special Sales=3)
# Invoice-level value overrides company default; falls back to Income.
taxpayer_type = (
    self.invoice.get("custom_jofotara_taxpayer_type")
    or self.company.get("custom_jofotara_taxpayer_type")
    or "Income"
)
tax_type = {"Income": "1", "General Sales": "2", "Special Sales": "3"}.get(taxpayer_type, "1")

return f"{is_export}{is_credit}{tax_type}"
```

**Effect on XML:** changes only the 3rd digit of the `InvoiceTypeCode` `name` attribute.

| Taxpayer Type | Old output | New output |
|---------------|-----------|-----------|
| Income (was `vat_registered=0`) | `xx1` | `xx1` (unchanged) |
| General Sales (was `vat_registered=1`) | `xx2` | `xx2` (unchanged) |
| Special Sales (new) | n/a | `xx3` |

For invoices submitted with Income or General Sales settings, the emitted `name` value is **identical** to pre-change output.

---

## 4. `corex_fotara/public/js/sales_invoice.js` — `validate_vat_registration_and_taxes()`

**Before:**
```js
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
```

**After:**
```js
const taxpayer_type = frm.doc.custom_jofotara_taxpayer_type;

if (has_taxes && taxpayer_type === "Income") {
    frappe.msgprint({
        title: __("JoFotara Compliance"),
        indicator: "red",
        message: __("Taxpayer Type is set to 'Income' (not registered for sales tax). Please remove taxes or change the Taxpayer Type to 'General Sales' or 'Special Sales'."),
    });
    frappe.validated = false;
    return false;
}
```

**Effect on XML:** none. Client-side validation only. If it fails, the invoice never reaches the XML generator.

---

## 5. `corex_fotara/translations/ar.csv`

Removed:
```
Registered for Sales Tax (VAT),مسجل لضريبة المبيعات (ضريبة القيمة المضافة)
"You are authorized to collect 16%, 4%, or 0% Sales Tax","أنت مخول بتحصيل ضريبة مبيعات بنسبة 16% أو 4% أو 0%"
"This company is not marked as VAT Registered. Please remove taxes or enable VAT Registration in Company settings.", ...
```

Added:
```
Taxpayer Type,فئة المكلف
"Income = not registered for sales tax; General Sales = VAT registered (16%/4%/0%); Special Sales = subject to special sales tax", ...
Income,دخل
General Sales,مبيعات عامة
Special Sales,مبيعات خاصة
"Defaults from Company. Override per invoice only if this transaction falls under a different taxpayer category.", ...
"Taxpayer Type is set to 'Income' (not registered for sales tax). Please remove taxes or change the Taxpayer Type to 'General Sales' or 'Special Sales'.", ...
```

**Effect on XML:** none. UI strings only.

---

## 6. `docs/conflicts.md` — §2.3

Rewrote §2.3 from "Not Supported" to "Resolved", pointing at the new field.

**Effect on XML:** none. Documentation only.

---

## Summary — which of these can affect the submitted XML?

| # | File | Affects XML? |
|---|------|--------------|
| 1 | `custom/company_fields.py` | No (form schema) |
| 2 | `custom/sales_invoice_fields.py` | No (form schema) |
| 3 | `jofotara/xml_generator.py` | **Yes — 3rd digit of `InvoiceTypeCode/@name` only.** Value unchanged for Income and General Sales taxpayers. |
| 4 | `public/js/sales_invoice.js` | No (JS validation, runs before XML) |
| 5 | `translations/ar.csv` | No (UI strings) |
| 6 | `docs/conflicts.md` | No (docs) |

If the submitted XML still looks wrong for an Income taxpayer, the cause is in code **outside the scope of this refactor** (e.g., tax-category logic, anonymous customer handling, currency attribute, etc. — see the remaining open items in `docs/conflicts.md`).
