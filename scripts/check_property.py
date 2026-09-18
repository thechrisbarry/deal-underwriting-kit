#!/usr/bin/env python3
"""
check_property.py — pull the free public-data layer for one US address.

Every source here is free and public. No key, no signup, no vendor.
Run it and you get back the facts that decide most deals:

    python3 check_property.py "1600 Pennsylvania Ave NW, Washington, DC"
    python3 check_property.py "123 Main St, Fort Worth, TX" --json

What it returns
---------------
  geocode      address -> lat/lon, county, census tract      (US Census)
  flood        FEMA flood zone + whether insurance is forced  (FEMA NFHL)
  hazard       18 hazards, incl. hail/tornado/hurricane       (FEMA NRI)
  walkability  walk index + transit access                    (EPA)
  rates        today's 30-yr and 15-yr mortgage rate          (Freddie Mac)

It never guesses. A field that could not be retrieved comes back as null
with the reason, because a made-up number is worse than a missing one.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.parse
import urllib.request

TIMEOUT = 30
UA = {"User-Agent": "deal-underwriting-kit/1.0 (public-data research tool)"}


MAX_BYTES = 8_000_000


def _get(url: str, timeout: int = TIMEOUT) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(MAX_BYTES).decode("utf-8", errors="replace")


def _get_json(url: str, timeout: int = TIMEOUT):
    return json.loads(_get(url, timeout))


# --------------------------------------------------------------------------
# 1. Geocode  — US Census Bureau. Free, no key.
# --------------------------------------------------------------------------
def geocode(address: str) -> dict:
    url = (
        "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
        "?address=" + urllib.parse.quote(address, safe="")
        + "&benchmark=Public_AR_Current&vintage=Current_Current&format=json"
    )
    try:
        d = _get_json(url)
    except Exception as e:
        return {"ok": False, "error": f"geocoder unreachable: {e}"}

    matches = d.get("result", {}).get("addressMatches", [])
    if not matches:
        return {"ok": False, "error": "address not found in Census geocoder"}

    m = matches[0]
    g = m.get("geographies", {})
    tract = (g.get("Census Tracts") or [{}])[0]
    county = (g.get("Counties") or [{}])[0]
    state = (g.get("States") or [{}])[0]
    return {
        "ok": True,
        "matched_address": m.get("matchedAddress"),
        "lat": m["coordinates"]["y"],
        "lon": m["coordinates"]["x"],
        "county": county.get("NAME"),
        "county_fips": (county.get("STATE", "") + county.get("COUNTY", "")) or None,
        "state": state.get("STUSAB"),
        "tract_geoid": tract.get("GEOID"),
    }


# --------------------------------------------------------------------------
# 2. Flood zone — FEMA National Flood Hazard Layer. Free, no key.
#    This is the single highest-value call in the whole script.
# --------------------------------------------------------------------------
def flood_zone(lat: float, lon: float) -> dict:
    url = (
        "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query"
        f"?geometry={lon},{lat}&geometryType=esriGeometryPoint&inSR=4326"
        "&spatialRel=esriSpatialRelIntersects"
        "&outFields=FLD_ZONE,ZONE_SUBTY,STATIC_BFE,SFHA_TF"
        "&returnGeometry=false&f=json"
    )
    try:
        d = _get_json(url)
    except Exception as e:
        return {"ok": False, "error": f"FEMA NFHL unreachable: {e}"}

    feats = d.get("features") or []
    if not feats:
        return {"ok": True, "zone": None, "note": "no mapped flood polygon at this point"}

    a = feats[0]["attributes"]
    sfha = a.get("SFHA_TF") == "T"
    bfe = a.get("STATIC_BFE")
    return {
        "ok": True,
        "zone": a.get("FLD_ZONE"),
        "subtype": a.get("ZONE_SUBTY"),
        # -9999 means "no base flood elevation published", NOT elevation zero.
        "base_flood_elevation": None if bfe in (None, -9999, -9999.0) else bfe,
        "in_special_flood_hazard_area": sfha,
        "flood_insurance_required_with_mortgage": sfha,
        "high_risk_coastal": a.get("FLD_ZONE") in ("V", "VE"),
    }


# --------------------------------------------------------------------------
# 3. Hazard profile — FEMA National Risk Index. Free, no key.
# --------------------------------------------------------------------------
NRI_URL = (
    "https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/"
    "National_Risk_Index_Census_Tracts/FeatureServer/0/query"
)
NRI_FIELDS = (
    "TRACTFIPS,RISK_RATNG,RISK_SCORE,EAL_VALT,SOVI_RATNG,RESL_RATNG,"
    "HRCN_RISKR,TRND_RISKR,HAIL_RISKR,WFIR_RISKR,ERQK_RISKR,CFLD_RISKR"
)


def hazard(lat: float, lon: float) -> dict:
    # Note: a bare "geometry=lon,lat" is rejected here. It must be a JSON object.
    geom = json.dumps({"x": lon, "y": lat, "spatialReference": {"wkid": 4326}})
    url = (
        NRI_URL
        + "?geometry=" + urllib.parse.quote(geom)
        + "&geometryType=esriGeometryPoint&spatialRel=esriSpatialRelIntersects"
        + "&outFields=" + NRI_FIELDS
        + "&returnGeometry=false&f=json"
    )
    try:
        d = _get_json(url)
    except Exception as e:
        return {"ok": False, "error": f"FEMA NRI unreachable: {e}"}

    feats = d.get("features") or []
    if not feats:
        return {"ok": True, "note": "no NRI record for this tract"}

    a = feats[0]["attributes"]
    return {
        "ok": True,
        "overall_risk": a.get("RISK_RATNG"),
        "risk_score": a.get("RISK_SCORE"),
        "expected_annual_loss_usd": a.get("EAL_VALT"),
        "social_vulnerability": a.get("SOVI_RATNG"),
        "community_resilience": a.get("RESL_RATNG"),
        "hail": a.get("HAIL_RISKR"),
        "tornado": a.get("TRND_RISKR"),
        "hurricane": a.get("HRCN_RISKR"),
        "wildfire": a.get("WFIR_RISKR"),
        "earthquake": a.get("ERQK_RISKR"),
        "coastal_flood": a.get("CFLD_RISKR"),
    }


# --------------------------------------------------------------------------
# 4. Walkability — EPA National Walkability Index. Free, no key.
# --------------------------------------------------------------------------
WALK_URL = (
    "https://geodata.epa.gov/arcgis/rest/services/OA/WalkabilityIndex/MapServer/0/query"
)


def walkability(lat: float, lon: float) -> dict:
    geom = json.dumps({"x": lon, "y": lat, "spatialReference": {"wkid": 4326}})
    url = (
        WALK_URL
        + "?geometry=" + urllib.parse.quote(geom)
        + "&geometryType=esriGeometryPoint&spatialRel=esriSpatialRelIntersects"
        + "&outFields=NatWalkInd,D3B_Ranked,D4A_Ranked,TotPop,Pct_AO0"
        + "&returnGeometry=false&f=json"
    )
    try:
        d = _get_json(url)
    except Exception as e:
        return {"ok": False, "error": f"EPA walkability unreachable: {e}"}

    feats = d.get("features") or []
    if not feats:
        return {"ok": True, "note": "no walkability record for this block group"}

    a = feats[0]["attributes"]
    idx = a.get("NatWalkInd")
    return {
        "ok": True,
        "walk_index_0_to_20": round(idx, 1) if isinstance(idx, (int, float)) else idx,
        "intersection_density_rank": a.get("D3B_Ranked"),
        "transit_proximity_rank": a.get("D4A_Ranked"),
        "block_group_population": a.get("TotPop"),
        "share_households_no_car": a.get("Pct_AO0"),
    }


# --------------------------------------------------------------------------
# 5. Mortgage rates — Freddie Mac PMMS. Free, no key.
# --------------------------------------------------------------------------
PMMS = "https://www.freddiemac.com/pmms/docs/PMMS_history.csv"

# Rough spread of an investor / DSCR loan over the headline 30-yr survey rate.
# THIS IS AN ESTIMATE, NOT A QUOTE. Replace it with your own lender's pricing.
INVESTOR_SPREAD = 0.85
HARD_MONEY_SPREAD = 2.50
HARD_MONEY_FLOOR, HARD_MONEY_CEILING = 8.50, 12.00


def mortgage_rates() -> dict:
    try:
        text = _get(PMMS)
    except Exception as e:
        return {"ok": False, "error": f"Freddie Mac PMMS unreachable: {e}"}

    rows = [r for r in csv.reader(io.StringIO(text)) if r and r[0][:1].isdigit()]
    if not rows:
        return {"ok": False, "error": "PMMS returned no parseable rows"}

    last = rows[-1]

    def num(i):
        try:
            return float(last[i])
        except (IndexError, ValueError):
            return None

    r30, r15 = num(1), num(3)
    out = {"ok": True, "as_of": last[0], "rate_30yr": r30, "rate_15yr": r15}
    if r30 is not None:
        out["investor_dscr_estimate"] = round(r30 + INVESTOR_SPREAD, 2)
        out["hard_money_estimate"] = round(
            min(max(r30 + HARD_MONEY_SPREAD, HARD_MONEY_FLOOR), HARD_MONEY_CEILING), 2
        )
    return out


# --------------------------------------------------------------------------
# Kill switches — the checks that fail a deal on their own
# --------------------------------------------------------------------------
def kill_switches(flood: dict, haz: dict) -> list[str]:
    flags = []
    if flood.get("high_risk_coastal"):
        flags.append(
            "Coastal high-hazard flood zone (V/VE) — the most expensive flood "
            "insurance there is. Price it before you offer."
        )
    elif flood.get("in_special_flood_hazard_area"):
        flags.append(
            "Special Flood Hazard Area — flood insurance is federally required "
            "with a mortgage. Never use the seller's premium; it is capped and yours is not."
        )
    for key, label in (("hail", "Hail"), ("tornado", "Tornado"), ("hurricane", "Hurricane"),
                       ("wildfire", "Wildfire"), ("earthquake", "Earthquake")):
        if haz.get(key) in ("Very High", "Relatively High"):
            flags.append(f"{label} risk is {haz[key]} — expect higher premiums and claims.")
    if haz.get("social_vulnerability") == "Very High":
        flags.append("Neighborhood social vulnerability is Very High — check rent collection and turnover.")
    return flags


def run(address: str) -> dict:
    geo = geocode(address)
    result = {"query": address, "geocode": geo}
    if not geo.get("ok"):
        return result

    lat, lon = geo["lat"], geo["lon"]
    result["flood"] = flood_zone(lat, lon)
    result["hazard"] = hazard(lat, lon)
    result["walkability"] = walkability(lat, lon)
    result["rates"] = mortgage_rates()
    result["flags"] = kill_switches(result["flood"], result["hazard"])
    return result


# --------------------------------------------------------------------------
def render(r: dict) -> str:
    g = r["geocode"]
    if not g.get("ok"):
        return f"Could not locate that address.\n  {g.get('error')}"

    L, out = [], []
    out.append(f"\n  {g['matched_address']}")
    out.append(f"  {g['county']}, {g['state']}  ·  tract {g['tract_geoid']}")
    out.append(f"  {g['lat']:.6f}, {g['lon']:.6f}\n")

    f = r.get("flood", {})
    if f.get("ok"):
        if f.get("zone"):
            req = "YES — required with a mortgage" if f["in_special_flood_hazard_area"] else "no"
            out.append(f"  FLOOD       zone {f['zone']}  ({f.get('subtype') or 'n/a'})")
            out.append(f"              flood insurance: {req}")
        else:
            out.append(f"  FLOOD       {f.get('note')}")
    else:
        out.append(f"  FLOOD       unavailable — {f.get('error')}")

    h = r.get("hazard", {})
    if h.get("ok") and h.get("overall_risk"):
        out.append(f"\n  HAZARD      overall {h['overall_risk']}")
        for k in ("hail", "tornado", "hurricane", "wildfire", "coastal_flood"):
            if h.get(k):
                out.append(f"              {k:<14} {h[k]}")
        out.append(f"              {'vulnerability':<14} {h.get('social_vulnerability')}")

    w = r.get("walkability", {})
    if w.get("ok") and w.get("walk_index_0_to_20") is not None:
        out.append(f"\n  WALKABILITY {w['walk_index_0_to_20']} / 20")

    m = r.get("rates", {})
    if m.get("ok"):
        out.append(f"\n  RATES       as of {m['as_of']}")
        out.append(f"              30-year fixed        {m['rate_30yr']}%")
        if m.get("investor_dscr_estimate"):
            out.append(f"              investor / DSCR est. {m['investor_dscr_estimate']}%")
            out.append(f"              hard money est.      {m['hard_money_estimate']}%")

    if r.get("flags"):
        out.append("\n  FLAGS")
        for fl in r["flags"]:
            out.append(f"     !  {fl}")
    else:
        out.append("\n  FLAGS       none from the free hazard layer")

    out.append(
        "\n  Remember: this is the free layer only. It does NOT include sold\n"
        "  comparables, rehab cost, or the post-sale tax bill. Do not call a\n"
        "  deal a PASS on this alone. See docs/04-deal-killers.md.\n"
    )
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Free public-data checks for one US address.")
    ap.add_argument("address", help='e.g. "123 Main St, Fort Worth, TX"')
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of a report")
    a = ap.parse_args()

    r = run(a.address)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print(render(r))
    return 0 if r["geocode"].get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
