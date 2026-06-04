# AAFAQ-Compatible Hospital BI Case Study Reproducibility Package

This repository contains reproducible code and a synthetic Hospital Business Intelligence (Hospital BI) case-study dataset formatted according to the AAFAQ-style annotation schema.

The package supports three goals:

1. Validate the Hospital BI case-study data schema.
2. Reproduce the Hospital BI adherence table reported in the manuscript.
3. Build taxonomy-conditioned and taxonomy-agnostic prompt inputs for Arabic question-answering experiments.

> Important: the included Hospital BI data are **synthetic** and application-oriented. They do not contain real hospital records, patient-level data, operational logs, or identifiable information.

## Repository structure

```text
.
├── data/
│   ├── case_study/
│   │   ├── hospital_bi_case_study_aafaq_compatible.csv
│   │   └── hospital_bi_case_study_dataset.xlsx
│   └── raw/
│       └── README.md
├── outputs/
│   ├── figures/
│   ├── prompts/
│   └── tables/
├── scripts/
│   ├── run_all.py
│   ├── 01_validate_case_study.py
│   ├── 02_compute_bi_adherence.py
│   ├── 03_compare_aafaq_schema.py
│   ├── 04_build_prompt_dataset.py
│   ├── 05_generate_synthetic_case_study.py
│   └── 06_train_multitask_classifier_optional.py
├── src/aafaq_bi/
│   ├── config.py
│   ├── data_io.py
│   ├── metrics.py
│   ├── prompts.py
│   ├── schema.py
│   ├── synthetic_generator.py
│   ├── validators.py
│   └── modeling.py
├── tests/
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_all.py
```

Expected core output:

```text
Criterion,Without conditioning,With conditioning
Answer-form adherence,78.9,89.7
Temporal adherence,81.3,92.4
Purpose alignment,74.6,86.1
```

Generated files will be saved under `outputs/`:

```text
outputs/tables/bi_adherence_summary.csv
outputs/tables/bi_adherence_summary.tex
outputs/tables/bi_slice_summary.csv
outputs/tables/format_compliance_by_answer_type.csv
outputs/figures/bi_adherence_summary.png
outputs/prompts/hospital_bi_prompts.jsonl
```

## Data files

The case-study dataset contains 1000 Arabic synthetic Hospital BI questions. Each record includes:

- Arabic question text.
- Hospital operational domain fields, such as department and operational metric.
- AAFAQ-compatible taxonomy columns.
- Reference answer.
- Direct answer without taxonomy conditioning.
- Taxonomy-conditioned answer.
- Binary adherence indicators for answer form, temporal scope, and purpose alignment.

The binary adherence columns are used to reproduce the Hospital BI adherence table.

## Optional AAFAQ compatibility check

The original AAFAQ dataset is not required to reproduce the Hospital BI table. If you want to compare schema compatibility with an AAFAQ CSV file, place it here:

```text
data/raw/AAFAQ_Dataset.csv
```

Then run:

```bash
python scripts/03_compare_aafaq_schema.py --aafaq data/raw/AAFAQ_Dataset.csv
```

## Optional multi-task classifier training

The code includes an optional transformer-based multi-task classifier with one prediction head per taxonomy dimension. Install the machine-learning dependencies first:

```bash
pip install -r requirements-ml.txt
python scripts/06_train_multitask_classifier_optional.py \
  --data data/raw/AAFAQ_Dataset.csv \
  --model aubmindlab/bert-base-arabertv02 \
  --epochs 3 \
  --batch-size 8
```

This optional script is provided as a reproducibility scaffold for the taxonomy-classification component. The Hospital BI case-study table itself is reproduced from the included synthetic evaluation file.

## Ethical and reproducibility note

The Hospital BI case-study data are synthetic and should not be interpreted as real hospital measurements. They are intended to test taxonomy-conditioned answer controllability in an operational Arabic question-answering scenario.

Recommended manuscript wording:

```latex
The Hospital BI case study used a synthetic application-oriented evaluation set formatted according to the AAFAQ annotation schema. It was used to evaluate answer-form adherence, temporal adherence, and purpose alignment under taxonomy-agnostic and taxonomy-conditioned generation settings. No real hospital records, patient-level data, or identifiable operational logs were used.
```
