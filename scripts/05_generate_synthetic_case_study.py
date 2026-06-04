import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.synthetic_generator import generate_synthetic_case_study
from aafaq_bi.data_io import write_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/case_study/generated_hospital_bi_case_study.csv")
    args = parser.parse_args()

    df = generate_synthetic_case_study(n=args.n, seed=args.seed)
    write_csv(df, Path(args.output))
    print(f"Generated {len(df)} rows at {args.output}")


if __name__ == "__main__":
    main()
