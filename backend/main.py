import asyncio
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import store
from models import TransactionRequest, TransactionResponse, UserSummary
from ranking import compute_rankings
from store import ensure_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 60  # seconds


def _get_user_lock(user_id: str) -> asyncio.Lock:
    if user_id not in store.user_locks:
        store.user_locks[user_id] = asyncio.Lock()
    return store.user_locks[user_id]


def _check_rate_limit(user_id: str) -> None:
    now = time.time()
    timestamps = store.rate_limit.get(user_id, [])
    # Keep only requests within the last minute
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    store.rate_limit[user_id] = timestamps

    if len(timestamps) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: max 5 transactions per minute",
        )


def _record_rate_limit(user_id: str) -> None:
    store.rate_limit.setdefault(user_id, []).append(time.time())


@app.post("/transaction", response_model=TransactionResponse)
async def create_transaction(req: TransactionRequest):
    # Idempotency: return cached result if we've seen this transaction_id before
    if req.transaction_id in store.transactions:
        return TransactionResponse(**store.transactions[req.transaction_id])

    lock = _get_user_lock(req.user_id)

    async with lock:
        # Re-check cache inside lock in case a concurrent request just finished
        if req.transaction_id in store.transactions:
            return TransactionResponse(**store.transactions[req.transaction_id])

        _check_rate_limit(req.user_id)

        user = ensure_user(req.user_id)

        if req.type == "debit" and user["balance"] < req.amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance for debit",
            )

        if req.type == "credit":
            user["balance"] += req.amount
            user["total_credited"] += req.amount
        else:
            user["balance"] -= req.amount
            user["total_debited"] += req.amount

        user["transaction_count"] += 1
        _record_rate_limit(req.user_id)

        result = TransactionResponse(
            success=True,
            message=f"{req.type.capitalize()} of {req.amount} successful",
            balance=user["balance"],
            transaction_id=req.transaction_id,
        )
        store.transactions[req.transaction_id] = result.model_dump()
        return result


@app.get("/summary/{user_id}", response_model=UserSummary)
async def get_summary(user_id: str):
    if user_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")

    user = store.users[user_id]
    age_days = int(
        (time.time() - user["created_at"].timestamp()) / 86400
    )

    return UserSummary(
        user_id=user_id,
        balance=user["balance"],
        total_credited=user["total_credited"],
        total_debited=user["total_debited"],
        transaction_count=user["transaction_count"],
        account_age_days=age_days,
    )


@app.get("/ranking")
async def get_ranking():
    return compute_rankings(store.users)
