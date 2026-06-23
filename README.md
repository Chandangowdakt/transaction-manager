# Transaction Management System

A transaction management system with a user leaderboard. Users can send credit/debit transactions, view their account summary, and see how they rank against others.

## Live Demo

| Component | URL |
|-----------|-----|
| **Repository** | https://github.com/Chandangowdakt/transaction-manager |
| **Frontend** | https://transaction-frontend.onrender.com _(deploy via Render — see below)_ |
| **Backend API** | https://transaction-api-04sb.onrender.com |
| **API Docs** | https://transaction-api-04sb.onrender.com/docs |

> **Note:** Render free tier sleeps after ~15 min of inactivity. The first request may take 30–60 seconds to wake up.

## Project Structure

```
├── backend/
│   ├── main.py            # FastAPI routes
│   ├── store.py           # In-memory data store
│   ├── models.py          # Request/response models
│   ├── ranking.py         # Leaderboard score calculation
│   └── requirements.txt
├── frontend/
│   └── index.html         # Single-page UI (HTML + CSS + JS)
├── render.yaml            # Deploy backend + frontend on Render
├── VIDEO_SCRIPT.md        # Outline for 3–5 min demo video
└── README.md
```

## Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 3001
```

### Frontend

Open `frontend/index.html` in a browser while the backend is running.

## Deploy on Render

### Backend (already live)

Your API is at **https://transaction-api-04sb.onrender.com**

### Frontend (do this now)

1. Go to [render.com](https://render.com) dashboard
2. Click **New +** → **Static Site**
3. Connect repo: `Chandangowdakt/transaction-manager`
4. Settings:
   - **Name:** `transaction-frontend`
   - **Branch:** `main`
   - **Publish directory:** `frontend`
5. Click **Create Static Site**
6. Wait ~1 min, then open your live URL (e.g. `https://transaction-frontend.onrender.com`)

CORS is enabled on the backend so the frontend can call the API from any origin.

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

Every transaction includes a client-generated `transaction_id`. If the server has already processed that ID, it returns the cached response without changing the balance. This prevents double-charging on network retries.

## Concurrency & Abuse Prevention

- **Per-user asyncio Lock** — serializes concurrent requests for the same `user_id`
- **Idempotency cache** — duplicate `transaction_id` values are never processed twice
- **Rate limiting** — max 5 transactions per user per rolling 60-second window

## Assumptions & Limitations

- **In-memory storage** — data resets when the server restarts
- **No authentication** — any client can transact for any `user_id`
- **Auto-created profiles** — first transaction for a new `user_id` creates a zero-balance account
- **Render cold starts** — free tier sleeps; first request after idle may be slow

## Video Walkthrough

See [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) for a 3–5 minute recording outline.

## Submission

- **Repo:** https://github.com/Chandangowdakt/transaction-manager
- **Live frontend:** _(your Render static site URL)_
- **Live backend:** https://transaction-api-04sb.onrender.com
- **Video:** _(your recording link)_
