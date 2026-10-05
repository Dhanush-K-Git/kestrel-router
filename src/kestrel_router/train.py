"""Train on where requests ACTUALLY ENDED UP (resolution_log.final_team), not on the
bot's queue (train.team_label). See reports/evidence.md for why.

Usage: python -m kestrel_router.train --data-dir /path/to/pack --out models/router.joblib
"""
import argparse
import glob
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .text import clean, canon


def find(d, name):
    return glob.glob(f"{d}/*{name}")[0]


def load_train(data_dir):
    tr = pd.read_csv(find(data_dir, "train.csv"))
    rl = pd.read_csv(find(data_dir, "resolution_log.csv"))
    m = tr.merge(rl, on="request_id")
    m["fin"] = m.final_team.map(canon)
    m["lab"] = m.team_label.map(canon)
    m["ts"] = pd.to_datetime(m.created_at_ist)
    m["t"] = m.request_text.map(clean)
    return m


def fit(df):
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    X = vec.fit_transform(df.t)
    clf = LogisticRegression(C=1, max_iter=3000).fit(X, df.fin)
    return vec, clf


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out", default="models/router.joblib")
    a = ap.parse_args()
    m = load_train(a.data_dir)
    vec, clf = fit(m)
    joblib.dump({"vectorizer": vec, "classifier": clf}, a.out, compress=3)
    print(f"trained on {len(m)} rows -> {a.out}")
