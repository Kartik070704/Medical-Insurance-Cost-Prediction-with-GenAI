# Medical Insurance Cost Prediction Using Machine Learning

## Abstract

This project presents a machine learning approach for predicting medical insurance charges using demographic, lifestyle, and health-related attributes. The dataset contains 10,000 records with features such as age, BMI, smoking status, income, exercise frequency, chronic disease status, and alcohol consumption. Multiple regression models were trained and compared using MAE, RMSE, R2 score, and MAPE. The final system includes data profiling, exploratory analysis, model comparison, tuned model selection, saved model artifacts, and a command-line prediction workflow.

## Introduction

Medical insurance cost estimation is an important problem for both insurance providers and customers. Traditional pricing can be difficult to understand because many health and lifestyle factors interact with one another. Machine learning provides a practical way to learn these patterns from historical data and estimate likely insurance charges for new cases.

## Problem Statement

The goal of this project is to predict medical insurance charges from user attributes. Since the target variable is continuous, the task is treated as a supervised regression problem.

## Objectives

- Study the dataset and identify important variables.
- Perform exploratory data analysis and summarize major patterns.
- Preprocess numeric and categorical features.
- Train multiple regression models.
- Tune selected models using cross-validation.
- Evaluate the final model using standard regression metrics.
- Save the trained model for future prediction.

## Dataset Description

The dataset used in this project is `combined_medical_insurance_dataset_10k.csv`. It contains 10,000 records and 11 columns. The target variable is `charges`. The input variables include demographic features, health indicators, and lifestyle-related attributes.

## Methodology

The project follows a structured machine learning pipeline:

1. Load the dataset.
2. Check dataset shape, missing values, duplicates, and statistical summaries.
3. Generate exploratory plots and group-level charge summaries.
4. Split the data into training and testing sets.
5. Apply preprocessing using standard scaling for numeric variables where required and one-hot encoding for categorical variables.
6. Train baseline models.
7. Tune selected models using grid search with cross-validation.
8. Compare models using test-set metrics.
9. Save the best model and prediction samples.

## Models Used

- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Evaluation Metrics

- Mean Absolute Error measures average absolute prediction error.
- Root Mean Squared Error penalizes larger errors more strongly.
- R2 score measures explained variance.
- Mean Absolute Percentage Error shows average percentage error.

## Implementation

The project is implemented in Python using pandas, NumPy, scikit-learn, matplotlib, and joblib. The main scripts are:

- `src/data_profile.py` for dataset profiling.
- `src/eda.py` for exploratory analysis.
- `src/train.py` for baseline model training.
- `src/tune_models.py` for cross-validated hyperparameter tuning.
- `src/predict.py` for command-line prediction.
- `src/run_all.py` for running the full non-UI pipeline.

## Results

The baseline model results are stored in `reports/model_comparison.csv`. Tuned model results are stored in `reports/tuned_model_comparison.csv`. The final selected model is saved in `models/`.

## Conclusion

The project demonstrates that machine learning can predict medical insurance charges with strong accuracy using structured tabular data. The work includes data analysis, preprocessing, model training, model comparison, hyperparameter tuning, and reusable prediction.

## Future Scope

- Use a larger real-world dataset from insurance providers.
- Add more medical history and claim history variables.
- Apply advanced explainability techniques.
- Deploy the trained model through a web or mobile interface.
- Add monitoring for model drift over time.

