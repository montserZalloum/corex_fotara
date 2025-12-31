This is a comprehensive Product Requirements Document (PRD) for the **JoFotara Integration App**. It serves as the single source of truth for developers, stakeholders, and QA testers.

---

# Product Requirements Document (PRD): JoFotara Integration for ERPNext

| Metadata | Details |
| :--- | :--- |
| **Project Name** | JoFotara Integration (Standalone App) |
| **Version** | 1.0.0 |
| **Target Platform** | Frappe Framework / ERPNext v15+ |
| **Compliance Standard** | Jordan National Invoicing System (v1.4) |
| **Doc Status** | **Approved** |

---

## 1. Executive Summary
The goal is to develop a standalone Frappe App that integrates ERPNext with the Jordanian National Invoicing System ("JoFotara"). The system ensures compliance by transmitting Sales Invoices and Return Invoices (Credit Notes) to the government API. The architecture is designed for **data integrity**, **concurrency safety**, and **multi-company isolation**.

### Key Design Philosophy
1.  **Just-In-Time Identity:** Government counters (ICV) and UUIDs are consumed *only* upon the intent to send, preserving sequence numbers.
2.  **Concurrency First:** Strict database locking prevents duplicate counters during high-volume sales (e.g., Supermarkets).
3.  **Auditability:** Raw XML logs provide transparency for debugging.
4.  **Non-Intrusive:** The core ERPNext logic remains untouched; all logic is handled via Hooks and Custom Fields.

---

## 2. System Architecture

*   **App Structure:** Standalone App (`corex_fotara`).
*   **Settings Scope:** **Company-Level**. (Allows multi-company setups with distinct credentials).
*   **Queueing Strategy:**
    1.  **Synchronous (Blocking):** ID Generation, Counter Increment, Database Locking. (Fast, ensures integrity).
    2.  **Asynchronous (Background):** XML Construction, Signing, API Transmission. (Prevents UI freezing).

---

## 3. Data Model & Configuration

### 3.1. Company DocType Extensions
*Rationale:* We inject settings here to allow Company A to use JoFotara while Company B does not.

**New Tab: "JoFotara Settings"**

| Field Label | Field Name | Type | Description / Logic |
| :--- | :--- | :--- | :--- |
| **Enable JoFotara** | `custom_enable_jofotara` | Check | Master switch. If OFF, all logic is bypassed. |
| **Auto-Send on Submit**| `custom_jofotara_auto_send` | Check | If Checked: Triggers flow on `on_submit`. If Unchecked: User must click "Send" button manually. |
| **Client ID** | `custom_jofotara_client_id` | Data | API Credential. |
| **Secret Key** | `custom_jofotara_secret_key` | Password | API Credential. |
| **Income Source Seq** | `custom_income_source_sequence`| Data | The Branch ID provided by the portal (e.g., `9932895`). |
| **Default City Code** | `custom_default_city_code` | Select | Options: `JO-AM`, `JO-IR`, etc. Fallback if Buyer address is missing. |
| **Starter ICV** | `custom_starter_icv` | Int | Manual Input. Sets the starting point for the counter (default 0). |
| **Latest Sent ICV** | `custom_latest_sent_icv` | Int | **Read Only**. Stores the last used counter. Updated programmatically. |
| **Last Daily Seq Date**| `custom_last_daily_seq_date` | Date | **Hidden**. Tracks the date for the custom ID format. |
| **Last Daily Seq No** | `custom_last_daily_seq_no` | Int | **Hidden**. Tracks the sequence for the custom ID format. |

**Child Table: JoFotara UOM Map**
*Field Name:* `custom_uom_mapping`
*Rationale:* Maps ERPNext internal UOMs to UBL standard codes (Concern A).
*   **Columns:** `UOM` (Link), `JoFotara Code` (Data - e.g., "PCE", "KGM").

### 3.2. Tax Configuration (The Supermarket Solution)
*Target DocType:* **Sales Taxes and Charges Template**
*Rationale:* Solves the "Mixed Tax" scenario (Soda 16%, Rice 0%) without creating new DocTypes.

| Field Label | Field Name | Type | Logic |
| :--- | :--- | :--- | :--- |
| **JoFotara Code** | `custom_jofotara_code` | Select | Options: **S** (Standard), **Z** (Zero/Exempt), **O** (Out of Scope). |

### 3.3. Master Data Extensions
*   **Address DocType:**
    *   `custom_jofotara_city_code` (Select): `JO-AM`, `JO-IR`, etc. Visible only if Country is Jordan.
*   **Customer DocType:**
    *   `custom_identification_type` (Select): `National ID`, `Tax ID`, `Passport`. required for Credit Sales.

---

## 4. Transactional Logic (Sales Invoice)

### 4.1. New Fields in Sales Invoice

| Field Label | Field Name | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **JoFotara ID** | `custom_jofotara_id` | Data | Read Only. Format: `[Abbr]-[Date]-[Seq]`. The "Daily ID". |
| **JoFotara UUID** | `custom_jofotara_uuid` | Data | Read Only. The standard UUID4 required by XML header. |
| **JoFotara ICV** | `custom_jofotara_icv` | Int | Read Only. The sequential audit counter (1, 2, 3...). |
| **JoFotara Status** | `custom_jofotara_status` | Select | `Pending` (Default), `Queued`, `Success`, `Error`. |
| **JoFotara QR** | `custom_jofotara_qr` | Long Text| Stores the base64 string or URL of the QR code returned/generated. |

### 4.2. The "Send" Logic (The Heart of the System)
This logic applies to both **Auto-Send** (Hook) and **Manual Button Click**.

**Phase A: ID Generation (Synchronous & Locked)**
1.  **Check:** Does `custom_jofotara_id` already exist?
    *   **Yes:** It's a retry. **SKIP** Phase A. Use existing values.
    *   **No:** Proceed to step 2.
2.  **DB Lock:** Execute `frappe.db.sql("SELECT ... FOR UPDATE")` on the **Company** row.
    *   *Why?* Prevents race conditions. If two cashiers click submit at 10:00:00, one waits for the other.
3.  **Calculate Daily ID:**
    *   Read `custom_last_daily_seq_no` from Company.
    *   If `custom_last_daily_seq_date` != Today -> Reset to 0.
    *   Increment +1.
    *   Format: `CX-2025-12-31-00001`.
4.  **Calculate ICV:**
    *   Read `custom_latest_sent_icv`.
    *   Compare with `custom_starter_icv` -> Take Max.
    *   Increment +1.
5.  **Generate UUID:** Standard Python `uuid.uuid4()`.
6.  **Write:** Update Invoice fields & Update Company Counters.
7.  **Unlock:** Release DB row.

**Phase B: XML Generation & API (Asynchronous)**
1.  **Validation:**
    *   If **Return Invoice**: Check `return_against`. Fetch its `custom_jofotara_uuid`. If missing $\rightarrow$ **Fail**.
    *   If **Credit Invoice** OR **Total > 10k**: Check Customer Tax ID/NIN. If missing $\rightarrow$ **Fail**.
2.  **XML Construction:**
    *   Use Jinja template.
    *   **Math:** Recalculate all totals (`Qty * Price`) using **9 decimal places** (Concern B). Do not trust ERPNext 2-decimal rounding for the XML payload.
    *   **Tax Grouping:** Group items by `custom_jofotara_code` (S, Z, O) for the `<cac:TaxTotal>` summary.
    *   **Address Fallback:** If Customer Address is empty, use Company's `Default City Code`.
3.  **Encoding:** Convert XML string to Bytes $\rightarrow$ Base64 String.
4.  **Request:** POST to JoFotara API with Headers (`Client-ID`, `Secret-Key`).
5.  **Response Handling:**
    *   **Success:** Update Status to `Success`. Save QR Code. Create Log.
    *   **Error:** Update Status to `Error`. Create Log. **User can click "Send" button to retry Phase B using IDs from Phase A.**

---

## 5. Logging & Audit (JoFotara Log)

*Rationale:* Debugging must be easy without decoding Base64 strings.

| Field Label | Field Name | Type | Logic |
| :--- | :--- | :--- | :--- |
| **Invoice** | `invoice` | Link | |
| **Company** | `company` | Link | |
| **Status** | `status` | Select | Success / Error |
| **Generated XML**| `generated_xml` | Code | **The RAW XML string** (Pre-Base64). Readable for humans. |
| **Response Body**| `response_body` | Code | JSON response from Government. |
| **Traceback** | `error_traceback` | Long Text| Python stack trace if code failed. |

---

## 6. Scenarios & Edge Cases

### 6.1. The "Internet Down" Scenario
*   **Action:** User submits invoice. System generates IDs (ICV 500). API call fails.
*   **Result:** Invoice Status = "Error".
*   **Resolution:** User clicks "Send to JoFotara".
*   **Logic:** System detects `custom_jofotara_icv` is already `500`. It **reuses** 500. It does NOT generate 501.
*   *Why?* To prevent gaps in the audit sequence on the government side.

### 6.2. The Supermarket Scenario (Mixed Basket)
*   **Data:** Invoice contains: 1x Pepsi (16% VAT), 1x Rice (Exempt), 1x Export Item (Zero).
*   **Logic:** The Tax Mapping logic iterates items.
    *   Pepsi $\rightarrow$ Tax Template "VAT 16%" $\rightarrow$ Code `S`.
    *   Rice $\rightarrow$ Tax Template "Exempt" $\rightarrow$ Code `Z`.
    *   Export $\rightarrow$ Tax Template "Export" $\rightarrow$ Code `O`.
*   **Result:** One single XML file with 3 `<cac:TaxSubtotal>` blocks. Valid.

### 6.3. Race Condition (Black Friday)
*   **Scenario:** 10 Cashiers submit invoices simultaneously.
*   **Mechanism:** `SELECT ... FOR UPDATE` on Company Settings.
*   **Result:** Cashier 1 gets ICV 100. Cashier 2 gets ICV 101. Cashier 3 gets ICV 102.
*   *Why?* Database serialization guarantees no duplicate numbers.

### 6.4. The "Forgot Address" Scenario
*   **Scenario:** Walk-in customer buys a TV (> 500 JOD). No address recorded.
*   **Logic:** System checks Customer Address $\rightarrow$ Empty. Checks Company `custom_default_city_code` $\rightarrow$ `JO-AM`.
*   **Result:** XML uses `JO-AM` for the buyer. Invoice accepted.

---

## 7. Future Considerations (Not in MVP)
*   **Purchase Invoices:** Currently only Sales are covered. Future versions may track Self-Billing.
*   **QR Printing:** Currently, we store the QR string. Future updates should include a dedicated Print Format Builder component to render this QR code natively without external APIs.

---

## 8. Implementation Steps

1.  **Scaffold App:** `corex_fotara`.
2.  **Create Fields:** Add fields to Company, Address, Customer via `hooks.py` (Fixtures).
3.  **Create Log DocType:** `JoFotara Log`.
4.  **Develop Logic:**
    *   `controller.py`: Hooks for `on_submit`.
    *   `id_manager.py`: The DB Locking and Counter logic.
    *   `xml_generator.py`: Jinja templates + 9-decimal math.
    *   `api.py`: Requests handler.
5.  **Testing:** Simulate Race Conditions and Network Failures.
6.  **Deployment:** Install on Production. Set Company Settings. Map Taxes. Go Live.

--

## 9. Apps & sites

we will use app `corex_fotara` and site `x.conanacademy.com` for testing