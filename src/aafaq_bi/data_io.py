from __future__ import annotations

from pathlib import Path
import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    """Read a UTF-8 CSV file with a clear error message."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    """Write a dataframe as UTF-8 CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")


def write_latex_table(df: pd.DataFrame, path: str | Path, caption: str, label: str) -> None:
    """Write a small LaTeX table snippet."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    latex = df.to_latex(index=False, escape=False, caption=caption, label=label)
    path.write_text(latex, encoding="utf-8")
