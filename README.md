# Deal Underwriting Kit

**Paste an address. Get back pass or fail — and the reason.**

An open playbook and toolkit for underwriting residential real estate deals
(single family, 2–4 units, and land) using **free public data**.

No paid vendor. No API key. No signup. The two scripts in here run today
against live public endpoints — free government APIs plus one open law-firm
docket feed — for $0.

---

## Why this exists

Most investors lose the good deal while they are still building the
spreadsheet for it. And the deals that *do* get underwritten carry traps that
no spreadsheet catches — because **the seller's own paperwork is what misleads
you**:

- **Their tax bill is not your tax bill.** In Florida the assessment resets the
  January after you close. A real Cape Coral house we measured jumped **+71% on
  day one**. Indiana rentals pay roughly double what an owner-occupant paid.
- **Their flood premium is capped. Yours is not.** Old policies rise 18% a year,
  so long-time owners pay far under true cost. In one Fort Myers ZIP the real
  number is **7.2× the declaration page**.
- **A "98% discount" that legally cannot be bought.** A tax sale flagged
  `HOMESTEAD` in Texas carries a multi-year redemption period — no title
  insurance, no financing, no assignment.

This kit encodes those traps so a machine catches them every time.

---

## Quick start

```bash
git clone https://github.com/<you>/deal-underwriting-kit.git
cd deal-underwriting-kit

# 1. Find live distressed deals in Texas — free, no key
python3 scripts/find_tx_tax_sales.py --county "TARRANT COUNTY" \
    --min-value 100000 --max-value 400000 --exclude-homestead

# 2. Run the free public-data checks on any US address
python3 scripts/check_property.py "123 Main St, Fort Worth, TX"
```

Python 3.9+. **No dependencies** — standard library only.

### What `check_property.py` gives you

```
  123 MAIN ST, FORT WORTH, TX, 76115
  Tarrant County, TX  ·  tract 48439104702

  FLOOD       zone X  (AREA OF MINIMAL FLOOD HAZARD)
              flood insurance: no

  HAZARD      overall Relatively Low
              hail           Very High
              tornado        Relatively High
              vulnerability  Very High

  WALKABILITY 12.2 / 20

  RATES       as of 9/17/2026
              30-year fixed        6.95%
              investor / DSCR est. 7.8%
              hard money est.      9.45%

  FLAGS
     !  Hail risk is Very High — expect higher premiums and claims.
```

---

## The documentation is the real product

| Doc | What's in it |
|---|---|
| **[01-buy-box.md](docs/01-buy-box.md)** | The pass/fail rules. One file, one place to change a number. |
| **[02-agent-design.md](docs/02-agent-design.md)** | How to build the agent: collect → analyze → decide, and the three phases to trust it. |
| **[03-data-sources.md](docs/03-data-sources.md)** | **Every data source, checked against the vendor's own docs.** What's free, what costs, what's a dead end, and what the terms actually let you do. |
| **[04-deal-killers.md](docs/04-deal-killers.md)** | The traps. State by state. This is the one to read first. |

---

## How the system works

```
        address
           │
           ▼
   ┌───────────────┐
   │   COLLECT     │   free gov APIs + your paid comps source
   └───────┬───────┘
           ▼
   ┌───────────────┐
   │    MODEL      │   all exits at once, against YOUR buy box
   └───────┬───────┘
           │
   ┌───────┴───────┬──────────┬──────────┐
   ▼               ▼          ▼          ▼
Wholesale       Flip       BRRRR       Land
   │               │          │          │
   └───────┬───────┴──────────┴──────────┘
           ▼
   ┌───────────────┐
   │    DECIDE     │   pass / fail + confidence grade
   └───────────────┘
```

**The rule that matters most:** low confidence never produces an automatic
pass. Thin comparables or a guessed rehab number routes the file to a human.
An automated yes on bad data is worse than no answer at all.

---

## What's free vs. what you'll pay for

**Free, no key, works right now** — this covers most of the risk layer:

| Source | Gives you | Used by a script here? |
|---|---|---|
| US Census Geocoder | address → coordinates, county, tract | ✅ |
| FEMA National Flood Hazard Layer | flood zone, whether insurance is mandatory | ✅ |
| FEMA National Risk Index | 18 hazards incl. hail, tornado, hurricane | ✅ |
| EPA Walkability Index | walk score, transit access | ✅ |
| Freddie Mac PMMS | today's mortgage rates | ✅ |
| Texas tax-sale docket *(a law firm's open feed, not government)* | thousands of live distressed properties | ✅ |
| FEMA NFIP claims | **every flood claim ever paid near the property** | add it yourself |
| Florida county tax rolls | full owner + value data, some updated nightly | add it yourself |
| Texas Comptroller | exact property tax rates incl. MUD districts | add it yourself |

**The one thing you will have to pay for: sold comparables.** See
[03-data-sources.md](docs/03-data-sources.md) for the honest comparison.

> ### The non-disclosure problem
> **Indiana and Texas do not publish sale prices.** No cheap data service
> knows what a house actually sold for there. Every valuation in those states
> is an estimate wearing a suit. The only real fix is MLS access, which needs a
> licensed agent or broker to sponsor you — budget 2–6 weeks. Florida is a
> disclosure state and is fine.

---

## Honest limitations

This kit will not:

- **Value a property.** No sold comparables are included. That's the hard part and it costs money.
- **Estimate rehab.** There is no good rehab-cost API at any price. Use your own completed jobs.
- **Tell you the condition.** No dataset can see inside a house.
- **Give legal or tax advice.** The state-specific notes are research, not counsel.

Anyone who tells you their software solves all four is selling you something.

---

## Contributing

Corrections are especially welcome. If a source moved, a price changed, or a
state rule is wrong, **open an issue with the primary source** and it gets
fixed. Vendor endpoints and state statutes change without notice, and stale
documentation here is worse than none.

## License

MIT — see [LICENSE](LICENSE). Use it, sell what you build with it, no attribution required.

## Disclaimer

Educational material only. **Not** legal, tax, investment, appraisal or title
advice. Real estate rules vary by state, county and city, and they change.
Every figure here came from a public source on the date noted and has not been
independently audited. Verify everything with qualified professionals before
you bid, offer or close. You are responsible for your own decisions.
