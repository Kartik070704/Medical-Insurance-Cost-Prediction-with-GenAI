import json
import os
from typing import Any


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS insurance_predictions (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    full_name TEXT,
    email TEXT,
    phone TEXT,
    birth_date DATE,
    age INTEGER,
    sex TEXT,
    bmi NUMERIC(6, 2),
    children INTEGER,
    smoker TEXT,
    region TEXT,
    income NUMERIC(12, 2),
    exercise_frequency INTEGER,
    chronic_disease TEXT,
    alcohol_consumption INTEGER,
    predicted_cost NUMERIC(12, 2) NOT NULL,
    model_name TEXT NOT NULL,
    reasoning_model TEXT,
    genai_reasoning TEXT,
    model_inputs JSONB,
    model_metrics JSONB
);
"""


def database_url() -> str | None:
    return os.getenv("DATABASE_URL")


def database_enabled() -> bool:
    return bool(database_url())


def get_connection():
    try:
        import psycopg
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "DATABASE_URL is set, but psycopg is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    return psycopg.connect(database_url(), autocommit=True)


def init_database() -> tuple[bool, str]:
    if not database_enabled():
        return False, "DATABASE_URL is not set; Neon storage is disabled."

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
    return True, "Neon database table is ready."


def save_prediction(
    personal: dict[str, Any],
    inputs: dict[str, Any],
    prediction: float,
    model_name: str,
    reasoning_model: str,
    reasoning: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    if not database_enabled():
        return {"saved": False, "reason": "DATABASE_URL is not set."}

    init_database()

    sql = """
        INSERT INTO insurance_predictions (
            full_name, email, phone, birth_date, age, sex, bmi, children,
            smoker, region, income, exercise_frequency, chronic_disease,
            alcohol_consumption, predicted_cost, model_name, reasoning_model,
            genai_reasoning, model_inputs, model_metrics
        )
        VALUES (
            %(full_name)s, %(email)s, %(phone)s, NULLIF(%(birth_date)s, '')::date,
            %(age)s, %(sex)s, %(bmi)s, %(children)s, %(smoker)s, %(region)s,
            %(income)s, %(exercise_frequency)s, %(chronic_disease)s,
            %(alcohol_consumption)s, %(predicted_cost)s, %(model_name)s,
            %(reasoning_model)s, %(genai_reasoning)s, %(model_inputs)s::jsonb,
            %(model_metrics)s::jsonb
        )
        RETURNING id;
    """

    params = {
        **personal,
        **inputs,
        "predicted_cost": round(float(prediction), 2),
        "model_name": model_name,
        "reasoning_model": reasoning_model,
        "genai_reasoning": reasoning,
        "model_inputs": json.dumps(inputs),
        "model_metrics": json.dumps(metrics),
    }

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            row_id = cur.fetchone()[0]

    return {"saved": True, "id": row_id}

