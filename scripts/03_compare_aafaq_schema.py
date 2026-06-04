import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.config import AAFAQ_RAW_CSV, CASE_STUDY_CSV, TABLE_DIR
from aafaq_bi.data_io import read_csv, write_csv
from aafaq_bi.validators import compare_aafaq_schema


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aafaq", default=str(AAFAQ_RAW_CSV))
    parser.add_argument("--case-study", default=str(CASE_STUDY_CSV))
    args = parser.parse_args()

    aafaq_path = Path(args.aafaq)
    if not aafaq_path.exists():
        print(f"AAFAQ file not found: {aafaq_path}")
        print("Place AAFAQ_Dataset.csv under data/raw/ or pass --aafaq PATH.")
        return

    aafaq_df = read_csv(aafaq_path)
    case_df = read_csv(args.case_study)
    report = compare_aafaq_schema(aafaq_df, case_df)
    write_csv(report, TABLE_DIR / "aafaq_schema_compatibility.csv")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
