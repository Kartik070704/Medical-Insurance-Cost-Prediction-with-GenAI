# Presentation Outline

## Slide 1: Title

Medical Insurance Cost Prediction Using Machine Learning

## Slide 2: Introduction

- Insurance charges depend on demographic, health, and lifestyle factors.
- Manual estimation can be inconsistent and difficult to explain.
- Machine learning can learn cost patterns from historical data.

## Slide 3: Problem Statement

Predict medical insurance charges from user attributes using supervised regression.

## Slide 4: Objectives

- Analyze the dataset.
- Build preprocessing and training pipeline.
- Compare regression models.
- Tune the best-performing models.
- Save a reusable prediction model.

## Slide 5: Dataset

- 10,000 records
- 10 input features
- Target variable: `charges`

## Slide 6: Methodology

- Data profiling
- Exploratory data analysis
- Feature preprocessing
- Train-test split
- Model training
- Hyperparameter tuning
- Model evaluation

## Slide 7: Models Used

- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Slide 8: Evaluation Metrics

- MAE
- RMSE
- R2 Score
- MAPE

## Slide 9: Results

Use `reports/model_comparison.csv` and `reports/tuned_model_comparison.csv` to fill the final values.

## Slide 10: Feature Importance

Use `plots/feature_importance.png` and `reports/feature_importance.csv`.

## Slide 11: Conclusion

- The system predicts insurance charges accurately.
- The model can assist in quick estimation.
- The pipeline is reusable and extendable.

## Slide 12: Future Scope

- Add more real-world medical features.
- Include explainability tools.
- Add deployment in a future phase.

