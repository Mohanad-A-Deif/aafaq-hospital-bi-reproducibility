from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.config import CASE_STUDY_CSV, TABLE_DIR, FIGURE_DIR, PROMPT_DIR
from aafaq_bi.data_io import read_csv, write_csv, write_latex_table
from aafaq_bi.metrics import compute_adherence_summary, compute_slice_summary, compute_format_compliance
from aafaq_bi.prompts import build_prompt_records, write_jsonl
from aafaq_bi.validators import validate_case_study_schema

import matplotlib.pyplot as plt


def main():
    df = read_csv(CASE_STUDY_CSV)
    validation = validate_case_study_schema(df)
    print("Validation:", validation)
    if not validation["is_valid"]:
        raise SystemExit("Case-study data validation failed.")

    summary = compute_adherence_summary(df)
    write_csv(summary, TABLE_DIR / "bi_adherence_summary.csv")
    write_latex_table(
        summary,
        TABLE_DIR / "bi_adherence_summary.tex",
        caption="Hospital BI case study: adherence of generated answers to taxonomy targets.",
        label="tab:bi_adherence",
    )

    slice_summary = compute_slice_summary(df)
    write_csv(slice_summary, TABLE_DIR / "bi_slice_summary.csv")

    format_summary = compute_format_compliance(df)
    write_csv(format_summary, TABLE_DIR / "format_compliance_by_answer_type.csv")

    # Figure: one clean plot, no custom colors.
    ax = summary.plot(
        x="Criterion",
        y=["Without conditioning", "With conditioning"],
        kind="bar",
        figsize=(8, 4),
        rot=0,
    )
    ax.set_ylabel("Adherence (%)")
    ax.set_xlabel("")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right")
    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURE_DIR / "bi_adherence_summary.png", dpi=300)
    plt.close()

    records = build_prompt_records(df)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(records, PROMPT_DIR / "hospital_bi_prompts.jsonl")

    print("\nHospital BI adherence summary:")
    print(summary.to_string(index=False))
    print("\nOutputs written to:", TABLE_DIR.parent)


if __name__ == "__main__":
    main()
