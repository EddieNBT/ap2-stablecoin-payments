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

"""Mock Merchant Agent for social entertainment platform.

Simulates a social platform's gift shop that:
1. Maintains a catalog of virtual gifts
2. Builds carts from user requests
3. Signs Cart Mandates (simplified for demo)
"""

import hashlib
import hmac
import json
import uuid
from datetime import datetime, timedelta, timezone

from models import (
    CartContents,
    CartMandate,
    PaymentCurrencyAmount,
    PaymentDetails,
    PaymentItem,
    PaymentMethodData,
    PaymentRequest,
    StablecoinMethodData,
)

# --- Gift Catalog ---

GIFT_CATALOG = {
    "golden_rose": {
        "name": "Golden Rose",
        "price_usd": 0.50,
        "description": "A beautiful golden rose animation",
    },
    "diamond_ring": {
        "name": "Diamond Ring",
        "price_usd": 5.00,
        "description": "A sparkling diamond ring effect",
    },
    "rocket": {
        "name": "Rocket",
        "price_usd": 10.00,
        "description": "Launch a rocket across the stream",
    },
    "castle": {
        "name": "Castle",
        "price_usd": 50.00,
        "description": "A grand castle animation with fireworks",
    },
}

MERCHANT_NAME = "SocialApp Gift Shop"
MERCHANT_ID = "merchant-socialapp-001"

# In production, this would be an RSA/EC private key
MOCK_SIGNING_KEY = b"demo-merchant-signing-key-do-not-use-in-production"


def build_cart(
    gift_id: str,
    quantity: int,
    recipient: str,
    preferred_chain: str = "tron",
) -> CartContents:
    """Build a cart for a gift purchase.

    Args:
        gift_id: Gift identifier from the catalog.
        quantity: Number of gifts to send.
        recipient: Username of the gift recipient.
        preferred_chain: Preferred blockchain for settlement.

    Returns:
        CartContents with the gift order details.
    """
    gift = GIFT_CATALOG.get(gift_id)
    if not gift:
        raise ValueError(f"Unknown gift: {gift_id}. Available: {list(GIFT_CATALOG.keys())}")

    total_amount = gift["price_usd"] * quantity
    cart_id = f"gift-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()

    return CartContents(
        id=cart_id,
        user_cart_confirmation_required=True,
        payment_request=PaymentRequest(
            details=PaymentDetails(
                id=f"pr-{uuid.uuid4().hex[:8]}",
                total=PaymentItem(
                    label=f"{gift['name']} × {quantity} → @{recipient}",
                    amount=PaymentCurrencyAmount(currency="USD", value=total_amount),
                ),
                display_items=[
                    PaymentItem(
                        label=f"{gift['name']} × {quantity}",
                        amount=PaymentCurrencyAmount(
                            currency="USD", value=total_amount
                        ),
                    ),
                ],
            ),
            method_data=[
                PaymentMethodData(
                    supported_methods="https://nusdpay.com/stablecoin/v1",
                    data=StablecoinMethodData(
                        supported_tokens=["USDT", "USDC"],
                        supported_chains=["tron", "bsc", "polygon"],
                        preferred_chain=preferred_chain,
                        settlement_currency="USD",
                    ),
                ),
            ],
        ),
        cart_expiry=expiry,
        merchant_name=MERCHANT_NAME,
    )


def _compute_cart_hash(cart: CartContents) -> str:
    """Compute SHA-256 hash of cart contents for JWT signing."""
    # Simplified: in production, use canonical JSON serialization
    cart_data = {
        "id": cart.id,
        "merchant_name": cart.merchant_name,
        "total_value": cart.payment_request.details.total.amount.value,
        "total_currency": cart.payment_request.details.total.amount.currency,
        "cart_expiry": cart.cart_expiry,
    }
    canonical = json.dumps(cart_data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def sign_cart_mandate(cart: CartContents) -> CartMandate:
    """Sign a CartContents to produce a CartMandate.

    In production, this would create a proper JWT with RSA/EC signing.
    For this demo, we use HMAC-SHA256 to illustrate the concept.

    Args:
        cart: The cart contents to sign.

    Returns:
        CartMandate with merchant_authorization set.
    """
    cart_hash = _compute_cart_hash(cart)

    # Simplified JWT-like structure (demo only)
    header = {"alg": "HS256", "kid": "merchant-key-001", "typ": "JWT"}
    payload = {
        "iss": MERCHANT_ID,
        "sub": MERCHANT_ID,
        "aud": "nusdpay-mpp",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int(
            (datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()
        ),
        "jti": cart.id,
        "cart_hash": cart_hash,
    }

    # In production: proper JWT signing with private key
    # Here: HMAC for demonstration
    sign_input = json.dumps(header) + "." + json.dumps(payload)
    signature = hmac.new(
        MOCK_SIGNING_KEY, sign_input.encode(), hashlib.sha256
    ).hexdigest()

    mock_jwt = f"header.{json.dumps(payload)}.{signature[:32]}"

    return CartMandate(
        contents=cart,
        merchant_authorization=mock_jwt,
    )
