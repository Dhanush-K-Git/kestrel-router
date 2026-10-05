"""Model wrapper: prediction + plain-English reasons. No network, no API key."""
import re
import joblib
import numpy as np
from .text import clean, current_name

VERSION = "tfidf-logreg-v1"
CONF_THRESHOLD = 0.70  # below this the screen says "needs a human to check"

PRODUCT_WORDS = {
    "Water Purifier": r"purifier", "Air Fryer": r"fryer", "Mixer Grinder": r"mixer|grinder",
    "Induction Cooktop": r"cooktop", "Room Heater": r"heater", "Ceiling Fan": r"ceiling fan|\bfan\b",
    "Robot Vacuum": r"vacuum",
}
FILLER = set("hi hello team sir pls please namaste good morning urgent kindly resolve thanks asap very disappointed about regarding with my me the a an of to for in on is it need help call back contact someone not happy complaint query issue service request i".split())
VAGUE = re.compile(r"\b(need help|help|complaint|query|issue|not happy|call back|contact me|service request)\b")
PAID = re.compile(r"\b(paid|payment|upi|card|emi)\b")


class Router:
    def __init__(self, path):
        art = joblib.load(path)
        self.vec, self.clf = art["vectorizer"], art["classifier"]
        self.names = np.array(self.vec.get_feature_names_out())

    def route(self, rec: dict) -> dict:
        text = clean(rec.get("request_text", ""))
        x = self.vec.transform([text])
        proba = self.clf.predict_proba(x)[0]
        order = np.argsort(-proba)
        top = self.clf.classes_[order[0]]
        conf = float(proba[order[0]])
        reasons = self._reasons(x, order[0])
        notes = self._notes(rec, text, top)
        needs_check = conf < CONF_THRESHOLD
        if needs_check:
            notes.insert(0, f"Model is only {conf:.0%} sure - a person should read this before routing.")
        return {
            "team": current_name(top),
            "confidence": round(conf, 3),
            "needs_human_check": needs_check,
            "alternatives": [{"team": current_name(self.clf.classes_[i]), "probability": round(float(proba[i]), 3)} for i in order[1:3]],
            "reasons": reasons,
            "notes": notes,
            "model_version": VERSION,
            "paid_api_calls": 0,
        }

    def _reasons(self, x, ci):
        contrib = x.multiply(self.clf.coef_[ci]).tocoo()
        pairs = sorted(zip(contrib.data, contrib.col), reverse=True)
        out = []
        for v, c in pairs:
            if v > 0.05 and not set(self.names[c].split()) <= FILLER:
                out.append(f'The words "{self.names[c]}" usually mean {current_name(self.clf.classes_[ci])}.')
            if len(out) == 3:
                break
        return out or ["No strong wording in the message points to one team; this is the model's best guess, not a clear signal."]

    def _notes(self, rec, text, top):
        notes = []
        named = [p for p, rx in PRODUCT_WORDS.items() if re.search(rx, text)]
        pf = rec.get("product_family")
        if len(named) == 1 and pf and named[0] != pf:
            notes.append(f"Message talks about a {named[0]} but the product field says {pf}. The message was trusted; the product field is wrong about 1 time in 6.")
        if PAID.search(text) and top != "Billing":
            notes.append("Customer mentions paying, but the problem is not the payment itself, so not Billing (Ops Policy section 3).")
        if VAGUE.search(text) and len(text.split()) <= 8:
            notes.append("Message is vague; these are the ones the model gets wrong most often.")
        return notes
