import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import (
    CATEGORICAL_FEATURES,
    DATA_PATH,
    MODELS_DIR,
    NUMERIC_FEATURES,
    PLOTS_DIR,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET_COLUMN,
    TEST_SIZE,
)


def make_one_hot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def make_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
            ("categorical", make_one_hot_encoder(), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def regression_metrics(y_true, y_pred) -> dict:
    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100)
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "mape_percent": round(mape, 2),
    }


def build_models() -> dict:
    return {
        "ridge_regression": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor(scale_numeric=True)),
                ("model", Ridge(alpha=1.0, random_state=RANDOM_STATE)),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor(scale_numeric=False)),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=250,
                        max_depth=14,
                        min_samples_leaf=3,
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "gradient_boosting": Pipeline(
            steps=[
                ("preprocessor", make_preprocessor(scale_numeric=False)),
                (
                    "model",
                    GradientBoostingRegressor(
                        n_estimators=250,
                        learning_rate=0.05,
                        max_depth=3,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def plot_actual_vs_predicted(y_true, y_pred) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_true, y_pred, alpha=0.45, color="#2f6f73")
    lower = min(y_true.min(), y_pred.min())
    upper = max(y_true.max(), y_pred.max())
    ax.plot([lower, upper], [lower, upper], color="#c44949", linewidth=2)
    ax.set_title("Actual vs Predicted Insurance Charges")
    ax.set_xlabel("Actual Charges")
    ax.set_ylabel("Predicted Charges")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "actual_vs_predicted.png", dpi=160)
    plt.close(fig)


def plot_residuals(y_true, y_pred) -> None:
    residuals = y_true - y_pred
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(y_pred, residuals, alpha=0.45, color="#2f6f73")
    ax.axhline(0, color="#c44949", linewidth=2)
    ax.set_title("Residual Plot")
    ax.set_xlabel("Predicted Charges")
    ax.set_ylabel("Residuals")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "residuals.png", dpi=160)
    plt.close(fig)


def plot_permutation_importance(model, x_test, y_test) -> None:
    result = permutation_importance(
        model,
        x_test,
        y_test,
        n_repeats=8,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        scoring="neg_root_mean_squared_error",
    )

    importance = pd.DataFrame(
        {
            "feature": x_test.columns,
            "importance": result.importances_mean,
        }
    ).sort_values("importance", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(importance["feature"], importance["importance"], color="#2f6f73")
    ax.set_title("Permutation Feature Importance")
    ax.set_xlabel("Mean importance")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "feature_importance.png", dpi=160)
    plt.close(fig)

    importance.sort_values("importance", ascending=False).to_csv(
        REPORTS_DIR / "feature_importance.csv",
        index=False,
    )


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

    results = []
    trained_models = {}

    for model_name, model in build_models().items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        metrics = regression_metrics(y_test, predictions)
        metrics["model"] = model_name
        results.append(metrics)
        trained_models[model_name] = model
        print(f"{model_name}: RMSE={metrics['rmse']} R2={metrics['r2']}")

    comparison = pd.DataFrame(results).sort_values("rmse")
    comparison.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    best_model_name = comparison.iloc[0]["model"]
    best_model = trained_models[best_model_name]
    best_predictions = best_model.predict(x_test)

    model_package = {
        "model": best_model,
        "model_name": best_model_name,
        "features": list(x.columns),
        "target": TARGET_COLUMN,
        "metrics": comparison.iloc[0].to_dict(),
    }
    joblib.dump(model_package, MODELS_DIR / "insurance_cost_model.joblib")

    sample_predictions = x_test.copy()
    sample_predictions["actual_charges"] = y_test
    sample_predictions["predicted_charges"] = np.round(best_predictions, 2)
    sample_predictions["absolute_error"] = np.round(
        np.abs(sample_predictions["actual_charges"] - sample_predictions["predicted_charges"]),
        2,
    )
    sample_predictions.head(50).to_csv(REPORTS_DIR / "prediction_sample.csv", index=False)

    metrics_payload = {
        "best_model": best_model_name,
        "best_model_metrics": comparison.iloc[0].to_dict(),
        "all_models": comparison.to_dict(orient="records"),
    }
    (REPORTS_DIR / "metrics.json").write_text(
        json.dumps(metrics_payload, indent=2),
        encoding="utf-8",
    )

    plot_actual_vs_predicted(y_test.to_numpy(), best_predictions)
    plot_residuals(y_test.to_numpy(), best_predictions)
    plot_permutation_importance(best_model, x_test, y_test)

    print(f"Best model saved: {best_model_name}")
    print("Saved model to models/insurance_cost_model.joblib")


if __name__ == "__main__":
    main()

