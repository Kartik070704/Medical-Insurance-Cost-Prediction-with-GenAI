import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_PATH, PLOTS_DIR, REPORTS_DIR, TARGET_COLUMN


def save_group_summary(df: pd.DataFrame) -> None:
    group_columns = ["sex", "smoker", "region", "chronic_disease", "children"]
    rows = []

    for column in group_columns:
        grouped = (
            df.groupby(column)[TARGET_COLUMN]
            .agg(["count", "mean", "median", "std", "min", "max"])
            .round(2)
            .reset_index()
        )
        grouped.insert(0, "feature", column)
        grouped = grouped.rename(columns={column: "category"})
        rows.append(grouped)

    summary = pd.concat(rows, ignore_index=True)
    summary.to_csv(REPORTS_DIR / "group_charge_summary.csv", index=False)


def save_scatter(df: pd.DataFrame, x_column: str, output_name: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = df["smoker"].map({"yes": "#c44949", "no": "#2f6f73"})
    ax.scatter(df[x_column], df[TARGET_COLUMN], alpha=0.45, c=colors)
    ax.set_title(f"{x_column.replace('_', ' ').title()} vs Insurance Charges")
    ax.set_xlabel(x_column.replace("_", " ").title())
    ax.set_ylabel("Charges")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / output_name, dpi=160)
    plt.close(fig)


def save_boxplot(df: pd.DataFrame, column: str, output_name: str) -> None:
    categories = sorted(df[column].unique())
    data = [df.loc[df[column] == category, TARGET_COLUMN] for category in categories]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot(data, tick_labels=categories, patch_artist=True)
    ax.set_title(f"Charges by {column.replace('_', ' ').title()}")
    ax.set_xlabel(column.replace("_", " ").title())
    ax.set_ylabel("Charges")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / output_name, dpi=160)
    plt.close(fig)


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    save_group_summary(df)

    save_scatter(df, "age", "age_vs_charges.png")
    save_scatter(df, "bmi", "bmi_vs_charges.png")
    save_scatter(df, "income", "income_vs_charges.png")
    save_scatter(df, "exercise_frequency", "exercise_vs_charges.png")

    save_boxplot(df, "smoker", "charges_by_smoker.png")
    save_boxplot(df, "chronic_disease", "charges_by_chronic_disease.png")
    save_boxplot(df, "region", "charges_by_region.png")

    print("EDA artifacts saved to reports/ and plots/")


if __name__ == "__main__":
    main()
