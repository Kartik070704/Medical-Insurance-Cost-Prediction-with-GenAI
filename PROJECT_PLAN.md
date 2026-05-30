# Medical Insurance Cost Prediction - Final Year Project Plan

## Project Title

Medical Insurance Cost Prediction Using Machine Learning

## Problem Statement

Health insurance pricing depends on multiple demographic, lifestyle, and medical factors. The objective of this project is to build a machine learning system that predicts estimated medical insurance charges from user attributes such as age, BMI, smoking status, income, chronic disease status, exercise frequency, and alcohol consumption.

## Objectives

- Analyze the medical insurance dataset and identify important cost-driving factors.
- Preprocess numeric and categorical features for machine learning.
- Train and compare multiple regression models.
- Select the best model using MAE, RMSE, R2 score, and MAPE.
- Build a reusable prediction pipeline that can estimate insurance charges for new users.
- Build a local web interface for collecting user details and prediction inputs.
- Present model insights using visualizations and feature importance.

## Dataset

- File: `combined_medical_insurance_dataset_10k.csv`
- Records: 10,000
- Target variable: `charges`
- Input features: `age`, `sex`, `bmi`, `children`, `smoker`, `region`, `income`, `exercise_frequency`, `chronic_disease`, `alcohol_consumption`

## Proposed Methodology

1. Data collection and understanding
2. Exploratory data analysis
3. Missing value and duplicate checks
4. Feature preprocessing
5. Train-test split
6. Model training
7. Model comparison
8. Final model saving
9. Command-line prediction workflow
10. Web UI prediction workflow
11. Report and presentation preparation

## Models To Compare

- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Evaluation Metrics

- Mean Absolute Error
- Root Mean Squared Error
- R2 Score
- Mean Absolute Percentage Error

## Expected Outputs

- Trained model file in `models/`
- Dataset profile in `reports/`
- Model comparison table in `reports/`
- Prediction samples in `reports/`
- Evaluation plots in `plots/`
- Command-line prediction script
- Flask-based web prediction UI
- Hyperparameter tuning results
- Data dictionary, report draft, presentation outline, and viva preparation file

## Suggested Final-Year Enhancements

- Add model explainability using SHAP if allowed by your environment.
- Add a database or CSV logging feature for predicted cases.
- Compare more algorithms such as XGBoost or LightGBM if installation is available.
- Deploy the model through an application in a later UI phase.

## Suggested Report Chapters

1. Introduction
2. Literature Review
3. System Analysis
4. Dataset Description
5. Methodology
6. Implementation
7. Results and Discussion
8. Conclusion and Future Scope
