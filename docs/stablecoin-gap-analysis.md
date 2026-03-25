# Stablecoin Gap Analysis: Push Payments × AP2

## Overview

AP2 v0.1 is designed primarily for **pull payment** methods (credit/debit cards) in **Human Present** scenarios. Stablecoin payments are fundamentally **push payments** — the payer initiates the transfer directly to the payee's address. This document analyzes where stablecoin push payments align with and diverge from the current AP2 specification, and proposes approaches for bridging the gaps.

## Compatibility Matrix

| AP2 Feature | Pull Payments (Cards) | Push Payments (Stablecoins) | Status |
|-------------|----------------------|---------------------------|--------|
| Human Present flow | ✅ Native support | ✅ Compatible | **Ready** |
| Cart Mandate | ✅ Native support | ✅ Compatible | **Ready** |
| Payment Mandate | ✅ Native support | ⚠️ Needs payment method extension | **Bridgeable** |
| PaymentMethodData | ✅ Card networks defined | ⚠️ No stablecoin method defined | **Bridgeable** |
| PaymentResponse | ✅ Card token/details | ⚠️ Needs chain/token/address fields | **Bridgeable** |
| Human Not Present | 🔜 v1.x roadmap | 🔜 Needed for subscriptions | **Waiting** |
| Push payment model | ❌ Not current focus | ✅ Core stablecoin model | **Gap** |
| Recurring payments | 🔜 v1.x roadmap | 🔜 Needed for subscriptions | **Waiting** |
| Multi-chain support | N/A | ⚠️ Chain selection not in spec | **Extension needed** |
| Settlement finality | Instant (authorization) | ⚠️ Block confirmations needed | **Extension needed** |

## Detailed Gap Analysis

### Gap 1: Payment Method Identifier

**Current state:** AP2 samples use `"https://sample-card-network.github.io/paymentmethod/types/v1"` as the payment method identifier for card payments.

**Gap:** No registered payment method identifier exists for stablecoin payments.

**Proposed approach:** Define a payment method URI following the W3C Payment Method convention:

```
https://nusdpay.com/stablecoin/v1
```

This method identifier would signal to the Shopping Agent and Credentials Provider that the merchant accepts stablecoin payments and that the payment flow follows push-payment semantics.

### Gap 2: Pull vs Push Payment Semantics

**Current state:** AP2's card flow assumes pull semantics:
1. User provides payment credentials (card token)
2. Merchant Payment Processor charges the card
3. Card network handles authorization and settlement

**Gap:** Stablecoin payments use push semantics:
1. User authorizes a transfer from their wallet
2. User's wallet initiates the on-chain transfer
3. Blockchain network confirms the transaction
4. Merchant verifies receipt

**Impact on AP2 flow:**

| Step | Cards (Pull) | Stablecoins (Push) |
|------|-------------|-------------------|
| Credentials Provider role | Returns card token | Returns wallet address + signed transfer intent |
| MPP role | Initiates charge | Verifies on-chain receipt |
| Authorization | Synchronous (card network) | Asynchronous (block confirmations) |
| Finality | Provisional (chargebacks possible) | Final after N confirmations |

**Proposed approach:** The core mandate flow remains unchanged. The Credentials Provider's role shifts from "provide credentials for merchant to charge" to "execute the transfer and return proof of payment." The MPP verifies on-chain receipt rather than initiating a charge.

### Gap 3: Settlement Finality and Confirmation

**Current state:** Card payments have instant authorization but provisional finality (chargebacks are possible for weeks/months).

**Gap:** Stablecoin payments have delayed confirmation (seconds to minutes depending on chain) but absolute finality (no chargebacks).

**Proposed extension to PaymentResponse:**

```json
{
  "method_name": "https://nusdpay.com/stablecoin/v1",
  "details": {
    "token": "USDT",
    "chain": "tron",
    "tx_hash": "0x...",
    "block_number": 12345678,
    "confirmations_required": 19,
    "confirmations_current": 19,
    "finality_status": "confirmed",
    "settlement_time_ms": 28500
  }
}
```

### Gap 4: Multi-Chain Selection

**Current state:** AP2's PaymentMethodData doesn't account for chain selection — cards don't have this concept.

**Gap:** A single stablecoin (e.g., USDT) can exist on multiple chains (Ethereum, Tron, BSC, etc.) with different gas costs, confirmation times, and liquidity.

**Proposed extension to PaymentMethodData:**

```json
{
  "supported_methods": "https://nusdpay.com/stablecoin/v1",
  "data": {
    "supported_tokens": [
      {
        "symbol": "USDT",
        "chains": ["ethereum", "tron", "bsc", "polygon", "arbitrum"],
        "contract_addresses": {
          "ethereum": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
          "tron": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
          "bsc": "0x55d398326f99059fF775485246999027B3197955"
        }
      },
      {
        "symbol": "USDC",
        "chains": ["ethereum", "polygon", "solana", "arbitrum"],
        "contract_addresses": {
          "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
          "solana": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        }
      }
    ],
    "preferred_chain": "tron",
    "chain_selection_criteria": "lowest_gas"
  }
}
```

### Gap 5: Currency Representation

**Current state:** AP2 uses ISO 4217 three-letter currency codes (USD, EUR, etc.) in `PaymentCurrencyAmount`.

**Gap:** Stablecoins don't have ISO 4217 codes. USDT and USDC are pegged to USD but are not USD.

**Proposed approach:** Use a two-layer representation:

```json
{
  "display_amount": {
    "currency": "USD",
    "value": 5.00
  },
  "settlement_amount": {
    "token": "USDT",
    "value": "5.00",
    "chain": "tron"
  }
}
```

The `display_amount` uses standard ISO 4217 for user-facing display. The `settlement_amount` captures the actual stablecoin transfer details. This approach is compatible with AP2's existing `PaymentCurrencyAmount` while adding stablecoin-specific settlement information.

## What Works Today (No Changes Needed)

1. **Cart Mandate flow** — The core mandate creation and signing flow works for stablecoins. A tip/gift cart is a cart regardless of payment method.

2. **Merchant authorization JWT** — The JWT-based cart signing mechanism is payment-method agnostic. Works as-is.

3. **Payment Mandate for trust** — The Payment Mandate's purpose (providing visibility into agentic transactions for the payment network) is equally applicable to stablecoin settlement networks.

4. **Human Present confirmation** — User confirmation before payment execution maps perfectly to stablecoin wallet signing flows.

5. **A2A transport** — The underlying Agent-to-Agent protocol for message exchange is independent of payment method.

## Recommendations

### For AP2 Protocol Team

1. **Define a stablecoin PaymentMethod spec** — Even a draft would unblock integration work
2. **Add push payment flow documentation** — The current flow assumes pull semantics; documenting push alternatives would support stablecoin, bank transfer, and e-wallet integrations
3. **Consider settlement finality fields** — Card authorization is provisional; stablecoin settlement is final. Both need representation in PaymentResponse.

### For Stablecoin Integrators (Our Path)

1. **Start with Human Present flow** — Fully compatible today
2. **Define a PaymentMethod extension** — Register a method identifier for stablecoin payments
3. **Implement Credentials Provider as wallet interface** — Map MPC wallet signing to CP role
4. **Wait for v1.x for subscriptions** — Human Not Present + recurring payment support needed

## AP2 Protocol Alignment

This analysis is based on:
- [AP2 Core Concepts](https://ap2-protocol.org/topics/core-concepts/)
- [AP2 Specification v0.1](https://ap2-protocol.org/topics/ap2-specification/)
- [AP2 Roadmap](https://ap2-protocol.org/roadmap/)
- [AP2 and x402](https://ap2-protocol.org/topics/ap2-and-x402/)
- [AP2 Source: mandate.py](https://github.com/google-agentic-commerce/AP2/blob/main/src/ap2/types/mandate.py)
- [AP2 Source: payment_request.py](https://github.com/google-agentic-commerce/AP2/blob/main/src/ap2/types/payment_request.py)
