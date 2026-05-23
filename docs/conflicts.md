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