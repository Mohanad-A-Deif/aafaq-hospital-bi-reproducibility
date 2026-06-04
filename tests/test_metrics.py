from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aafaq_bi.config import CASE_STUDY_CSV
from aafaq_bi.data_io import read_csv
from aafaq_bi.metrics import compute_adherence_summary


def test_bi_adherence_summary_values():
    df = read_csv(CASE_STUDY_CSV)
    summary = compute_adherence_summary(df)
    values = {(r["Criterion"]): (r["Without conditioning"], r["With conditioning"]) for _, r in summary.iterrows()}
    assert values["Answer-form adherence"] == (78.9, 89.7)
    assert values["Temporal adherence"] == (81.3, 92.4)
    assert values["Purpose alignment"] == (74.6, 86.1)
