# The buy box

**Your pass/fail rules live here and nowhere else.** The agent reads this file.
Change a number here and the system changes with it.

Everything below is a **starting template**. The numbers are common industry
defaults, not a recommendation. Replace them with yours.

---

## 1. What you buy

| Type | In the box? |
|---|---|
| Single-family house | ☐ |
| Small multifamily, 2–4 units | ☐ |
| Land / lots | ☐ |
| 5+ unit apartments | ☐ — different model, different financing |

## 2. Markets

List exact metros or counties, not whole states. The agent should treat
anything outside the list as an automatic fail, and flag low confidence in any
market where you have not validated comp quality.

> **Before adding a market, answer one question:** is it a disclosure state?
> If not, your after-repair value is an estimate until you have MLS access.
> See [04-deal-killers.md](04-deal-killers.md) §4.

## 3. The exit ladder

Test **every exit on every deal**, in your preferred order, and report the best
one. If it fails all of them, it's a fail. If it passes one, name which and why.

A common order for a wholesaler:

| Order | Exit | Why there |
|---|---|---|
| 1 | **Wholesale** | Fastest, no rehab risk, no lender |
| 2 | **Fix and flip** | When the spread is too large to assign away |
| 3 | **BRRRR** | When it cash-flows and the refinance returns your capital |

## 4. The math

### Wholesale

```
MAO = (ARV × 0.70) − Rehab − Assignment Fee

PASS if:  Asking Price ≤ MAO
```

The 0.70 is the conventional rule because most cash buyers accept it. Tighten
it in a soft market, loosen it only if you know your buyer list will take it.

| Input | Where it comes from |
|---|---|
| **ARV** | Sold comps: same or adjacent ZIP, ±20% square feet, same bed count, sold within 6 months. **Minimum 3 comps.** |
| **Rehab** | $/sq ft by condition tier × square feet, adjusted by a regional cost factor |
| **Assignment fee** | Your target. `$______` |

### Fix and flip

```
Profit = ARV − Purchase − Rehab − Holding − Selling Costs

PASS if:  Profit ≥ $______   AND   Profit ÷ (Purchase + Rehab) ≥ ____%
```

| Input | Common default |
|---|---|
| Holding | 6 months × (loan interest + taxes + insurance + utilities) |
| Selling costs | 8% of ARV (commission, title, concessions) |
| Hard money | ~12% interest, 2 points, 90% of purchase, 100% of rehab |

### BRRRR

```
Cash Left In = (Purchase + Rehab + Closing) − (ARV × 0.75)

PASS if:  Cash Left In ≤ $0
    AND:  DSCR ≥ 1.25
    AND:  Cash flow ≥ $____ per unit per month
```

75% is the standard cash-out limit on a rental loan. Confirm your lender's.

**Expenses that must be subtracted — no skipping:**

property tax *(rebuilt post-sale, see below)* · insurance *(at true cost, not
the seller's)* · vacancy · maintenance · capital reserve · property management
· HOA · any utility the landlord pays

Common reserve defaults are 8% each for vacancy, maintenance and capital, and
8–12% for management. But note what the large single-family rental operators
disclose in their public annual filings: roughly **$5,700 per home per year** in
repairs and turnover and **$1,200–2,000** in recurring capital on a 2,000 sq ft, 18-year-old house —
and they get scale pricing and in-house crews. **Underwrite above their
numbers, not at them.**

> The popular "$1 per square foot per year" rule is calibrated to **recurring
> capital only**, not total maintenance. Real repairs and turnover run roughly
> three times that. The "1% rule" has no traceable origin or supporting data —
> use it to screen, never to underwrite.

### Land

```
PASS if:  Price ≤ ____% of market $ per acre for comparable parcels
```

Plus all of these must be true, or it fails regardless of price:

- legal access to a public road
- utilities at the lot line, or a priced plan to get them
- not in a flood zone that blocks building
- zoning permits the intended use
- perc test passed, or sewer tap available

## 5. Rehab cost tiers

| Tier | Scope | $/sq ft |
|---|---|---|
| Light | Paint, floor coverings, clean, minor repairs | `____` |
| Medium | Kitchen, baths, flooring, paint, some mechanicals | `____` |
| Heavy | Full gut, roof, HVAC, electrical, plumbing | `____` |
| Teardown | Structure has no value | land math only |

Then multiply by a **regional cost factor** — construction costs vary 10–20%
between metros for identical work.

> **This is the weakest number in any underwrite, and there is no good rehab
> cost API at any price.** Build this table from your own completed jobs.
> Until you have, every report must show what a **±$20,000 swing** does to the
> verdict. If a deal only passes at the low estimate, that is not a pass.
>
> And remember the line items that are **not** $/sq ft: foundation work is
> priced per pier, roofs per square, septic and well as their own jobs.

## 6. Automatic fail — the kill switches

Fail the deal on any of these without finishing the math:

- Fewer than 3 usable sold comps → **fail, low confidence.** Never guess an ARV.
- Repeat federal flood claims at or near the parcel
- Coastal high-hazard flood zone where the true premium erases the profit
- Open lien, permit or code violation exceeding the spread
- Square footage or bed/bath disagreeing across sources by more than 15% → send to a human
- Clouded title, or a tax-sale redemption period that blocks your exit
- HOA with a rental cap or a pending special assessment
- Mobile or manufactured home on leased land
- Owner deceased with no probate filed

## 7. Confidence grade

Every report carries one, because **an automated pass on bad data is worse
than no answer.**

| Grade | Means |
|---|---|
| 🟢 High | 5+ close comps, paid data, sources agree |
| 🟡 Medium | 3–4 comps, or one input estimated |
| 🔴 Low | Under 3 comps, sources disagree, or rehab is a guess |

**🔴 Low never gets an automatic pass.** It gets "pass, pending human review."
