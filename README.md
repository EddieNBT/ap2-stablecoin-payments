# AP2 Stablecoin Payments — Social Entertainment Use Cases
> Exploring the [Agent Payments Protocol (AP2)](https://ap2-protocol.org/) for stablecoin-based payments in social entertainment scenarios.
## About
This repository documents our ongoing work integrating AP2 with stablecoin payment infrastructure for cross-border social entertainment use cases — including **creator tipping**, **digital gifting**, and **subscription payments**.
**Organization:** [Newborn Town](https://www.newborntown.com/) (HKEX: 9911.HK)
**Product:** [NUSD Pay](https://nusdpay.com/) — Enterprise stablecoin payment infrastructure
**Markets:** MENA · Southeast Asia · Global
## Why Social Entertainment × AP2?
Social entertainment platforms process millions of micro-transactions daily — tips for live streamers, virtual gifts between users, creator subscriptions. These payments are:
- **High frequency, low value** — averaging $0.50–$50 per transaction
- **Cross-border by default** — users and creators span different countries and currencies
- **Increasingly agent-mediated** — AI agents recommend gifts, auto-subscribe to creators, manage spending budgets
AP2's mandate-based architecture provides the trust and accountability framework these agentic payment flows need, while stablecoins (USDT/USDC) solve the cross-border settlement challenge.
## Repository Contents
### 📄 Documentation
| Document | Description |
|----------|-------------|
| [Use Case: Social Payments](docs/use-case-social-payments.md) | Three AP2 scenarios for social entertainment payments |
| [Mandate Field Mapping](docs/mandate-mapping.md) | How NUSD Pay objects map to AP2 mandates |
| [Stablecoin Gap Analysis](docs/stablecoin-gap-analysis.md) | Where stablecoin push payments meet and diverge from current AP2 spec |
| [AP2 × x402 Integration Notes](docs/x402-integration-notes.md) | How AP2 and x402 complement each other for stablecoin settlement |
### 💻 Sample Code
| Sample | Description |
|--------|-------------|
| [Social Gifting Flow](samples/social-gifting/) | Minimal AP2 Human Present flow for a digital gifting scenario |
## Our AP2 Context
| Metric | Value |
|--------|-------|
| Payment volume | Significant daily transaction volume |
| Supported stablecoins | USDT, USDC, NUSD |
| Supported chains | Multi-chain support |
| Compliance | Full compliance stack |
| AP2 Interest Form | ✅ Submitted |
| AP2 Discussion | [#193](https://github.com/google-agentic-commerce/AP2/discussions/193) |
## Current Status
🟡 **Active exploration** — We are mapping AP2 mandates to our existing payment flows and building sample implementations. Contributions and feedback are welcome.
### Roadmap
- [x] AP2 protocol research and core concepts analysis
- [x] Use case documentation (tipping, gifting, subscriptions)
- [x] Mandate field mapping (NUSD Pay ↔ AP2)
- [x] Stablecoin gap analysis
- [x] Sample: Human Present gifting flow
- [x] Contributed stablecoin payments documentation to AP2 official repo ([#196](https://github.com/google-agentic-commerce/AP2/pull/196))
- [ ] x402 Facilitator integration
- [ ] Human Not Present flow (pending AP2 v1.x)
- [ ] Production deployment
## Related
- [AP2 Protocol](https://github.com/google-agentic-commerce/AP2) — Agent Payments Protocol
- [AP2 Documentation](https://ap2-protocol.org/) — Official protocol docs
- [a2a-x402](https://github.com/google-agentic-commerce/a2a-x402) — A2A + x402 implementation
- [x402 Protocol](https://www.x402.org/) — HTTP 402 payment standard
## License
Apache License 2.0 — see [LICENSE](LICENSE).
