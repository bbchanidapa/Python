from typing import Any

from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text

from app.config import settings
from app.database import engine

app = FastAPI(title="FastAPI DB Connection", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/db-check")
def db_check() -> dict[str, str]:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"database": "connected"}


@app.get("/checkout_orders")
def get_checkout_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[dict[str, Any]]:
    stmt = text(
        """
        SELECT
            o.*,
            u.id AS user_ref_id,
            u.firstname AS user_firstname,
            u.lastname AS user_lastname,
            u.email AS user_email,
            u.role AS user_role,
            u.is_active AS user_is_active
        FROM users.checkout_orders AS o
        LEFT JOIN users.users AS u
            ON u.id = o.user_id
        ORDER BY o.created_at DESC NULLS LAST
        OFFSET :skip
        LIMIT :limit
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(stmt, {"skip": skip, "limit": limit}).mappings().all()
    payload: list[dict[str, Any]] = []
    for row in rows:
        row_dict = dict(row)
        user_ref_id = row_dict.pop("user_ref_id", None)
        user_info = {
            "firstname": row_dict.pop("user_firstname", None),
            "lastname": row_dict.pop("user_lastname", None),
            "email": row_dict.pop("user_email", None),
            "role": row_dict.pop("user_role", None),
            "is_active": row_dict.pop("user_is_active", None),
        }
        row_dict["user"] = user_info if user_ref_id is not None else None
        payload.append(jsonable_encoder(row_dict))
    return payload
