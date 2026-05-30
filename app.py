import os
from datetime import date, datetime

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

from src.database import init_database, save_prediction
from src.env_loader import load_local_env
from src.grok_reasoning import generate_reasoning
from src.config import MODELS_DIR


load_local_env()
app = Flask(__name__)


FEATURE_COLUMNS = [
    "age",
    "sex",
    "bmi",
    "children",
    "smoker",
    "region",
    "income",
    "exercise_frequency",
    "chronic_disease",
    "alcohol_consumption",
]


def load_model_package() -> dict:
    tuned_model = MODELS_DIR / "tuned_insurance_cost_model.joblib"
    model_path = tuned_model if tuned_model.exists() else MODELS_DIR / "insurance_cost_model.joblib"
    return joblib.load(model_path)


MODEL_PACKAGE = load_model_package()
try:
    DATABASE_STATUS = init_database()
except Exception as exc:
    DATABASE_STATUS = (False, f"Database initialization failed: {exc}")


def calculate_age(birth_date: str) -> int | None:
    if not birth_date:
        return None

    born = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def clean_payload(payload: dict) -> tuple[dict, dict]:
    personal = {
        "full_name": payload.get("full_name", "").strip(),
        "email": payload.get("email", "").strip(),
        "phone": payload.get("phone", "").strip(),
        "birth_date": payload.get("birth_date", "").strip(),
    }

    model_inputs = {
        "age": int(payload.get("age") or calculate_age(personal["birth_date"]) or 0),
        "sex": payload["sex"],
        "bmi": float(payload["bmi"]),
        "children": int(payload["children"]),
        "smoker": payload["smoker"],
        "region": payload["region"],
        "income": float(payload["income"]),
        "exercise_frequency": int(payload["exercise_frequency"]),
        "chronic_disease": payload["chronic_disease"],
        "alcohol_consumption": int(payload["alcohol_consumption"]),
    }
    return personal, model_inputs


@app.route("/")
def index():
    return render_template("index.html", model_name=MODEL_PACKAGE["model_name"])


@app.post("/predict")
def predict():
    try:
        personal, model_inputs = clean_payload(request.get_json(force=True))
        row = pd.DataFrame([model_inputs], columns=FEATURE_COLUMNS)
        prediction = float(MODEL_PACKAGE["model"].predict(row)[0])
        metrics = MODEL_PACKAGE.get("metrics", {})
        reasoning, reasoning_model = generate_reasoning(
            personal=personal,
            inputs=model_inputs,
            prediction=prediction,
            metrics=metrics,
        )

        try:
            storage = save_prediction(
                personal=personal,
                inputs=model_inputs,
                prediction=prediction,
                model_name=MODEL_PACKAGE["model_name"],
                reasoning_model=reasoning_model,
                reasoning=reasoning,
                metrics=metrics,
            )
        except Exception as exc:
            storage = {"saved": False, "reason": str(exc)}

        return jsonify(
            {
                "ok": True,
                "prediction": round(prediction, 2),
                "formatted_prediction": f"{prediction:,.2f}",
                "model_name": MODEL_PACKAGE["model_name"],
                "reasoning_model": reasoning_model,
                "reasoning": reasoning,
                "storage": storage,
                "personal": personal,
                "inputs": model_inputs,
                "metrics": metrics,
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
