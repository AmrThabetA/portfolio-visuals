"""
prepare_data.py — Build the data bundle for the Observable Plot visual suite.

Reads the P1 claims and P3 chronic-disease datasets, aggregates them, and
writes src/data.js (a single JS object the HTML page loads). Re-run this
whenever the underlying data changes.

Usage:
    python prepare_data.py
"""
import os, json
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

claims = pd.read_csv(os.path.join(DATA, "claims_clean.csv"))
chronic = pd.read_csv(os.path.join(DATA, "chronic_disease_cohort.csv"))

# Chart 1 — denial rate by specialty x claim type (+ TOTAL)
pivot = (claims.groupby(["ProviderSpecialty", "ClaimType"])
         .apply(lambda x: round((x["ClaimStatus"] == "Denied").mean() * 100, 1),
                include_groups=False).reset_index(name="rate"))
tot = (claims.groupby("ProviderSpecialty")
       .apply(lambda x: round((x["ClaimStatus"] == "Denied").mean() * 100, 1),
              include_groups=False).reset_index(name="rate"))
spec_order = tot.sort_values("rate", ascending=False)["ProviderSpecialty"].tolist()
tot["ClaimType"] = "TOTAL"
heat1 = pd.concat([pivot, tot]).rename(
    columns={"ProviderSpecialty": "specialty", "ClaimType": "type"})

# Chart 2 — monthly denial rate
counts = claims.groupby("ClaimMonth").size()
keep = counts[counts >= counts.median() * 0.4].index
monthly = (claims[claims["ClaimMonth"].isin(keep)].groupby("ClaimMonth")
           .apply(lambda x: round((x["ClaimStatus"] == "Denied").mean() * 100, 1),
                  include_groups=False).reset_index(name="rate")
           .sort_values("ClaimMonth"))
avg_rate = round((claims["ClaimStatus"] == "Denied").mean() * 100, 1)

# Chart 3 — strip sample (cap for browser performance)
np.random.seed(1)
strip = []
for st in ["Approved", "Pending", "Denied"]:
    sub = claims[claims["ClaimStatus"] == st]["ClaimAmount"]
    for v in sub.sample(min(600, len(sub)), random_state=1):
        strip.append({"status": st, "amount": round(float(v), 0)})
medians = {st: round(float(claims[claims["ClaimStatus"] == st]["ClaimAmount"].median()), 0)
           for st in ["Approved", "Pending", "Denied"]}

# Chart 4 — cost by condition x emirate (+ AVG)
piv = chronic.pivot_table(index="condition", columns="emirate",
                          values="total_cost_aed", aggfunc="mean").round(0)
avg = chronic.groupby("condition")["total_cost_aed"].mean().round(0)
cond_order = avg.sort_values(ascending=False).index.tolist()
heat4 = []
for cond in chronic["condition"].unique():
    for em in chronic["emirate"].unique():
        heat4.append({"condition": cond, "emirate": em, "cost": float(piv.loc[cond, em])})
    heat4.append({"condition": cond, "emirate": "AVG", "cost": float(avg.loc[cond])})


# Chart 5 - revenue leakage by denial reason (P2 RCM verified figures)
denial_reasons = [
    {"reason": "Missing Pre-authorisation", "value": 2376496},
    {"reason": "Coding Error (ICD-10)",     "value": 1658665},
    {"reason": "Patient Not Eligible",      "value": 851492},
    {"reason": "Duplicate Claim",           "value": 718448},
    {"reason": "Missing Documentation",     "value": 643844},
    {"reason": "Service Not Covered",       "value": 512300},
    {"reason": "Late Submission",           "value": 389210},
]
leak_total = sum(d["value"] for d in denial_reasons)
for d in denial_reasons:
    d["pct"] = round(d["value"] / leak_total * 100, 1)

bundle = {
    "heat1": heat1.to_dict(orient="records"), "specOrder": spec_order,
    "line2": monthly.to_dict(orient="records"), "avgRate": avg_rate,
    "strip3": strip, "medians3": medians,
    "heat4": heat4, "condOrder": cond_order,
    "emirateOrder": sorted(chronic["emirate"].unique().tolist()) + ["AVG"],
    "claimTypeOrder": ["Emergency", "Inpatient", "Outpatient", "Routine", "TOTAL"],
    "reasons5": denial_reasons, "leakTotal": leak_total,
}
with open(os.path.join(HERE, "data.js"), "w") as f:
    f.write("window.VIZ_DATA = " + json.dumps(bundle) + ";")
print("data.js written —", len(bundle["heat1"]), "heatmap cells,",
      len(bundle["strip3"]), "strip points")
