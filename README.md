# Kestrel Home - service-request router

Reads a customer's opening message and says which of the 7 teams should get it, with plain-English reasons.
Runs fully offline. **No API key, no paid calls, no internet needed after install.**

## Start it (clean machine, Python 3.10+)

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn kestrel_router.app:app --app-dir src --port 8000    # Windows PowerShell: $env:PYTHONPATH="src"
```
Open http://localhost:8000 (the screen). The trained model is in `models/router.joblib`, so nothing else is needed.

Endpoint:
```bash
curl -X POST localhost:8000/route -H "Content-Type: application/json" \
  -d '{"request_text":"installer did not turn up for room heater, i paid extra","product_family":"Room Heater"}'
```
Returns `team`, `confidence`, `needs_human_check`, `alternatives`, `reasons`, `notes`.
Only `request_text` is required. Empty text gets a polite 422. No external services are called, so there is nothing to fail without a key.

## Key decision: what the model is trained on
`train.csv.team_label` is the queue the **old bot** chose. `resolution_log.final_team` is where the request **actually ended up**.
They agree only 77% of the time. The model is trained on `final_team`. Copying the labels to 90% would copy the bot's mistakes
(a model trained on the labels scores ~96% on them and ~76% on real outcomes). Details and numbers: `reports/evidence.md`.

## Reproduce everything (needs the Kestrel data pack, which is NOT in this repo - policy section 10)
```bash
pip install -r requirements-dev.txt
export PYTHONPATH=src
python -m kestrel_router.train    --data-dir /path/to/pack --out models/router.joblib
python -m kestrel_router.evaluate --data-dir /path/to/pack            # writes reports/evidence.md
python -m kestrel_router.predict  --test /path/to/pack/test_unlabelled.csv --out predictions.csv
pytest -q tests
```

## Files
- `predictions.csv` - one row per test request, same shape as sample_submission.csv. Team names are the post-15-Jan-2026 names (every test row is after the rename). `reports/predictions_with_confidence.csv` adds confidence and the human-check flag.
- `src/kestrel_router/` - `text.py` (cleaning), `train.py`, `evaluate.py`, `predict.py`, `model.py` (prediction + reasons), `app.py` (service).
- `static/index.html` - the screen. `tests/` - 6 service tests.

## Known limits
- About 1 request in 6 is wrongly routed; vague messages ("need help with my purifier") are the main cause and default to Repairs.
  The screen flags those as "needs a person" (confidence under 70%, about 20% of requests).
- `product_family` is wrong about 17% of the time, so the model reads the product from the message instead.
- Trained on 15 months of data; re-train quarterly and re-check against real outcomes.
