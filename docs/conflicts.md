# JoFotara Integration — Conflicts & Discrepancies

> This document covers **only** the points where the three sources disagree.
> If something is consistent across the Official Documentation, the PHP SDK Reference, and our Codebase, it is not listed here.
>
> **Sources:**
> - **Official Docs** — `docs/documentation.md` (JoFotara PDF guide v1.4 + SQL reference) — **Source of Truth**
> - **Reference** — `docs/someone_implementation.md` (extracted from PHP SDK: jafar-albadarneh/jofotara)
> - **Codebase** — The `corex_fotara` Frappe module

---

## 1. Conflicts Between Official Docs and Reference Implementation

These are points where the two documentation sources directly contradict each other. A decision must be made (ideally by testing against the actual API).

### 1.8 Invoice-Level TaxTotal — With or Without Subtotals

| Source | What it says |
|--------|-------------|
| **Official Docs** | Does not detail invoice-level `TaxTotal` structure (only describes line-level) |
| **Reference** (section 11 XML) | Invoice-level `TaxTotal` contains ONLY `TaxAmount` — no `TaxSubtotal` blocks |
| **Codebase** | Invoice-level `TaxTotal` includes `TaxAmount` AND `TaxSubtotal` blocks — `invoice.xml:125-140` |

```xml
<!-- Reference (invoice-level): -->
<cac:TaxTotal>
    <cbc:TaxAmount currencyID="JO">{total}</cbc:TaxAmount>
</cac:TaxTotal>

<!-- Codebase (invoice-level): -->
<cac:TaxTotal>
    <cbc:TaxAmount currencyID="JOD">{{ totals.total_tax }}</cbc:TaxAmount>
    <cac:TaxSubtotal>
        <cbc:TaxableAmount>...</cbc:TaxableAmount>
        <cbc:TaxAmount>...</cbc:TaxAmount>
        <cac:TaxCategory>...</cac:TaxCategory>
    </cac:TaxSubtotal>
</cac:TaxTotal>
```

> **Decision needed:** Official docs are silent. The extra subtotals may be harmless or may cause XSD issues.

### 1.9 Line-Item Discount Structure

| Source | What it says |
|--------|-------------|
| **Official Docs** (section 6.1) | `Price/PriceAmount` = "Unit Price Exclusive of Tax." No mention of discount block inside Price. |
| **Reference** (section 11, gotcha #11) | `AllowanceCharge` inside `<cac:Price>` is always present, even when discount = 0. |
| **Codebase** | NET PRICE approach — no `AllowanceCharge` inside `<cac:Price>` at all. Conditional `AllowanceCharge` as sibling of `TaxTotal` (different XML location). |

```xml
<!-- Reference approach (inside Price, always present): -->
<cac:Price>
    <cbc:PriceAmount currencyID="JO">{unit_price}</cbc:PriceAmount>
    <cac:AllowanceCharge>
        <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
        <cbc:AllowanceChargeReason>DISCOUNT</cbc:AllowanceChargeReason>
        <cbc:Amount currencyID="JO">{discount}</cbc:Amount>
    </cac:AllowanceCharge>
</cac:Price>

<!-- Codebase approach (NET PRICE, no discount block): -->
<cac:Price>
    <cbc:PriceAmount currencyID="JOD">{{ item.unit_price }}</cbc:PriceAmount>
</cac:Price>
```

> **Decision needed:** The official docs are silent on discount structure. If the API validates the presence of `AllowanceCharge` inside `Price`, the NET PRICE approach will fail.

---


### 2.3 Special Sales Tax Type (3rd Digit = 3) Not Supported

- **Official Docs** (section 4.1): Lists codes `013` (Local, Cash, Special) and `023` (Local, Credit, Special) for special sales tax invoices.
- **Codebase:** `xml_generator.py:119-120` only produces `1` (income) or `2` (sales):
  ```python
  tax_type = "2" if vat_registered else "1"
  ```

> **Impact:** Cannot generate invoices for taxpayers subject to special sales tax.

### 2.4 Telephone Marked as Required but Rendered Conditionally

- **Official Docs** (section 5.2): Lists Telephone as "Required" for the customer.
- **Codebase:** `invoice.xml:94-97` wraps the phone block in `{%- if buyer.phone %}`, omitting it entirely when no phone exists.

> **Impact:** Could cause validation failure if the API enforces this.

### 2.5 Validation Checks Customer Tax ID Instead of Customer Name

- **Official Docs** (section 5.2): "If the invoice is Credit OR Cash > 10,000 JOD, the Customer **Name** is Mandatory."
- **Codebase:** `controller.py:338-346` validates `customer.tax_id` instead:
  ```python
  if is_credit_invoice or grand_total > 10000:
      customer = frappe.get_doc("Customer", invoice.customer)
      if not customer.tax_id:
          frappe.throw(...)
  ```

> **Impact:** The code enforces the wrong field.

### 2.6 Z/O Tax Category Based on Geography Instead of Item Properties

- **Official Docs** (section 6.2): Z = Exempt items, O = Zero Rated / Out of Scope items. Recommends handling Z correctly for exempt goods.
- **Codebase:** `xml_generator.py:291` uses customer country as the differentiator:
  ```python
  tax_category = "S" if tax_rate > 0 else ("Z" if self._get_customer_country() == "Jordan" else "O")
  ```

> **Impact:** A domestically exempt item (e.g., bread, medicine) gets `Z` because the customer is in Jordan — not because the item is actually exempt. An export of a taxable item with 0 tax would also get `O` by this logic. The distinction should be driven by the item's tax properties, not the customer's location.
>
> **Note — Real-world example:** Selling to tax-exempt entities like the Jordanian Armed Forces (القوات المسلحة) where tax must be 0%. The correct category is `Z` (Exempt) because the buyer is legally exempt — not because of geography. The current code happens to produce `Z` for this case (Armed Forces are in Jordan), but for the wrong reason. It would break for:
> - A zero-rated **export** to a Jordanian free zone → code gives `Z`, should be `O`
> - An **exempt item** sold to a foreign buyer → code gives `O`, should be `Z`
> - A **standard-rated item** sold to an exempt entity with a special 0% arrangement → code gives `Z` by accident (geography), but the logic is fragile
>
> The fix should derive Z/O from the **Item Tax Template** or a dedicated tax category field, not from `_get_customer_country()`.

### 2.7 `PayableAmount` Formula Difference

- **Official Docs** (section 8): `PayableAmount = TaxInclusiveAmount - PrepaidAmount`
- **Codebase:** `xml_generator.py:365`: `payable = tax_inclusive - allowance_total`

> **Impact:** Subtracts allowance (discount) instead of prepaid amounts. For most invoices (no prepayment, no global discount) the result is the same, but the formula doesn't match the spec.

---

## 3. Extras from Reference — Not in Official Docs, Not in Codebase

These are things the PHP SDK reference mentions that the official docs are completely silent about. Since they come from a working implementation that has been tested against the real API, they carry practical weight.

### 3.1 API Response Handling — Two Response Formats

- **Official Docs:** Say nothing about API response structure.
- **Reference** (section 2): Documents two response formats the API has returned over time.
- **Codebase:** Only handles Format B (`EINV_*` keys).

**Format A (newer):**
```json
{
  "validationResults": { "status": "PASS", "errorMessages": [], ... },
  "invoiceStatus": "SUBMITTED",
  "submittedInvoice": "<base64>",
  "qrCode": "<data>",
  "invoiceNumber": "...",
  "invoiceUUID": "..."
}
```

**Format B (older) — the only one the codebase handles:**
```json
{
  "EINV_RESULTS": { "status": "...", "ERRORS": [], ... },
  "EINV_STATUS": "SUBMITTED",
  "EINV_SINGED_INVOICE": "<base64>",
  "EINV_QR": "<data>",
  "EINV_NUM": "...",
  "EINV_INV_UUID": "..."
}
```

The codebase (`controller.py:179`) only reads Format B keys:
```python
einv_results = response_data.get("EINV_RESULTS", {})
api_status = einv_results.get("status")
```

If the API returns Format A, `EINV_RESULTS` would be `{}`, `api_status` would be `None`, and the code would fall into the success branch regardless of actual validation status.

> **Risk: High.** The codebase could silently treat a failed invoice as successful.

### 3.2 `ALREADY_SUBMITTED` Should Be Treated as Success

- **Official Docs:** Not mentioned.
- **Reference** (gotcha #21): "If you submit the same invoice twice (same ID + UUID), the API returns `ALREADY_SUBMITTED` — treat as success."
- **Codebase:** Does not check `EINV_STATUS` / `invoiceStatus` at all. Only checks `EINV_RESULTS.status`.

> **Risk: High.** On manual retry of a successfully-sent invoice, the codebase would not recognize the success.

### 3.3 Anonymous Customer Must Default to `NIN` + Empty String

- **Official Docs:** Lists customer ID as a required field but doesn't specify anonymous behavior.
- **Reference** (section 6, gotcha #10): "Even without customer info, `AccountingCustomerParty` must exist with `NIN` + empty ID."
- **Codebase:** `xml_generator.py:196` sets `id_value = None` for anonymous cash customers, and `invoice.xml:67` skips the `PartyIdentification` block entirely.

```xml
<!-- Reference says anonymous customer should look like: -->
<cac:PartyIdentification>
    <cbc:ID schemeID="NIN"></cbc:ID>
</cac:PartyIdentification>

<!-- Codebase skips the block entirely for anonymous customers -->
```

> **Risk: High.** Cash/walk-in customers with no ID on file would produce invalid XML.

### 3.4 XML Escaping Not Applied to All Text Fields

- **Official Docs:** Not mentioned.
- **Reference** (gotcha #15): "All text values must be XML-escaped (`&` -> `&amp;`, `<` -> `&lt;`, etc.)."
- **Codebase:** Uses Jinja's `| e` filter on some fields but not all.

| Field | Escaped? |
|-------|----------|
| `seller.name` | Yes (`| e`) |
| `buyer.name` | Yes (`| e`) |
| `invoice.remarks` | Yes (`| e`) |
| `item.name` | Yes (`| e`) |
| `buyer.id_value` | **No** |
| `buyer.phone` | **No** |
| `seller.tax_id` | **No** |
| `income_source_sequence` | **No** |
| `billing_reference.id` | **No** |

> **Risk: Medium.** If any unescaped field contains `&`, `<`, or `>`, the XML becomes malformed and the API will reject it.

### 3.5 Empty/Invalid API Response Not Explicitly Handled

- **Official Docs:** Not mentioned.
- **Reference** (gotcha #18): "If the API returns an empty body or invalid JSON, treat as an error."
- **Codebase:** `api.py:76-78` catches `JSONDecodeError` and wraps raw text, but still returns `success: True` on HTTP 200:
  ```python
  except json.JSONDecodeError:
      response_data = {"raw_response": response.text}
  # Falls through to: return {"success": True, ...}
  ```

> **Risk: Low-Medium.** A malformed 200 response would be treated as success.

### 3.8 Customer `CompanyID` Inside `PartyTaxScheme`

- **Official Docs:** Not explicitly shown in XML structure.
- **Reference** (section 11 XML): Includes `<cbc:CompanyID>{customer_tin}</cbc:CompanyID>` inside the customer's `PartyTaxScheme`.
- **Codebase:** `invoice.xml:83-86` has the `PartyTaxScheme` block but without `CompanyID`:

```xml
<!-- Reference: -->
<cac:PartyTaxScheme>
    <cbc:CompanyID>{customer_tin}</cbc:CompanyID>
    <cac:TaxScheme>
        <cbc:ID>VAT</cbc:ID>
    </cac:TaxScheme>
</cac:PartyTaxScheme>

<!-- Codebase: -->
<cac:PartyTaxScheme>
    <cac:TaxScheme>
        <cbc:ID>VAT</cbc:ID>
    </cac:TaxScheme>
</cac:PartyTaxScheme>
```