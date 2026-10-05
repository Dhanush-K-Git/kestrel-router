# Submission form answers (draft - items marked [YOU] need your real input)

**1. What did you build, and what business decision does it support? State the number and the rupees.**
A text-based router (FastAPI service + one screen) that picks the team for a new service request and explains why. It supports Ritu's decision to retire the Rs 3.2 lakh/yr bot. Number: 84% correct against where requests actually end up (bot: 77%); 97% correct on the ~80% it is confident about, the other ~20% flagged for a person. Rupees: today about Rs 18.4 lakh/yr (licence + transfer/repeat-contact costs); with the router about Rs 4-7 lakh/yr; saving roughly Rs 11-14 lakh/yr, Rs 0 AI charges.

**2. What score do you expect predictions.csv to get on the hidden outcomes, on which metric, and why that metric? How did you estimate it?**
About 84% accuracy (plausible range 82-86%), macro-F1 about 0.84, measured against the team that finally closed each request. Accuracy because it is Ritu's own "match" test and each wrong routing costs about Rs 685. Estimated by training only on the past and testing on the next 3 months twice (Jan-Mar 2026: 84.5%, Apr-Jun 2026: 83.7%). The final model uses all 10,822 rows. The test set is Jul-Sep 2026, so some drift is possible. If the hidden score is against the bot's queue instead, expect about 77%.

**3. How do you know it works? How you validated, on what split, error rate, and the kind of case it gets wrong.**
Out-of-time split (never random: the test set is the most recent requests). Error rate about 16%. Per-team recall 78-91%. It gets vague messages wrong ("need help with my purifier", "complaint about X"), about a third of requests, and over-predicts Repairs for them (Repairs precision 76%). 92 identical text+product combinations ended in different teams, so some cases cannot be routed from text. Confidence gate: at 70%, 80% of requests are auto-routed at 96.6% accuracy.

**4. Did you change, narrow, or push back on the client's ask? What, when, and why.**
Yes, at the start, after comparing team_label with resolution_log. Ritu asked to match the labels at 90%. The labels are the bot's own queue and agree with the final team only 77% of the time. I trained on final_team instead and recommended a confidence gate with a human check for unclear messages, rather than 90% on everything. Reason: copying the labels reproduces the bot's errors (a label-trained model scored ~96% on labels and ~76% on real outcomes).

**5. What is wrong with what you are handing us, or with the data?**
Data: product_family disagrees with the product in the text in 17.5% of rows; `transfers` contradicts first/final team in 477 rows (351 with transfers but same team, 126 with none but different teams); Legacy Zoho resolved_at is in UTC (26% resolve before creation); 11% of legacy texts have broken characters; two team names changed on 15 Jan 2026; train labels are the bot's queue. Handing-over problems: vague messages are mostly wrong; Repairs is over-predicted (614 of 2,178 test rows = 28%, vs about 23% real share), so use real final-team counts for headcount, not these predictions; the "reasons" are the model's strongest words, not a guarantee; the Rs 150 human-check cost is my assumption; the model has not seen July-Sep 2026 outcomes.

**6. What did you deliberately leave out, and why that rather than something else?**
No LLM/API calls: the vague messages are the limit, not the model, and a paid API would add running cost Farhan explicitly doesn't want. No product_family/warranty/channel features: adding them did not improve out-of-time accuracy. No resolution_log fields as features: they exist only after the fact. No deep model or char n-grams (+~1 point) because the reasons must be readable. No deployment/auth/logging: "a small thing that runs beats a large thing that does not".

**7. Anything you built or found that nobody asked for?**
The finding that the labels are the bot's queue (77% right). The confidence gate and per-request reasons with warnings (wrong product field, "paid" but not billing). The cost model in rupees. The headcount warning: the bot's queue overstates Repairs (29% vs 23% real) and Billing (15% vs 12%).

**8. What did you use AI for? Tools and models, where they helped, where they wasted your time, what you threw away. Link your 3-minute recording.**
[YOU: edit to match what actually happened] Used Claude (claude.ai chat) for data exploration, the modelling code, the service and the draft memo/form. It helped most on audit and error analysis. It wasted time on a shell brace-expansion bug that created no folders and on silly "reasons" for vague messages (fixed by filtering filler words). Discarded: label-trained model, char n-gram + meta-feature variants, an SVC (+0.5 pt, no probabilities). Recording: [YOU: Google Drive link]

**9. Someone picks this up on Monday and you are unreachable. The three things they need to know.**
(1) Train on resolution_log.final_team, never team_label; the model is `models/router.joblib` and `python -m kestrel_router.evaluate` regenerates every number. (2) The confidence gate (0.70, in model.py) is a business setting, not a model fact; set it with Meenal's team's capacity. (3) Customer data must not be published (policy section 10): the repo has no data; re-train quarterly and check against real outcomes before trusting the 84%.

**10. Honest hours spent. One number.** [YOU]

**11. GitHub Repo Link** [YOU: public repo with this folder; do NOT add the CSVs]

**12. What does one prediction cost, and what would a month cost at ~700 orders?**
No paid calls. 1 prediction = Rs 0 in API charges (about 1 ms of CPU on any machine). 700 x Rs 0 = Rs 0/month. Hosting is the only cost (can run on the CRM's existing server). The business cost is human checks of flagged requests: 700 x 20% x Rs 150 = Rs 21,000/month (my assumption) plus wrong routings of the auto-routed 80%: 700 x 80% x 3.4% x Rs 685 = Rs 13,000, total about Rs 35,000/month.
