import argparse

import joblib
import pandas as pd

from config import MODELS_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict medical insurance charges.")
    parser.add_argument(
        "--model_file",
        default=None,
        help="Optional model filename inside models/. Defaults to tuned model if available.",
    )
    parser.add_argument("--age", type=int, required=True)
    parser.add_argument("--sex", choices=["male", "female"], required=True)
    parser.add_argument("--bmi", type=float, required=True)
    parser.add_argument("--children", type=int, required=True)
    parser.add_argument("--smoker", choices=["yes", "no"], required=True)
    parser.add_argument(
        "--region",
        choices=["northeast", "northwest", "southeast", "southwest"],
        required=True,
    )
    parser.add_argument("--income", type=float, required=True)
    parser.add_argument("--exercise_frequency", type=int, required=True)
    parser.add_argument("--chronic_disease", choices=["yes", "no"], required=True)
    parser.add_argument("--alcohol_consumption", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_file = args.model_file
    if model_file is None:
        tuned_model = MODELS_DIR / "tuned_insurance_cost_model.joblib"
        model_file = tuned_model.name if tuned_model.exists() else "insurance_cost_model.joblib"

    model_path = MODELS_DIR / model_file
    model_package = joblib.load(model_path)
    model = model_package["model"]

    input_values = vars(args)
    input_values.pop("model_file")
    row = pd.DataFrame([input_values])
    prediction = model.predict(row)[0]

    print(f"Model: {model_package['model_name']}")
    print(f"Model file: {model_path.name}")
    print(f"Predicted insurance charges: {prediction:.2f}")


if __name__ == "__main__":
    main()
