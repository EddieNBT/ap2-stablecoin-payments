# Sample: Social Gifting — AP2 Human Present Flow

A minimal demonstration of the AP2 Human Present payment flow applied to a social entertainment gifting scenario.

## Scenario

A user on a social platform wants to send a virtual gift (a bundle of "Golden Roses") to a friend. The payment is settled in USDT via stablecoin transfer.

**Flow:**
1. User tells their Shopping Agent: *"Send 50 Golden Roses to @alice"*
2. Shopping Agent contacts the platform's Merchant Agent
3. Merchant Agent builds a cart and signs a **Cart Mandate**
4. User reviews and confirms the cart (Human Present)
5. Credentials Provider processes the stablecoin payment
6. A **Payment Mandate** is generated for the payment network

## What This Demonstrates

- AP2 mandate creation and signing for a social payment use case
- Stablecoin payment method extension for `PaymentMethodData`
- The full mandate lifecycle: Intent → Cart → Payment
- Mock settlement (no real blockchain transactions)

## Running

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager (recommended) or pip

### Install & Run

```bash
# Clone and navigate
git clone https://github.com/EddieNBT/ap2-stablecoin-payments.git
cd ap2-stablecoin-payments/samples/social-gifting

# Install dependencies
uv pip install -r requirements.txt
# or: pip install -r requirements.txt

# Run the demo
python payment_flow.py
```

### Expected Output

```
═══════════════════════════════════════════════════
  AP2 Social Gifting Demo — Human Present Flow
═══════════════════════════════════════════════════

[1/5] User Intent
  → "Send 50 Golden Roses to @alice"

[2/5] Merchant Agent: Building Cart
  → Cart ID: gift-20250325-a1b2c3
  → Items: Golden Rose × 50
  → Total: $25.00 USD
  → Payment Method: USDT (Tron)
  → Cart Expiry: 2025-03-25T12:15:00Z

[3/5] Cart Mandate: Signed by Merchant
  → JWT Header: {"alg": "RS256", "kid": "merchant-key-001"}
  → Cart Hash: sha256:9f86d08...
  → Signature: ✅ Valid

[4/5] User Confirmation (Human Present)
  → "Send 50 Golden Roses to @alice for $25.00 USDT?"
  → User: ✅ Confirmed

[5/5] Payment Mandate: Generated
  → Payment ID: pm-20250325-d4e5f6
  → Method: https://nusdpay.com/stablecoin/v1
  → Token: USDT
  → Chain: tron
  → Amount: 25.00
  → Tx Hash: (mock) 0x7a8b9c...
  → Status: ✅ Settled

═══════════════════════════════════════════════════
  Demo Complete — All mandates generated successfully
═══════════════════════════════════════════════════
```

## File Structure

| File | Description |
|------|-------------|
| `payment_flow.py` | Main demo — runs the complete AP2 flow |
| `merchant_agent.py` | Mock Merchant Agent — builds carts and signs Cart Mandates |
| `models.py` | AP2 data models adapted for stablecoin payments |
| `config.example.yaml` | Configuration template |
| `requirements.txt` | Python dependencies |

## Limitations

- **Mock settlement** — No real blockchain transactions. The demo simulates on-chain transfer and confirmation.
- **Simplified signing** — Uses HMAC for demonstration. Production would use RSA/EC keys with proper JWT signing.
- **Single scenario** — Only covers Human Present gifting. See [use case docs](../../docs/use-case-social-payments.md) for tipping and subscription scenarios.

## Related

- [Use Case: Social Payments](../../docs/use-case-social-payments.md)
- [Mandate Field Mapping](../../docs/mandate-mapping.md)
- [AP2 Official Samples](https://github.com/google-agentic-commerce/AP2/tree/main/samples)
