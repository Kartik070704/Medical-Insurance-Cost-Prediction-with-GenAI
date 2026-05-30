import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(script_name: str) -> None:
    print(f"\n--- Running {script_name} ---", flush=True)
    subprocess.run(
        [sys.executable, str(ROOT / "src" / script_name)],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    run("data_profile.py")
    run("eda.py")
    run("train.py")
    run("tune_models.py")
    print("\nFull non-UI ML pipeline completed successfully.", flush=True)


if __name__ == "__main__":
    main()
