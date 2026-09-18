# Data sources

Where every number comes from, what it costs, and what the terms let you do.

Checked against each provider's own documentation in **September 2026**.
Endpoints and pricing change without notice — **verify before you build.**

---

## Start here: the free tier

These need no key or an instant free one, no sales call, and no contract.
Together they cover most of the risk layer for any US address.

| # | Source | Gives you | Key? |
|---|---|---|---|
| 1 | **US Census Geocoder** | address → coordinates, county, tract. The spine everything else hangs off. | none |
| 2 | **FEMA National Flood Hazard Layer** | flood zone, whether insurance is mandatory | none |
| 3 | **FEMA National Risk Index** | 18 hazards, composite rating, expected annual loss | none |
| 4 | **FEMA NFIP claims** | every flood claim ever paid, with location | none |
| 5 | **Census American Community Survey** | income, renter share, values, rents, vacancy | free, instant |
| 6 | **Bureau of Labor Statistics** | county unemployment, wages, job counts | free, instant |
| 7 | **EPA Walkability Index** | walk index, transit proximity, car ownership | none |
| 8 | **Freddie Mac PMMS** | this week's mortgage rates | none |

`scripts/check_property.py` in this repo calls 1, 2, 3, 7 and 8.

### Endpoints worth knowing

**Flood zone** — the highest-value single call in the stack. Layer 28:

```
https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query
  ?geometry=<lon>,<lat>&geometryType=esriGeometryPoint&inSR=4326
  &spatialRel=esriSpatialRelIntersects
  &outFields=FLD_ZONE,ZONE_SUBTY,STATIC_BFE,SFHA_TF
  &returnGeometry=false&f=json
```

`SFHA_TF = "T"` means flood insurance is federally required with a mortgage.
**`STATIC_BFE = -9999` means no base flood elevation published, not elevation
zero** — a classic parsing bug.

**Flood claims paid** — use the v3 path; the older v2 one is being retired:

```
https://www.fema.gov/api/open/v3/NfipClaims
https://www.fema.gov/api/open/v3/NfipPolicies
```

**Full-risk flood premium by ZIP** — a static spreadsheet worth caching once.
This is the number that decides coastal deals:

```
https://www.fema.gov/sites/default/files/documents/fema_risk-rating_exhibits-2-3-4.xlsx
```

**Mortgage rates**, no key:

```
https://www.freddiemac.com/pmms/docs/PMMS_history.csv
https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US
```

### Things that changed recently — older tutorials are wrong

1. **The Census API now requires a key.** A keyless call returns an HTML
   "Missing Key" page, not an error, so a naive client parses HTML as data and
   fails silently. The key is free and instant.
2. FEMA's older risk-index endpoint moved. Use the hosted feature service.
3. The FBI's older crime API base is dead. The live base is `cde.ucr.cjis.gov`.
4. Google Maps replaced its monthly credit with per-product free call caps.
5. The Bureau of Labor Statistics unregistered limit is ~25 queries/day and is
   shared by IP. Register for a free key.

---

## Deal sourcing

### Texas — solved, free

One of the largest Texas delinquent-tax law firms publishes its sale docket as
open JSON. **Note this is a private firm's feed, not a government one:**

```
https://taxsales.lgbs.com/api/property_sales/?state=TX&limit=500
```

Thousands of live records with address, county, cause number, sale date,
appraised value, minimum bid and sale notes. No key, no auth. Filter by
`&county=HARRIS+COUNTY`. There is no date filter, so pull the set and diff it
against yesterday's.

`scripts/find_tx_tax_sales.py` does exactly this.

**Check their terms of use and robots.txt before automating against it, and keep
your pull rate low.** It does not cover every Texas county. For the rest, check Perdue Brandon,
McCreary Veselka, or the county tax assessor-collector.

### Florida — free county rolls

Several southwest Florida property appraisers publish full tax rolls as free
downloads, some updated nightly. They include **owner names and mailing
addresses**, which means you can derive absentee-owner and high-equity lists
yourself rather than paying for a "quicklist":

- absentee = mailing address ≠ situs address
- equity proxy = assessed value vs. last sale price

Florida also publishes a **statewide parcel layer** built from what all 67
counties file, and a **statewide cadastral** carrying school and non-school
assessed values separately — which is exactly what you need for the tax-reset
math in [04-deal-killers.md](04-deal-killers.md).

### Indiana — free statewide parcels

Indiana publishes a **statewide parcel layer** and, in at least one major
metro, free zoning and a very large code-violation dataset. Of the three
markets studied, Indiana had the best free parcel coverage.

Indiana **is** a disclosure state for sales-disclosure filings, but the data is
not exposed as a clean API — plan on scheduled file ingest.

### Auction platforms — none of them work

Every commercial foreclosure-auction site checked offers **no API, no export,
no data feed**, and each bans automated access in its terms, blocks bots at
the network, or both. One defines more than ten requests per minute from a
single IP as a breach.

Buying a third-party scraper for these does not cure the terms problem.

**Clean exceptions:** federal seizure listings publish email alerts and plain
HTML. And **government-sponsored REO already flows into the MLS** — so if you
solve the comps problem with MLS access, you get those listings free as a side
effect. Two problems, one fix.

### The discovery trick that scales

```
https://www.arcgis.com/sharing/rest/search?q=<county> parcels type:"Feature Service"&f=json
```

Free, no key. When you hit a county you haven't mapped, search for its map
service at runtime and cache the endpoint. That turns "onboard 3,000 counties"
into something that onboards itself.

---

## The paid layer

**The one thing you will have to pay for is sold comparables.** Everything else
has a free substitute good enough to start.

### What to look for in a comps provider

| Question | Why it matters |
|---|---|
| Does it return the **individual comparables**, or only a score? | If you can't see the comps, you can't show your work or overrule a bad selection. |
| Can you sign up **self-serve**, or is it a sales call? | Sales-gated pricing is negotiated, opaque, and slow. |
| Is there a **free tier** to test with? | Test 10 addresses where you know the answer before paying anyone. |
| **Non-disclosure state coverage?** | Most public-record vendors return blank or an estimate in IN and TX. |
| What do the **terms** allow? | See below. |

Prices observed in September 2026 ranged from a genuinely free tier (tens of
calls a month) through roughly $75–450/month for self-serve tiers, up to
four-figure monthly minimums for sales-gated enterprise data. Several
well-known names offer **no public API at all**.

### Terms clauses that break an underwriting system

Read these before you design around a vendor. Observed in real published terms:

- **No caching beyond 24 hours**, and no using the data to build a database.
  That is incompatible with a standing lead list.
- **No storing the data in your own database**, no feeding it to a large
  language model, and **search-volume monitoring** with account termination as
  the stated remedy.
- **No using the data as input to generative AI.** If your plan is to have a
  model reason over comps, that clause is a direct conflict.
- **Bulk extraction caps** as a percentage of the database per pull.

None of this is unusual or unreasonable from the vendor's side. It just means
**check the terms first**, because the architecture you can build depends on them.

### The MLS route

For non-disclosure states this is the only real fix. Several resellers offer
RESO-standard APIs from roughly $50–400/month, but **all of them require MLS
approval, which in practice means a licensed agent or broker signs for you.**
Budget **2–6 weeks**. No credit card gets you past it.

Start this conversation early — it is the longest lead time in the whole build.

---

## Things with no data source at any price

Be honest about these rather than faking them.

| Gap | Reality |
|---|---|
| **Rehab cost** | No self-serve API exists. The industry-standard cost books are subscriptions without APIs. One publisher has a real REST API but it is licensed, not self-serve. **Build the table from your own jobs.** |
| **Water and sewer rates** | No API anywhere. Municipal rate schedules are PDFs. Hand-build a per-utility table. |
| **HOA fees** | Not in assessor records, so no public-record product has it. It comes from the MLS side or from a human reading an estoppel document. |
| **Property management fee norms** | No dataset, no survey with published methodology. Scrape or call. |
| **Street-level crime** | Only exists where a city publishes it. Several large metros publish nothing. **Say "unknown" rather than inventing a number.** |
| **Assigned elementary school** | District boundaries are free and current. The only free national *attendance zone* map is about a decade stale. |
| **Interior condition** | No dataset will ever solve this. |

---

## Cost summary

| Setup | Monthly | What you get |
|---|---|---|
| **Free** | **$0** | Everything in this repo. Risk layer, deal sourcing in covered states, rates. |
| **+ comps** | ~$20–200 | A real valuation input. The first thing worth paying for. |
| **+ MLS** | ~$50–400 | True sold prices in non-disclosure states. Needs a licensed sponsor. |

---

## Rules for connecting anything

1. **Keys in `.env`.** Never in a note, a report, or the repo.
2. **Hard spend cap in each provider's console** before the first call.
3. **Free checks run first**, so most candidates fail out before you spend.
4. **Cache 30 days.**
5. **Every number carries its source and timestamp.** No source means low
   confidence, not a silent guess.
