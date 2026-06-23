"""In-memory data store — resets when the server restarts."""

from datetime import datetime, timezone

users: dict = {}  # user_id -> user data dict
transactions: dict = {}  # transaction_id -> cached TransactionResponse dict
user_locks: dict = {}  # user_id -> asyncio.Lock()
rate_limit: dict = {}  # user_id -> list of timestamps (float, unix time)


def ensure_user(user_id: str) -> dict:
    """Create a user profile on first sight with zero balance."""
    if user_id not in users:
        users[user_id] = {
            "balance": 0.0,
            "total_credited": 0.0,
            "total_debited": 0.0,
            "transaction_count": 0,
            "created_at": datetime.now(timezone.utc),
        }
    return users[user_id]
