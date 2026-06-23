"""
Ranking score combines four factors (each min-max normalized across all users):
  - 40% balance
  - 30% transaction count
  - 20% account age (days)
  - 10% consistency ratio: credited / (credited + debited + 1)
Higher score = better rank.
"""

from datetime import datetime, timezone

from models import RankedUser


def _min_max_normalize(values: list[float]) -> list[float]:
    """Scale values to [0, 1]. Equal values all get 0.5; single value gets 1.0."""
    if not values:
        return []
    if len(values) == 1:
        return [1.0]
    lo, hi = min(values), max(values)
    if lo == hi:
        return [0.5] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


def compute_rankings(users_dict: dict) -> list[RankedUser]:
    if not users_dict:
        return []

    now = datetime.now(timezone.utc)
    user_ids = list(users_dict.keys())

    balances = [users_dict[uid]["balance"] for uid in user_ids]
    tx_counts = [users_dict[uid]["transaction_count"] for uid in user_ids]
    ages = [
        (now - users_dict[uid]["created_at"]).total_seconds() / 86400
        for uid in user_ids
    ]
    consistency = [
        users_dict[uid]["total_credited"]
        / (users_dict[uid]["total_credited"] + users_dict[uid]["total_debited"] + 1)
        for uid in user_ids
    ]

    norm_balance = _min_max_normalize(balances)
    norm_tx = _min_max_normalize([float(c) for c in tx_counts])
    norm_age = _min_max_normalize(ages)
    norm_consistency = _min_max_normalize(consistency)

    scored = []
    for i, uid in enumerate(user_ids):
        score = (
            0.4 * norm_balance[i]
            + 0.3 * norm_tx[i]
            + 0.2 * norm_age[i]
            + 0.1 * norm_consistency[i]
        )
        scored.append(
            {
                "user_id": uid,
                "score": round(score, 4),
                "balance": balances[i],
                "transaction_count": tx_counts[i],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)

    return [
        RankedUser(rank=rank, **entry)
        for rank, entry in enumerate(scored, start=1)
    ]
