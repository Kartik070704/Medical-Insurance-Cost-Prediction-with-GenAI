# Data Dictionary

| Column | Type | Description |
| --- | --- | --- |
| `age` | Numeric | Age of the insured person in years. |
| `sex` | Categorical | Gender of the insured person. |
| `bmi` | Numeric | Body Mass Index, used as a health risk indicator. |
| `children` | Numeric | Number of dependents covered by the insurance plan. |
| `smoker` | Categorical | Whether the person is a smoker. |
| `region` | Categorical | Residential region of the insured person. |
| `income` | Numeric | Annual income value present in the dataset. |
| `exercise_frequency` | Numeric | Frequency of exercise, represented as a numeric count. |
| `chronic_disease` | Categorical | Whether the person has a chronic disease. |
| `alcohol_consumption` | Numeric | Alcohol consumption level represented numerically. |
| `charges` | Numeric | Medical insurance charge amount. This is the target variable. |

## Target Variable

The model predicts `charges`, making this a supervised regression problem.

## Feature Groups

Numeric features:

- `age`
- `bmi`
- `children`
- `income`
- `exercise_frequency`
- `alcohol_consumption`

Categorical features:

- `sex`
- `smoker`
- `region`
- `chronic_disease`

