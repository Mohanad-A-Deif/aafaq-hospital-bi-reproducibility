from __future__ import annotations

import pandas as pd

CRITERION_MAP = {
    "Answer-form adherence": ("answer_form_adherent_without", "answer_form_adherent_with"),
    "Temporal adherence": ("temporal_adherent_without", "temporal_adherent_with"),
    "Purpose alignment": ("purpose_aligned_without", "purpose_aligned_with"),
}


def percent_mean(series: pd.Series) -> float:
    return round(float(series.mean() * 100.0), 1)


def compute_adherence_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for criterion, (without_col, with_col) in CRITERION_MAP.items():
        rows.append({
            "Criterion": criterion,
            "Without conditioning": percent_mean(df[without_col]),
            "With conditioning": percent_mean(df[with_col]),
            "Absolute gain": round(percent_mean(df[with_col]) - percent_mean(df[without_col]), 1),
        })
    return pd.DataFrame(rows)


def compute_overall_bi_adherence(df: pd.DataFrame, suffix: str = "with") -> float:
    if suffix == "with":
        cols = ["answer_form_adherent_with", "temporal_adherent_with", "purpose_aligned_with"]
    elif suffix == "without":
        cols = ["answer_form_adherent_without", "temporal_adherent_without", "purpose_aligned_without"]
    else:
        raise ValueError("suffix must be either 'with' or 'without'")
    return round(float(df[cols].mean(axis=1).mean() * 100), 1)


def compute_slice_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute adherence by operational slice/metric using the taxonomy-conditioned outputs."""
    rows = []
    for metric, sdf in df.groupby("operational_metric_ar", dropna=False):
        rows.append({
            "Slice": metric,
            "N": len(sdf),
            "Answer-form adherence": percent_mean(sdf["answer_form_adherent_with"]),
            "Temporal adherence": percent_mean(sdf["temporal_adherent_with"]),
            "Purpose alignment": percent_mean(sdf["purpose_aligned_with"]),
            "Overall BI adherence": compute_overall_bi_adherence(sdf, suffix="with"),
        })
    return pd.DataFrame(rows).sort_values(["Overall BI adherence", "N"], ascending=[False, False])


def compute_format_compliance(df: pd.DataFrame) -> pd.DataFrame:
    """Compute answer-form compliance by expected answer type."""
    rows = []
    group_col = "answer_type" if "answer_type" in df.columns else "AAFAQ_AnswerType"
    for answer_type, sdf in df.groupby(group_col, dropna=False):
        rows.append({
            "Answer type": answer_type,
            "N": len(sdf),
            "Without conditioning": percent_mean(sdf["answer_form_adherent_without"]),
            "With conditioning": percent_mean(sdf["answer_form_adherent_with"]),
            "Absolute gain": round(
                percent_mean(sdf["answer_form_adherent_with"]) - percent_mean(sdf["answer_form_adherent_without"]),
                1,
            ),
        })
    return pd.DataFrame(rows).sort_values("N", ascending=False)
