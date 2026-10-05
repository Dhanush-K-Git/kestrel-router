"""Text cleaning shared by training, evaluation and the service.

Why this exists: ~11% of legacy_zoho rows came across with broken characters
(e.g. 'Ã©' for 'é'). Order/registration numbers are unique per request and
carry no routing signal, so they are removed.
"""
import re
import unicodedata

# Teams were renamed on 15 Jan 2026 (ops-policy section 5). Responsibilities did
# not change, so we train on ONE canonical name per team and map back on output.
TO_CANON = {"Installs & Demo": "Installations", "Filters & Consumables": "Consumables"}
TO_CURRENT = {v: k for k, v in TO_CANON.items()}  # names in force since 15 Jan 2026


def canon(team: str) -> str:
    return TO_CANON.get(team, team)


def current_name(team: str) -> str:
    return TO_CURRENT.get(team, team)


def clean(s: str) -> str:
    s = str(s).replace("Ã¢â‚¬Â¦", "...")
    try:  # undo double-encoded UTF-8 (legacy Zoho export)
        s = s.encode("latin-1").decode("utf-8")
    except Exception:
        pass
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\b(SR|KO)\d+\b", " ", s)  # request / order numbers
    s = re.sub(r"\d+", " ", s)
    return re.sub(r"\s+", " ", s.lower()).strip()
