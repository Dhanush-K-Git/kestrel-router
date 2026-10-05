**To:** Ritu Deshpande, Head of D2C Operations  **Cc:** Farhan Sheikh, Meenal Joshi, Tanmay Kulkarni
**Subject:** Routing bot - switch it off, but not against the 90% test

**The decision.** Yes, we can replace the bot and stop paying the licence. But I recommend we do not judge the replacement by "matches the old labels at 90%". Those labels are where the bot *sent* each request, and the bot is wrong about 1 in 4 times: only 77% of requests ended with the team the bot picked. A system that copies the labels to 90% would copy those mistakes. I trained on where each request actually ended up instead.

**The number.** Tested on months it had never seen, the new router picks the right team **84% of the time, against 77% for the bot**. For the roughly 80% of requests where it is confident, it is right **97% of the time**. The other 20% are mostly vague messages ("need help with my purifier") that nobody can route without asking, as Meenal noted. The router flags these for a person instead of guessing. 90% on every request is not reachable from the message text alone.

**The rupees** (using Policy section 4 costs and about 726 requests a month):
- Today: licence Rs 26,700/month, plus about Rs 1.27 lakh/month in transfers and repeat calls. About Rs 18.4 lakh a year.
- New router, confident requests automatic, the rest checked by a person: about Rs 35,000/month (assuming Rs 150 per human check; still about Rs 58,000/month at Rs 305). About Rs 4-7 lakh a year.
- Saving: roughly **Rs 11-14 lakh a year**. Running cost of the router: Rs 0 in AI charges (no paid AI service is used), so Farhan's "bill that grows with every request" does not exist.

**What to do next week.**
1. Run the router alongside the bot for 2 weeks, with Meenal's team routing as usual. Compare against where requests actually end up.
2. If it holds at 83%+ overall and 95%+ on confident requests, switch the bot off and do not renew the licence.
3. Have Meenal's team handle the flagged 20% with a short "which product / what is wrong" reply before routing.
4. For headcount, count requests by the team that finally closes them, not the bot's queue. The bot sends 29% to Repairs, but only 23% actually belong there; Billing is 12%, not 15%.
5. Ask Tanmay to fix the product field (wrong about 1 in 6) and the old Zoho time stamps before we retrain.
