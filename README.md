# Bekaa Valley Health & Water Access — MSNA 2026

Survey-weighted descriptive analysis of **Lebanese households in Bekaa Governorate, Lebanon**, using the **REACH Multi-Sector Needs Assessment (MSNA) 2026** cleaned household dataset.

> **Scope:** Bekaa Governorate only (`admin1_label_en = Bekaa`), Lebanese households only (`pop_group_label_en = Lebanese`). The analytic subset contains **624 households**. Do not interpret these estimates as covering all residents of the Beqaa Valley or neighboring Baalbek-Hermel Governorate.

## Main findings

| Indicator | Survey-weighted result | Unweighted sample |
|---|---:|---:|
| At least one household member needed healthcare | **56.78%** | 401 / 624 |
| Any financial healthcare barrier (consultation, treatment, or transport) | **63.14%** | 120 / 173 households with recorded barrier responses |
| No nearby healthcare facility | **51.01%** | 79 / 173 |
| Cannot afford consultation | **50.12%** | 90 / 173 |
| Cannot afford treatment | **32.67%** | 73 / 173 |
| No piped water received in preceding week | **26.39%** | 68 / 290 question-eligible responses |
| Drinking-water difficulty reported at least rarely | **8.08%** | 40 / 624 |
| Drinking-water worry reported at least rarely | **15.02%** | 88 / 624 (excluding two non-substantive responses from the percentage) |

**Important:** The healthcare-barriers question was recorded for **173 of 624** households. The other 451 have missing/skipped responses, so the barrier percentages **must not** be presented as rates among all 624 households until skip logic and the survey population are verified.

## Income and water insecurity

Among **604 households with valid income and survey weights**, reported drinking-water difficulty declined across household income groups, from **12.26%** in the lowest group (up to US$500 in recorded income) to **3.22%** in the highest (above US$970). Drinking-water worry similarly declined from **25.81%** to **5.37%**. These are descriptive associations, not evidence of causality or survey-design-adjusted statistical significance. Income reference period requires verification.

## Repository contents

- [Healthcare findings and limitations](analysis/msna_2026_bekaa_health_findings.md)
- [Reproducible Python analysis](scripts/msna_2026_bekaa_health.py)
- [Python requirements](requirements.txt)

## Running the analysis

The cleaned REACH MSNA 2026 workbook is **not included** in this public repository. Obtain it through the data provider under its applicable access and reuse terms. Run:

```bash
pip install -r requirements.txt
python scripts/msna_2026_bekaa_health.py --input "path/to/REACH_LBN_Clean_Dataset_MSNA_2026.xlsx" --output results
```

The script reads `Household Data`, applies the population and governorate filters, checks weights, and exports aggregate results only. Do **not** commit individual household records or identifiable survey data.

## Interpretation

These household indicators document healthcare-access and drinking-water challenges but **do not measure waterborne illness or agricultural water contamination**. They do not establish that biochar filtration would improve healthcare outcomes. The precise survey questions, weighting design, skip patterns and relevant sampling documentation should be checked before formal publication.

## Data attribution

Data source: REACH / IMPACT Initiatives, Lebanon MSNA 2026 (cleaned household dataset). This repository contains independent secondary analysis and should not be mistaken for an official REACH publication.

## Project status

Exploratory descriptive analysis; results are provisional pending questionnaire, skip-logic, survey-design, and independent reproducibility checks.
