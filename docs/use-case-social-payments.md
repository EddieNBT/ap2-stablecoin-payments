# Use Case: AP2 for Social Entertainment Payments

## Overview

Social entertainment platforms — live streaming, social networking, short video — generate massive volumes of micro-payments across borders. Users tip creators, send virtual gifts, and subscribe to premium content. These transactions are increasingly mediated by AI agents that recommend gifts, manage budgets, and optimize spending.

This document maps three core social entertainment payment scenarios to the AP2 protocol's mandate architecture.

## Scenario 1: Creator Tipping (Human Present)

**Description:** A user watches a live stream and wants to tip the creator $5 in USDT. The user's AI shopping agent facilitates the payment through the platform's merchant agent.

### Participants

| AP2 Role | Actor | Description |
|----------|-------|-------------|
| User | Live stream viewer | Wants to tip a creator |
| Shopping Agent (SA) | User's AI assistant | Facilitates the tipping flow |
| Merchant Endpoint (ME) | Platform merchant agent | Represents the social platform |
| Credentials Provider (CP) | NUSD Pay wallet | Manages user's stablecoin credentials |
| Merchant Payment Processor (MPP) | NUSD Pay settlement | Processes the stablecoin transfer |

### Flow (Human Present — Cart Mandate)

```
┌──────┐     ┌────────────┐     ┌──────────────┐     ┌────────────┐     ┌─────┐
│ User │     │ Shopping   │     │  Merchant    │     │Credentials │     │ MPP │
│      │     │ Agent (SA) │     │ Endpoint(ME) │     │Provider(CP)│     │     │
└──┬───┘     └─────┬──────┘     └──────┬───────┘     └─────┬──────┘     └──┬──┘
   │               │                   │                   │               │
   │ "Tip @creator │                   │                   │               │
   │  $5 USDT"     │                   │                   │               │
   │──────────────>│                   │                   │               │
   │               │                   │                   │               │
   │               │  Request cart     │                   │               │
   │               │  (tip intent)     │                   │               │
   │               │──────────────────>│                   │               │
   │               │                   │                   │               │
   │               │  CartMandate      │                   │               │
   │               │  (signed by ME)   │                   │               │
   │               │<──────────────────│                   │               │
   │               │                   │                   │               │
   │ Confirm tip   │                   │                   │               │
   │ details?      │                   │                   │               │
   │<──────────────│                   │                   │               │
   │               │                   │                   │               │
   │ ✅ Approved   │                   │                   │               │
   │──────────────>│                   │                   │               │
   │               │                   │                   │               │
   │               │  Request payment  │                   │               │
   │               │  credentials      │                   │               │
   │               │──────────────────────────────────────>│               │
   │               │                   │                   │               │
   │               │  PaymentResponse  │                   │               │
   │               │  (USDT token)     │                   │               │
   │               │<─────────────────────────────────────│               │
   │               │                   │                   │               │
   │               │  PaymentMandate + CartMandate         │               │
   │               │──────────────────────────────────────────────────────>│
   │               │                   │                   │               │
   │               │                   │                   │    USDT       │
   │               │                   │                   │  Transfer     │
   │               │                   │                   │    on-chain   │
   │               │                   │                   │               │
   │ "Tip sent ✅" │                   │                   │               │
   │<──────────────│                   │                   │               │
```

### Key Design Decisions

- **Human Present flow**: User explicitly confirms the tip amount — critical for financial transactions
- **Cart contains single item**: The tip itself, with creator ID as the product identifier
- **Settlement in USDT**: Stablecoin push payment via on-chain transfer
- **CartMandate signed by platform**: Guarantees the tip amount and recipient

---

## Scenario 2: Digital Gifting (Human Present)

**Description:** A user purchases a virtual gift package ($20 worth of virtual roses) to send to a friend on a social platform. The gift includes platform-specific virtual items.

### Participants

Same role mapping as Scenario 1, with the Merchant Endpoint representing the platform's gift shop.

### Cart Contents

```json
{
  "id": "gift-order-20250325-001",
  "user_cart_confirmation_required": true,
  "payment_request": {
    "id": "pr-gift-001",
    "details": {
      "total": {
        "label": "Virtual Rose Bundle (x50)",
        "amount": { "currency": "USD", "value": 20.00 }
      },
      "display_items": [
        {
          "label": "Virtual Rose × 50",
          "amount": { "currency": "USD", "value": 18.00 }
        },
        {
          "label": "Gift wrapping animation",
          "amount": { "currency": "USD", "value": 2.00 }
        }
      ]
    },
    "method_data": [
      {
        "supported_methods": "https://nusdpay.com/stablecoin/v1",
        "data": {
          "supported_tokens": ["USDT", "USDC"],
          "supported_chains": ["tron", "bsc", "polygon"],
          "settlement_currency": "USD"
        }
      }
    ]
  },
  "cart_expiry": "2025-03-25T12:00:00Z",
  "merchant_name": "SocialApp Gift Shop"
}
```

### What's Different from Tipping

| Aspect | Tipping | Gifting |
|--------|---------|--------|
| Item count | Single (tip amount) | Multiple (virtual items) |
| Recipient | Creator wallet | Friend's account (platform-internal) |
| Refundability | Non-refundable | Platform policy dependent |
| Price variability | User-defined amount | Fixed catalog price |

---

## Scenario 3: Creator Subscription (Human Not Present — Future)

> ⚠️ **Note:** Human Not Present flows are part of AP2 v1.x roadmap. This scenario documents the expected mapping for when the capability becomes available.

**Description:** A user subscribes to a creator's premium content at $9.99/month, paid in USDC. The AI agent handles automatic monthly renewals without requiring the user to be present each time.

### Intent Mandate (User-Signed)

```json
{
  "user_cart_confirmation_required": false,
  "natural_language_description": "Subscribe to @creator_jane's premium content at $9.99/month, paid in USDC. Auto-renew monthly. Cancel if price increases above $12.",
  "merchants": ["socialapp-creator-jane"],
  "requires_refundability": false,
  "intent_expiry": "2026-03-25T00:00:00Z"
}
```

### Key Considerations for Subscriptions

| Challenge | AP2 Approach | Stablecoin Consideration |
|-----------|-------------|-------------------------|
| Recurring authorization | Intent Mandate with TTL | Push payment requires agent-initiated transfer each cycle |
| Price changes | Constraints in natural language description | Stablecoin amount may vary with USD peg fluctuations |
| Cancellation | Intent Mandate expiry | Agent must stop initiating transfers |
| Multi-currency | PaymentMethodData supports multiple methods | User may switch between USDT/USDC between cycles |

---

## Cross-Cutting Concerns

### Multi-Currency Stablecoin Support

Social entertainment platforms operate across borders. A single transaction may involve:
- **User's preferred token**: USDT on Tron (low gas fees)
- **Platform's settlement token**: USDC on Ethereum (institutional preference)
- **Display currency**: USD (user-facing price)

AP2's `PaymentMethodData` can be extended to express stablecoin preferences:

```json
{
  "supported_methods": "https://nusdpay.com/stablecoin/v1",
  "data": {
    "supported_tokens": ["USDT", "USDC", "NUSD"],
    "supported_chains": ["ethereum", "tron", "bsc", "polygon", "solana", "arbitrum"],
    "preferred_chain": "tron",
    "settlement_currency": "USD",
    "max_slippage_bps": 50
  }
}
```

### Compliance and Trust

| Requirement | Implementation |
|-------------|----------------|
| KYB (Know Your Business) | Merchant onboarding via NUSD Pay |
| KYT (Know Your Transaction) | On-chain transaction monitoring |
| MPC Wallet Custody | User credentials secured via MPC key shards |
| Regulatory | Compliant with local payment regulations per market |

### Transaction Economics

| Metric | Typical Value |
|--------|---------------|
| Average tip size | $0.50 – $5.00 |
| Average gift purchase | $5.00 – $50.00 |
| Subscription price range | $1.99 – $19.99/month |
| Platform fee | 1% (via NUSD Pay) |
| On-chain gas (Tron) | < $0.01 |
| Settlement time | < 30 seconds |
