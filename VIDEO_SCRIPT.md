# Video Walkthrough Script (~4 minutes)

Use this outline to record a 3–5 minute screen recording. Demo the **live deployed** frontend if available; otherwise run locally.

---

## 1. Introduction (30 sec)

> "I built a transaction management system with a FastAPI backend and a plain HTML/JS frontend. Users can send credit and debit transactions, view their account summary, and appear on a multi-factor leaderboard. The focus is on API design, data consistency, and fair ranking."

**Show:** Live frontend homepage (or `frontend/index.html` locally).

---

## 2. What You Built (45 sec)

> "The backend has three endpoints: POST /transaction, GET /summary, and GET /ranking. Data is stored in memory using Python dicts — no database — which keeps the assignment simple but means data resets on server restart."

**Show:** Project folder structure in IDE (`backend/`, `frontend/`, `README.md`).

---

## 3. API Demo (90 sec)

### Transaction
> "To send money, the client provides user_id, amount, type, and a unique transaction_id."

**Do:** Credit $100 to user `alice`. Show success message and balance.

### Summary
> "Summary returns balance, totals, transaction count, and account age."

**Do:** Click Get Summary for `alice`.

### Ranking
> "The leaderboard ranks all users by a composite score."

**Do:** Create a second user `bob` with a different balance, refresh leaderboard, explain ranks.

### Error handling
**Do:** Try debiting more than balance — show error message.
**Do:** Resubmit the same transaction_id — show idempotent response (balance unchanged).

---

## 4. Concurrency & Fairness (60 sec)

> "Three mechanisms protect data integrity:"

1. **Per-user lock** — "Concurrent requests for the same user are serialized with an asyncio Lock, so two debits can't both pass a balance check."
2. **Idempotency** — "Duplicate transaction_ids return the cached result without re-processing — important for network retries."
3. **Rate limiting** — "Each user is capped at 5 transactions per minute to prevent abuse."

> "Ranking uses four normalized factors — balance, activity, account age, and a consistency ratio — so no single metric dominates. A user can't win the leaderboard just by spamming tiny transactions."

**Show:** Briefly open `backend/ranking.py` or README ranking table.

---

## 5. Trade-offs & Limitations (30 sec)

> "Trade-offs I made:"
> - In-memory store instead of a database — simpler code, but no persistence across restarts.
> - No authentication — out of scope for this assignment.
> - Render free tier sleeps after inactivity — first request may be slow.

---

## 6. Closing (15 sec)

> "The README covers how to run locally, deploy to Render and GitHub Pages, and how each feature works. Thanks for watching."

---

## Recording Tips

- Use OBS, Loom, or Windows Game Bar (`Win + G`).
- Speak clearly; 4 minutes is enough — don't rush the demo.
- Upload to YouTube (unlisted), Google Drive, or Loom and paste the link in your submission.
