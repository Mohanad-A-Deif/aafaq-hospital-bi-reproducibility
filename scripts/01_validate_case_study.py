import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.data_io import read_csv
from aafaq_bi.validators import validate_case_study_schema
from aafaq_bi.config import CASE_STUDY_CSV


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(CASE_STUDY_CSV))
    args = parser.parse_args()

    df = read_csv(args.data)
    report = validate_case_study_schema(df)
    for key, value in report.items():
        print(f"{key}: {value}")
    if not report["is_valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
