# Data Card: Synthetic Hospital BI Case Study

## Dataset name
Synthetic Hospital BI AAFAQ-compatible case-study dataset.

## Intended use
The dataset is intended for application-oriented evaluation of taxonomy-conditioned Arabic question answering in hospital business intelligence scenarios.

## Not intended use
The dataset must not be used as real hospital evidence, clinical evidence, or operational performance evidence for any hospital.

## Data source
The dataset is synthetic. Questions and answers were generated to simulate common hospital BI question types such as bed occupancy, emergency waiting time, resource utilization, laboratory turnaround time, surgery cancellations, and staffing pressure.

## Privacy
No real patient data, hospital records, operational logs, staff identifiers, or patient identifiers are included.

## Schema
The dataset includes AAFAQ-compatible annotation fields and additional case-study fields used to compute adherence metrics.

## Main evaluation fields

- `answer_form_adherent_without`
- `answer_form_adherent_with`
- `temporal_adherent_without`
- `temporal_adherent_with`
- `purpose_aligned_without`
- `purpose_aligned_with`

Each field is binary: 1 indicates adherence, 0 indicates non-adherence.
