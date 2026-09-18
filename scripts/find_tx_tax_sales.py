#!/usr/bin/env python3
"""
find_tx_tax_sales.py — pull live Texas tax-foreclosure properties. Free, no key.

One of the largest delinquent-tax law firms in Texas publishes its sale docket
as an open JSON feed. Thousands of properties, with address, sale date,
appraised value and minimum bid. No signup, no key.

BE A GOOD CITIZEN: this is a PRIVATE FIRM'S feed, not a government one. Read
their terms of use and robots.txt before automating against it, keep your pull
rate low, and cache results. This script sleeps between pages for that reason.

    python3 find_tx_tax_sales.py --county "TARRANT COUNTY" --min-value 100000
    python3 find_tx_tax_sales.py --scheduled-only --limit 25
    python3 find_tx_tax_sales.py --csv out.csv

Coverage note: this firm does not serve every Texas county. Counties it does
not cover will simply be absent. For those, check Perdue Brandon or McCreary
Veselka, or the county tax assessor-collector directly.

READ THIS BEFORE YOU BID
------------------------
A "HOMESTEAD" note on a sale is a hard stop for most strategies. Texas gives
the former owner a right of redemption on a homestead — commonly cited as two
years — during which you cannot get title insurance, cannot finance it, and
cannot assign it. The script flags these for you. It is not legal advice:
confirm the current rule with a Texas title attorney before bidding.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://taxsales.lgbs.com/api/property_sales/"
PAGE = 500
UA = {"User-Agent": "deal-underwriting-kit/1.0", "Accept": "application/json"}


PAGE_DELAY_SECONDS = 1.0  # be polite; this is someone else's server


def fetch_all(state: str = "TX", max_records: int = 6000) -> list[dict]:
    rows, offset = [], 0
    while offset < max_records:
        if offset:
            time.sleep(PAGE_DELAY_SECONDS)
        q = urllib.parse.urlencode({"state": state, "limit": PAGE, "offset": offset})
        req = urllib.request.Request(f"{API}?{q}", headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.loads(r.read().decode())
        except Exception as e:
            print(f"  ! request failed at offset {offset}: {e}", file=sys.stderr)
            break

        batch = d.get("results") or []
        rows.extend(batch)
        total = d.get("count") or 0
        offset += PAGE
        if offset >= total or not batch:
            break
    return rows


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def clean(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        val, bid = fnum(r.get("value")), fnum(r.get("minimum_bid"))
        notes = (r.get("sale_notes") or "").upper()
        out.append({
            "address": (r.get("prop_address_one") or "").strip(),
            "city": (r.get("prop_city") or "").strip(),
            "zip": (r.get("prop_zipcode") or "").strip(),
            "county": (r.get("county") or "").strip(),
            "account": r.get("account_nbr"),
            "cause": r.get("cause_nbr"),
            "sale_date": r.get("sale_date_only"),
            "sale_type": r.get("sale_type"),
            "status": r.get("status"),
            "appraised_value": val,
            "minimum_bid": bid,
            "bid_to_value": round(bid / val, 4) if (val and bid) else None,
            # The two flags that change what you are actually buying:
            "homestead": "HOMESTEAD" in notes,
            "subject_to_taxes": "SUBJECT TO" in notes,
            "notes": r.get("sale_notes") or "",
        })
    return out


def apply_filters(rows, a) -> list[dict]:
    out = []
    for r in rows:
        if a.county and a.county.upper() not in r["county"].upper():
            continue
        if a.city and a.city.upper() not in r["city"].upper():
            continue
        if a.require_address and not (r["address"] and r["city"]):
            continue
        if a.min_value and (r["appraised_value"] or 0) < a.min_value:
            continue
        if a.max_value and (r["appraised_value"] or 0) > a.max_value:
            continue
        if a.scheduled_only and r["sale_type"] != "SALE":
            continue
        if a.exclude_homestead and r["homestead"]:
            continue
        out.append(r)
    out.sort(key=lambda r: (r["bid_to_value"] is None, r["bid_to_value"] or 9e9))
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Live Texas tax-foreclosure properties. Free.")
    p.add_argument("--county", help='e.g. "TARRANT COUNTY"')
    p.add_argument("--city", help='e.g. "FORT WORTH"')
    p.add_argument("--min-value", type=float, default=0)
    p.add_argument("--max-value", type=float, default=0)
    p.add_argument("--scheduled-only", action="store_true",
                   help="only sales with a set auction date")
    p.add_argument("--allow-missing-address", action="store_false",
                   dest="require_address",
                   help="keep rows with no street address (off by default)")
    p.add_argument("--exclude-homestead", action="store_true",
                   help="hide homestead sales (2-year redemption — usually unbuyable)")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--csv", help="also write results to this CSV path")
    p.add_argument("--force", action="store_true", help="allow overwriting --csv")
    a = p.parse_args()

    print("  fetching Texas tax-sale docket …", file=sys.stderr)
    rows = clean(fetch_all())
    print(f"  {len(rows)} records retrieved", file=sys.stderr)

    hits = apply_filters(rows, a)
    print(f"  {len(hits)} after filters\n", file=sys.stderr)

    show = hits[: a.limit]
    print(f"  {'ADDRESS':<30} {'CITY':<14} {'VALUE':>10} {'MIN BID':>10} {'%':>5}  {'SALE DATE':<11} FLAGS")
    print(f"  {'-'*30} {'-'*14} {'-'*10} {'-'*10} {'-'*5}  {'-'*11} -----")
    for r in show:
        pct = f"{r['bid_to_value']*100:.0f}%" if r["bid_to_value"] is not None else "  —"
        flags = []
        if r["homestead"]:
            flags.append("HOMESTEAD(2yr redemption)")
        if r["subject_to_taxes"]:
            flags.append("owes back taxes")
        print(
            f"  {r['address'][:30]:<30} {r['city'][:14]:<14} "
            f"{(r['appraised_value'] or 0):>10,.0f} {(r['minimum_bid'] or 0):>10,.0f} "
            f"{pct:>5}  {str(r['sale_date'] or '—'):<11} {', '.join(flags)}"
        )

    n_home = sum(1 for r in hits if r["homestead"])
    if n_home:
        print(f"\n  ! {n_home} of {len(hits)} are HOMESTEAD sales. In Texas those carry a")
        print("    redemption period during which you cannot insure title, finance,")
        print("    or assign. Confirm the current rule with a Texas title attorney.")
        print("    Re-run with --exclude-homestead to hide them.")

    if a.csv:
        if os.path.exists(a.csv) and not a.force:
            print(f"\n  ! {a.csv} exists. Re-run with --force to overwrite.")
            return 1
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(hits[0].keys()) if hits else ["address"])
            w.writeheader()
            w.writerows(hits)
        print(f"\n  wrote {len(hits)} rows to {a.csv}")

    print("\n  Next: run check_property.py on anything that survives.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
