from pathlib import Path

from config import MODELS_DIR, PLOTS_DIR, REPORTS_DIR, ROOT_DIR


REQUIRED_FILES = [
    ROOT_DIR / "combined_medical_insurance_dataset_10k.csv",
    ROOT_DIR / "README.md",
    ROOT_DIR / "PROJECT_PLAN.md",
    ROOT_DIR / "DATA_DICTIONARY.md",
    ROOT_DIR / "FINAL_REPORT.md",
    ROOT_DIR / "PRESENTATION_OUTLINE.md",
    ROOT_DIR / "VIVA_QUESTIONS.md",
    ROOT_DIR / "requirements.txt",
    ROOT_DIR / "Procfile",
    ROOT_DIR / "render.yaml",
    ROOT_DIR / ".env.example",
    ROOT_DIR / "DEPLOYMENT.md",
    ROOT_DIR / "schema.sql",
    ROOT_DIR / "app.py",
    ROOT_DIR / "run_ui.ps1",
    ROOT_DIR / "setup_env.ps1",
    ROOT_DIR / "templates" / "index.html",
    ROOT_DIR / "static" / "style.css",
    ROOT_DIR / "static" / "app.js",
    ROOT_DIR / "src" / "data_profile.py",
    ROOT_DIR / "src" / "eda.py",
    ROOT_DIR / "src" / "train.py",
    ROOT_DIR / "src" / "tune_models.py",
    ROOT_DIR / "src" / "predict.py",
    ROOT_DIR / "src" / "run_all.py",
    ROOT_DIR / "src" / "database.py",
    ROOT_DIR / "src" / "env_loader.py",
    ROOT_DIR / "src" / "grok_reasoning.py",
    ROOT_DIR / "src" / "check_integrations.py",
    MODELS_DIR / "insurance_cost_model.joblib",
    MODELS_DIR / "tuned_insurance_cost_model.joblib",
    REPORTS_DIR / "data_profile.md",
    REPORTS_DIR / "model_comparison.csv",
    REPORTS_DIR / "tuned_model_comparison.csv",
    REPORTS_DIR / "metrics.json",
    REPORTS_DIR / "tuned_metrics.json",
    REPORTS_DIR / "feature_importance.csv",
    REPORTS_DIR / "group_charge_summary.csv",
    PLOTS_DIR / "charges_distribution.png",
    PLOTS_DIR / "correlation_heatmap.png",
    PLOTS_DIR / "actual_vs_predicted.png",
    PLOTS_DIR / "feature_importance.png",
    PLOTS_DIR / "tuned_model_comparison.png",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]

    if missing:
        print("Project validation failed. Missing files:")
        for path in missing:
            print(f"- {path.relative_to(ROOT_DIR)}")
        raise SystemExit(1)

    print("Project validation passed. Required non-UI deliverables are present.")


if __name__ == "__main__":
    main()
