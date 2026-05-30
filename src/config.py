from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "combined_medical_insurance_dataset_10k.csv"
MODELS_DIR = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
PLOTS_DIR = ROOT_DIR / "plots"

TARGET_COLUMN = "charges"
RANDOM_STATE = 42
TEST_SIZE = 0.2

NUMERIC_FEATURES = [
    "age",
    "bmi",
    "children",
    "income",
    "exercise_frequency",
    "alcohol_consumption",
]

CATEGORICAL_FEATURES = [
    "sex",
    "smoker",
    "region",
    "chronic_disease",
]

