import json

import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_PATH, PLOTS_DIR, REPORTS_DIR, TARGET_COLUMN


def save_bar(series: pd.Series, title: str, output_path) -> None:
    counts = series.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    counts.plot(kind="bar", ax=ax, color="#2f6f73")
    ax.set_title(title)
    ax.set_xlabel(series.name)
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    PLOTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": df.isna().sum().astype(int).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "target": TARGET_COLUMN,
        "target_summary": df[TARGET_COLUMN].describe().round(2).to_dict(),
    }

    numeric_summary = df.select_dtypes(include="number").describe().round(2)
    categorical_summary = {
        col: df[col].value_counts().to_dict()
        for col in df.select_dtypes(exclude="number").columns
    }

    (REPORTS_DIR / "data_profile.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    with (REPORTS_DIR / "data_profile.md").open("w", encoding="utf-8") as file:
        file.write("# Data Profile\n\n")
        file.write(f"- Rows: {summary['rows']}\n")
        file.write(f"- Columns: {summary['columns']}\n")
        file.write(f"- Target variable: `{TARGET_COLUMN}`\n")
        file.write(f"- Duplicate rows: {summary['duplicate_rows']}\n\n")
        file.write("## Missing Values\n\n")
        file.write(pd.Series(summary["missing_values"]).to_markdown())
        file.write("\n\n## Numeric Summary\n\n")
        file.write(numeric_summary.to_markdown())
        file.write("\n\n## Categorical Summary\n\n")
        for col, counts in categorical_summary.items():
            file.write(f"### {col}\n\n")
            file.write(pd.Series(counts).to_markdown())
            file.write("\n\n")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df[TARGET_COLUMN], bins=40, color="#2f6f73", edgecolor="white")
    ax.set_title("Insurance Charges Distribution")
    ax.set_xlabel("Charges")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "charges_distribution.png", dpi=160)
    plt.close(fig)

    save_bar(df["smoker"], "Smoker Distribution", PLOTS_DIR / "smoker_distribution.png")
    save_bar(df["region"], "Region Distribution", PLOTS_DIR / "region_distribution.png")

    corr = df.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="viridis")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Numeric Feature Correlation")
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "correlation_heatmap.png", dpi=160)
    plt.close(fig)

    print("Data profile saved to reports/data_profile.md")


if __name__ == "__main__":
    main()

