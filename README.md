# Medical Insurance Cost Prediction

This project predicts medical insurance charges using demographic, lifestyle, and health-related features. It is structured as a final-year machine learning project with data profiling, model training, evaluation artifacts, and a reusable prediction script.

## Dataset

The project uses:

```text
combined_medical_insurance_dataset_10k.csv
```

Target column:

```text
charges
```

## Project Structure

```text
.
+-- combined_medical_insurance_dataset_10k.csv
+-- models/
+-- plots/
+-- reports/
+-- src/
|   +-- config.py
|   +-- data_profile.py
|   +-- eda.py
|   +-- predict.py
|   +-- run_all.py
|   +-- train.py
|   +-- tune_models.py
|   +-- validate_project.py
+-- static/
+-- templates/
+-- app.py
+-- DATA_DICTIONARY.md
+-- FINAL_REPORT.md
+-- PRESENTATION_OUTLINE.md
+-- PROJECT_PLAN.md
+-- README.md
+-- VIVA_QUESTIONS.md
+-- requirements.txt
```

## How To Run

Create the dataset profile:

```bash
python src/data_profile.py
```

Train and evaluate models:

```bash
python src/train.py
```

Run EDA:

```bash
python src/eda.py
```

Run hyperparameter tuning:

```bash
python src/tune_models.py
```

Run the full non-UI pipeline:

```bash
python src/run_all.py
```

Start the web UI:

```bash
python app.py
```

On Windows PowerShell, you can also run:

```powershell
./run_ui.ps1
```

Create a local `.env` file for Neon and Groq Cloud:

```powershell
./setup_env.ps1
```

Check integrations after creating `.env`:

```powershell
python src/check_integrations.py
```

Then open:

```text
http://127.0.0.1:5000
```

Do not open `templates/index.html` directly from the browser. The prediction endpoint needs the Flask server.

Validate expected project artifacts:

```bash
python src/validate_project.py
```

Make a prediction:

```bash
python src/predict.py --age 35 --sex male --bmi 28.4 --children 2 --smoker no --region northwest --income 75000 --exercise_frequency 3 --chronic_disease no --alcohol_consumption 2
```

## Outputs

- `reports/data_profile.md`
- `reports/model_comparison.csv`
- `reports/tuned_model_comparison.csv`
- `reports/metrics.json`
- `reports/tuned_metrics.json`
- `reports/prediction_sample.csv`
- `reports/tuned_prediction_sample.csv`
- `reports/feature_importance.csv`
- `reports/group_charge_summary.csv`
- `plots/charges_distribution.png`
- `plots/correlation_heatmap.png`
- `plots/actual_vs_predicted.png`
- `plots/residuals.png`
- `plots/feature_importance.png`
- `plots/tuned_model_comparison.png`
- `models/insurance_cost_model.joblib`
- `models/tuned_insurance_cost_model.joblib`

## Web UI

The Flask UI uses a three-step wizard:

- Personal information
- Insurance input features
- Prediction result

The UI loads the tuned model from `models/tuned_insurance_cost_model.joblib` when available.

The prediction result also includes:

- AI-generated cost reasoning using the Grok API when `XAI_API_KEY` or `GROK_API_KEY` is configured.
- Neon Postgres storage when `DATABASE_URL` is configured.

## Deployment

Deployment instructions are available in:

```text
DEPLOYMENT.md
```

Required deployment environment variables:

```text
XAI_API_KEY or GROQ_API_KEY
XAI_MODEL or GROQ_MODEL
DATABASE_URL
```

## Current Models

- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Evaluation Metrics

- MAE
- RMSE
- R2 Score
- MAPE
