import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from config import (
    DATA_PATH,
    MODELS_DIR,
    PLOTS_DIR,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET_COLUMN,
    TEST_SIZE,
)
from train import make_preprocessor


def metrics(y_true, y_pred) -> dict:
    mse = mean_squared_error(y_true, y_pred)
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(np.sqrt(mse)), 2),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "mape_percent": round(
            float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100),
            2,
        ),
    }


def search_spaces() -> dict:
    return {
        "tuned_ridge": {
            "estimator": Pipeline(
                steps=[
                    ("preprocessor", make_preprocessor(scale_numeric=True)),
                    ("model", Ridge(random_state=RANDOM_STATE)),
                ]
            ),
            "params": {
                "model__alpha": [0.1, 1.0, 10.0, 25.0, 50.0],
            },
        },
        "tuned_random_forest": {
            "estimator": Pipeline(
                steps=[
                    ("preprocessor", make_preprocessor(scale_numeric=False)),
                    (
                        "model",
                        RandomForestRegressor(
                            random_state=RANDOM_STATE,
                            n_jobs=-1,
                        ),
                    ),
                ]
            ),
            "params": {
                "model__n_estimators": [150, 250],
                "model__max_depth": [10, 14, None],
                "model__min_samples_leaf": [2, 4],
            },
        },
        "tuned_gradient_boosting": {
            "estimator": Pipeline(
                steps=[
                    ("preprocessor", make_preprocessor(scale_numeric=False)),
                    ("model", GradientBoostingRegressor(random_state=RANDOM_STATE)),
                ]
            ),
            "params": {
                "model__n_estimators": [150, 250],
                "model__learning_rate": [0.03, 0.05],
                "model__max_depth": [2, 3],
            },
        },
    }


def plot_model_comparison(results: pd.DataFrame) -> None:
    ordered = results.sort_values("rmse", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(ordered["model"], ordered["rmse"], color="#2f6f73")
    ax.set_title("Tuned Model RMSE Comparison")
    ax.set_xlabel("Model")
    ax.set_ylabel("RMSE")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "tuned_model_comparison.png", dpi=160)
    plt.close(fig)


def main() -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    x = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    result_rows = []
    best_estimators = {}
    best_params = {}

    for model_name, spec in search_spaces().items():
        print(f"Running grid search for {model_name}...")
        grid = GridSearchCV(
            estimator=spec["estimator"],
            param_grid=spec["params"],
            scoring="neg_root_mean_squared_error",
            cv=3,
            n_jobs=-1,
            refit=True,
        )
        grid.fit(x_train, y_train)
        predictions = grid.predict(x_test)
        row = metrics(y_test, predictions)
        row["model"] = model_name
        row["cv_rmse"] = round(float(-grid.best_score_), 2)
        result_rows.append(row)
        best_estimators[model_name] = grid.best_estimator_
        best_params[model_name] = grid.best_params_
        print(f"{model_name}: test RMSE={row['rmse']} CV RMSE={row['cv_rmse']}")

    results = pd.DataFrame(result_rows).sort_values("rmse")
    results.to_csv(REPORTS_DIR / "tuned_model_comparison.csv", index=False)

    best_model_name = results.iloc[0]["model"]
    best_model = best_estimators[best_model_name]
    best_predictions = best_model.predict(x_test)

    joblib.dump(
        {
            "model": best_model,
            "model_name": best_model_name,
            "features": list(x.columns),
            "target": TARGET_COLUMN,
            "metrics": results.iloc[0].to_dict(),
            "best_params": best_params[best_model_name],
        },
        MODELS_DIR / "tuned_insurance_cost_model.joblib",
    )

    payload = {
        "best_tuned_model": best_model_name,
        "best_tuned_metrics": results.iloc[0].to_dict(),
        "best_params": best_params,
        "all_tuned_models": results.to_dict(orient="records"),
    }
    (REPORTS_DIR / "tuned_metrics.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    prediction_rows = x_test.copy()
    prediction_rows["actual_charges"] = y_test
    prediction_rows["predicted_charges"] = np.round(best_predictions, 2)
    prediction_rows["absolute_error"] = np.round(
        np.abs(prediction_rows["actual_charges"] - prediction_rows["predicted_charges"]),
        2,
    )
    prediction_rows.head(50).to_csv(
        REPORTS_DIR / "tuned_prediction_sample.csv",
        index=False,
    )

    plot_model_comparison(results)
    print(f"Best tuned model saved: {best_model_name}")


if __name__ == "__main__":
    main()

