from __future__ import annotations

import pandas as pd
from .schema import CASE_STUDY_CORE_COLUMNS, AAFAQ_COMPATIBLE_COLUMNS, ADHERENCE_COLUMNS, AAFAQ_COLUMNS


def missing_columns(df: pd.DataFrame, required: list[str]) -> list[str]:
    return [c for c in required if c not in df.columns]


def validate_case_study_schema(df: pd.DataFrame, require_aafaq_compatible: bool = True) -> dict:
    """Validate the case-study dataset schema and binary adherence indicators."""
    required = list(CASE_STUDY_CORE_COLUMNS)
    if require_aafaq_compatible:
        required += AAFAQ_COMPATIBLE_COLUMNS

    missing = missing_columns(df, required)
    invalid_binary = {}
    for col in ADHERENCE_COLUMNS:
        if col in df.columns:
            values = set(pd.Series(df[col]).dropna().unique().tolist())
            bad = sorted([v for v in values if v not in {0, 1, False, True}])
            if bad:
                invalid_binary[col] = bad

    empty_text = []
    for col in ["question_ar", "reference_answer_ar", "conditioned_answer_ar"]:
        if col in df.columns and df[col].isna().any():
            empty_text.append(col)

    return {
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "missing_columns": missing,
        "invalid_binary_columns": invalid_binary,
        "text_columns_with_missing_values": empty_text,
        "is_valid": not missing and not invalid_binary and not empty_text,
    }


def compare_aafaq_schema(aafaq_df: pd.DataFrame, case_df: pd.DataFrame) -> pd.DataFrame:
    """Compare original AAFAQ columns with the AAFAQ-compatible columns in the case-study file."""
    rows = []
    for col in AAFAQ_COLUMNS:
        case_col = f"AAFAQ_{col}"
        rows.append({
            "AAFAQ column": col,
            "present_in_aafaq": col in aafaq_df.columns,
            "case_study_column": case_col,
            "present_in_case_study": case_col in case_df.columns,
        })
    return pd.DataFrame(rows)
