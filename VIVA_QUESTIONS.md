# Viva Questions and Answers

## 1. What type of machine learning problem is this?

This is a supervised regression problem because the target variable, `charges`, is continuous.

## 2. Why did you use one-hot encoding?

One-hot encoding converts categorical variables such as `sex`, `smoker`, `region`, and `chronic_disease` into numeric columns that machine learning models can process.

## 3. Why did you compare multiple models?

Different algorithms learn patterns differently. Comparing models helps select the approach that performs best on unseen test data.

## 4. What is RMSE?

RMSE is Root Mean Squared Error. It measures prediction error and penalizes larger mistakes more strongly than MAE.

## 5. What is R2 score?

R2 score measures how much variance in the target variable is explained by the model. A value closer to 1 indicates better performance.

## 6. Why use train-test split?

Train-test split allows the model to be trained on one part of the data and evaluated on unseen data, which helps estimate real-world performance.

## 7. What is hyperparameter tuning?

Hyperparameter tuning searches for the best model settings, such as regularization strength or tree depth, using validation performance.

## 8. What are the most important features?

The final feature importance values are generated in `reports/feature_importance.csv`. Typically, variables such as smoking status, BMI, age, and chronic disease can strongly influence insurance charges.

## 9. What are the limitations of this project?

The project depends on the quality and completeness of the available dataset. It does not include detailed medical history, previous claims, location-level healthcare cost differences, or hospital network information.

## 10. How can the project be improved?

It can be improved by using a larger real-world dataset, adding more medical features, applying advanced explainability tools, and deploying the model through an application.

