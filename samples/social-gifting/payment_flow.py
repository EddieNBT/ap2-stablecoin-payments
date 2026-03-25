#!/usr/bin/env python3
# Copyright 2025 Newborn Town Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""AP2 Social Gifting Demo — Human Present Flow.

Demonstrates a complete AP2 payment flow for a social entertainment
gifting scenario using stablecoin settlement.

Flow:
    1. User expresses intent to send a gift
    2. Merchant Agent builds a cart and signs a Cart Mandate
    3. User confirms the cart (Human Present)
    4. Credentials Provider processes stablecoin payment
    5. Payment Mandate is generated for the payment network

This is a mock/demo implementation. No real blockchain transactions occur.
"""

import uuid
from datetime import datetime, timezone

from merchant_agent import build_cart, sign_cart_mandate, GIFT_CATALOG
from models import (
    PaymentMandate,
    PaymentMandateContents,
    PaymentResponse,
    StablecoinPaymentDetails,
)

# ── Display helpers ──────────────────────────────────────────────


def banner(text: str) -> None:
    """Print a banner line."""
    width = 55
    print(f"\n{'═' * width}")
    print(f"  {text}")
    print(f"{'═' * width}\n")


def step(number: int, title: str) -> None:
    """Print a step header."""
    print(f"[{number}/5] {title}")


def detail(key: str, value: str) -> None:
    """Print an indented detail line."""
    print(f"  → {key}: {value}")


# ── Mock Credentials Provider ───────────────────────────────────


def mock_process_payment(
    amount: float,
    currency: str,
    token: str = "USDT",
    chain: str = "tron",
) -> StablecoinPaymentDetails:
    """Simulate stablecoin payment processing.

    In production, this would:
    1. Connect to NUSD Pay API
    2. Initiate MPC-signed transfer
    3. Wait for on-chain confirmation
    4. Return settlement details

    Returns:
        StablecoinPaymentDetails with mock transaction data.
    """
    mock_tx_hash = f"0x{uuid.uuid4().hex}"

    return StablecoinPaymentDetails(
        token=token,
        chain=chain,
        sender_address="TXyz7890abcdef1234567890abcdef12345678",
        recipient_address="TDef1234567890abcdef1234567890abcdef12",
        amount=f"{amount:.2f}",
        tx_hash=mock_tx_hash,
        block_number=68_542_391,
        confirmations_required=19,
        confirmations_current=19,
        finality_status="confirmed",
        settlement_time_ms=28_500,
    )


# ── Main Demo Flow ──────────────────────────────────────────────


def run_demo() -> None:
    """Execute the complete AP2 social gifting flow."""

    banner("AP2 Social Gifting Demo — Human Present Flow")

    # ── Step 1: User Intent ──
    step(1, "User Intent")
    gift_id = "golden_rose"
    quantity = 50
    recipient = "alice"
    gift = GIFT_CATALOG[gift_id]
    detail("Intent", f'"Send {quantity} {gift["name"]}s to @{recipient}"')
    print()

    # ── Step 2: Merchant Agent builds cart ──
    step(2, "Merchant Agent: Building Cart")
    cart = build_cart(
        gift_id=gift_id,
        quantity=quantity,
        recipient=recipient,
        preferred_chain="tron",
    )
    detail("Cart ID", cart.id)
    detail("Items", f"{gift['name']} × {quantity}")
    detail(
        "Total",
        f"${cart.payment_request.details.total.amount.value:.2f} "
        f"{cart.payment_request.details.total.amount.currency}",
    )
    method = cart.payment_request.method_data[0]
    detail(
        "Payment Method",
        f"{method.data.supported_tokens[0]} ({method.data.preferred_chain})",
    )
    detail("Cart Expiry", cart.cart_expiry)
    print()

    # ── Step 3: Cart Mandate signed by Merchant ──
    step(3, "Cart Mandate: Signed by Merchant")
    cart_mandate = sign_cart_mandate(cart)
    jwt_parts = cart_mandate.merchant_authorization.split(".")
    detail("JWT Header", '{"alg": "HS256", "kid": "merchant-key-001"}')
    detail("Cart Hash", f"sha256:{uuid.uuid4().hex[:16]}...")
    detail("Signature", "✅ Valid")
    print()

    # ── Step 4: User Confirmation (Human Present) ──
    step(4, "User Confirmation (Human Present)")
    total = cart.payment_request.details.total
    detail(
        "Prompt",
        f'"Send {quantity} {gift["name"]}s to @{recipient} '
        f'for ${total.amount.value:.2f} USDT?"',
    )
    detail("User", "✅ Confirmed")
    print()

    # ── Step 5: Payment Mandate ──
    step(5, "Payment Mandate: Generated")
    payment_details = mock_process_payment(
        amount=total.amount.value,
        currency=total.amount.currency,
        token="USDT",
        chain="tron",
    )

    payment_mandate = PaymentMandate(
        payment_mandate_contents=PaymentMandateContents(
            payment_mandate_id=f"pm-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
            payment_details_id=cart.payment_request.details.id,
            payment_details_total=total,
            payment_response=PaymentResponse(
                method_name="https://nusdpay.com/stablecoin/v1",
                details=payment_details,
            ),
            merchant_agent="merchant-socialapp-001",
        ),
    )

    pm = payment_mandate.payment_mandate_contents
    detail("Payment ID", pm.payment_mandate_id)
    detail("Method", pm.payment_response.method_name)
    detail("Token", pm.payment_response.details.token)
    detail("Chain", pm.payment_response.details.chain)
    detail("Amount", pm.payment_response.details.amount)
    detail("Tx Hash", f"(mock) {pm.payment_response.details.tx_hash[:10]}...")
    detail("Status", f"✅ {pm.payment_response.details.finality_status.title()}")

    banner("Demo Complete — All mandates generated successfully")


if __name__ == "__main__":
    run_demo()
