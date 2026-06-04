import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.config import CASE_STUDY_CSV, PROMPT_DIR
from aafaq_bi.data_io import read_csv
from aafaq_bi.prompts import build_prompt_records, write_jsonl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(CASE_STUDY_CSV))
    parser.add_argument("--output", default=str(PROMPT_DIR / "hospital_bi_prompts.jsonl"))
    args = parser.parse_args()

    df = read_csv(args.data)
    records = build_prompt_records(df)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(records, output)
    print(f"Wrote {len(records)} prompt records to {output}")


if __name__ == "__main__":
    main()
