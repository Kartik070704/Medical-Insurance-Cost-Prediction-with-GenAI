from src.database import init_database
from src.env_loader import load_local_env
from src.grok_reasoning import generate_reasoning


def main() -> None:
    load_local_env()

    db_ok, db_message = init_database()
    print(f"Database: {'ready' if db_ok else 'disabled'} - {db_message}")

    reasoning, reasoning_model = generate_reasoning(
        personal={"full_name": "Integration Test"},
        inputs={
            "age": 35,
            "sex": "male",
            "bmi": 28.4,
            "children": 2,
            "smoker": "no",
            "region": "northwest",
            "income": 75000,
            "exercise_frequency": 3,
            "chronic_disease": "no",
            "alcohol_consumption": 2,
        },
        prediction=17096.63,
        metrics={"r2": 0.9626, "rmse": 1988.4, "mae": 1564.35},
    )

    print(f"Reasoning provider: {reasoning_model}")
    print(f"Reasoning preview: {reasoning[:220]}")


if __name__ == "__main__":
    main()

