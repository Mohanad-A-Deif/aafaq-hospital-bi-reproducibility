import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.config import CASE_STUDY_CSV, TABLE_DIR
from aafaq_bi.data_io import read_csv, write_csv, write_latex_table
from aafaq_bi.metrics import compute_adherence_summary, compute_slice_summary, compute_format_compliance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(CASE_STUDY_CSV))
    parser.add_argument("--outdir", default=str(TABLE_DIR))
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    df = read_csv(args.data)

    adherence = compute_adherence_summary(df)
    slices = compute_slice_summary(df)
    formats = compute_format_compliance(df)

    write_csv(adherence, outdir / "bi_adherence_summary.csv")
    write_csv(slices, outdir / "bi_slice_summary.csv")
    write_csv(formats, outdir / "format_compliance_by_answer_type.csv")
    write_latex_table(
        adherence,
        outdir / "bi_adherence_summary.tex",
        caption="Hospital BI case study: adherence of generated answers to taxonomy targets.",
        label="tab:bi_adherence",
    )
    print(adherence.to_string(index=False))


if __name__ == "__main__":
    main()
