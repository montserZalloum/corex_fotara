# JoFotara E-Invoice Integration Specification

> Extracted from the PHP SDK (jafar-albadarneh/jofotara). This is the single source of truth for building the ERPNext/Frappe integration.

---

## 1. API Protocol

### Endpoint

```
POST https://backend.jofotara.gov.jo/core/invoices/
```

### Authentication

Authentication is done via HTTP headers (no OAuth, no tokens — just static credentials):

| Header         | Value                |
|----------------|----------------------|
| `Client-Id`    | Your client ID       |
| `Secret-Key`   | Your client secret   |
| `Content-Type` | `application/json`   |

### Request Body

```json
{
  "invoice": "<base64_encoded_xml_string>"
}
```

### HTTP Method

`POST` — no other methods are used. No GET for status, no PUT for updates. One endpoint, one method.

### Full Flow

1. Build UBL 2.1 compliant XML string
2. Base64 encode the entire XML string (standard base64, not URL-safe)
3. POST as JSON `{"invoice": "<base64_string>"}` with auth headers
4. Parse the JSON response
5. On success: store QR code, signed invoice, invoice number, and UUID
6. On `ALREADY_SUBMITTED`: treat as success (idempotent — same invoice won't be duplicated)

---

## 2. API Response

The API has returned two different response formats over time. The integration must handle both.

### Format A (newer)

```json
{
  "validationResults": {
    "status": "PASS",
    "errorMessages": [],
    "warningMessages": [],
    "infoMessages": [
      {
        "type": "INFO",
        "code": "XSD_VALID",
        "category": "XSD validation",
        "message": "Complied with UBL 2.1 standards in line with ZATCA specifications",
        "status": "PASS"
      }
    ]
  },
  "invoiceStatus": "SUBMITTED",
  "submittedInvoice": "<base64_signed_invoice>",
  "qrCode": "<qr_code_data>",
  "invoiceNumber": "INV-001",
  "invoiceUUID": "123e4567-..."
}
```

### Format B (older)

```json
{
  "EINV_RESULTS": {
    "status": "...",
    "ERRORS": [],
    "WARNINGS": [],
    "INFO": []
  },
  "EINV_STATUS": "SUBMITTED",
  "EINV_SINGED_INVOICE": "<base64_signed_invoice>",
  "EINV_QR": "<qr_code_data>",
  "EINV_NUM": "...",
  "EINV_INV_UUID": "..."
}
```

### Success Criteria

Success logic **differs between the two formats**:

**Format A:**
- HTTP status code = `200`
- AND `validationResults.status === "PASS"` (exact match)
- AND `invoiceStatus` = `"SUBMITTED"` or `"ALREADY_SUBMITTED"`

**Format B:**
- HTTP status code = `200`
- AND `EINV_RESULTS.status !== "ERROR"` (allows other statuses like `"WARNING"`)
- AND `EINV_STATUS` = `"SUBMITTED"` or `"ALREADY_SUBMITTED"`

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| `200`       | Check `validationResults.status` — could still have errors |
| `400`       | Validation error — check `error` or `errors` field |
| `403`       | Authentication failed — bad Client-Id or Secret-Key |
| Other       | Network/server errors — treat as transient failure |

### Response Fields to Store

| Field | Format A Key | Format B Key | Purpose |
|-------|-------------|-------------|---------|
| Invoice status | `invoiceStatus` | `EINV_STATUS` | SUBMITTED, NOT_SUBMITTED, ALREADY_SUBMITTED |
| Signed invoice | `submittedInvoice` | `EINV_SINGED_INVOICE` | Base64-encoded signed XML (can decode back to XML) |
| QR code | `qrCode` | `EINV_QR` | QR code data for printing |
| Invoice number | `invoiceNumber` | `EINV_NUM` | System-assigned invoice number |
| Invoice UUID | `invoiceUUID` | `EINV_INV_UUID` | System-assigned UUID |
| Errors | `validationResults.errorMessages` | `EINV_RESULTS.ERRORS` | Array of error objects |
| Warnings | `validationResults.warningMessages` | `EINV_RESULTS.WARNINGS` | Array of warning objects |
| Info | `validationResults.infoMessages` | `EINV_RESULTS.INFO` | Array of info objects |

### Error Object Structure

Error/warning/info objects also differ between formats:

**Format A:** `{"type": "...", "code": "...", "category": "...", "message": "...", "status": "..."}`

**Format B:** `{"EINV_CODE": "...", "EINV_MESSAGE": "...", "EINV_CATEGORY": "..."}`

> **Note:** The Format B key `EINV_SINGED_INVOICE` is NOT a typo in this spec — it is the actual key returned by the API (missing the second "N" in "SIGNED"). Use this exact string.

---

## 3. Invoice Types & Payment Methods

### Invoice Types

| Type Key | Arabic | Description |
|----------|--------|-------------|
| `income` | فاتورة دخل | For taxpayers NOT registered for sales tax |
| `general_sales` | فاتورة مبيعات عامة | For taxpayers registered for sales tax (VAT) |
| `special_sales` | فاتورة مبيعات خاصة | For taxpayers subject to special sales tax |

### Payment Method Codes

The payment method code is a 3-digit string that encodes BOTH the invoice type AND the payment method:

| Invoice Type | Cash | Receivable (آجل) |
|-------------|------|-------------------|
| `income` | `011` | `021` |
| `general_sales` | `012` | `022` |
| `special_sales` | `013` | `023` |

### Invoice Type Codes (in XML)

| Scenario | `InvoiceTypeCode` value |
|----------|------------------------|
| Regular invoice (sale) | `388` |
| Credit invoice (return/correction) | `381` |

The payment method code goes in the `name` attribute:
```xml
<cbc:InvoiceTypeCode name="012">388</cbc:InvoiceTypeCode>
```

---

## 4. Tax Categories

| Code | Name | Tax Rate | Use Case |
|------|------|----------|----------|
| `S` | Standard Rate | 1% to 16% | Normal taxable items (Jordan VAT = 16%) |
| `Z` | Exempt | 0% | Tax-exempt items |
| `O` | Zero-rated | 0% | Zero-rated items (e.g., exports) |

---

## 5. Credit Invoices (Returns)

Credit invoices reverse a previously submitted invoice. They require:

1. `InvoiceTypeCode` = `381` (instead of `388`)
2. A `BillingReference` section with:
   - Original invoice ID
   - Original invoice UUID
   - Original full amount (in `DocumentDescription`)
3. A `PaymentMeans` section with:
   - `PaymentMeansCode` = `10` (with `listID="UN/ECE 4461"`)
   - `InstructionNote` = reason for return
4. A reason for return (mandatory)

---

## 6. Customer Information

### ID Types

| Code | Name | Description |
|------|------|-------------|
| `NIN` | National ID Number | Jordanian national ID |
| `PN` | Passport Number | Passport number |
| `TIN` | Tax ID Number | Tax identification number |

### When Customer Name is Required

Customer name is **mandatory** when:
- Payment method is **receivable** (codes: `021`, `022`, `023`)
- OR payable amount > **10,000 JOD**

### Anonymous Customer

If no customer information is provided, the system defaults to:
- ID type: `NIN`
- ID value: empty string `""`

### Jordan City Codes

| Code | City |
|------|------|
| `JO-AM` | Amman (عمان) |
| `JO-IR` | Irbid (إربد) |
| `JO-AZ` | Zarqa (الزرقاء) |
| `JO-BA` | Balqa (البلقاء) |
| `JO-MA` | Mafraq (المفرق) |
| `JO-KA` | Karak (الكرك) |
| `JO-JA` | Jerash (جرش) |
| `JO-AJ` | Ajloun (عجلون) |
| `JO-MN` | Ma'an (معان) |
| `JO-MD` | Madaba (مادبا) |
| `JO-AT` | Tafilah (الطفيلة) |
| `JO-AQ` | Aqaba (العقبة) |

---

## 7. Seller Information

| Field | Required | Validation |
|-------|----------|------------|
| TIN (Tax ID) | Yes | Must be 6+ digits (numeric only) |
| Name | Yes | Cannot be empty |
| Country Code | Fixed | Always `JO` |

---

## 8. Supplier Income Source

- Field: `sequenceId` (تسلسل مصدر الدخل)
- Required: **Yes**
- Validation: Must be numeric digits only
- Found in JoFotara portal under the table that shows client ID and secret

---

## 9. Calculations

### Per Line Item

```
amount_before_discount = quantity * unit_price
amount_after_discount  = amount_before_discount - discount
tax_amount             = amount_after_discount * (tax_percent / 100)   [only if category = 'S']
tax_amount             = 0                                             [if category = 'Z' or 'O']
tax_inclusive_amount   = amount_after_discount + tax_amount
```

### Invoice Totals

```
tax_exclusive_amount  = SUM(item.amount_before_discount)     -- sum of (qty * unit_price) per item
discount_total        = SUM(item.discount)                    -- sum of discounts per item
tax_total             = SUM(item.tax_amount)                  -- sum of tax per item
tax_inclusive_amount  = tax_exclusive_amount - discount_total + tax_total
payable_amount        = tax_inclusive_amount
```

### Important Notes

- All amounts use **9 decimal places** in XML (`%.9f` format)
- All totals are also **rounded to 9 decimal places** when being set (before XML output)
- Discounts are per-item, NOT on the invoice total
- The SDK validates that manually-set totals match calculated values from line items
- Currency ID in XML attributes is `"JO"` (not `"JOD"`)
- `DocumentCurrencyCode` and `TaxCurrencyCode` values are `"JOD"`

### Field Name Clarifications (confusing names in UBL)

| XML Field | Where | Actually Means |
|-----------|-------|---------------|
| `TaxExclusiveAmount` | `LegalMonetaryTotal` | Sum of (qty * unit_price) per item — **BEFORE discounts and tax** |
| `LineExtensionAmount` | `InvoiceLine` | Item amount **AFTER discount** (qty * price - discount) |
| `RoundingAmount` | `InvoiceLine > TaxTotal` | Item **tax-inclusive amount** (after discount + tax) |
| `AllowanceTotalAmount` | `LegalMonetaryTotal` | Total discount across all items (same value as `AllowanceCharge > Amount`) |

---

## 10. Validation Rules Summary

### Required Sections
- Basic invoice information
- Seller information
- Invoice items (at least 1)
- Invoice totals
- Supplier income source

### Field Validations

| Field | Rule |
|-------|------|
| Invoice ID | Non-empty string |
| UUID | UUID v4 format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Issue date | Input `dd-mm-yyyy`, stored as DateTime, output `yyyy-mm-dd` |
| Invoice type | Must be: `income`, `general_sales`, or `special_sales` |
| Payment method | Must be set AFTER invoice type; must match the type |
| Invoice counter (ICV) | Integer >= 1 |
| Seller TIN | 6+ numeric digits |
| Seller name | Non-empty |
| Customer ID + type | Required (defaults to NIN + empty if anonymous) |
| Customer name | Required if receivable OR payable > 10,000 JOD |
| Item quantity | Must be > 0 |
| Item unit price | Must be >= 0 |
| Item discount | >= 0 AND <= (quantity * unit_price) |
| Item description | Non-empty |
| Tax percent (for S) | Between 0 and 16 |
| Supplier income source | Numeric digits, non-empty |

### Cross-Section Validations
- Credit invoices require: original invoice ID, UUID, amount (> 0), AND a reason for return
- Invoice totals must match calculated values from line items (array equality check)
- Customer name required when receivable or > 10,000 JOD
- Payment method code must be valid for the selected invoice type (e.g., `012` only valid for `general_sales`)

### Validation Bypass Mode

The SDK supports disabling detailed validations (`enableValidations=false`). When bypassed:
- Required **sections** are still checked (basic info, seller, items, totals, supplier income source)
- Detailed **field-level** validations are skipped (format checks, range checks)
- **Cross-section** validations are skipped (totals matching items, customer name requirement)
- No automatic calculations or consistency checks

This is useful for edge cases where the API accepts data that the SDK would reject.

### Defaults

| Field | Default Value |
|-------|--------------|
| Invoice counter (ICV) | `1` |
| Currency | `JOD` |
| Line item tax category | `S` (Standard) |
| Line item tax percent | `16.0` |
| Line item unit code | `PCE` (Piece) |
| Line item discount | `0.0` |
| Customer (if not set) | Anonymous: `NIN` + empty ID |

---

## 11. Complete XML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
         xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">

  <cbc:UBLVersionID>2.1</cbc:UBLVersionID>

  <!-- ========== SECTION 1: Basic Information ========== -->
  <cbc:ID>{invoice_id}</cbc:ID>
  <cbc:UUID>{uuid_v4}</cbc:UUID>
  <cbc:IssueDate>{YYYY-MM-DD}</cbc:IssueDate>
  <cbc:InvoiceTypeCode name="{payment_method_code}">{388_or_381}</cbc:InvoiceTypeCode>
  <!-- Optional: -->
  <cbc:Note>{note_text}</cbc:Note>
  <cbc:DocumentCurrencyCode>JOD</cbc:DocumentCurrencyCode>
  <cbc:TaxCurrencyCode>JOD</cbc:TaxCurrencyCode>

  <!-- ========== SECTION 2: Billing Reference (CREDIT INVOICES ONLY) ========== -->
  <cac:BillingReference>
    <cac:InvoiceDocumentReference>
      <cbc:ID>{original_invoice_id}</cbc:ID>
      <cbc:UUID>{original_invoice_uuid}</cbc:UUID>
      <cbc:DocumentDescription>{original_full_amount_formatted_2_decimals}</cbc:DocumentDescription>
    </cac:InvoiceDocumentReference>
  </cac:BillingReference>

  <!-- ========== SECTION 3: Invoice Counter ========== -->
  <cac:AdditionalDocumentReference>
    <cbc:ID>ICV</cbc:ID>
    <cbc:UUID>{sequential_counter}</cbc:UUID>
  </cac:AdditionalDocumentReference>

  <!-- ========== SECTION 4: Seller ========== -->
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cac:PostalAddress>
        <cac:Country>
          <cbc:IdentificationCode>JO</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>{seller_tin}</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>{seller_name}</cbc:RegistrationName>
      </cac:PartyLegalEntity>
    </cac:Party>
  </cac:AccountingSupplierParty>

  <!-- ========== SECTION 5: Customer ========== -->
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cac:PartyIdentification>
        <cbc:ID schemeID="{NIN|PN|TIN}">{customer_id}</cbc:ID>
      </cac:PartyIdentification>
      <!-- Optional: Postal Address -->
      <cac:PostalAddress>
        <cbc:PostalZone>{postal_code}</cbc:PostalZone>
        <cbc:CountrySubentityCode>{JO-XX}</cbc:CountrySubentityCode>
        <cac:Country>
          <cbc:IdentificationCode>JO</cbc:IdentificationCode>
        </cac:Country>
      </cac:PostalAddress>
      <!-- Optional: Tax Scheme -->
      <cac:PartyTaxScheme>
        <cbc:CompanyID>{customer_tin}</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID>VAT</cbc:ID>
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <!-- Optional/Conditional: Legal Entity (name) -->
      <cac:PartyLegalEntity>
        <cbc:RegistrationName>{customer_name}</cbc:RegistrationName>
      </cac:PartyLegalEntity>
    </cac:Party>
    <!-- Optional: Contact -->
    <cac:AccountingContact>
      <cbc:Telephone>{phone}</cbc:Telephone>
    </cac:AccountingContact>
  </cac:AccountingCustomerParty>

  <!-- ========== SECTION 6: Supplier Income Source ========== -->
  <cac:SellerSupplierParty>
    <cac:Party>
      <cac:PartyIdentification>
        <cbc:ID>{supplier_income_source_sequence}</cbc:ID>
      </cac:PartyIdentification>
    </cac:Party>
  </cac:SellerSupplierParty>

  <!-- ========== SECTION 7: Reason for Return (CREDIT INVOICES ONLY) ========== -->
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode listID="UN/ECE 4461">10</cbc:PaymentMeansCode>
    <cbc:InstructionNote>{reason_for_return}</cbc:InstructionNote>
  </cac:PaymentMeans>

  <!-- ========== SECTION 8: Invoice-Level Discount (only if discount > 0) ========== -->
  <cac:AllowanceCharge>
    <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="JO">{total_discount_amount}</cbc:Amount>
  </cac:AllowanceCharge>

  <!-- ========== SECTION 9: Tax Total ========== -->
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="JO">{total_tax_amount}</cbc:TaxAmount>
  </cac:TaxTotal>

  <!-- ========== SECTION 10: Monetary Totals ========== -->
  <cac:LegalMonetaryTotal>
    <cbc:TaxExclusiveAmount currencyID="JO">{sum_of_qty_x_unit_price}</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="JO">{exclusive_minus_discount_plus_tax}</cbc:TaxInclusiveAmount>
    <!-- Only if discount > 0: -->
    <cbc:AllowanceTotalAmount currencyID="JO">{total_discount}</cbc:AllowanceTotalAmount>
    <cbc:PayableAmount currencyID="JO">{final_payable}</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>

  <!-- ========== SECTION 11: Line Items (repeat per item) ========== -->
  <cac:InvoiceLine>
    <cbc:ID>{item_serial_id}</cbc:ID>
    <cbc:InvoicedQuantity unitCode="PCE">{quantity_9_decimals}</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="JO">{amount_after_discount_9_decimals}</cbc:LineExtensionAmount>
    <cac:TaxTotal>
      <cbc:TaxAmount currencyID="JO">{item_tax_amount}</cbc:TaxAmount>
      <cbc:RoundingAmount currencyID="JO">{item_tax_inclusive_amount}</cbc:RoundingAmount>
      <cac:TaxSubtotal>
        <cbc:TaxAmount currencyID="JO">{item_tax_amount}</cbc:TaxAmount>
        <cac:TaxCategory>
          <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5305">{S_or_Z_or_O}</cbc:ID>
          <cbc:Percent>{tax_percent_9_decimals}</cbc:Percent>
          <cac:TaxScheme>
            <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5153">VAT</cbc:ID>
          </cac:TaxScheme>
        </cac:TaxCategory>
      </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:Item>
      <cbc:Name>{item_description}</cbc:Name>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="JO">{unit_price_9_decimals}</cbc:PriceAmount>
      <cac:AllowanceCharge>
        <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
        <cbc:AllowanceChargeReason>DISCOUNT</cbc:AllowanceChargeReason>
        <cbc:Amount currencyID="JO">{item_discount_9_decimals}</cbc:Amount>
      </cac:AllowanceCharge>
    </cac:Price>
  </cac:InvoiceLine>

</Invoice>
```

---

## 12. XML Section Order (MUST follow this order)

1. `cbc:UBLVersionID`
2. `cbc:ID` (invoice ID)
3. `cbc:UUID`
4. `cbc:IssueDate`
5. `cbc:InvoiceTypeCode`
6. `cbc:Note` (optional)
7. `cbc:DocumentCurrencyCode`
8. `cbc:TaxCurrencyCode`
9. `cac:BillingReference` (credit invoices only)
10. `cac:AdditionalDocumentReference` (ICV counter)
11. `cac:AccountingSupplierParty` (seller)
12. `cac:AccountingCustomerParty` (customer)
13. `cac:SellerSupplierParty` (supplier income source)
14. `cac:PaymentMeans` (credit invoices only — reason for return)
15. `cac:AllowanceCharge` (invoice-level discount, only if > 0)
16. `cac:TaxTotal` (invoice-level tax total)
17. `cac:LegalMonetaryTotal` (monetary totals)
18. `cac:InvoiceLine` (repeat for each item)

---

## 13. Example: Complete General Sales Invoice (Cash)

**Scenario:** 2 units of "Premium Widget" at 100 JOD each, 16% VAT, no discount.

```
amount_before_discount = 2 * 100 = 200
discount = 0
amount_after_discount = 200
tax = 200 * 0.16 = 32
tax_inclusive = 200 + 32 = 232
payable = 232
```

**Payment method code:** `012` (general_sales + cash)

---

## 14. Example: Credit Invoice (Return)

**Scenario:** Returning 1 unit of "Product" at 0.01 JOD from income invoice INV-001.

- `InvoiceTypeCode` = `381`
- `BillingReference` with original INV-001 details
- `PaymentMeans` with reason "Defective item returned"
- Payment method code: `011` (income + cash)

---

## 15. Gotchas & Edge Cases

1. **Currency attribute mismatch:** `DocumentCurrencyCode` = `JOD` but `currencyID` attribute in amount fields = `JO`
2. **9 decimal places:** All monetary and quantity values in XML use `%.9f` formatting
3. **Original amount in credit invoice:** Formatted to 2 decimal places (not 9) in `DocumentDescription`
4. **Invoice counter (ICV):** Stored inside `AdditionalDocumentReference` with ID = "ICV", the counter value goes in the nested `UUID` element (confusing but correct)
5. **AllowanceCharge appears twice:** Once at invoice level (section 8, totals) and once per line item (inside `Price`)
6. **Discount at item level only:** Discounts must be distributed to individual items, not applied to the invoice total
7. **`AllowanceTotalAmount` only if discount > 0:** This element is omitted entirely if there's no discount
8. **No sandbox:** JoFotara does not provide a sandbox/test environment. Use past dates and issue credit invoices to reverse test transactions
9. **Both response formats:** The API may return either Format A or Format B — handle both
10. **Anonymous customer still needs XML:** Even without customer info, the `AccountingCustomerParty` section must exist with `NIN` + empty ID
11. **Line-item discount block is ALWAYS included:** The `AllowanceCharge` inside each `InvoiceLine > Price` is always present (even when discount = 0.0). The invoice-level `AllowanceCharge` (section 8) is ONLY included when discount > 0.
12. **AllowanceChargeReason casing differs:** Invoice-level uses lowercase `"discount"`, line-item level uses uppercase `"DISCOUNT"`. This may be validated by the API — preserve exact casing.
13. **Default values in line items:** `taxCategory = "S"`, `taxPercent = 16.0`, `unitCode = "PCE"`, `discount = 0.0`. If you don't explicitly set tax, it defaults to 16% standard rate.
14. **Invoice counter defaults to 1:** If `setInvoiceCounter()` is never called, it defaults to `1`.
15. **XML escaping:** All text values must be XML-escaped (e.g., `&` -> `&amp;`, `<` -> `&lt;`, `>` -> `&gt;`, `"` -> `&quot;`, `'` -> `&apos;`). In Python, use `xml.sax.saxutils.escape()` or `html.escape()`.
16. **XML line endings:** All XML is normalized to Unix LF (`\n`). Any `\r\n` must be replaced with `\n` before encoding.
17. **Customer XML sub-element ordering inside `Party`:** Must follow: (1) `PartyIdentification` (always), (2) `PostalAddress` (only if postal_code or city_code set), (3) `PartyTaxScheme` (only if customer TIN set), (4) `PartyLegalEntity` (only if name set). Then outside `Party` but still inside `AccountingCustomerParty`: (5) `AccountingContact` (only if phone set).
18. **Empty response handling:** If the API returns an empty body or invalid JSON, treat as an error with message "Empty response from API" or "Invalid JSON response from API".
19. **Root `<Invoice>` element must be on ONE line:** In the actual XML output, the opening `<Invoice xmlns="..." xmlns:cac="..." xmlns:cbc="..." xmlns:ext="...">` tag is a single line (not multiline). The template in section 11 shows it multiline for readability only.
20. **XML sections joined with `\n`:** Each section's XML output is joined with newlines (`\n`). The final XML is all sections joined by `\n`.
21. **`ALREADY_SUBMITTED` is idempotent success:** If you submit the same invoice twice (same ID + UUID), the API returns `ALREADY_SUBMITTED` — this should be treated as a success, not an error.
