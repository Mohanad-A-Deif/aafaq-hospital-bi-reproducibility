from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
CASE_STUDY_DIR = DATA_DIR / "case_study"
OUTPUT_DIR = REPO_ROOT / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"
PROMPT_DIR = OUTPUT_DIR / "prompts"

CASE_STUDY_CSV = CASE_STUDY_DIR / "hospital_bi_case_study_aafaq_compatible.csv"
CASE_STUDY_XLSX = CASE_STUDY_DIR / "hospital_bi_case_study_dataset.xlsx"
AAFAQ_RAW_CSV = DATA_DIR / "raw" / "AAFAQ_Dataset.csv"

RANDOM_SEED = 42
