# Deal killers

The traps that make a good-looking deal a bad one. Read this first.

Every figure here was pulled from a primary public source in September 2026.
**Rules change — verify before you rely on any of it.**

---

## 1. The seller's tax bill is not your tax bill

The single most common underwriting error. You copy the current owner's
property tax line into your model. **It resets after you buy.**

### Florida

Long-time owners sit behind an assessment cap. **You do not get it.**

| The same house | Taxable value |
|---|---|
| Seller, 20 years of cap protection | ~$336,000 |
| **You, the January after closing** | **~$573,000** |

That's **+71% on the tax base** with no change in the property. Measured on a
real Cape Coral parcel.

Two more Florida specifics:

- The 10% non-homestead cap **does not apply to school taxes** — usually the
  largest single line on the bill. Florida's own tax roll carries school and
  non-school assessed values as separate fields for exactly this reason.
- The homestead exemption disappears. Assessor records show roughly **$51,000**
  of exemption on homesteaded parcels and **$0** on non-homesteaded.
- Change of ownership includes **transferring more than 50% of the LLC** that
  owns it. You cannot dodge the reset with an entity sale.

### Indiana

Rentals pay roughly **double** an owner-occupant, because the homeowner
deductions vanish. From the state's own worked example on a $200,000 home:

| | Annual tax |
|---|---|
| Owner-occupied | **$714** |
| Same house, rented | **$1,418** |

Caps are 1% homestead / 2% other residential / 3% everything else, applied to
**gross** assessed value before deductions. A rental single-family is 2% — but
the cap is rarely what bites. **Losing the deductions is the whole story.**

> **Open item:** Indiana SEA 1 (2025) reportedly converts the homestead
> deduction to a credit from 2026. Confirm current law before modeling.

### Texas

Same trap. The 10% appraisal cap is **homestead only**. Buy a long-held family
home and the cap comes off — the first bill jumps to full market value.

Also: **MUD districts.** Municipal Utility Districts around Houston can add a
large amount that no commercial data vendor breaks out. They are published
free by the state comptroller in the special-district rate file.

Texas is non-disclosure, so the appraisal district never learns your purchase
price. The reset is to *their* opinion of market value, which can land either
side of what you paid.

**The rule:** rebuild the tax bill from current market value × the full local
rate, with every homeowner discount stripped out. Never inherit the seller's number.

---

## 2. Coastal flood insurance costs 2–7× what the seller pays

Older flood policies are capped at 18% annual increases. A long-time owner is
paying far below true cost. **A new buyer's policy converges on the full-risk
price.**

FEMA publishes the real numbers by ZIP code in a free spreadsheet:

| Place | Seller's current cost | **Full-risk cost** | Multiple |
|---|---|---|---|
| Fort Myers, FL 33901 | $798 | **$5,773** | **7.2×** |
| Naples, FL 34102 | $1,301 | **$8,480** | **6.5×** |
| Collier County, FL | $853 | $3,195 | 3.7× |
| Lee County, FL | $1,089 | $3,795 | 3.5× |
| Charlotte County, FL | $1,307 | $3,414 | 2.6× |
| Sarasota County, FL | $799 | $1,495 | 1.9× |
| Marion County, IN | $830 | $975 | 1.2× |

**Note the spread inside a single county.** Venice is $1,238; Fort Myers is
$5,773. A county-level flood assumption is useless in southwest Florida.

**Free and underused:** FEMA publishes every flood claim ever paid, with
location. One Cape Coral ZIP shows **2,773 claims — 2,237 of them in 2022**
from Hurricane Ian, median payout **$95,155**. Count paid claims within ~500m
over 20 years. **Repeat losses are a hard fail** regardless of price.

Zone codes that matter: `V`/`VE` is coastal high-hazard and the most expensive
there is. `AE` is the 1% annual chance zone. `X` is outside it.

---

## 3. Tax sales that legally cannot be bought

A tax auction can show a house assessed near $188,000 opening around **$4,500**.
That is not a 98% discount.

**Texas.** A sale notice carrying `HOMESTEAD` triggers a right of redemption —
commonly cited as **two years** for a residential homestead. During it:

- you **cannot assign** the position — there is no marketable deed to wholesale
- **no title insurer** will write a policy
- **no lender** will finance or refinance against a redeemable tax deed
- your capital is committed for two years to learn if you own anything

Statute compensates a redeemed purchaser with a penalty premium. That's a
*lending* return with a multi-year lockup — a different business than acquisition.

`SOLD SUBJECT TO … TAXES` on the notice means the winning bid is **not** your
cost. Unpaid taxes come with it.

And you cannot see inside. Tax auctions convey sight-unseen.

> **Always confirm redemption rules with a title attorney in that state before
> bidding.** One hour of counsel time protects every future auction.

---

## 4. The non-disclosure states

**Indiana and Texas do not publish sale prices.** County records never show
what a house sold for.

Every public-record data service — the cheap ones and the expensive ones —
either returns blank or an **estimate presented as a fact** in those states.
One major vendor says so plainly in its own documentation.

Since almost every deal formula starts with after-repair value, **a guessed
ARV produces a guessed decision.**

**Options, cheapest first:**

1. **Measure the gap.** Pull 10 addresses where you already know the real sale
   price. Compare. Costs nothing, takes an hour.
2. **Small gap** — use an estimate service with MLS relationships and mark
   every deal in those states as medium confidence. Never auto-approve.
3. **Big gap** — get MLS access. Needs a licensed agent or broker to sponsor
   you. $50–200/month and **2–6 weeks**. This is the only real fix, and it's
   the longest lead time in the whole build. Start it early.

Florida is a disclosure state. Real sold prices are public.

---

## 5. Foreclosure lead time varies wildly by state

| State type | Early warning | What you get |
|---|---|---|
| **Texas** (non-judicial) | The pre-default notice is **never publicly recorded.** Only the trustee's sale notice, ~**21 days** before auction. | Nobody can sell you long-lead Texas pre-foreclosure. Anyone claiming to is selling a list, not a lead. |
| **Indiana, Florida** (judicial) | Court filing lands **months** ahead. | Real lead time. Weight these markets for pre-foreclosure. |

---

## 6. Regional cost traps

| Market | Trap |
|---|---|
| **Dallas–Fort Worth** | **Expansive clay soil.** Foundation work is priced **per pier at $1,000–$3,000**, and a serious job is 20–40 piers — $20,000 to $120,000 **outside** any per-square-foot rehab estimate. Free USDA soil data flags it. |
| **Texas broadly** | **Hail.** Drives roof claims and insurance pricing. Free NOAA storm history lets you count events within N miles. |
| **Southwest Florida** | **Water and sewer run ~2× Texas.** Fixed charges alone are $50–75/month before a drop is used, and most utilities there do not cap summer sewer on a winter average — so every irrigation gallon is billed twice. |
| **Cape Coral, FL** | **Utility assessments of roughly $10,000–$36,000 per lot**, financed over decades and billed on the *property tax bill*, invisible on the utility bill. Make it a required diligence field. |
| **Southwest Florida condos** | Water, sewer and trash are usually inside the HOA fee. Adding a separate utility line **double-counts $150–190/month**. |
| **Houston** | **No zoning at all.** Land use runs on deed restrictions. Your agent must not fail a Houston deal for "zoning not found." |
| **Indiana** | Much of the state is in the EPA's highest radon zone. |

---

## 7. Florida condo law — a category of its own

Post-Surfside legislation reshaped the math on any Florida condo:

- **Milestone inspection** is required for buildings of **three habitable
  stories or more** at 30 years, then every 10.
- The old blanket 3-mile-coastal 25-year rule was **repealed** and replaced
  with local option — so the 25-year trigger is now a **per-jurisdiction
  variable**, not a statewide geographic rule.
- **The reserve waiver is gone.** Associations may no longer vote to fund no
  reserves or reduced reserves.
- One state-level review of early milestone filings reported that roughly
  **29% of buildings completing the first inspection phase showed substantial
  structural deterioration.** Reporting was incomplete — treat it as an order of
  magnitude, not a precise rate, and check the current figure yourself.
- **The estoppel certificate does not disclose milestone or reserve-study
  status** — it only shows assessments already levied. It is a lagging
  indicator. The forward-looking disclosure comes with the sale contract and
  carries a cancellation window; structure your underwriting to land inside it.
- Median HOA dues: **Naples–Marco Island $711/month** and **Cape Coral–Fort
  Myers $475/month**, versus a US median of $135.
- Federal loan-buyer reserve minimums are reported to rise in **early 2027**, which
  would mean a condo fully compliant with Florida law can still be non-warrantable.
  Verify the current threshold with a lender. That's an
  exit-liquidity problem — flag it separately.

Treat the three legal deferrals available to associations as **red flags, not
relief**. The cost is still there; it just isn't in this year's dues.

---

## 8. Data you are not allowed to keep

Some vendors forbid the thing you want to build. Check the terms before you
design around a source.

- One major property platform bans storing its data in your own database,
  bans feeding it to an AI model, and **monitors search volume** for that
  pattern. The stated remedy is account termination.
- One large data provider forbids caching beyond 24 hours and forbids using
  its data to build a database — which is incompatible with a standing lead list.
- **Every commercial foreclosure-auction site** bans automated access. One
  defines more than ten requests a minute from a single IP as a breach. Buying
  a third-party scraper does not cure this; it moves who pressed the button.

**Free government sources carry essentially none of this risk.** That is the
strongest argument for building on them first.

---

## 9. Outreach law

A phone number you bought is **not permission to call it.** Vendors disclaim
this explicitly and place the entire compliance burden on you.

- Scrub against the national and state do-not-call lists **before** dialing.
- Keep your own suppression list and honor opt-outs.
- **Direct mail carries none of this exposure.** For cold outreach, mail first.
- Marketing-sourced skip-trace data is **not** credit-bureau data. Never use it
  to screen a tenant or make a credit decision.

---

*Nothing here is legal advice. Verify with qualified professionals in the
relevant state before acting.*
