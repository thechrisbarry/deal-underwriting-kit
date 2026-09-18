# Sample report — a real underwrite, anonymized

> **Anonymized on purpose.** This is a real underwrite of a real auction
> property. The street address and all owner details have been changed, and
> **every identifying figure has been rounded**, so the parcel cannot be matched
> back to the source docket.
> The property was occupied by a family facing tax foreclosure, and publishing
> their name and address would be a harm with no upside. The *findings* are
> untouched — they are the point.

---

## VERDICT

# FAIL

**Confidence: 🔴 Low** — zero verifiable sold comparables.

| | |
|---|---|
| Best exit | None. Fails all three. |
| Primary reason | **Homestead tax sale.** Multi-year redemption period. Cannot be assigned, insured or financed. |
| Secondary reason | Zero sold comps — automatic fail on its own |

> **This deal looks like a 98% discount and is not one.**
> Assessed at about $188,000. Opening bid about $4,500.

---

## 1 · The property

| Field | Value |
|---|---|
| Location | Fort Worth, TX — Tarrant County |
| Year built | **early 1920s** — about 100 years old |
| Living area | ~1,200 sq ft |
| Lot | ~7,000 sq ft |
| Central air | **None** — a required capital item in this market |
| Assessed value | ~$188,000 *(roughly 78% improvement, 22% land)* |
| Occupancy | Owner-occupied |
| Disposition | County tax foreclosure |
| Sale notice | Flags land + improvement, **HOMESTEAD**, and sale subject to prior-year taxes |

---

## 2 · Why it fails

### Kill switch 1 — the word HOMESTEAD

Texas gives the former owner a right of redemption on a homestead — commonly
cited as **two years**. During that window:

- the position **cannot be assigned** — no marketable deed to wholesale
- **no title insurer** will write a policy
- **no lender** will finance or refinance a redeemable tax deed
- capital is **committed for two years** to learn whether you own anything

Statute compensates a redeemed purchaser with a penalty premium. That is a
*lending* return with a multi-year lockup, not an acquisition.

> **Not verified by counsel.** This reading comes from the auction notice's own
> HOMESTEAD designation plus standard Texas practice. Confirm the current rule
> with a Texas title attorney before bidding at any Texas tax sale.

### Kill switch 2 — no sold comparables

Texas is a non-disclosure state. County records never publish sale prices.
**Zero verifiable comps exist**, which fails the minimum-comparable rule
outright. Every valuation below is built on ZIP-level indices.

### Kill switch 3 — sold subject to prior-year taxes

The winning bid is not the cost. Unpaid taxes convey with the property.

### Kill switch 4 — no interior access

Tax auctions convey sight-unseen. A century-old house with no central air
could hide knob-and-tube wiring, cast iron drains, a failed foundation or
asbestos. **The rehab number below is an educated guess.**

---

## 3 · The math, for the record

Every figure is low confidence for the reasons above.

| Input | Value | Basis |
|---|---|---|
| Working ARV | $180,000 | ZIP typical ~$182,000, **falling ~2% YoY**; lower-third ~$156,000 |
| Rehab | $55,000 | heavy tier, $46/sq ft, regional factor +6% |
| Assignment fee | $15,000 | target |

```
MAO = (ARV × 0.70) − Rehab − Fee
    = ($180,000 × 0.70) − $55,000 − $15,000
    = $126,000 − $55,000 − $15,000
    = $56,000

Opening bid: ~$4,500
```

**The arithmetic clears. It is irrelevant** — a homestead tax deed cannot be
assigned, so the wholesale exit does not legally exist at any price.

Note also that an opening bid is a **floor, not a clearing price**. County tax
auctions are competitive.

| Exit | Test | Result | Finding |
|---|---|---|---|
| **Wholesale** | Price ≤ MAO | **FAIL** | Math clears at $56,000 MAO, but a redeemable homestead deed cannot be assigned. No legal exit. |
| **Fix & flip** | ≥ $40,000 and ≥ 15% | **FAIL** | $32,600 — about 26% on $125,000 in (bid $60,000 + back taxes $10,000 + rehab $55,000). Clears the percentage test but **misses the $40,000 floor**, before any foundation work. |
| **BRRRR** | DSCR ≥ 1.25 | **FAIL** | DSCR 0.41. Negative $577/month. |

### Rental detail

| Monthly | |
|---|---|
| Market rent *(ZIP median ~$1,600; subject below median)* | $1,400 |
| Property tax — **rebuilt at 2.09843%, no homestead exemption** | −$329 |
| Insurance — hail risk here is **Very High** | −$200 |
| Vacancy + maintenance + capital reserve (8% each) | −$336 |
| Property management (10%) | −$140 |
| **Net operating income** | **$395** |
| Debt service — $135,000 at 7.80% | −$972 |
| **Cash flow** | **−$577** |

Tax rate verified from the state comptroller's 2025 filing: city 0.670 + school
district 1.029 + county 0.186 + college 0.112 + emergency services 0.074 +
water district 0.027 = **2.09843 per $100**.

Loan rate = 30-year survey rate 6.95% + a 0.85% investor premium. **That spread
is a rough estimate, not a quote** — replace it with your own lender's pricing.

---

## 4 · Risk register

| Factor | Finding | Note |
|---|---|---|
| Flood zone | ✅ **Zone X — clear** | Outside the special flood hazard area. No mandatory flood insurance. |
| Composite hazard | ✅ Relatively Low | FEMA National Risk Index |
| **Hail** | 🔴 **Very High** | Top national band. Drives roof claims on a century-old structure. |
| Tornado | 🟠 Relatively High | |
| Neighborhood vulnerability | 🔴 Very High | Community resilience Relatively Low |
| ZIP value trend | 🟠 **−1.7% YoY** | Values declining, not appreciating |
| Title | 🔴 Redeemable | Uninsurable for the redemption period |
| Occupancy | 🔴 Owner in place | Possession requires eviction |

---

## 5 · Sources

Every figure retrieved from a primary source on the run date. **No paid vendor
was used.**

| Data | Source |
|---|---|
| Auction record, bid, notice text | Law-firm public sale docket (open JSON) |
| Parcel, structure, values | County appraisal district GIS |
| Geocoding, census tract | US Census Geocoder |
| Flood zone | FEMA National Flood Hazard Layer, layer 28 |
| Hazard, hail, tornado, vulnerability | FEMA National Risk Index |
| Property tax rates | State comptroller, 2025 rates & levies |
| Value and rent indices | Public research data, Aug 2026 |
| Mortgage rate | Freddie Mac PMMS |
| Rehab cost factor | Published regional construction index |

**Total spent: $0. Total time: about four minutes.**

---

## 6 · What a human still must check

1. **The redemption rule** — with a title attorney, before any tax-sale bid.
2. **Real sold comps** — everything here rests on ZIP averages.
3. **Condition** — nobody has been inside.
4. **Exact back-tax balance** conveyed with the property.
5. **A bound insurance quote** — "Very High" hail on a century-old roof may far exceed
   the $200/month modeled.

---

## What this demonstrates

| Worked | Didn't |
|---|---|
| ✅ Sourcing — free, live, thousands of records | ❌ **ARV. No sold comps exist in this state.** The binding constraint. |
| ✅ Property facts — free county GIS | ❌ **Rehab.** No data source. Needs your own numbers. |
| ✅ Flood, hazard, hail — free and instant | ❌ Condition. No data source will ever fix this. |
| ✅ Exact tax rate — free, from the state | |
| ✅ Current loan pricing — free | |

**The single highest-value upgrade is real sold comparables.** Everything else
already works for $0.

---

*Not legal, tax, investment or appraisal advice. Verify before bidding or closing.*
