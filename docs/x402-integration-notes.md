# AP2 × x402 Integration Notes

## Overview

[AP2](https://ap2-protocol.org/) and [x402](https://www.x402.org/) are complementary protocols in the agentic payments ecosystem. As stated in the [official AP2 documentation](https://ap2-protocol.org/topics/ap2-and-x402/):

> "AP2 provides the overarching secure, interoperable protocol and trust mechanisms necessary for AI agents to make payments, while x402 represents a type of emerging payment method that AP2 is specifically designed to accommodate and support securely within the agentic payments ecosystem."

This document explores how NUSD Pay can leverage both protocols for stablecoin payment flows in social entertainment.

## How They Complement Each Other

| Aspect | AP2 | x402 |
|--------|-----|------|
| **Scope** | End-to-end payment protocol for AI agents | HTTP-native payment standard (402 Payment Required) |
| **Focus** | Trust, accountability, mandate-based authorization | Simple pay-per-request API monetization |
| **Payment model** | Supports pull and push (roadmap) | Push (stablecoin transfer) |
| **Transaction type** | Complex purchases (carts, subscriptions) | Simple one-shot payments |
| **Trust mechanism** | VDCs (Verifiable Digital Credentials) | On-chain payment verification |
| **Agent interaction** | Multi-agent (SA, ME, CP, MPP) | Two-party (client → server) |

## Integration Architecture

### Layer 1: x402 for Simple API Payments

x402 is ideal for straightforward, programmatic payments:

```
Agent ──── HTTP Request ────> API Server
       <── 402 Payment Required ──
Agent ──── Payment (stablecoin) ──> Facilitator ──> Blockchain
       <── Payment Receipt ──
Agent ──── HTTP Request + Receipt ──> API Server
       <── 200 OK + Response ──
```

**Social entertainment use cases for x402:**
- Pay-per-API-call for content recommendation engines
- Micropayments for AI-generated content (stickers, filters, effects)
- Machine-to-machine settlement between platform services

### Layer 2: AP2 for Complex Payment Flows

AP2 handles multi-party, trust-sensitive transactions:

```
User ──> Shopping Agent ──> Merchant Agent ──> Cart Mandate
                                              ↓
User <── Confirm ──────── Shopping Agent <── CartMandate (signed)
                                              ↓
User ──> Approve ────────> Shopping Agent ──> Credentials Provider
                                              ↓
                           Payment Mandate ──> MPP ──> Settlement
```

**Social entertainment use cases for AP2:**
- User-initiated tips and gifts (requires Human Present confirmation)
- Subscription management (requires Intent Mandate)
- Multi-item purchases (gift bundles, virtual item packages)

### Layer 3: AP2 + x402 Combined

Some flows benefit from both protocols working together:

```
                    ┌─────────────────────────────────────────┐
                    │           AP2 Layer (Trust)              │
                    │                                         │
User ──> SA ──> ME ──> CartMandate ──> User Confirms          │
                    │                    │                     │
                    │                    ▼                     │
                    │  ┌──────────────────────────────┐       │
                    │  │    x402 Layer (Settlement)    │       │
                    │  │                              │       │
                    │  │  CP ──402──> NUSD Pay API    │       │
                    │  │       <──── Payment Receipt  │       │
                    │  │                              │       │
                    │  └──────────────────────────────┘       │
                    │                    │                     │
                    │                    ▼                     │
                    │  PaymentMandate (includes x402 receipt)  │
                    └─────────────────────────────────────────┘
```

**Example:** A user tips a creator $5. AP2 handles the mandate flow (trust, authorization, accountability). The actual stablecoin transfer uses x402's HTTP 402 mechanism through NUSD Pay's API, and the x402 payment receipt becomes part of the AP2 PaymentMandate.

## NUSD Pay's Role in Both Protocols

### As x402 Facilitator

NUSD Pay can serve as an [x402 Facilitator](https://github.com/google-agentic-commerce/a2a-x402) — the entity that:
1. Receives payment requests from resource servers
2. Processes stablecoin transfers on-chain
3. Returns payment receipts to clients

This role maps directly to NUSD Pay's existing payment processing capability.

### As AP2 Credentials Provider + MPP

In the AP2 architecture, NUSD Pay operates as:
- **Credentials Provider (CP):** Manages user's stablecoin wallet credentials (MPC-secured)
- **Merchant Payment Processor (MPP):** Verifies on-chain receipt and confirms settlement

## Implementation Priority

| Phase | Protocol | Deliverable | Complexity |
|-------|----------|-------------|------------|
| 1 | x402 | NUSD Pay as x402 Facilitator | Low — wraps existing API |
| 2 | AP2 | Human Present flow with stablecoin CartMandate | Medium — new mandate logic |
| 3 | AP2 + x402 | Combined flow with x402 settlement inside AP2 mandates | Medium — integration layer |
| 4 | AP2 | Human Not Present + subscriptions | High — requires AP2 v1.x |

## Key Insight

Starting with x402 Facilitator (Phase 1) provides immediate value:
- **Low effort:** Essentially an API wrapper around NUSD Pay's existing payment endpoint
- **Visible contribution:** Can be submitted as a reference implementation to the [a2a-x402 repo](https://github.com/google-agentic-commerce/a2a-x402)
- **AP2 bridge:** x402 integration naturally feeds into AP2 as a supported payment method

The [AP2 documentation explicitly states](https://ap2-protocol.org/topics/ap2-and-x402/) that shared samples for AP2 + x402 are currently being built. Contributing a stablecoin-focused implementation positions NUSD Pay as a practical contributor to this effort.

## References

- [AP2 and x402 — Official Documentation](https://ap2-protocol.org/topics/ap2-and-x402/)
- [a2a-x402 Repository](https://github.com/google-agentic-commerce/a2a-x402)
- [x402 Protocol](https://www.x402.org/)
- [AP2 Core Concepts](https://ap2-protocol.org/topics/core-concepts/)
- [AP2 Roadmap](https://ap2-protocol.org/roadmap/)
