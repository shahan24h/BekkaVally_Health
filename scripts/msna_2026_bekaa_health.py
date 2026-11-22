#!/usr/bin/env python3
"""Aggregate REACH MSNA 2026 healthcare indicators for Lebanese HH in Bekaa.

Only reads the original workbook on the user's machine. Exports aggregate CSVs.
No household-level records or identifiable data are written.

Usage:
  python scripts/msna_2026_bekaa_health.py --input /path/to/workbook.xlsx --output results
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

GOV = "admin1_label_en"
POP = "pop_group_label_en"
WEIGHT = "weight"
NEEDS = "health_ind_healthcare_needed_n"
BARRIERS = "health_barriers"
BARRIER_LABELS = {
    "no_facility_nearby": "No nearby healthcare facility",
    "cant_afford_consult": "Cannot afford consultation",
    "cant_afford_treatment": "Cannot afford treatment",
    "cant_afford_transport": "Cannot afford transport",
    "long_wait_time": "Long waiting time",
    "service_unavailable": "Service unavailable",
    "facility_too_far": "Facility too far",
    "no_transport_means": "No transport available",
}
COST_KEYS = (
    "cant_afford_consult",
    "cant_afford_treatment",
    "cant_afford_transport",
)


def percent(flag, weights):
    """Survey-weighted descriptive percent over the given valid respondents."""
    return 100 * weights.loc[flag].sum() / weights.sum()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path, help="MSNA 2026 .xlsx workbook")
    ap.add_argument("--output", default=Path("results"), type=Path)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    needed_cols = [GOV, POP, WEIGHT, NEEDS, BARRIERS] + [
        f"health_barriers.{k}" for k in BARRIER_LABELS
    ]
    data = pd.read_excel(
        args.input,
        sheet_name="Household Data",
        usecols=lambda col: col in needed_cols,
        engine="openpyxl",
    )
    absent = [c for c in needed_cols if c not in data.columns]
    if absent:
        raise ValueError(f"Workbook missing columns: {absent}")

    subset = data.loc[
        data[GOV].astype("string").str.strip().eq("Bekaa")
        & data[POP].astype("string").str.strip().eq("Lebanese")
    ].copy()

    subset[WEIGHT] = pd.to_numeric(subset[WEIGHT], errors="coerce")
    if ((~np.isfinite(subset[WEIGHT])) | subset[WEIGHT].le(0)).any():
        raise ValueError("Some Bekaa Lebanese households have invalid survey weights.")
    if subset.empty:
        raise ValueError("No households match Bekaa + Lebanese filters.")

    print(f"Study households: {len(subset)}")

    # Healthcare need: valid numeric nonnegative counts.
    counts = pd.to_numeric(subset[NEEDS], errors="coerce")
    valid_needs = np.isfinite(counts) & counts.ge(0)
    need_data = subset.loc[valid_needs].copy()
    need_data["_needs"] = counts.loc[valid_needs]
    need_rows = []
    for n, group in need_data.groupby("_needs"):
        need_rows.append({
            "members_needing_healthcare": int(n),
            "unweighted_households": len(group),
            "eligible_households": len(need_data),
            "weighted_percent": 100 * group[WEIGHT].sum() / need_data[WEIGHT].sum(),
        })
    need_rows.append({
        "members_needing_healthcare": "at_least_one",
        "unweighted_households": int(need_data["_needs"].gt(0).sum()),
        "eligible_households": len(need_data),
        "weighted_percent": percent(need_data["_needs"].gt(0), need_data[WEIGHT]),
    })
    need_table = pd.DataFrame(need_rows)
    need_table.to_csv(args.output / "healthcare_needs_summary.csv", index=False)

    # Only recorded answers are in the barrier denominator. We do not
    # treat zeros in missing/skipped rows as evidence of no barrier.
    raw = subset[BARRIERS].astype("string").str.strip()
    recorded = (
        raw.notna()
        & raw.ne("")
        & ~raw.str.lower().isin(["nan", "null", "none"])
    ).fillna(False)
    answered = subset.loc[recorded].copy()
    print(f"Healthcare barrier respondents: {len(answered)}")
    print(f"Missing/skipped barrier responses: {len(subset) - len(answered)}")
    if answered.empty:
        raise ValueError("No recorded healthcare barrier answers.")

    barrier_rows = []
    for key, label in BARRIER_LABELS.items():
        flag_col = f"health_barriers.{key}"
        vals = pd.to_numeric(answered[flag_col], errors="coerce")
        eligible_flag = vals.isin([0, 1])
        if not eligible_flag.all():
            print(f"WARNING: {flag_col} has {int((~eligible_flag).sum())} non-binary entries")
        eligible = answered.loc[eligible_flag]
        yes = vals.loc[eligible_flag].eq(1)
        barrier_rows.append({
            "barrier": key,
            "description": label,
            "unweighted_households_reporting": int(yes.sum()),
            "eligible_households": len(eligible),
            "weighted_percent": percent(yes, eligible[WEIGHT]) if len(eligible) else np.nan,
        })

    cost_cols = [f"health_barriers.{k}" for k in COST_KEYS]
    cost = answered[cost_cols].apply(pd.to_numeric, errors="coerce")
    cost_valid = cost.isin([0, 1]).all(axis=1)
    eligible_cost = answered.loc[cost_valid]
    any_cost = cost.loc[cost_valid].eq(1).any(axis=1)
    barrier_rows.append({
        "barrier": "any_financial_barrier",
        "description": "Any consultation, treatment, or transport cost barrier",
        "unweighted_households_reporting": int(any_cost.sum()),
        "eligible_households": len(eligible_cost),
        "weighted_percent": (
            percent(any_cost, eligible_cost[WEIGHT]) if len(eligible_cost) else np.nan
        ),
    })

    barrier_table = pd.DataFrame(barrier_rows).sort_values(
        "weighted_percent", ascending=False
    )
    barrier_table.to_csv(args.output / "healthcare_barriers_summary.csv", index=False)

    print("\nHealthcare needs:")
    print(need_table.to_string(index=False))
    print("\nBarriers (conditional on recorded respondents):")
    print(barrier_table.to_string(index=False))
    print(f"\nAggregate CSVs saved in {args.output.resolve()}")
    print("Check questionnaire skip logic and survey design before publication.")


if __name__ == "__main__":
    main()
