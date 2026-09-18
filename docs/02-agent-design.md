# Agent design

How to build the thing that turns an address into a decision.

---

## What "done" looks like

```
you:    underwrite 123 Main St, Fort Worth TX, asking 139k

agent:  PASS — wholesale
        MAO $148,000 · Asking $139,000 · Spread $18,500
        Confidence: High (6 comps)

        Full report: reports/2026-09-17-123-main-st-fort-worth.md
```

Seconds, not an afternoon. One document, good enough to attach to an offer.

---

## The three jobs

### Job 1 — Collect

Fire every source **in parallel** for one address:

| Layer | Answers |
|---|---|
| Subject property | beds, baths, sq ft, lot, year, last sale, owner, taxes |
| Comparables | what similar houses actually sold for, recently, nearby |
| Rent | what it rents for |
| Distress | foreclosure stage, tax delinquency, liens, code violations, vacancy |
| Risk | flood zone, hazard ratings, soil, storm history |
| Costs | property tax rate, insurance, HOA |
| Market | jobs, income, renter share, days on market, price trend |
| Financing | current rental-loan and hard-money pricing |

**Every field carries its source and a retrieval timestamp.** A field with no
source is not a number — it is a guess, and it must be graded as one.

### Job 2 — Analyze

```
                  ┌─→ Wholesale ──→ MAO vs asking
   collected      ├─→ Flip ───────→ profit $ and %
   data ──────────┤
                  ├─→ BRRRR ──────→ cash left in, DSCR, cash flow
                  └─→ Land ───────→ $/acre vs comps
                              │
                              ▼
                       best exit wins
```

Run them all. Don't let the agent pick one strategy and stop — the whole point
is finding the exit the human wouldn't have thought to check.

### Job 3 — Decide

One line at the top: **pass or fail**, the winning exit, the deciding number,
and a confidence grade. The reasoning sits underneath for the times you want it.

---

## The report

`reports/YYYY-MM-DD-street-city.md`

| # | Section | Contents |
|---|---|---|
| 1 | **Verdict** | pass/fail · best exit · the one number · confidence |
| 2 | **Property** | address, specs, tax record, owner, distress status |
| 3 | **Comparables** | the comps table, adjustments shown, how ARV was reached |
| 4 | **Rehab** | tier, $/sq ft used, total, what drove it |
| 5 | **All exits** | full math, side by side |
| 6 | **Risk flags** | flood, hazard, liens, HOA, title |
| 7 | **Market** | jobs, income, renters, days on market, trend |
| 8 | **Sources** | every API, every field, pulled-at time |
| 9 | **Human checklist** | what the agent could not verify |

**Section 9 is the most important one early on.** It's the list you work
through to calibrate the system.

---

## Build order — earn the automation

Do not start at full automation. You will not trust it, and you will be right
not to.

### Phase 1 — Agent proposes, you review everything

The agent does the work. You check every deal. **Log every disagreement** in a
calibration file, with what it said, what you said, and why.

Those disagreements are the product. They tell you which thresholds are wrong.

**Exit test:** 20 consecutive deals where you agree with the verdict.

### Phase 2 — Agent decides, you spot-check

Automatic pass only at high confidence. Everything else routes to you.

**Exit test:** 50 deals with zero bad automatic passes.

### Phase 3 — Automated

```
daily → pull new auction / foreclosure / tax lists
      → underwrite every one
      → notify on passes only
      → write every report to disk
```

You only ever see the passes. But keep the reports for the fails — that archive
is how you prove your buy box is working, and it's what you show an investor.

---

## Interfaces

| Way in | What it looks like |
|---|---|
| Command line | `underwrite "123 Main St, Fort Worth TX" --asking 139000` |
| Bulk | paste 40 rows from a tax list, get back the 3 that pass |
| Scheduled | runs itself, posts passes to chat |

---

## What goes wrong, and the guard for each

| Risk | Guard |
|---|---|
| **Bad ARV → bad pass** | Minimum comp count. Confidence grade. Never auto-pass on low. |
| **Rehab wrong** | Show the verdict at ±$20k. If it only passes at the low number, it's not a pass. |
| **Stale data** | Timestamp every field. Flag anything over 30 days. |
| **API cost creep** | Hard spend cap at every provider. **Run the free checks first** and fail the deal out before any paid call fires. |
| **Confident and wrong** | Every number cites a source. No source means low confidence, not a silent guess. |
| **Terms violation** | Check each vendor's terms before you design around them. Some forbid storing their data or feeding it to a model. |

---

## Security

Standing rules for anything you build from this:

1. **Keys live in `.env`, never in code, never in a report, never in the repo.**
   Ship `.env.example` with empty values.
2. **Set a hard spend cap in every paid provider's own console** before the
   first call. Rate limiting in your code is not the last line of defense.
3. **Free checks run first.** Flood zone, tax status and market filters cost
   nothing and eliminate most candidates before you spend anything.
4. **Cache for 30 days.** The same address twice in a month should cost nothing
   the second time.
5. If you put a web form on it, validate input against a schema at the boundary
   and rate-limit **by IP** before any paid call.
