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

---

## 3. Extras from Reference — Not in Official Docs, Not in Codebase

These are things the PHP SDK reference mentions that the official docs are completely silent about. Since they come from a working implementation that has been tested against the real API, they carry practical weight.

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