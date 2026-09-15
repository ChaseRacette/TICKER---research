# Lab 07 — Comparable-Company Policy and Implied Range

## DCF reopening and pre-AI explanation

My Week 3 MSFT DCF range is driven most by the FCFF-growth path, AI-infrastructure capex normalization, WACC, terminal growth, and the cash/debt bridge. I cannot yet fully explain how to decide when a peer's different business mix requires a qualification rather than exclusion, or how differences in EPS quality affect a P/E comparison.

**Specific question to investigate:** When two vehicle retailers both sell franchised vehicles and earn service/parts income, what business-mix differences are material enough to qualify rather than use a peer's P/E multiple?

## P/E concepts

P/E is price per share divided by diluted earnings per share (EPS). Price per share is the market value of one common share; diluted EPS is the profit attributable to common shareholders divided by diluted shares. The multiple expresses what investors pay for one dollar of earnings.

Using P/E lets companies of different sizes be compared on a per-dollar-of-earnings basis. It complements a DCF by providing a market-based reference point, while a DCF values the company's own forecast cash flows.

P/E is most useful when companies have positive, reasonably comparable earnings, accounting policies, capital structures, business mixes, growth prospects, and risk. It can mislead when earnings are negative, contain unusual gains or losses, or differ in growth, margins, leverage, or cyclicality. A lower P/E is not automatically better: it may reflect slower expected growth, higher risk, lower-quality earnings, or a weaker business.

## Peer policy before the result

| Candidate | Decision | Business rationale |
| --- | --- | --- |
| AutoNation (AN) | Use | Its core business is franchised vehicle retail, supported by service and parts, which aligns closely with Asbury's recurring operating model. |
| Group 1 Automotive (GPI) | Qualify and use | It also operates franchised dealerships and service/parts operations, but its broader geographic and business mix can affect growth, risk, and the appropriate multiple. Its P/E is useful evidence, not a mechanically identical benchmark. |
| Asbury (ABG) | Exclude from peer set | ABG is the target; including it would contaminate the comparison. |

Franchised vehicle retail and service/parts matter more than a broad industry label because they determine the revenue mix, recurring earnings, inventory economics, and cyclicality that investors are pricing.

## Frozen case inputs and manual check

These are retrospective training inputs supplied in Lab 07: December 31, 2024 closing prices paired with subsequently reported FY2024 total GAAP diluted EPS.

| Company | Role | Price | FY2024 GAAP diluted EPS |
| --- | --- | ---: | ---: |
| Asbury Automotive (ABG) | Target | $243.03 | $21.50 |
| AutoNation (AN) | Peer | $169.84 | $16.92 |
| Group 1 Automotive (GPI) | Qualified peer | $421.48 | $36.81 |

Manual check: AN P/E = $169.84 / $16.92 = **10.037825x**. Applying that to ABG EPS gives $21.50 × 10.037825 = **$215.81**.

## Calculator and validation

Run from the repository root:

```powershell
python models\asbury_pe_comps.py
```

| Check | Result |
| --- | ---: |
| AutoNation P/E | 10.037825x |
| Group 1 P/E | 11.450149x |
| Peer median P/E | 10.743987x |
| ABG peer-implied range | $215.81–$246.18 |
| ABG at peer median | $231.00 |
| Remove GPI: remaining AN estimate | $215.81 |
| Change from full-peer median estimate | −$15.18 |

The calculator uses full precision for calculations, displays P/E to six decimals and prices to cents, excludes the target, deduplicates peers, labels nonpositive or missing inputs as not meaningful, and does not bridge P/E with cash or debt.

## Changed-peer interpretation

Before reading the result, I predict that removing GPI will lower the implied price because GPI has the higher P/E. The result confirms this: removing GPI leaves AN's 10.037825x multiple and lowers the implied ABG reference estimate to $215.81, $15.18 below the two-peer median estimate. With one valid peer, the result is a reference estimate rather than a range because there is no remaining distribution of peer multiples.

## Reflection and conditional conclusion

The comparison does not prove that ABG is fairly valued. It is one market-based perspective that depends on a defensible peer policy and comparable, sustainable earnings. The MSFT DCF remains a separate cash-flow valuation with different drivers and assumptions.

> Disclaimer: I have no licensure in any field of finance. This material is for educational purposes only and is not financial advice.
