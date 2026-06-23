# Transaction Management System

A transaction management system with a user leaderboard. Users can send credit/debit transactions, view their account summary, and see how they rank against others.

## Live Demo

| Component | URL |
|-----------|-----|
| **Repository** | https://github.com/Chandangowdakt/transaction-manager |
| **Frontend** | https://chandangowdakt.github.io/transaction-manager/ _(enable GitHub Pages — see below)_ |
| **Backend API** | https://transaction-api-04sb.onrender.com |
| **API Docs** | https://transaction-api-04sb.onrender.com/docs |

> **Note:** Render free tier sleeps after ~15 min of inactivity. The first request may take 30–60 seconds to wake up.

## Project Structure

```
project/
├── backend/
│   ├── main.py            # FastAPI routes
│   ├── store.py           # In-memory data store
│   ├── models.py          # Request/response models
│   ├── ranking.py         # Leaderboard score calculation
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html         # Single-page UI (HTML + CSS + JS)
├── render.yaml            # One-click backend deploy on Render
├── .github/workflows/     # GitHub Pages auto-deploy for frontend
└── README.md
```

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 3001
```

API available at `http://localhost:3001`. Interactive docs at `http://localhost:3001/docs`.

> On Windows, if `uvicorn` is not on PATH, always use `python -m uvicorn`.

### Frontend

Open `frontend/index.html` in a browser while the backend is running. The frontend auto-detects localhost and points to port `3001`.

## Deploying Live

### Backend (Render — free)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect the repo — Render reads `render.yaml` automatically.
4. Deploy. Your API will be at `https://transaction-api.onrender.com` (or the name you choose).
5. Update the production URL in `frontend/index.html` if your service name differs.

### Frontend (GitHub Pages — free)

1. Push to GitHub (`main` branch).
2. Repo **Settings** → **Pages** → **Source**: select **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` deploys `frontend/` on every push.
4. Your live URL will be `https://<username>.github.io/<repo-name>/`.

CORS is enabled on the backend (`allow_origins=["*"]`) so the deployed frontend can call the API.

## API Endpoints

### `POST /transaction`

Creates a credit or debit transaction. Body: `user_id`, `amount` (positive), `type` (`"credit"` or `"debit"`), `transaction_id` (client-provided unique string).

On success, returns `{ success, message, balance, transaction_id }`. Debits are rejected with `400` if balance is insufficient. Rate-limited to 5 transactions per user per minute (`429`). Validation errors return `422` with a `detail` field.

### `GET /summary/{userId}`

Returns `{ user_id, balance, total_credited, total_debited, transaction_count, account_age_days }`. Returns `404` if the user has never transacted.

### `GET /ranking`

Returns a list of `{ rank, user_id, score, balance, transaction_count }` sorted by score descending. Returns `[]` when no users exist.

## Ranking Calculation

Each user's score blends four min-max-normalized factors (scaled 0–1 across all users):

| Weight | Factor | Description |
|--------|--------|-------------|
| 40% | Balance | Higher balance ranks better |
| 30% | Transaction count | More activity ranks better |
| 20% | Account age | Older accounts rank better |
| 10% | Consistency ratio | `total_credited / (total_credited + total_debited + 1)` |

Users are sorted by final score descending; rank 1 is highest.

## Duplicate Request Prevention (Idempotency)

Every transaction includes a client-generated `transaction_id`. If the server has already processed that ID, it returns the cached response without changing the balance. This prevents double-charging on network retries. The cache is checked both before and inside the per-user lock to handle concurrent duplicates safely.

## Concurrency & Abuse Prevention

- **Per-user asyncio Lock** — serializes concurrent requests for the same `user_id` so balance updates stay consistent.
- **Idempotency cache** — duplicate `transaction_id` values are never processed twice.
- **Rate limiting** — max 5 successful (non-duplicate) transactions per user per rolling 60-second window.

## Assumptions & Limitations

- **In-memory storage** — data resets when the server restarts (Render redeploys wipe state).
- **No authentication** — any client can transact for any `user_id`.
- **Auto-created profiles** — first transaction for a new `user_id` creates a zero-balance account.
- **Summary requires existing user** — `GET /summary` returns 404 for unknown users.
- **Render cold starts** — free tier sleeps; first request after idle may be slow.

## Video Walkthrough

See [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) for a 3–5 minute recording outline covering architecture, APIs, concurrency, ranking fairness, and trade-offs.

## Submission Checklist

- [x] Source code (backend + frontend)
- [x] README (run, APIs, ranking, idempotency)
- [ ] Live deployed frontend URL (GitHub Pages)
- [ ] Live deployed backend URL (Render)
- [ ] 3–5 min screen recording (use VIDEO_SCRIPT.md)
- [ ] GitHub repo link or zip file
