# Mandate Field Mapping: NUSD Pay ↔ AP2

## Overview

This document maps NUSD Pay's existing payment data model to AP2's mandate-based architecture. The goal is to identify direct mappings, required transformations, and gaps that need to be addressed for AP2 integration.

## AP2 Mandate Types

AP2 uses three types of Verifiable Digital Credentials (VDCs):

1. **Cart Mandate** — Merchant-signed commitment to specific items and prices (Human Present)
2. **Intent Mandate** — User-signed authorization for future purchases (Human Not Present)
3. **Payment Mandate** — Transaction visibility credential shared with payment network/issuer

## Cart Mandate Mapping

### CartContents ↔ NUSD Pay Order

| AP2 Field | Type | NUSD Pay Equivalent | Notes |
|-----------|------|---------------------|-------|
| `id` | string | `order_id` | Direct mapping. UUID format. |
| `user_cart_confirmation_required` | bool | Always `true` for stablecoin | Stablecoin push payments require explicit user confirmation |
| `payment_request.id` | string | `payment_request_id` | Direct mapping |
| `payment_request.details.total.label` | string | `order_description` | Human-readable description |
| `payment_request.details.total.amount.currency` | string | `settlement_currency` | AP2 uses ISO 4217; stablecoin needs extension (see Gap Analysis) |
| `payment_request.details.total.amount.value` | float | `order_amount` | Direct mapping |
| `payment_request.details.display_items[]` | array | `line_items[]` | Each line item maps to a PaymentItem |
| `payment_request.method_data[].supported_methods` | string | N/A | New field: `"https://nusdpay.com/stablecoin/v1"` |
| `payment_request.method_data[].data` | object | Token/chain config | Stablecoin-specific: tokens, chains, settlement currency |
| `cart_expiry` | ISO 8601 | `order_expiry_time` | Direct mapping |
| `merchant_name` | string | `merchant_display_name` | Direct mapping |

### PaymentItem ↔ NUSD Pay Line Item

| AP2 Field | Type | NUSD Pay Equivalent | Notes |
|-----------|------|---------------------|-------|
| `label` | string | `item_name` | Direct mapping |
| `amount.currency` | string | `item_currency` | ISO 4217 code |
| `amount.value` | float | `item_amount` | Direct mapping |
| `pending` | bool | `is_pending` | Rarely used in social payments |
| `refund_period` | int (days) | `refund_window_days` | Default 30 in AP2; social payments often 0 (non-refundable) |

### Merchant Authorization (JWT)

| JWT Field | NUSD Pay Equivalent | Notes |
|-----------|---------------------|-------|
| `iss` | `merchant_id` | Merchant's unique identifier |
| `sub` | `merchant_id` | Same as issuer for self-signed |
| `aud` | N/A | Payment processor identifier (NUSD Pay) |
| `iat` | `order_created_at` | Timestamp of cart creation |
| `exp` | `order_expiry_time` | Short-lived: 5–15 minutes recommended |
| `jti` | `order_id` | Unique token ID to prevent replay |
| `cart_hash` | N/A | New: SHA-256 hash of canonical CartContents JSON |

## Payment Mandate Mapping

### PaymentMandateContents ↔ NUSD Pay Transaction

| AP2 Field | Type | NUSD Pay Equivalent | Notes |
|-----------|------|---------------------|-------|
| `payment_mandate_id` | string | `transaction_id` | Direct mapping |
| `payment_details_id` | string | `payment_request_id` | Links to the original payment request |
| `payment_details_total.label` | string | `order_description` | Direct mapping |
| `payment_details_total.amount` | PaymentCurrencyAmount | `{currency, amount}` | Direct mapping |
| `payment_response.method_name` | string | `payment_method` | `"https://nusdpay.com/stablecoin/v1"` |
| `payment_response.details` | object | Transaction details | Chain, token, tx_hash, wallet addresses |
| `merchant_agent` | string | `merchant_id` | Direct mapping |
| `timestamp` | ISO 8601 | `transaction_created_at` | Direct mapping |

### PaymentResponse Details for Stablecoin

```json
{
  "method_name": "https://nusdpay.com/stablecoin/v1",
  "details": {
    "token": "USDT",
    "chain": "tron",
    "sender_address": "TXyz...abc",
    "recipient_address": "TDef...ghi",
    "amount": "5.00",
    "tx_hash": "0x...",
    "block_number": 12345678,
    "confirmation_count": 19,
    "mpc_signature_id": "sig-uuid-001"
  }
}
```

## Intent Mandate Mapping (Future — AP2 v1.x)

### IntentMandate ↔ NUSD Pay Subscription

| AP2 Field | Type | NUSD Pay Equivalent | Notes |
|-----------|------|---------------------|-------|
| `user_cart_confirmation_required` | bool | `auto_renew` (inverted) | `false` = auto-renew allowed |
| `natural_language_description` | string | N/A | New: AI-generated description of subscription terms |
| `merchants` | list[str] | `merchant_id` | Single merchant for subscriptions |
| `skus` | list[str] | `subscription_plan_id` | Maps to specific plan |
| `requires_refundability` | bool | `is_refundable` | Direct mapping |
| `intent_expiry` | ISO 8601 | `subscription_end_date` | When the subscription authorization expires |

## Transformation Summary

### Direct Mappings (No Change Required)

- Order ID → Cart ID
- Amount/Currency → PaymentCurrencyAmount
- Line items → PaymentItems
- Merchant name → merchant_name
- Transaction ID → payment_mandate_id
- Timestamps → ISO 8601 format

### Required Additions

| New Component | Purpose |
|---------------|---------|
| Merchant JWT signing | CartMandate requires cryptographic signature |
| Cart hash computation | SHA-256 over canonical JSON for JWT `cart_hash` claim |
| PaymentMethod registration | Define `https://nusdpay.com/stablecoin/v1` as method identifier |
| User authorization (VP) | Verifiable Presentation for PaymentMandate `user_authorization` |
| Stablecoin payment details schema | Standardize token/chain/address fields in PaymentResponse |

### Gaps Requiring Protocol Extension

See [Stablecoin Gap Analysis](stablecoin-gap-analysis.md) for detailed analysis.
