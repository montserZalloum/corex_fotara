# JoFotara SDK - Complete Technical Documentation

## Table of Contents

- [1. Project Overview](#1-project-overview)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Author and License](#12-author-and-license)
  - [1.3 Requirements](#13-requirements)
  - [1.4 Installation](#14-installation)
  - [1.5 Project Statistics](#15-project-statistics)
- [2. Project Structure](#2-project-structure)
  - [2.1 Directory Layout](#21-directory-layout)
  - [2.2 File Inventory](#22-file-inventory)
  - [2.3 Namespace and Autoloading](#23-namespace-and-autoloading)
- [3. Architecture](#3-architecture)
  - [3.1 Design Patterns](#31-design-patterns)
  - [3.2 Class Hierarchy](#32-class-hierarchy)
  - [3.3 Data Flow](#33-data-flow)
- [4. Core Service: JoFotaraService](#4-core-service-jofotaraservice)
  - [4.1 Constructor](#41-constructor)
  - [4.2 Properties](#42-properties)
  - [4.3 Section Builder Methods](#43-section-builder-methods)
  - [4.4 XML Generation](#44-xml-generation)
  - [4.5 Invoice Encoding](#45-invoice-encoding)
  - [4.6 Invoice Submission](#46-invoice-submission)
  - [4.7 Section Validation](#47-section-validation)
  - [4.8 HTTP Request Execution](#48-http-request-execution)
- [5. Contracts](#5-contracts)
  - [5.1 ValidatableSection Interface](#51-validatablesection-interface)
- [6. Traits](#6-traits)
  - [6.1 WithValidationConfigs Trait](#61-withvalidationconfigs-trait)
  - [6.2 XmlHelperTrait](#62-xmlhelpertrait)
- [7. Sections (Invoice Components)](#7-sections-invoice-components)
  - [7.1 BasicInvoiceInformation](#71-basicinvoiceinformation)
    - [7.1.1 Constants](#711-constants)
    - [7.1.2 Properties](#712-properties)
    - [7.1.3 Methods](#713-methods)
    - [7.1.4 Invoice Type and Payment Method Mapping](#714-invoice-type-and-payment-method-mapping)
    - [7.1.5 Credit Invoice Support](#715-credit-invoice-support)
    - [7.1.6 Validation Rules](#716-validation-rules)
    - [7.1.7 XML Output](#717-xml-output)
  - [7.2 SellerInformation](#72-sellerinformation)
    - [7.2.1 Static Defaults](#721-static-defaults)
    - [7.2.2 Properties](#722-properties)
    - [7.2.3 Methods](#723-methods)
    - [7.2.4 Validation Rules](#724-validation-rules)
    - [7.2.5 XML Output](#725-xml-output)
  - [7.3 CustomerInformation](#73-customerinformation)
    - [7.3.1 Constants](#731-constants)
    - [7.3.2 Properties](#732-properties)
    - [7.3.3 Methods](#733-methods)
    - [7.3.4 Anonymous Customer](#734-anonymous-customer)
    - [7.3.5 Validation Rules](#735-validation-rules)
    - [7.3.6 XML Output](#736-xml-output)
  - [7.4 SupplierIncomeSource](#74-supplierincomesource)
    - [7.4.1 Properties](#741-properties)
    - [7.4.2 Methods](#742-methods)
    - [7.4.3 Validation Rules](#743-validation-rules)
    - [7.4.4 XML Output](#744-xml-output)
  - [7.5 InvoiceItems](#75-invoiceitems)
    - [7.5.1 Properties](#751-properties)
    - [7.5.2 Methods](#752-methods)
    - [7.5.3 Validation Rules](#753-validation-rules)
  - [7.6 InvoiceLineItem](#76-invoicelineitem)
    - [7.6.1 Properties](#761-properties)
    - [7.6.2 Default Values](#762-default-values)
    - [7.6.3 Methods](#763-methods)
    - [7.6.4 Tax Category Methods](#764-tax-category-methods)
    - [7.6.5 Calculation Methods](#765-calculation-methods)
    - [7.6.6 Validation Rules](#766-validation-rules)
    - [7.6.7 XML Output](#767-xml-output)
  - [7.7 InvoiceTotals](#77-invoicetotals)
    - [7.7.1 Properties](#771-properties)
    - [7.7.2 Methods](#772-methods)
    - [7.7.3 Automatic Calculation](#773-automatic-calculation)
    - [7.7.4 Validation Rules](#774-validation-rules)
    - [7.7.5 XML Output](#775-xml-output)
  - [7.8 ReasonForReturn](#78-reasonforreturn)
    - [7.8.1 Properties](#781-properties)
    - [7.8.2 Methods](#782-methods)
    - [7.8.3 Validation Rules](#783-validation-rules)
    - [7.8.4 XML Output](#784-xml-output)
- [8. Response Handling: JoFotaraResponse](#8-response-handling-jofotararesponse)
  - [8.1 Dual Response Format Support](#81-dual-response-format-support)
  - [8.2 Success Determination Logic](#82-success-determination-logic)
  - [8.3 Properties](#83-properties)
  - [8.4 Methods](#84-methods)
  - [8.5 Error Handling](#85-error-handling)
- [9. API Protocol](#9-api-protocol)
  - [9.1 Endpoint](#91-endpoint)
  - [9.2 Authentication](#92-authentication)
  - [9.3 Request Format](#93-request-format)
  - [9.4 Response Formats](#94-response-formats)
  - [9.5 HTTP Status Codes](#95-http-status-codes)
- [10. XML Specification](#10-xml-specification)
  - [10.1 UBL 2.1 Compliance](#101-ubl-21-compliance)
  - [10.2 XML Namespaces](#102-xml-namespaces)
  - [10.3 Section Ordering](#103-section-ordering)
  - [10.4 Complete XML Template](#104-complete-xml-template)
  - [10.5 Number Formatting](#105-number-formatting)
  - [10.6 XML Escaping](#106-xml-escaping)
  - [10.7 Currency Quirks](#107-currency-quirks)
- [11. Invoice Types](#11-invoice-types)
  - [11.1 Income Invoice](#111-income-invoice)
  - [11.2 General Sales Invoice](#112-general-sales-invoice)
  - [11.3 Special Sales Invoice](#113-special-sales-invoice)
  - [11.4 Credit Invoice (Return)](#114-credit-invoice-return)
- [12. Payment Methods](#12-payment-methods)
  - [12.1 Cash](#121-cash)
  - [12.2 Receivable](#122-receivable)
  - [12.3 Payment Method Code Matrix](#123-payment-method-code-matrix)
- [13. Tax System](#13-tax-system)
  - [13.1 Tax Categories](#131-tax-categories)
  - [13.2 Tax Calculation Formulas](#132-tax-calculation-formulas)
- [14. Calculations](#14-calculations)
  - [14.1 Per Line Item Calculations](#141-per-line-item-calculations)
  - [14.2 Invoice-Level Totals](#142-invoice-level-totals)
  - [14.3 Rounding](#143-rounding)
- [15. Validation System](#15-validation-system)
  - [15.1 Validation Architecture](#151-validation-architecture)
  - [15.2 Field-Level Validations](#152-field-level-validations)
  - [15.3 Cross-Section Validations](#153-cross-section-validations)
  - [15.4 Validation Bypass Mode](#154-validation-bypass-mode)
- [16. Customer Information Details](#16-customer-information-details)
  - [16.1 Customer ID Types](#161-customer-id-types)
  - [16.2 Jordan City Codes](#162-jordan-city-codes)
  - [16.3 Conditional Requirements](#163-conditional-requirements)
- [17. Examples](#17-examples)
  - [17.1 Example: Income Invoice (GenerateIncomeInvoice.php)](#171-example-income-invoice-generateincomeinvoicephp)
  - [17.2 Example: Credit Income Invoice (GenerateCreditIncomeInvoice.php)](#172-example-credit-income-invoice-generatecreditincomeinvoicephp)
- [18. Gotchas and Edge Cases](#18-gotchas-and-edge-cases)
- [19. Testing](#19-testing)
  - [19.1 Test Suite](#191-test-suite)
  - [19.2 Production Testing](#192-production-testing)
- [20. Development Tools](#20-development-tools)
- [21. Composer Configuration Details](#21-composer-configuration-details)
- [22. Security Considerations](#22-security-considerations)

---

## 1. Project Overview

### 1.1 Purpose

JoFotara SDK is a PHP library designed to integrate with Jordan's electronic tax invoicing system known as **JoFotara** (الفوترة الإلكترونية الأردنية). It provides a developer-friendly, fluent API for building, validating, encoding, and submitting UBL 2.1 compliant electronic invoices to the Jordan Tax Authority (Income and Sales Tax Department - ISTD).

The name "JoFotara" is an abbreviation commonly used for the Jordanian e-invoicing portal operated by the government at `backend.jofotara.gov.jo`.

### 1.2 Author and License

- **Package Name:** `jafar-albadarneh/jofotara`
- **Author:** Jafar Albadarneh (`jafar.albadarneh@gmail.com`)
- **Role:** Software Engineer
- **Homepage:** `https://github.com/jafar-albadarneh/jofotara`
- **License:** MIT License
- **Copyright:** jafar-albadarneh

### 1.3 Requirements

| Requirement | Version/Details |
|---|---|
| PHP | `^8.3` (PHP 8.3 or higher) |
| ext-curl | Required (for HTTP API communication) |
| ext-dom | Required for development only |
| ext-libxml | Required for development only |

### 1.4 Installation

```bash
composer require jafar-albadarneh/jofotara
```

### 1.5 Project Statistics

| Metric | Value |
|---|---|
| Total PHP source files | 13 |
| Total PHP lines of code | 2,834 |
| Source classes | 11 |
| Example files | 2 |
| Contracts (interfaces) | 1 |
| Traits | 2 |
| Section classes | 8 |
| Response classes | 1 |
| Core service classes | 1 |

---

## 2. Project Structure

### 2.1 Directory Layout

```
jofotara-main/
├── CHANGELOG.md                          # Empty changelog placeholder
├── JOFOTARA_INTEGRATION_SPEC.md          # Detailed integration specification
├── LICENSE.md                            # MIT License
├── README.md                             # Project readme with usage examples
├── composer.json                         # Composer package configuration
├── examples/
│   ├── GenerateCreditIncomeInvoice.php   # Credit invoice example (152 lines)
│   └── GenerateIncomeInvoice.php         # Income invoice example (147 lines)
└── src/
    ├── Contracts/
    │   └── ValidatableSection.php        # Interface for validatable sections (26 lines)
    ├── JoFotaraService.php               # Main entry-point service class (424 lines)
    ├── Response/
    │   └── JoFotaraResponse.php          # API response wrapper (286 lines)
    ├── Sections/
    │   ├── BasicInvoiceInformation.php   # Invoice header/basic info section (396 lines)
    │   ├── CustomerInformation.php       # Buyer/customer section (256 lines)
    │   ├── InvoiceItems.php              # Item collection container (119 lines)
    │   ├── InvoiceLineItem.php           # Individual line item (374 lines)
    │   ├── InvoiceTotals.php             # Invoice monetary totals (250 lines)
    │   ├── ReasonForReturn.php           # Credit invoice reason (69 lines)
    │   ├── SellerInformation.php         # Seller/supplier party section (183 lines)
    │   └── SupplierIncomeSource.php      # Income source sequence (92 lines)
    └── Traits/
        ├── WithValidationConfigs.php     # Validation toggle trait (28 lines)
        └── XmlHelperTrait.php            # XML escaping/normalization (32 lines)
```

### 2.2 File Inventory

| File | Path | Type | Lines | Description |
|---|---|---|---|---|
| `composer.json` | `/` | Config | 51 | Package metadata, dependencies, autoloading |
| `README.md` | `/` | Docs | 428 | Usage guide and API documentation |
| `CHANGELOG.md` | `/` | Docs | 3 | Placeholder (no entries yet) |
| `LICENSE.md` | `/` | Docs | 21 | MIT License text |
| `JOFOTARA_INTEGRATION_SPEC.md` | `/` | Docs | 601 | Detailed integration specification |
| `JoFotaraService.php` | `src/` | Class | 424 | Main service, orchestrates all sections |
| `ValidatableSection.php` | `src/Contracts/` | Interface | 26 | Contract for section validation |
| `JoFotaraResponse.php` | `src/Response/` | Class | 286 | API response parsing and access |
| `BasicInvoiceInformation.php` | `src/Sections/` | Class | 396 | Invoice header data |
| `SellerInformation.php` | `src/Sections/` | Class | 183 | Seller/supplier party data |
| `CustomerInformation.php` | `src/Sections/` | Class | 256 | Customer/buyer party data |
| `SupplierIncomeSource.php` | `src/Sections/` | Class | 92 | Income source sequence ID |
| `InvoiceItems.php` | `src/Sections/` | Class | 119 | Collection of line items |
| `InvoiceLineItem.php` | `src/Sections/` | Class | 374 | Single line item with tax |
| `InvoiceTotals.php` | `src/Sections/` | Class | 250 | Monetary and tax totals |
| `ReasonForReturn.php` | `src/Sections/` | Class | 69 | Return reason (credit invoices) |
| `XmlHelperTrait.php` | `src/Traits/` | Trait | 32 | XML escaping and line normalization |
| `WithValidationConfigs.php` | `src/Traits/` | Trait | 28 | Validation enable/disable toggle |
| `GenerateIncomeInvoice.php` | `examples/` | Script | 147 | Complete income invoice example |
| `GenerateCreditIncomeInvoice.php` | `examples/` | Script | 152 | Complete credit invoice example |

### 2.3 Namespace and Autoloading

The project uses **PSR-4** autoloading.

| Namespace | Directory |
|---|---|
| `JBadarneh\JoFotara\` | `src/` |
| `JBadarneh\JoFotara\Tests\` | `tests/` (dev only) |

All source classes reside under the root namespace `JBadarneh\JoFotara`. Sub-namespaces mirror the directory structure:

- `JBadarneh\JoFotara\Contracts` - Interfaces
- `JBadarneh\JoFotara\Response` - API response handling
- `JBadarneh\JoFotara\Sections` - Invoice section builders
- `JBadarneh\JoFotara\Traits` - Reusable traits

---

## 3. Architecture

### 3.1 Design Patterns

The SDK employs several design patterns:

1. **Builder Pattern**: The main `JoFotaraService` class and each section class use a fluent builder pattern. Methods return `$this` (or the section instance) allowing method chaining:
   ```php
   $invoice->basicInformation()
       ->setInvoiceId('INV-001')
       ->setUuid('...')
       ->setIssueDate('16-02-2025')
       ->setInvoiceType('general_sales')
       ->cash();
   ```

2. **Lazy Initialization**: Section objects (`SellerInformation`, `CustomerInformation`, `InvoiceItems`, etc.) are only instantiated when first accessed through their builder methods. They are stored as nullable private properties on `JoFotaraService`.

3. **Strategy Pattern (implicit)**: Each section class knows how to validate itself and generate its own XML fragment, following the `ValidatableSection` interface contract.

4. **Template Method Pattern (implicit)**: The `generateXml()` method in `JoFotaraService` orchestrates all sections in a fixed order, calling each section's `toXml()` method.

5. **Static Configuration**: `SellerInformation` supports static defaults via `configureDefaults()` so that the same seller info can be reused across multiple invoice instances without repetition.

### 3.2 Class Hierarchy

```
ValidatableSection (Interface)
├── BasicInvoiceInformation (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── SellerInformation (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── CustomerInformation (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── SupplierIncomeSource (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── InvoiceItems (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── InvoiceLineItem (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
├── InvoiceTotals (implements ValidatableSection)
│   └── uses WithValidationConfigs, XmlHelperTrait
└── ReasonForReturn (implements ValidatableSection)
    └── uses WithValidationConfigs, XmlHelperTrait

JoFotaraService (orchestrator - no interface)
    └── Composes all section classes

JoFotaraResponse (standalone - no interface)
    └── Wraps and normalizes API responses
```

### 3.3 Data Flow

```
[User Code]
    │
    ▼
JoFotaraService (instantiate with clientId + clientSecret)
    │
    ├── basicInformation() → BasicInvoiceInformation (set ID, UUID, date, type, payment)
    ├── sellerInformation() → SellerInformation (set TIN, name)
    ├── customerInformation() → CustomerInformation (set ID, name, address, phone)
    ├── supplierIncomeSource() → SupplierIncomeSource (set sequence ID)
    ├── items() → InvoiceItems
    │       └── addItem() → InvoiceLineItem (set quantity, price, description, tax)
    ├── invoiceTotals() → InvoiceTotals (auto-calculated or manual)
    └── setReasonForReturn() → ReasonForReturn (credit invoices only)
    │
    ▼
generateXml()
    │
    ├── 1. validateSections() — checks required sections + cross-section rules
    ├── 2. Builds XML declaration + root <Invoice> element
    ├── 3. Adds UBLVersionID
    ├── 4. Calls basicInfo.toXml()
    ├── 5. Calls sellerInfo.toXml()
    ├── 6. Calls customerInfo.toXml()
    ├── 7. Calls supplierIncomeSource.toXml()
    ├── 8. Calls reasonForReturn.toXml() (credit invoices only)
    ├── 9. Calls invoiceTotals.toXml()
    ├── 10. Calls items.toXml()
    └── 11. Closes </Invoice>
    │
    ▼
encodeInvoice()
    │
    └── base64_encode(xml)
    │
    ▼
send()
    │
    ├── 1. Calls encodeInvoice()
    ├── 2. Builds JSON payload {"invoice": "<base64>"}
    ├── 3. Sets headers (Client-Id, Secret-Key, Content-Type)
    ├── 4. Executes HTTP POST via cURL
    ├── 5. Parses JSON response
    └── 6. Returns JoFotaraResponse
```

---

## 4. Core Service: JoFotaraService

**File:** `src/JoFotaraService.php`
**Namespace:** `JBadarneh\JoFotara`
**Lines:** 424

This is the main entry point of the SDK. It orchestrates all invoice sections, validates data integrity, generates UBL 2.1 XML, encodes it to base64, and sends it to the JoFotara API.

### 4.1 Constructor

```php
public function __construct(string $clientId, string $clientSecret, bool $enableValidations = true)
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `$clientId` | `string` | Yes | - | JoFotara API client ID |
| `$clientSecret` | `string` | Yes | - | JoFotara API secret key |
| `$enableValidations` | `bool` | No | `true` | Enable/disable built-in validations |

**Behavior:**
- Throws `InvalidArgumentException` if either `$clientId` or `$clientSecret` is empty.
- Stores credentials as private properties.
- Immediately creates a `BasicInvoiceInformation` instance (the only section created eagerly).
- Propagates the `$enableValidations` flag to the basic info section.

### 4.2 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `API_URL` | `const string` | `'https://backend.jofotara.gov.jo/core/invoices/'` | JoFotara API endpoint |
| `$basicInfo` | `BasicInvoiceInformation` | (created in constructor) | Invoice header information |
| `$sellerInfo` | `?SellerInformation` | `null` | Seller/supplier party info |
| `$customerInfo` | `?CustomerInformation` | `null` | Customer/buyer info |
| `$supplierIncomeSource` | `?SupplierIncomeSource` | `null` | Income source sequence |
| `$items` | `?InvoiceItems` | `null` | Collection of line items |
| `$invoiceTotals` | `?InvoiceTotals` | `null` | Monetary totals |
| `$reasonForReturn` | `?ReasonForReturn` | `null` | Credit invoice reason |
| `$clientId` | `string` | - | API client ID |
| `$clientSecret` | `string` | - | API secret key |
| `$validationsEnabled` | `bool` | `true` | Global validation toggle |

### 4.3 Section Builder Methods

Each section builder method uses lazy initialization: the section object is created on first access and reused on subsequent calls.

#### `basicInformation(): BasicInvoiceInformation`
Returns the basic invoice information builder. This section is always available (created in constructor).

#### `sellerInformation(): SellerInformation`
Returns the seller information builder. Creates a new `SellerInformation` instance on first call. Propagates the validation flag.

#### `customerInformation(): CustomerInformation`
Returns the customer information builder. Creates a new `CustomerInformation` instance on first call. **Also sets default anonymous customer** (`setId('', 'NIN')`) immediately after creation. Propagates the validation flag.

#### `supplierIncomeSource(string $sequence): SupplierIncomeSource`
Returns the supplier income source builder. Unlike other builders, this method requires the `$sequence` parameter (the income source sequence ID from the JoFotara portal). Creates a new `SupplierIncomeSource` instance on first call. Propagates the validation flag.

#### `items(): InvoiceItems`
Returns the invoice items builder. Creates a new `InvoiceItems` instance on first call. Propagates the validation flag.

#### `setReasonForReturn(string $reason): self`
Sets the reason for return (used in credit invoices). Creates a `ReasonForReturn` instance on first call and sets the reason text. Returns `$this` for chaining.

#### `invoiceTotals(): InvoiceTotals`
Returns the invoice totals builder. Creates a new `InvoiceTotals` instance on first call. **Performs automatic calculation** if items already exist:
1. Iterates all items.
2. Sums `amountBeforeDiscount`, `taxAmount`, and `discount` for each item.
3. Calculates `taxInclusiveAmount = amountBeforeDiscount - discountTotalAmount + totalTaxAmount`.
4. Sets `payableAmount = taxInclusiveAmount`.
5. Populates the totals object with calculated values.

### 4.4 XML Generation

```php
public function generateXml(): string
```

Builds the complete UBL 2.1 XML string. Steps:
1. Calls `validateSections()` (respects `validationsEnabled` flag).
2. Adds XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`.
3. Adds the root `<Invoice>` element with all four UBL namespaces on a single line.
4. Adds `<cbc:UBLVersionID>2.1</cbc:UBLVersionID>`.
5. Appends basic info XML.
6. Appends seller info XML (if set).
7. Appends customer info XML (if set).
8. Appends supplier income source XML (if set).
9. Appends reason for return XML (if credit invoice and reason is set).
10. Appends invoice totals XML.
11. Appends items XML (if set).
12. Closes `</Invoice>`.
13. Joins all sections with `\n` (newline).

Returns the complete XML as a string.

### 4.5 Invoice Encoding

```php
public function encodeInvoice(): string
```

Calls `generateXml()` and then applies `base64_encode()` to the result. Returns the base64-encoded XML string. This is the format required by the JoFotara API.

### 4.6 Invoice Submission

```php
public function send(): JoFotaraResponse
```

Complete submission flow:
1. Calls `encodeInvoice()` to get the base64-encoded XML.
2. Calls `executeRequest()` with:
   - URL: `https://backend.jofotara.gov.jo/core/invoices/`
   - Headers: `Client-Id`, `Secret-Key`, `Content-Type: application/json`
   - Body: `{"invoice": "<base64_string>"}`
3. If cURL returns an error, throws `RuntimeException`.
4. If HTTP status is 403, returns a `JoFotaraResponse` with authentication error.
5. Parses JSON response with `json_decode()`.
6. If response is empty or JSON is invalid, creates an error response object.
7. Returns a `JoFotaraResponse` wrapping the parsed data.

**Exceptions thrown:**
- `InvalidArgumentException` - from validation during encoding
- `RuntimeException` - from cURL communication errors

### 4.7 Section Validation

```php
private function validateSections(): void
```

This method is called by `generateXml()` before any XML is built.

**Always checked (regardless of validation flag):**
1. Credit invoices must have a reason for return.
2. Seller information must be initialized.
3. Customer information must be initialized (if not, creates anonymous customer automatically).
4. Supplier income source must be initialized.
5. Items must be initialized.
6. Invoice totals must be initialized.

**Only checked when validations are enabled:**
1. Calls `validateSection()` on each section.
2. **Cross-section: Customer name requirement** - Customer name is required if:
   - Payment method is receivable (codes `021`, `022`, `023`), OR
   - Payable amount exceeds 10,000 JOD.
3. **Cross-section: Totals consistency** - Recalculates totals from line items and compares with the provided totals using strict array equality (`!==`). Throws `InvalidArgumentException` if they don't match.

### 4.8 HTTP Request Execution

```php
protected function executeRequest(string $url, array $headers, string $body): array
```

Low-level HTTP POST using cURL:
- Uses `CURLOPT_RETURNTRANSFER` to capture response.
- Uses `CURLOPT_POST` for POST method.
- Sets custom headers via `CURLOPT_HTTPHEADER`.
- Sets body via `CURLOPT_POSTFIELDS`.
- Returns an array: `[$response, $statusCode, $error]`.
- This method is `protected`, allowing subclasses to override it for testing/mocking.

---

## 5. Contracts

### 5.1 ValidatableSection Interface

**File:** `src/Contracts/ValidatableSection.php`
**Namespace:** `JBadarneh\JoFotara\Contracts`
**Lines:** 26

Defines the contract that all invoice section classes must implement.

```php
interface ValidatableSection
{
    public function validateSection(): void;
    public function setValidationsEnabled(bool $enabled): self;
    public function isValidationsEnabled(): bool;
}
```

| Method | Return | Description |
|---|---|---|
| `validateSection()` | `void` | Validates all required fields; throws `InvalidArgumentException` on failure |
| `setValidationsEnabled(bool)` | `self` | Enables or disables validation for this section |
| `isValidationsEnabled()` | `bool` | Returns whether validations are currently enabled |

Every section class in the SDK implements this interface. The implementation of `setValidationsEnabled()` and `isValidationsEnabled()` is provided by the `WithValidationConfigs` trait.

---

## 6. Traits

### 6.1 WithValidationConfigs Trait

**File:** `src/Traits/WithValidationConfigs.php`
**Namespace:** `JBadarneh\JoFotara\Traits`
**Lines:** 28

Provides the standard implementation for the validation toggle methods declared in `ValidatableSection`.

**Property:**
```php
protected bool $validationsEnabled = true;
```

**Methods:**

| Method | Return | Description |
|---|---|---|
| `setValidationsEnabled(bool $enabled)` | `self` | Sets the validation flag and returns `$this` for chaining |
| `isValidationsEnabled()` | `bool` | Returns the current validation flag value |

Used by: `BasicInvoiceInformation`, `SellerInformation`, `CustomerInformation`, `SupplierIncomeSource`, `InvoiceItems`, `InvoiceLineItem`, `InvoiceTotals`, `ReasonForReturn` (all 8 section classes).

### 6.2 XmlHelperTrait

**File:** `src/Traits/XmlHelperTrait.php`
**Namespace:** `JBadarneh\JoFotara\Traits`
**Lines:** 32

Provides XML utility methods used by all section classes for safe XML output.

**Methods:**

#### `escapeXml(?string $value): string`
- Escapes special characters for XML output.
- Returns empty string if input is `null`.
- Uses `htmlspecialchars()` with `ENT_XML1 | ENT_QUOTES` flags and `UTF-8` encoding.
- Escapes: `&` -> `&amp;`, `<` -> `&lt;`, `>` -> `&gt;`, `"` -> `&quot;`, `'` -> `&apos;`.

#### `normalizeXml(string $xml): string`
- Normalizes line endings to Unix LF (`\n`).
- Replaces all `\r\n` (Windows-style) with `\n`.
- Applied to the final XML output of each section's `toXml()` method.

Used by: All 8 section classes.

---

## 7. Sections (Invoice Components)

Each section represents a distinct part of the UBL 2.1 invoice XML. All sections implement `ValidatableSection` and use both `WithValidationConfigs` and `XmlHelperTrait`.

### 7.1 BasicInvoiceInformation

**File:** `src/Sections/BasicInvoiceInformation.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 396

Handles the invoice header: ID, UUID, date, type, payment method, currency, invoice counter, optional notes, and credit invoice references.

#### 7.1.1 Constants

```php
public const INVOICE_TYPES = [
    'income'        => ['cash' => '011', 'receivable' => '021'],
    'general_sales' => ['cash' => '012', 'receivable' => '022'],
    'special_sales' => ['cash' => '013', 'receivable' => '023'],
];
```

This constant maps each invoice type to its two possible payment method codes. The first digit indicates payment method (0 = cash, 0 = receivable prefix), the second digit is always a prefix, and the third digit indicates invoice type (1 = income, 2 = general sales, 3 = special sales).

#### 7.1.2 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$invoiceId` | `string` | (uninitialized) | Unique invoice identifier |
| `$uuid` | `string` | (uninitialized) | UUID v4 format identifier |
| `$issueDate` | `DateTime` | (uninitialized) | Invoice issue date |
| `$paymentMethod` | `string` | (uninitialized) | 3-digit payment method code |
| `$invoiceType` | `?string` | `null` | Invoice type key |
| `$note` | `?string` | `null` | Optional note/description |
| `$currency` | `string` | `'JOD'` | Currency code (fixed) |
| `$invoiceCounter` | `int` | `1` | Sequential invoice counter (ICV) |
| `$isCreditInvoice` | `bool` | `false` | Whether this is a credit invoice |
| `$originalInvoiceId` | `?string` | `null` | Original invoice ID (credit only) |
| `$originalInvoiceUuid` | `?string` | `null` | Original invoice UUID (credit only) |
| `$originalFullAmount` | `?float` | `null` | Original invoice amount (credit only) |

#### 7.1.3 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `setInvoiceId(string $invoiceId)` | Invoice ID string | `self` | Sets the unique invoice identifier |
| `setUuid(string $uuid)` | UUID string | `self` | Sets the invoice UUID (v4 format) |
| `setIssueDate(string\|DateTime $date)` | Date in `dd-mm-yyyy` format or DateTime object | `self` | Sets the issue date; validates format if enabled |
| `setInvoiceType(string $type)` | `'income'`, `'general_sales'`, or `'special_sales'` | `self` | Sets the invoice type; validates against `INVOICE_TYPES` keys |
| `getPaymentMethod()` | - | `?string` | Returns the current payment method code |
| `setPaymentMethod(string $method)` | 3-digit code | `self` | Sets payment method directly; requires invoice type to be set first; validates code against type |
| `cash()` | - | `self` | Shorthand: sets payment method to the cash code for the current invoice type |
| `receivable()` | - | `self` | Shorthand: sets payment method to the receivable code for the current invoice type |
| `setNote(?string $note)` | Note text or null | `self` | Sets an optional invoice note |
| `setInvoiceCounter(int $counter)` | Integer >= 1 | `self` | Sets the invoice counter (ICV); throws if < 1 |
| `asCreditInvoice(string, string, float)` | Original ID, UUID, amount | `self` | Marks as credit invoice and sets original invoice references |
| `isCreditInvoice()` | - | `bool` | Returns whether this is a credit invoice |
| `toXml()` | - | `string` | Generates XML fragment for this section |
| `toArray()` | - | `array` | Returns current state as associative array (for testing) |
| `validateSection()` | - | `void` | Validates all fields; throws on failure |

#### 7.1.4 Invoice Type and Payment Method Mapping

The invoice type **must** be set before the payment method. The `cash()` and `receivable()` convenience methods automatically look up the correct code based on the current invoice type:

| Invoice Type | `cash()` Code | `receivable()` Code |
|---|---|---|
| `income` | `011` | `021` |
| `general_sales` | `012` | `022` |
| `special_sales` | `013` | `023` |

Calling `cash()` or `receivable()` without setting the invoice type first throws `InvalidArgumentException`.

#### 7.1.5 Credit Invoice Support

To create a credit invoice (return/correction of a previously submitted invoice):

```php
->asCreditInvoice(
    originalInvoiceId: 'INV-001',
    originalInvoiceUuid: '123e4567-e89b-12d3-a456-426614174000',
    originalFullAmount: 200.00
)
```

This:
1. Sets `$isCreditInvoice = true`.
2. Stores the three original invoice references.
3. Changes the `InvoiceTypeCode` value from `388` (regular) to `381` (credit).
4. Adds a `<cac:BillingReference>` section to the XML with:
   - `<cbc:ID>` = original invoice ID
   - `<cbc:UUID>` = original invoice UUID
   - `<cbc:DocumentDescription>` = original amount formatted to 2 decimal places

#### 7.1.6 Validation Rules

When `validateSection()` is called (and validations are enabled):

| Field | Rule |
|---|---|
| Invoice ID | Must be set and non-empty (after trim) |
| UUID | Must be set and match UUID v4 regex: `/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i` |
| Issue Date | Must be set |
| Invoice Type | Must be set (one of `income`, `general_sales`, `special_sales`) |
| Payment Method | Must be set |
| Original Invoice ID | Required and non-empty (credit invoices only) |
| Original Invoice UUID | Required and non-empty (credit invoices only) |
| Original Full Amount | Must be > 0 (credit invoices only) |

#### 7.1.7 XML Output

The `toXml()` method generates the following XML elements:

```xml
<cbc:ID>{invoiceId}</cbc:ID>
<cbc:UUID>{uuid}</cbc:UUID>
<cbc:IssueDate>{YYYY-MM-DD}</cbc:IssueDate>
<cbc:InvoiceTypeCode name="{paymentMethodCode}">{388|381}</cbc:InvoiceTypeCode>
<cbc:Note>{note}</cbc:Note>                          <!-- optional, only if note is set -->
<cbc:DocumentCurrencyCode>JOD</cbc:DocumentCurrencyCode>
<cbc:TaxCurrencyCode>JOD</cbc:TaxCurrencyCode>
<cac:BillingReference>                                <!-- only for credit invoices -->
    <cac:InvoiceDocumentReference>
        <cbc:ID>{originalInvoiceId}</cbc:ID>
        <cbc:UUID>{originalInvoiceUuid}</cbc:UUID>
        <cbc:DocumentDescription>{originalFullAmount_2decimals}</cbc:DocumentDescription>
    </cac:InvoiceDocumentReference>
</cac:BillingReference>
<cac:AdditionalDocumentReference>
    <cbc:ID>ICV</cbc:ID>
    <cbc:UUID>{invoiceCounter}</cbc:UUID>
</cac:AdditionalDocumentReference>
```

**Note:** The issue date is converted from the input format (`dd-mm-yyyy`) to the XML format (`YYYY-MM-DD`) using `DateTime::format('Y-m-d')`.

---

### 7.2 SellerInformation

**File:** `src/Sections/SellerInformation.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 183

Represents the seller/supplier accounting party. The country code is hardcoded to `JO` (Jordan).

#### 7.2.1 Static Defaults

The class supports static default configuration to avoid repeating seller info across multiple invoices:

```php
public static function configureDefaults(string $tin, string $name): void
```

- Validates that both `$tin` and `$name` are non-empty (after trim).
- Stores in `private static ?array $defaults`.
- When a new `SellerInformation` instance is created, the constructor checks for defaults and auto-populates.

```php
public static function clearDefaults(): void
```

Resets the static defaults to `null`.

#### 7.2.2 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$defaults` | `static ?array` | `null` | Shared default seller values |
| `$tin` | `string` | (uninitialized or from defaults) | Tax Identification Number |
| `$name` | `string` | (uninitialized or from defaults) | Registered company name |

#### 7.2.3 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `configureDefaults(string, string)` | TIN, name | `void` | (static) Sets shared defaults for all new instances |
| `clearDefaults()` | - | `void` | (static) Clears shared defaults |
| `setTin(string $tin)` | TIN string | `self` | Sets the seller's TIN; validates non-empty if enabled |
| `setName(string $name)` | Name string | `self` | Sets the seller's name; validates non-empty if enabled |
| `toArray()` | - | `array` | Returns `['tin' => ..., 'name' => ..., 'countryCode' => 'JO']` |
| `toXml()` | - | `string` | Generates XML fragment; calls `toArray()` internally |
| `validateSection()` | - | `void` | Validates TIN format (6+ digits) and name (non-empty) |

#### 7.2.4 Validation Rules

| Field | Rule |
|---|---|
| TIN | Must be set, must match `/^\d{6,}$/` (6 or more digits, numeric only) |
| Name | Must be set and non-empty (after trim) |

#### 7.2.5 XML Output

```xml
<cac:AccountingSupplierParty>
    <cac:Party>
        <cac:PostalAddress>
            <cac:Country>
                <cbc:IdentificationCode>JO</cbc:IdentificationCode>
            </cac:Country>
        </cac:PostalAddress>
        <cac:PartyTaxScheme>
            <cbc:CompanyID>{tin}</cbc:CompanyID>
            <cac:TaxScheme>
                <cbc:ID>VAT</cbc:ID>
            </cac:TaxScheme>
        </cac:PartyTaxScheme>
        <cac:PartyLegalEntity>
            <cbc:RegistrationName>{name}</cbc:RegistrationName>
        </cac:PartyLegalEntity>
    </cac:Party>
</cac:AccountingSupplierParty>
```

---

### 7.3 CustomerInformation

**File:** `src/Sections/CustomerInformation.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 256

Represents the buyer/customer accounting party. All fields except ID/type are optional, but customer name becomes conditionally required based on payment method and amount.

#### 7.3.1 Constants

```php
private const VALID_CITY_CODES = [
    'JO-BA', 'JO-MN', 'JO-MD', 'JO-MA', 'JO-KA', 'JO-JA',
    'JO-IR', 'JO-AZ', 'JO-AT', 'JO-AQ', 'JO-AM', 'JO-AJ',
];
```

The 12 Jordanian governorate codes.

#### 7.3.2 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$id` | `?string` | `null` | Customer identification number |
| `$idType` | `?string` | `null` | ID type: `NIN`, `PN`, or `TIN` |
| `$postalCode` | `?string` | `null` | Postal code |
| `$cityCode` | `?string` | `null` | Jordan city code (`JO-XX`) |
| `$name` | `?string` | `null` | Customer name |
| `$phone` | `?string` | `null` | Phone number |
| `$tin` | `?string` | `null` | Customer TIN |

#### 7.3.3 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `setId(string $id, string $type)` | ID value, type (`NIN`/`PN`/`TIN`) | `self` | Sets customer ID and type; validates type if enabled |
| `setPostalCode(string $code)` | Postal code | `self` | Sets postal code |
| `setCityCode(string $code)` | City code (`JO-XX`) | `self` | Sets city code; **always** validates against `VALID_CITY_CODES` (even with validations disabled) |
| `getName()` | - | `?string` | Returns the customer name |
| `setName(string $name)` | Name string | `self` | Sets customer name |
| `setPhone(string $phone)` | Phone string | `self` | Sets phone number |
| `setTin(string $tin)` | TIN string | `self` | Sets customer TIN |
| `setupAnonymousCustomer()` | - | `self` | Sets `idType = 'NIN'` and `id = ''` for anonymous |
| `toXml()` | - | `string` | Generates XML fragment with conditional sub-elements |
| `toArray()` | - | `array` | Returns all properties as associative array |
| `validateSection()` | - | `void` | Validates that ID and ID type are set |

#### 7.3.4 Anonymous Customer

If no customer information is explicitly set, the SDK defaults to an anonymous customer:
- ID Type: `NIN`
- ID Value: empty string `""`

This is set automatically by `JoFotaraService.customerInformation()` on first access, and also by `validateSections()` if customer info was never accessed.

#### 7.3.5 Validation Rules

| Field | Rule |
|---|---|
| Customer ID | Must not be null (can be empty for anonymous) |
| ID Type | Must not be null |
| City Code | Must be in `VALID_CITY_CODES` (validated at setter, not in `validateSection()`) |
| ID Type value | Must be `NIN`, `PN`, or `TIN` (validated at setter) |

**Cross-section validation** (performed in `JoFotaraService.validateSections()`):
- Customer **name** is required if payment is receivable OR payable > 10,000 JOD.

#### 7.3.6 XML Output

The XML structure is dynamic based on which optional fields are set:

```xml
<cac:AccountingCustomerParty>
    <cac:Party>
        <cac:PartyIdentification>                          <!-- always present -->
            <cbc:ID schemeID="{NIN|PN|TIN}">{id}</cbc:ID>
        </cac:PartyIdentification>
        <cac:PostalAddress>                                <!-- only if postalCode or cityCode set -->
            <cbc:PostalZone>{postalCode}</cbc:PostalZone>               <!-- only if postalCode set -->
            <cbc:CountrySubentityCode>{cityCode}</cbc:CountrySubentityCode> <!-- only if cityCode set -->
            <cac:Country>
                <cbc:IdentificationCode>JO</cbc:IdentificationCode>
            </cac:Country>
        </cac:PostalAddress>
        <cac:PartyTaxScheme>                               <!-- only if tin set -->
            <cbc:CompanyID>{tin}</cbc:CompanyID>
            <cac:TaxScheme>
                <cbc:ID>VAT</cbc:ID>
            </cac:TaxScheme>
        </cac:PartyTaxScheme>
        <cac:PartyLegalEntity>                             <!-- only if name set -->
            <cbc:RegistrationName>{name}</cbc:RegistrationName>
        </cac:PartyLegalEntity>
    </cac:Party>
    <cac:AccountingContact>                                <!-- only if phone set -->
        <cbc:Telephone>{phone}</cbc:Telephone>
    </cac:AccountingContact>
</cac:AccountingCustomerParty>
```

**Important sub-element ordering inside `<cac:Party>`:**
1. `PartyIdentification` (always)
2. `PostalAddress` (if postal code or city code set)
3. `PartyTaxScheme` (if customer TIN set)
4. `PartyLegalEntity` (if name set)

Then outside `<cac:Party>` but still inside `<cac:AccountingCustomerParty>`:
5. `AccountingContact` (if phone set)

---

### 7.4 SupplierIncomeSource

**File:** `src/Sections/SupplierIncomeSource.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 92

Represents the supplier income source sequence (تسلسل مصدر الدخل). This is a required value obtained from the JoFotara portal that identifies the business's income source.

#### 7.4.1 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$sequenceId` | `string` | (constructor parameter) | Income source sequence ID |

#### 7.4.2 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `__construct(string $sequenceId)` | Sequence ID | - | Sets the sequence ID via constructor |
| `setSequenceId(string $id)` | Sequence ID | `self` | Alternative setter for sequence ID |
| `toXml()` | - | `string` | Generates XML fragment |
| `toArray()` | - | `array` | Returns `['sequenceId' => ...]` |
| `validateSection()` | - | `void` | Validates format |

#### 7.4.3 Validation Rules

| Field | Rule |
|---|---|
| Sequence ID | Must be set, non-empty (after trim), must match `/^\d+$/` (numeric digits only) |

#### 7.4.4 XML Output

```xml
<cac:SellerSupplierParty>
    <cac:Party>
        <cac:PartyIdentification>
            <cbc:ID>{sequenceId}</cbc:ID>
        </cac:PartyIdentification>
    </cac:Party>
</cac:SellerSupplierParty>
```

---

### 7.5 InvoiceItems

**File:** `src/Sections/InvoiceItems.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 119

A container/collection class that manages `InvoiceLineItem` instances. This class acts as a factory for line items and aggregates their XML output.

#### 7.5.1 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$items` | `array` | `[]` | Associative array: `$id => InvoiceLineItem` |

#### 7.5.2 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `setValidationsEnabled(bool)` | Enabled flag | `self` | Overrides trait method: also propagates to all existing items |
| `addItem(string $id)` | Item serial ID | `InvoiceLineItem` | Creates and returns a new line item; checks for duplicate IDs if validated |
| `getItems()` | - | `array` | Returns the items array (keyed by ID) |
| `toXml()` | - | `string` | Joins all items' XML with newlines |
| `validateSection()` | - | `void` | Validates at least 1 item exists, then validates each item |
| `toArray()` | - | `array` | Returns all items as arrays |

**Note:** The `setValidationsEnabled()` method is overridden (not just using the trait) to propagate the flag to all child `InvoiceLineItem` instances.

#### 7.5.3 Validation Rules

| Rule | Description |
|---|---|
| At least 1 item | The items array must not be empty |
| No duplicate IDs | `addItem()` rejects duplicate IDs if validations enabled |
| Each item valid | Calls `validateSection()` on every item |

---

### 7.6 InvoiceLineItem

**File:** `src/Sections/InvoiceLineItem.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 374

Represents a single line item on the invoice. Contains quantity, unit price, discount, description, tax category/rate, and computed amounts.

#### 7.6.1 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$id` | `string` | (constructor) | Item serial identifier |
| `$quantity` | `float` | (uninitialized) | Item quantity |
| `$unitPrice` | `float` | (uninitialized) | Price per unit |
| `$discount` | `float` | `0.0` | Discount amount (absolute, not percentage) |
| `$description` | `string` | (uninitialized) | Item description/name |
| `$taxCategory` | `string` | `'S'` | Tax category: `S`, `Z`, or `O` |
| `$taxPercent` | `float` | `16.0` | Tax percentage |
| `$unitCode` | `string` | `'PCE'` | Unit of measure code (Piece) |

#### 7.6.2 Default Values

| Property | Default | Meaning |
|---|---|---|
| `$discount` | `0.0` | No discount |
| `$taxCategory` | `'S'` | Standard rate |
| `$taxPercent` | `16.0` | 16% VAT (Jordan standard rate) |
| `$unitCode` | `'PCE'` | Piece (unit of measure) |

#### 7.6.3 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `__construct(string $id)` | Item ID | - | Sets the item serial ID |
| `setQuantity(float $quantity)` | Quantity > 0 | `self` | Sets quantity; validates > 0 |
| `setUnitPrice(float $price)` | Price >= 0 | `self` | Sets unit price; validates >= 0 |
| `setDiscount(float $amount)` | Amount >= 0 | `self` | Sets discount; validates >= 0 and <= qty * price |
| `setDescription(string)` | Description text | `self` | Sets item description; validates non-empty |
| `getDiscount()` | - | `float` | Returns the discount amount |

#### 7.6.4 Tax Category Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `taxExempted()` | - | `self` | Sets category to `Z` (Exempt), tax = 0% |
| `zeroTax()` | - | `self` | Sets category to `O` (Zero-rated), tax = 0% |
| `tax(float $rate)` | Rate (1-16) | `self` | Sets category to `S` (Standard) with given rate |
| `setTaxCategory(string, ?float)` | Category + optional percent | `self` | Low-level setter; validates category and percent |

**Tax category logic in `setTaxCategory()`:**
- If category is `S`: percent is required, must be > 0.
- If category is `Z` or `O`: percent is forced to 0, any passed percent is ignored.

#### 7.6.5 Calculation Methods

| Method | Return | Formula |
|---|---|---|
| `getAmountBeforeDiscount()` | `float` | `quantity * unitPrice` |
| `getAmountAfterDiscount()` | `float` | `(quantity * unitPrice) - discount` |
| `getTaxAmount()` | `float` | If `S`: `amountAfterDiscount * (taxPercent / 100)`. If `Z` or `O`: `0` |
| `getTaxInclusiveAmount()` | `float` | `amountAfterDiscount + taxAmount` |

All calculation methods throw `InvalidArgumentException` if `quantity` or `unitPrice` are not set.

#### 7.6.6 Validation Rules

| Field | Rule |
|---|---|
| Quantity | Must be set, must be > 0 |
| Unit Price | Must be set, must be >= 0 |
| Description | Must be set, must not be empty |
| Discount | Must be >= 0 and <= (quantity * unitPrice) |
| Tax Category | Must be `S`, `Z`, or `O` |
| Tax Percent | If category `S`: must be > 0 and <= 16 |

#### 7.6.7 XML Output

All monetary values are formatted to 9 decimal places using `%.9f`.

```xml
<cac:InvoiceLine>
    <cbc:ID>{id}</cbc:ID>
    <cbc:InvoicedQuantity unitCode="PCE">{quantity_9dp}</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="JO">{amountAfterDiscount_9dp}</cbc:LineExtensionAmount>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="JO">{taxAmount_9dp}</cbc:TaxAmount>
        <cbc:RoundingAmount currencyID="JO">{taxInclusiveAmount_9dp}</cbc:RoundingAmount>
        <cac:TaxSubtotal>
            <cbc:TaxAmount currencyID="JO">{taxAmount_9dp}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5305">{S|Z|O}</cbc:ID>
                <cbc:Percent>{taxPercent_9dp}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5153">VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:Item>
        <cbc:Name>{description}</cbc:Name>
    </cac:Item>
    <cac:Price>
        <cbc:PriceAmount currencyID="JO">{unitPrice_9dp}</cbc:PriceAmount>
        <cac:AllowanceCharge>
            <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
            <cbc:AllowanceChargeReason>DISCOUNT</cbc:AllowanceChargeReason>
            <cbc:Amount currencyID="JO">{discount_9dp}</cbc:Amount>
        </cac:AllowanceCharge>
    </cac:Price>
</cac:InvoiceLine>
```

**Important notes on the XML:**
- `LineExtensionAmount` = amount **after** discount (not before).
- `RoundingAmount` = tax-inclusive amount (confusing UBL naming).
- The `AllowanceCharge` block inside `Price` is **always included**, even when discount is 0.
- `AllowanceChargeReason` uses uppercase `"DISCOUNT"` at the line-item level.

---

### 7.7 InvoiceTotals

**File:** `src/Sections/InvoiceTotals.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 250

Manages the invoice-level monetary totals: tax-exclusive amount, tax-inclusive amount, discount total, tax total, and payable amount.

#### 7.7.1 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$taxExclusiveAmount` | `float` | `0.0` | Sum of (qty * unitPrice) per item (before discounts) |
| `$taxInclusiveAmount` | `float` | `0.0` | taxExclusive - discountTotal + taxTotal |
| `$discountTotalAmount` | `float` | `0.0` | Sum of all item discounts |
| `$taxTotalAmount` | `float` | `0.0` | Sum of all item tax amounts |
| `$payableAmount` | `float` | `0.0` | Final payable = taxInclusiveAmount |

#### 7.7.2 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `getPayableAmount()` | - | `float` | Returns the payable amount |
| `setTaxExclusiveAmount(float)` | Amount >= 0 | `self` | Sets tax exclusive amount; rounded to 9 dp |
| `setTaxInclusiveAmount(float)` | Amount >= 0 | `self` | Sets tax inclusive amount; validates >= (exclusive - discount); rounded to 9 dp |
| `setDiscountTotalAmount(?float)` | Amount >= 0 or null | `self` | Sets discount total; null defaults to 0.0; validates <= exclusive; rounded to 9 dp |
| `setTaxTotalAmount(float)` | Amount >= 0 | `self` | Sets tax total; validates consistency; rounded to 9 dp |
| `setPayableAmount(float)` | Amount >= 0 | `self` | Sets payable amount; validates >= (inclusive - discount); rounded to 9 dp |
| `toXml()` | - | `string` | Generates XML including AllowanceCharge, TaxTotal, LegalMonetaryTotal |
| `toArray()` | - | `array` | Returns all 5 amounts as associative array |
| `validateSection()` | - | `void` | Validates non-zero required amounts and relationships |

#### 7.7.3 Automatic Calculation

When `JoFotaraService.invoiceTotals()` is called **after items have been added**, the totals are automatically calculated:

```
taxExclusiveAmount  = SUM(item.getAmountBeforeDiscount())    // qty * unitPrice per item
discountTotalAmount = SUM(item.getDiscount())                // sum of discounts
taxTotalAmount      = SUM(item.getTaxAmount())               // sum of tax amounts
taxInclusiveAmount  = taxExclusiveAmount - discountTotalAmount + taxTotalAmount
payableAmount       = taxInclusiveAmount
```

Manual totals can be set instead, but they must match the calculated values if cross-section validation is enabled.

#### 7.7.4 Validation Rules

| Field | Rule |
|---|---|
| Tax Exclusive Amount | Must be > 0 (uses `==` check, not strict) |
| Tax Inclusive Amount | Must be > 0, must be >= (exclusive - discount) |
| Discount Total | Must be >= 0, must be <= exclusive |
| Tax Total | Must be >= 0 |
| Payable Amount | Must be > 0, must be >= (inclusive - discount) |

**Relationship validation:**
- `taxInclusiveAmount >= taxExclusiveAmount - discountTotalAmount`
- `payableAmount >= taxInclusiveAmount - discountTotalAmount`

#### 7.7.5 XML Output

The totals section generates up to 3 XML blocks:

**Block 1: AllowanceCharge (only if discount > 0)**
```xml
<cac:AllowanceCharge>
    <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="JO">{discountTotalAmount_9dp}</cbc:Amount>
</cac:AllowanceCharge>
```

**Note:** The invoice-level `AllowanceChargeReason` uses lowercase `"discount"` (unlike line-item level which uses uppercase `"DISCOUNT"`).

**Block 2: TaxTotal (always present)**
```xml
<cac:TaxTotal>
    <cbc:TaxAmount currencyID="JO">{taxTotalAmount_9dp}</cbc:TaxAmount>
</cac:TaxTotal>
```

**Block 3: LegalMonetaryTotal (always present)**
```xml
<cac:LegalMonetaryTotal>
    <cbc:TaxExclusiveAmount currencyID="JO">{taxExclusiveAmount_9dp}</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="JO">{taxInclusiveAmount_9dp}</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="JO">{discountTotal_9dp}</cbc:AllowanceTotalAmount>  <!-- only if discount > 0 -->
    <cbc:PayableAmount currencyID="JO">{payableAmount_9dp}</cbc:PayableAmount>
</cac:LegalMonetaryTotal>
```

---

### 7.8 ReasonForReturn

**File:** `src/Sections/ReasonForReturn.php`
**Namespace:** `JBadarneh\JoFotara\Sections`
**Lines:** 69

Represents the reason for returning an invoice. Only used with credit invoices (type code `381`). Generates the `<cac:PaymentMeans>` XML section.

#### 7.8.1 Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `$reason` | `?string` | `null` | The return reason text |

#### 7.8.2 Methods

| Method | Parameters | Return | Description |
|---|---|---|---|
| `setReason(string $reason)` | Reason text | `self` | Sets the return reason |
| `toXml()` | - | `string` | Generates XML; calls `validateSection()` first |
| `toArray()` | - | `array` | Returns `['reason' => ...]` |
| `validateSection()` | - | `void` | Validates reason is not null |

#### 7.8.3 Validation Rules

| Field | Rule |
|---|---|
| Reason | Must not be null |

#### 7.8.4 XML Output

The XML is generated as a single line (no line breaks within):

```xml
<cac:PaymentMeans><cbc:PaymentMeansCode listID="UN/ECE 4461">10</cbc:PaymentMeansCode><cbc:InstructionNote>{reason}</cbc:InstructionNote></cac:PaymentMeans>
```

**Key details:**
- `PaymentMeansCode` is always `10`.
- `listID` is always `"UN/ECE 4461"`.
- The reason text is placed in `<cbc:InstructionNote>`.
- The reason text is XML-escaped.

---

## 8. Response Handling: JoFotaraResponse

**File:** `src/Response/JoFotaraResponse.php`
**Namespace:** `JBadarneh\JoFotara\Response`
**Lines:** 286

Wraps and normalizes the JoFotara API response, handling two different response formats that the API has returned over time.

### 8.1 Dual Response Format Support

The JoFotara API has returned two different JSON response formats:

**Format A (newer):**
```json
{
  "validationResults": { "status": "PASS", "errorMessages": [], "warningMessages": [], "infoMessages": [] },
  "invoiceStatus": "SUBMITTED",
  "submittedInvoice": "<base64>",
  "qrCode": "<data>",
  "invoiceNumber": "INV-001",
  "invoiceUUID": "123e4567-..."
}
```

**Format B (older):**
```json
{
  "EINV_RESULTS": { "status": "...", "ERRORS": [], "WARNINGS": [], "INFO": [] },
  "EINV_STATUS": "SUBMITTED",
  "EINV_SINGED_INVOICE": "<base64>",
  "EINV_QR": "<data>",
  "EINV_NUM": "...",
  "EINV_INV_UUID": "..."
}
```

**Important:** The key `EINV_SINGED_INVOICE` in Format B is **not a typo** in the SDK -- it is the actual key returned by the JoFotara API (missing the second "N" in "SIGNED").

### 8.2 Success Determination Logic

The constructor determines success based on:

1. **HTTP status code must be 200.** If not 200, `success = false` immediately.

2. **If HTTP 200, check the response structure:**
   - **Format A** (has `validationResults`):
     - `validationResults.status` must be exactly `"PASS"`
     - AND `invoiceStatus` must be `"SUBMITTED"` or `"ALREADY_SUBMITTED"`
   - **Format B** (has `EINV_RESULTS`):
     - `EINV_RESULTS.status` must NOT be `"ERROR"` (allows other values like `"WARNING"`)
     - AND `EINV_STATUS` must be `"SUBMITTED"` or `"ALREADY_SUBMITTED"`
   - **Neither format recognized:** `success = false`

**Note the asymmetry:** Format A requires an exact `"PASS"` match, while Format B only rejects `"ERROR"`.

### 8.3 Properties

| Property | Type | Description |
|---|---|---|
| `$rawResponse` | `array` | The raw parsed API response |
| `$success` | `bool` | Whether the submission was successful |
| `$statusCode` | `int` | HTTP status code |

### 8.4 Methods

| Method | Return | Description |
|---|---|---|
| `isSuccess()` | `bool` | Whether submission was successful |
| `getRawResponse()` | `array` | Returns the raw response array |
| `getInvoiceStatus()` | `?string` | Returns `invoiceStatus` or `EINV_STATUS` |
| `getSubmittedInvoice()` | `?string` | Returns base64-encoded signed invoice (`submittedInvoice` or `EINV_SINGED_INVOICE`) |
| `getInvoiceAsXml()` | `?string` | Decodes the signed invoice from base64 to XML; returns null if decoding fails |
| `getQrCode()` | `?string` | Returns QR code data (`qrCode` or `EINV_QR`) |
| `getInvoiceNumber()` | `?string` | Returns system-assigned invoice number (`invoiceNumber` or `EINV_NUM`) |
| `getInvoiceUuid()` | `?string` | Returns system-assigned UUID (`invoiceUUID` or `EINV_INV_UUID`) |
| `getStatusCode()` | `int` | Returns the HTTP status code |
| `getErrors()` | `array` | Returns error messages array (handles all formats + 403 + 400) |
| `getWarnings()` | `array` | Returns warning messages array |
| `getInfoMessages()` | `array` | Returns info messages array |
| `getValidationStatus()` | `?string` | Returns validation status string (`PASS`, `ERROR`, etc.) |
| `hasErrors()` | `bool` | Whether there are any error messages |
| `hasWarnings()` | `bool` | Whether there are any warning messages |
| `getErrorSummary()` | `?string` | Formatted multi-line error summary string; handles both Format A and B field names |

### 8.5 Error Handling

The `getErrors()` method handles multiple error scenarios:

1. **HTTP 403:** Returns `[['code' => 'AUTH_ERROR', 'message' => 'Authentication failed...', 'category' => 'Authentication']]`.

2. **Format A errors:** Returns `$rawResponse['validationResults']['errorMessages']`.

3. **Format B errors:** Returns `$rawResponse['EINV_RESULTS']['ERRORS']`.

4. **HTTP 400 or `error` key present:**
   - If `errors` key exists: returns it as array.
   - If `error` key exists: wraps it in `[['code' => ..., 'message' => ..., 'category' => 'API Validation']]`.
   - If neither format recognized: returns `[['code' => 'API_ERROR', 'message' => json_encode($rawResponse), 'category' => 'API Validation']]`.

5. **No errors:** Returns empty array `[]`.

The `getErrorSummary()` method formats errors as:
```
[CODE] Category: Message
[CODE] Category: Message
...
```
It handles both Format A keys (`code`, `message`, `category`) and Format B keys (`EINV_CODE`, `EINV_MESSAGE`, `EINV_CATEGORY`).

---

## 9. API Protocol

### 9.1 Endpoint

```
POST https://backend.jofotara.gov.jo/core/invoices/
```

There is only one endpoint and one HTTP method. No GET for status checks, no PUT for updates.

### 9.2 Authentication

Authentication is done via HTTP headers (no OAuth, no token exchange):

| Header | Value |
|---|---|
| `Client-Id` | Your client ID from the JoFotara portal |
| `Secret-Key` | Your client secret from the JoFotara portal |
| `Content-Type` | `application/json` |

### 9.3 Request Format

```json
{
  "invoice": "<base64_encoded_xml_string>"
}
```

The XML is encoded using standard base64 (not URL-safe variant).

### 9.4 Response Formats

The API returns JSON in one of two formats (Format A or Format B, as described in section 8.1). The SDK handles both transparently.

**Response fields mapping:**

| Purpose | Format A Key | Format B Key |
|---|---|---|
| Invoice status | `invoiceStatus` | `EINV_STATUS` |
| Signed invoice (base64) | `submittedInvoice` | `EINV_SINGED_INVOICE` |
| QR code | `qrCode` | `EINV_QR` |
| Invoice number | `invoiceNumber` | `EINV_NUM` |
| Invoice UUID | `invoiceUUID` | `EINV_INV_UUID` |
| Validation status | `validationResults.status` | `EINV_RESULTS.status` |
| Error messages | `validationResults.errorMessages` | `EINV_RESULTS.ERRORS` |
| Warning messages | `validationResults.warningMessages` | `EINV_RESULTS.WARNINGS` |
| Info messages | `validationResults.infoMessages` | `EINV_RESULTS.INFO` |

**Error/Warning/Info object structure:**

| Field | Format A | Format B |
|---|---|---|
| Code | `type`, `code` | `EINV_CODE` |
| Message | `message` | `EINV_MESSAGE` |
| Category | `category` | `EINV_CATEGORY` |
| Status | `status` | (not present) |

### 9.5 HTTP Status Codes

| Code | Meaning | SDK Behavior |
|---|---|---|
| `200` | Request processed | Check `validationResults.status` - could still contain errors |
| `400` | Validation error | Check `error` or `errors` field in response |
| `403` | Authentication failed | Bad Client-Id or Secret-Key |
| Other | Network/server error | Treated as transient failure |

---

## 10. XML Specification

### 10.1 UBL 2.1 Compliance

The SDK generates XML compliant with the UBL (Universal Business Language) 2.1 standard, specifically tailored to Jordan Tax Authority (ZATCA-aligned) specifications.

### 10.2 XML Namespaces

Four namespaces are declared on the root `<Invoice>` element:

| Prefix | Namespace URI |
|---|---|
| (default) | `urn:oasis:names:specification:ubl:schema:xsd:Invoice-2` |
| `cac` | `urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2` |
| `cbc` | `urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2` |
| `ext` | `urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2` |

**Important:** The root `<Invoice>` element with all namespace declarations must be on a **single line** in the output XML.

### 10.3 Section Ordering

The XML sections must follow this exact order:

| Order | Element | Condition |
|---|---|---|
| 1 | `cbc:UBLVersionID` | Always |
| 2 | `cbc:ID` (invoice ID) | Always |
| 3 | `cbc:UUID` | Always |
| 4 | `cbc:IssueDate` | Always |
| 5 | `cbc:InvoiceTypeCode` | Always |
| 6 | `cbc:Note` | Optional |
| 7 | `cbc:DocumentCurrencyCode` | Always |
| 8 | `cbc:TaxCurrencyCode` | Always |
| 9 | `cac:BillingReference` | Credit invoices only |
| 10 | `cac:AdditionalDocumentReference` (ICV) | Always |
| 11 | `cac:AccountingSupplierParty` (seller) | Always |
| 12 | `cac:AccountingCustomerParty` (customer) | Always |
| 13 | `cac:SellerSupplierParty` (income source) | Always |
| 14 | `cac:PaymentMeans` (reason for return) | Credit invoices only |
| 15 | `cac:AllowanceCharge` (invoice discount) | Only if discount > 0 |
| 16 | `cac:TaxTotal` | Always |
| 17 | `cac:LegalMonetaryTotal` | Always |
| 18 | `cac:InvoiceLine` (repeat per item) | Always (at least 1) |

### 10.4 Complete XML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
<cbc:UBLVersionID>2.1</cbc:UBLVersionID>
<cbc:ID>{invoice_id}</cbc:ID>
<cbc:UUID>{uuid}</cbc:UUID>
<cbc:IssueDate>{YYYY-MM-DD}</cbc:IssueDate>
<cbc:InvoiceTypeCode name="{payment_method_code}">{388_or_381}</cbc:InvoiceTypeCode>
<cbc:Note>{optional_note}</cbc:Note>
<cbc:DocumentCurrencyCode>JOD</cbc:DocumentCurrencyCode>
<cbc:TaxCurrencyCode>JOD</cbc:TaxCurrencyCode>
<!-- BillingReference: credit invoices only -->
<cac:BillingReference>
    <cac:InvoiceDocumentReference>
        <cbc:ID>{original_invoice_id}</cbc:ID>
        <cbc:UUID>{original_invoice_uuid}</cbc:UUID>
        <cbc:DocumentDescription>{original_amount_2dp}</cbc:DocumentDescription>
    </cac:InvoiceDocumentReference>
</cac:BillingReference>
<cac:AdditionalDocumentReference>
    <cbc:ID>ICV</cbc:ID>
    <cbc:UUID>{invoice_counter}</cbc:UUID>
</cac:AdditionalDocumentReference>
<!-- Seller -->
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
<!-- Customer -->
<cac:AccountingCustomerParty>
    <cac:Party>
        <cac:PartyIdentification>
            <cbc:ID schemeID="{NIN|PN|TIN}">{customer_id}</cbc:ID>
        </cac:PartyIdentification>
        <!-- Optional sub-elements based on data -->
    </cac:Party>
</cac:AccountingCustomerParty>
<!-- Supplier Income Source -->
<cac:SellerSupplierParty>
    <cac:Party>
        <cac:PartyIdentification>
            <cbc:ID>{income_source_sequence}</cbc:ID>
        </cac:PartyIdentification>
    </cac:Party>
</cac:SellerSupplierParty>
<!-- PaymentMeans: credit invoices only -->
<cac:PaymentMeans>
    <cbc:PaymentMeansCode listID="UN/ECE 4461">10</cbc:PaymentMeansCode>
    <cbc:InstructionNote>{reason_for_return}</cbc:InstructionNote>
</cac:PaymentMeans>
<!-- AllowanceCharge: only if discount > 0 -->
<cac:AllowanceCharge>
    <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
    <cbc:AllowanceChargeReason>discount</cbc:AllowanceChargeReason>
    <cbc:Amount currencyID="JO">{total_discount_9dp}</cbc:Amount>
</cac:AllowanceCharge>
<!-- Tax Total -->
<cac:TaxTotal>
    <cbc:TaxAmount currencyID="JO">{total_tax_9dp}</cbc:TaxAmount>
</cac:TaxTotal>
<!-- Monetary Totals -->
<cac:LegalMonetaryTotal>
    <cbc:TaxExclusiveAmount currencyID="JO">{amount_9dp}</cbc:TaxExclusiveAmount>
    <cbc:TaxInclusiveAmount currencyID="JO">{amount_9dp}</cbc:TaxInclusiveAmount>
    <cbc:AllowanceTotalAmount currencyID="JO">{discount_9dp}</cbc:AllowanceTotalAmount>
    <cbc:PayableAmount currencyID="JO">{amount_9dp}</cbc:PayableAmount>
</cac:LegalMonetaryTotal>
<!-- Line Items (repeat) -->
<cac:InvoiceLine>
    <!-- ... line item XML ... -->
</cac:InvoiceLine>
</Invoice>
```

### 10.5 Number Formatting

- All monetary amounts: `%.9f` (9 decimal places)
- All quantities: `%.9f` (9 decimal places)
- All tax percentages: `%.9f` (9 decimal places)
- Original invoice amount in credit invoices: `number_format($amount, 2)` (2 decimal places)
- All totals are `round($amount, 9)` before being set

### 10.6 XML Escaping

All text values are escaped using `htmlspecialchars()` with:
- `ENT_XML1 | ENT_QUOTES` flags
- `UTF-8` encoding

Escaped characters: `&`, `<`, `>`, `"`, `'`

Line endings are normalized: `\r\n` -> `\n`

### 10.7 Currency Quirks

There is a deliberate mismatch in currency codes:

| Context | Code Used |
|---|---|
| `DocumentCurrencyCode` element value | `JOD` |
| `TaxCurrencyCode` element value | `JOD` |
| `currencyID` attribute on amount elements | `JO` |

This is by design per the JoFotara specification -- `JOD` for the document/tax currency declarations but `JO` for the `currencyID` attribute on all monetary amount elements.

---

## 11. Invoice Types

### 11.1 Income Invoice

- **Type key:** `income`
- **Arabic:** فاتورة دخل
- **Use case:** For taxpayers **NOT** registered for sales tax
- **Invoice type code in XML:** `388` (regular) or `381` (credit)
- **Cash payment code:** `011`
- **Receivable payment code:** `021`

### 11.2 General Sales Invoice

- **Type key:** `general_sales`
- **Arabic:** فاتورة مبيعات عامة
- **Use case:** For taxpayers registered for sales tax (VAT)
- **Invoice type code in XML:** `388` (regular) or `381` (credit)
- **Cash payment code:** `012`
- **Receivable payment code:** `022`

### 11.3 Special Sales Invoice

- **Type key:** `special_sales`
- **Arabic:** فاتورة مبيعات خاصة
- **Use case:** For taxpayers subject to special sales tax
- **Invoice type code in XML:** `388` (regular) or `381` (credit)
- **Cash payment code:** `013`
- **Receivable payment code:** `023`

### 11.4 Credit Invoice (Return)

A credit invoice reverses a previously submitted invoice. It can be applied to any of the three invoice types above. Requirements:

1. `InvoiceTypeCode` value = `381` (instead of `388`)
2. A `BillingReference` section containing:
   - Original invoice ID
   - Original invoice UUID
   - Original full amount (2 decimal places)
3. A `PaymentMeans` section containing:
   - `PaymentMeansCode` = `10` with `listID="UN/ECE 4461"`
   - `InstructionNote` = the reason for return
4. A reason for return (mandatory, set via `setReasonForReturn()`)

---

## 12. Payment Methods

### 12.1 Cash

Payment at the time of transaction. Code format: `01X` where X is the invoice type digit.

### 12.2 Receivable

Deferred payment (آجل). Code format: `02X` where X is the invoice type digit.

**When payment is receivable, customer name becomes mandatory.**

### 12.3 Payment Method Code Matrix

| | Cash | Receivable |
|---|---|---|
| **Income** | `011` | `021` |
| **General Sales** | `012` | `022` |
| **Special Sales** | `013` | `023` |

The payment method code is placed in the `name` attribute of `<cbc:InvoiceTypeCode>`:
```xml
<cbc:InvoiceTypeCode name="012">388</cbc:InvoiceTypeCode>
```

---

## 13. Tax System

### 13.1 Tax Categories

| Code | Name | Tax Rate | Use Case |
|---|---|---|---|
| `S` | Standard Rate | 1% to 16% | Normal taxable items (Jordan standard VAT = 16%) |
| `Z` | Exempt | 0% | Tax-exempt items |
| `O` | Zero-rated | 0% | Zero-rated items (e.g., exports) |

**SDK convenience methods:**
- `->tax(16)` sets category `S` with 16% rate
- `->taxExempted()` sets category `Z` with 0% rate
- `->zeroTax()` sets category `O` with 0% rate

### 13.2 Tax Calculation Formulas

**For Standard Rate (`S`):**
```
tax_amount = amount_after_discount * (tax_percent / 100)
```

**For Exempt (`Z`) and Zero-rated (`O`):**
```
tax_amount = 0
```

---

## 14. Calculations

### 14.1 Per Line Item Calculations

```
amount_before_discount = quantity * unit_price
amount_after_discount  = amount_before_discount - discount
tax_amount             = amount_after_discount * (tax_percent / 100)   [if category = 'S']
tax_amount             = 0                                             [if category = 'Z' or 'O']
tax_inclusive_amount   = amount_after_discount + tax_amount
```

### 14.2 Invoice-Level Totals

```
tax_exclusive_amount  = SUM(item.quantity * item.unit_price)           -- per item, before discount
discount_total        = SUM(item.discount)                             -- sum of all item discounts
tax_total             = SUM(item.tax_amount)                           -- sum of all item taxes
tax_inclusive_amount  = tax_exclusive_amount - discount_total + tax_total
payable_amount        = tax_inclusive_amount
```

**Important clarifications:**
- `TaxExclusiveAmount` in the XML means the sum of (qty * unit_price) per item -- it is **before discounts AND before tax**.
- Discounts are at the item level only, never at the invoice level.
- The invoice-level `AllowanceCharge` is the sum of item-level discounts.

### 14.3 Rounding

- All totals are rounded to 9 decimal places using PHP's `round($amount, 9)`.
- All XML monetary output uses `sprintf('%.9f', $amount)`.
- The original amount in credit invoice `DocumentDescription` uses `number_format($amount, 2)` (2 decimal places).

---

## 15. Validation System

### 15.1 Validation Architecture

The validation system operates at three levels:

1. **Setter-level validation**: Immediate validation in setter methods (e.g., `setQuantity()` rejects values <= 0).
2. **Section-level validation**: Comprehensive validation via `validateSection()` on each section class.
3. **Cross-section validation**: Consistency checks between sections in `JoFotaraService.validateSections()`.

All three levels respect the `validationsEnabled` flag, except:
- Required section presence checks (always enforced).
- City code validation in `CustomerInformation.setCityCode()` (always enforced).
- Invoice counter minimum check (`setInvoiceCounter()` always rejects < 1).

### 15.2 Field-Level Validations

| Section | Field | Rule |
|---|---|---|
| BasicInvoiceInformation | Invoice ID | Non-empty string |
| BasicInvoiceInformation | UUID | UUID v4 format regex |
| BasicInvoiceInformation | Issue Date | Valid `dd-mm-yyyy` format |
| BasicInvoiceInformation | Invoice Type | Must be `income`, `general_sales`, or `special_sales` |
| BasicInvoiceInformation | Payment Method | Must be set after invoice type; must match the type |
| BasicInvoiceInformation | Invoice Counter | Integer >= 1 |
| BasicInvoiceInformation | Original Invoice ID | Non-empty (credit only) |
| BasicInvoiceInformation | Original Invoice UUID | Non-empty (credit only) |
| BasicInvoiceInformation | Original Amount | > 0 (credit only) |
| SellerInformation | TIN | 6+ numeric digits (`/^\d{6,}$/`) |
| SellerInformation | Name | Non-empty |
| CustomerInformation | ID + Type | Both must be set |
| CustomerInformation | City Code | Must be valid Jordan code |
| CustomerInformation | ID Type | Must be `NIN`, `PN`, or `TIN` |
| SupplierIncomeSource | Sequence ID | Non-empty, numeric digits only |
| InvoiceItems | Items | At least 1 item |
| InvoiceLineItem | Quantity | > 0 |
| InvoiceLineItem | Unit Price | >= 0 |
| InvoiceLineItem | Discount | >= 0 and <= (quantity * unitPrice) |
| InvoiceLineItem | Description | Non-empty |
| InvoiceLineItem | Tax Category | `S`, `Z`, or `O` |
| InvoiceLineItem | Tax Percent | > 0 and <= 16 (for category `S` only) |
| InvoiceTotals | Tax Exclusive Amount | > 0 |
| InvoiceTotals | Tax Inclusive Amount | > 0, >= (exclusive - discount) |
| InvoiceTotals | Discount Total | >= 0, <= exclusive |
| InvoiceTotals | Tax Total | >= 0 |
| InvoiceTotals | Payable Amount | > 0, >= (inclusive - discount) |
| ReasonForReturn | Reason | Not null |

### 15.3 Cross-Section Validations

Performed in `JoFotaraService.validateSections()`:

1. **Credit invoice requires reason for return**: If `isCreditInvoice()` is true, `$reasonForReturn` must be set.
2. **Customer name requirement**: Customer name is mandatory when:
   - Payment method is receivable (`021`, `022`, `023`), OR
   - Payable amount > 10,000 JOD.
3. **Totals match items**: Recalculates totals from line items and compares with provided totals using strict array equality (`$providedTotals !== $expectedTotals`).

### 15.4 Validation Bypass Mode

```php
$invoice = new JoFotaraService($clientId, $clientSecret, enableValidations: false);
```

When `enableValidations = false`:

| What is still checked | What is skipped |
|---|---|
| Required sections exist (basic info, seller, items, totals, supplier) | Detailed field format validation |
| Credit invoices need a reason | Cross-section totals consistency |
| | Customer name requirement |
| | UUID format check |
| | TIN format check |
| | Amount range checks |
| | Discount limit checks |

---

## 16. Customer Information Details

### 16.1 Customer ID Types

| Code | Name | Description |
|---|---|---|
| `NIN` | National ID Number | Jordanian national identification number |
| `PN` | Passport Number | Passport number |
| `TIN` | Tax ID Number | Tax identification number |

### 16.2 Jordan City Codes

| Code | City | Arabic |
|---|---|---|
| `JO-AM` | Amman | عمان |
| `JO-IR` | Irbid | إربد |
| `JO-AZ` | Zarqa | الزرقاء |
| `JO-BA` | Balqa | البلقاء |
| `JO-MA` | Mafraq | المفرق |
| `JO-KA` | Karak | الكرك |
| `JO-JA` | Jerash | جرش |
| `JO-AJ` | Ajloun | عجلون |
| `JO-MN` | Ma'an | معان |
| `JO-MD` | Madaba | مادبا |
| `JO-AT` | Tafilah | الطفيلة |
| `JO-AQ` | Aqaba | العقبة |

### 16.3 Conditional Requirements

- **Customer name is mandatory when:**
  - Payment method is receivable (codes: `021`, `022`, `023`)
  - OR payable amount exceeds 10,000 JOD

- **Anonymous customer defaults:**
  - ID Type: `NIN`
  - ID Value: empty string `""`
  - The `AccountingCustomerParty` XML section is always present, even for anonymous customers.

---

## 17. Examples

### 17.1 Example: Income Invoice (GenerateIncomeInvoice.php)

**File:** `examples/GenerateIncomeInvoice.php`
**Lines:** 147

Demonstrates creating a complete income invoice with:
- Invoice type: `income`
- Payment: cash
- Tax category: exempt (`Z`)
- Customer with full details (TIN, name, city code, phone)
- Single product: 2 units at 100.00 JOD
- Auto-calculated totals
- Mock response handling demonstration

**Configuration used:**
```php
$configs = [
    'client_id'               => 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'client_secret'           => 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'invoice_type'            => 'income',
    'invoice_id'              => 'INV-001',
    'uuid'                    => '123e4567-e89b-12d3-a456-426614174000',
    'seller_tin'              => '12345678',
    'seller_name'             => 'Your Company Name',
    'supplier_income_source'  => '987654321',
    'customer_id'             => '987654321',
    'customer_tin'            => '98765432',
    'customer_name'           => 'Customer Name',
    'customer_city_code'      => 'JO-IR',
    'customer_phone'          => '0791234567',
    'product_id'              => 'PROD-001',
    'product_name'            => 'Sample Product',
    'product_quantity'        => 2,
    'product_unit_price'      => 100.00,
    'product_description'     => 'Sample Product Description',
    'issue_date'              => '16-02-2023',
];
```

**Flow:**
1. Creates `JoFotaraService` with credentials.
2. Sets basic information (type, ID, UUID, date, cash).
3. Sets seller info (TIN, name).
4. Sets customer info (ID as TIN, customer TIN, name, city, phone).
5. Sets supplier income source.
6. Adds one item (2 units at 100.00, tax exempt).
7. Calls `invoiceTotals()` for automatic calculation.
8. Calls `generateXml()` and `encodeInvoice()`.
9. Creates a mock successful response and demonstrates `JoFotaraResponse` usage.

### 17.2 Example: Credit Income Invoice (GenerateCreditIncomeInvoice.php)

**File:** `examples/GenerateCreditIncomeInvoice.php`
**Lines:** 152

Demonstrates creating a credit invoice to reverse a previous income invoice:
- Invoice type: `income`
- Payment: cash
- Credit invoice referencing original `INV-001`
- Reason for return: `"Test"`
- Single product: 1 unit at 0.01 JOD (minimal amount)
- Tax category: exempt (`Z`)

**Additional configuration vs income example:**
```php
'old_invoice_id'    => 'INV-001',
'old_uuid'          => '123e4567-e89b-12d3-a456-111111111111',
'old_full_amount'   => 0.01,
'reason'            => 'Test',
```

**Key differences from regular invoice:**
1. Calls `->asCreditInvoice($oldId, $oldUuid, $oldAmount)` on basic information.
2. Calls `$invoice->setReasonForReturn($reason)`.
3. This produces `InvoiceTypeCode` = `381` and adds `BillingReference` + `PaymentMeans` sections.

---

## 18. Gotchas and Edge Cases

1. **Currency attribute mismatch:** `DocumentCurrencyCode` = `JOD` but `currencyID` attribute on all amount elements = `JO`. This is intentional per the JoFotara specification.

2. **9 decimal places:** All monetary values, quantities, and tax percentages in XML use `%.9f` formatting.

3. **Original amount in credit invoices:** Formatted to 2 decimal places (not 9) in `DocumentDescription`.

4. **ICV counter in UUID element:** The invoice counter value goes inside a `<cbc:UUID>` element nested in `AdditionalDocumentReference` with ID = "ICV". The element name is misleading but correct.

5. **AllowanceCharge appears twice:**
   - Once at invoice level (totals section) -- only if discount > 0
   - Once per line item (inside `Price`) -- always present, even if discount = 0

6. **Discounts are per-item only:** Discounts must be applied to individual items, not to the invoice total.

7. **AllowanceTotalAmount conditional:** The `AllowanceTotalAmount` element inside `LegalMonetaryTotal` is only included if discount > 0.

8. **No sandbox environment:** JoFotara does not provide a test/sandbox. Use past dates and issue credit invoices to reverse test transactions.

9. **Dual response formats:** The API may return Format A or Format B at any time. Both must be handled.

10. **Anonymous customer still requires XML:** Even without customer data, the `AccountingCustomerParty` section must exist with `NIN` + empty ID.

11. **Line-item discount block always present:** The `AllowanceCharge` inside each `InvoiceLine > Price` is always output, even when discount = 0.0. The invoice-level `AllowanceCharge` (section 15 in XML order) is only included when discount > 0.

12. **AllowanceChargeReason casing:**
    - Invoice level: lowercase `"discount"`
    - Line-item level: uppercase `"DISCOUNT"`

13. **Default tax values:** If `tax()`, `taxExempted()`, or `zeroTax()` is never called, the defaults are `taxCategory = "S"` and `taxPercent = 16.0`.

14. **Invoice counter defaults to 1:** If `setInvoiceCounter()` is never called.

15. **XML escaping:** All text values are escaped for XML special characters.

16. **XML line endings:** Normalized to Unix LF (`\n`). Any `\r\n` is replaced.

17. **Root Invoice tag on one line:** The opening `<Invoice>` tag with all namespace declarations is a single line.

18. **Empty/invalid JSON responses:** If the API returns empty body or invalid JSON, the SDK creates an error response with descriptive message.

19. **`ALREADY_SUBMITTED` is success:** Submitting the same invoice twice returns `ALREADY_SUBMITTED` status -- treated as success (idempotent).

20. **`EINV_SINGED_INVOICE` typo is real:** The Format B response key for the signed invoice is literally `EINV_SINGED_INVOICE` (missing "N" in "SIGNED"). This is the actual API key, not a bug in the SDK.

21. **Payment method requires invoice type first:** Calling `cash()`, `receivable()`, or `setPaymentMethod()` before `setInvoiceType()` throws an exception.

---

## 19. Testing

### 19.1 Test Suite

The project uses **Pest PHP v4** for testing.

```bash
# Run tests
composer test
# or
vendor/bin/pest

# Run with coverage
composer test-coverage
# or
vendor/bin/pest --coverage
```

Test namespace: `JBadarneh\JoFotara\Tests\` (mapped to `tests/` directory).

### 19.2 Production Testing

Since JoFotara has no sandbox environment:

1. You need a registered entity with the Jordan Tax Department.
2. Your entity must be registered for JoFotara e-invoicing.
3. Use **past dates** for test invoices.
4. **Always issue credit invoices** to reverse test transactions.
5. Use the example scripts to generate and verify XML before submission:
   ```bash
   php examples/GenerateIncomeInvoice.php
   # On macOS, copy base64 output to clipboard:
   php examples/GenerateIncomeInvoice.php | pbcopy
   ```

---

## 20. Development Tools

| Tool | Purpose | Command |
|---|---|---|
| Pest PHP v4 | Testing framework | `composer test` |
| Laravel Pint v1 | Code formatting (PSR-12) | `composer format` |
| ext-dom | XML testing (dev only) | - |
| ext-libxml | XML validation (dev only) | - |

Composer scripts:
```json
{
    "test": "vendor/bin/pest",
    "test-coverage": "vendor/bin/pest --coverage",
    "format": "vendor/bin/pint"
}
```

---

## 21. Composer Configuration Details

**Full `composer.json` analysis:**

| Field | Value | Notes |
|---|---|---|
| `name` | `jafar-albadarneh/jofotara` | Packagist package name |
| `description` | PHP SDK to integrate with the Jordanian E-Invoice Portal | - |
| `keywords` | `jafar-albadarneh`, `jofotara` | Search keywords |
| `homepage` | `https://github.com/jafar-albadarneh/jofotara` | GitHub repository |
| `license` | `MIT` | Open source |
| `minimum-stability` | `dev` | Allows dev dependencies |
| `prefer-stable` | `true` | Prefers stable releases |
| `config.sort-packages` | `true` | Auto-sorts require sections |

**Allowed plugins:**
- `pestphp/pest-plugin` - Pest testing framework plugin
- `phpstan/extension-installer` - PHPStan extension auto-installer

---

## 22. Security Considerations

1. **Credentials:** Client ID and Secret Key should **never** be committed to version control. Use environment variables:
   ```php
   $invoice = new JoFotaraService(
       clientId: getenv('JOFOTARA_CLIENT_ID'),
       clientSecret: getenv('JOFOTARA_CLIENT_SECRET')
   );
   ```

2. **XML Injection Prevention:** All user-provided text values are escaped via `htmlspecialchars()` with XML-safe flags before being embedded in XML output.

3. **Input Validation:** Comprehensive validation prevents malformed data from reaching the API. Even with validations disabled, the XML structure remains safe due to escaping.

4. **HTTPS Only:** The API endpoint uses HTTPS exclusively (`https://backend.jofotara.gov.jo/core/invoices/`).

5. **No Token Storage:** The SDK does not cache or store authentication tokens. Credentials are sent as headers with each request.

6. **Protected HTTP Method:** The `executeRequest()` method is `protected`, allowing subclasses to override it for testing without exposing it publicly.

7. **Security Reporting:** Security issues should be reported to `security@jbadarneh.com` (not via public issue tracker).
