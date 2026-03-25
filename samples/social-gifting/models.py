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

"""AP2 data models adapted for stablecoin social entertainment payments.

Based on the AP2 protocol types:
- https://github.com/google-agentic-commerce/AP2/blob/main/src/ap2/types/mandate.py
- https://github.com/google-agentic-commerce/AP2/blob/main/src/ap2/types/payment_request.py
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


# --- W3C Payment Request objects (AP2-compatible) ---


@dataclass
class PaymentCurrencyAmount:
    """Monetary amount with currency code (W3C Payment Request API)."""

    currency: str  # ISO 4217 code (e.g., "USD")
    value: float


@dataclass
class PaymentItem:
    """An item for purchase (W3C Payment Request API)."""

    label: str
    amount: PaymentCurrencyAmount
    pending: bool = False
    refund_period: int = 0  # Social payments are typically non-refundable


@dataclass
class StablecoinMethodData:
    """Stablecoin-specific payment method data.

    Extension to W3C PaymentMethodData for stablecoin payments.
    Method identifier: https://nusdpay.com/stablecoin/v1
    """

    supported_tokens: list[str] = field(
        default_factory=lambda: ["USDT", "USDC"]
    )
    supported_chains: list[str] = field(
        default_factory=lambda: ["ethereum", "tron", "bsc", "polygon", "solana", "arbitrum"]
    )
    preferred_chain: str = "tron"
    settlement_currency: str = "USD"
    max_slippage_bps: int = 50  # 0.5% max slippage


@dataclass
class PaymentMethodData:
    """Payment method with associated data (W3C Payment Request API)."""

    supported_methods: str = "https://nusdpay.com/stablecoin/v1"
    data: Optional[StablecoinMethodData] = None

    def __post_init__(self):
        if self.data is None:
            self.data = StablecoinMethodData()


@dataclass
class PaymentDetails:
    """Payment details including total and line items."""

    id: str
    total: PaymentItem
    display_items: list[PaymentItem] = field(default_factory=list)


@dataclass
class PaymentRequest:
    """W3C PaymentRequest adapted for AP2."""

    details: PaymentDetails
    method_data: list[PaymentMethodData] = field(default_factory=list)

    def __post_init__(self):
        if not self.method_data:
            self.method_data = [PaymentMethodData()]


# --- AP2 Mandate types ---


@dataclass
class CartContents:
    """The detailed contents of a cart, signed by the merchant.

    Maps to ap2.types.mandate.CartContents.
    """

    id: str
    user_cart_confirmation_required: bool = True
    payment_request: PaymentRequest = None
    cart_expiry: str = ""
    merchant_name: str = ""


@dataclass
class CartMandate:
    """A cart whose contents have been digitally signed by the merchant.

    Maps to ap2.types.mandate.CartMandate.
    """

    contents: CartContents = None
    merchant_authorization: Optional[str] = None  # JWT in production


@dataclass
class StablecoinPaymentDetails:
    """Stablecoin-specific payment response details.

    Extension for stablecoin settlement information in PaymentResponse.
    """

    token: str = "USDT"
    chain: str = "tron"
    sender_address: str = ""
    recipient_address: str = ""
    amount: str = "0.00"
    tx_hash: str = ""
    block_number: int = 0
    confirmations_required: int = 19
    confirmations_current: int = 0
    finality_status: str = "pending"  # pending | confirming | confirmed
    settlement_time_ms: int = 0


@dataclass
class PaymentResponse:
    """Payment response containing method and details."""

    method_name: str = "https://nusdpay.com/stablecoin/v1"
    details: Optional[StablecoinPaymentDetails] = None

    def __post_init__(self):
        if self.details is None:
            self.details = StablecoinPaymentDetails()


@dataclass
class PaymentMandateContents:
    """The data contents of a PaymentMandate.

    Maps to ap2.types.mandate.PaymentMandateContents.
    """

    payment_mandate_id: str = ""
    payment_details_id: str = ""
    payment_details_total: Optional[PaymentItem] = None
    payment_response: Optional[PaymentResponse] = None
    merchant_agent: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class PaymentMandate:
    """Contains the user's instructions & authorization for payment.

    Maps to ap2.types.mandate.PaymentMandate.
    """

    payment_mandate_contents: Optional[PaymentMandateContents] = None
    user_authorization: Optional[str] = None  # Verifiable Presentation
