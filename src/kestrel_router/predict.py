"""Write predictions.csv in the shape of sample_submission.csv.
Usage: python -m kestrel_router.predict --test /path/test_unlabelled.csv --out predictions.csv
Team names are the names in force since 15 Jan 2026 (every test row is after it)."""
import argparse
import pandas as pd
from .model import Router

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", required=True)
    ap.add_argument("--model", default="models/router.joblib")
    ap.add_argument("--out", default="predictions.csv")
    a = ap.parse_args()
    r = Router(a.model)
    df = pd.read_csv(a.test)
    res = [r.route(row) for row in df.to_dict("records")]
    df["team"] = [x["team"] for x in res]
    df[["request_id", "team"]].to_csv(a.out, index=False)
    df.assign(confidence=[x["confidence"] for x in res], needs_human_check=[x["needs_human_check"] for x in res])[["request_id", "team", "confidence", "needs_human_check"]].to_csv(a.out.replace(".csv", "_with_confidence.csv"), index=False)
    print(df.team.value_counts(), "\nneeds human check:", sum(x["needs_human_check"] for x in res) / len(res))
