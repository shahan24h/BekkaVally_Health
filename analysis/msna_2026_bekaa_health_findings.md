# MSNA 2026: Healthcare access and drinking-water vulnerability in Bekaa

## Population and method

- Source: REACH MSNA 2026 cleaned household workbook, worksheet `Household Data`.
- Study population: `admin1_label_en = Bekaa` and `pop_group_label_en = Lebanese`.
- Total eligible household records: **624**; all 624 had valid positive `weight` values.
- Descriptive percentage = 100 × sum of weights among qualifying eligible responses / sum of weights among all valid eligible responses for that indicator.
- Reported sample sizes are **unweighted**; reported percentages are **survey-weighted**.
- Analyses are observational; no formal sampling-design-adjusted confidence intervals or hypothesis tests have been calculated.

## 1. Healthcare needs

Variable: `health_ind_healthcare_needed_n`. Valid responses: **624**.

| Members needing healthcare | Survey-weighted household % | Unweighted n |
|---|---:|---:|
| 0 | 43.22 | 223 |
| 1 | 31.22 | 210 |
| 2 | 20.44 | 148 |
| 3 | 3.43 | 27 |
| 4 | 1.30 | 11 |
| 5 | 0.39 | 5 |
| **At least 1** | **56.78** | **401** |

The item records healthcare need, **not a diagnosis or illness attributable to water**.

## 2. Barriers to healthcare

Variable: `health_barriers`, a multiple-selection question, with binary flags `health_barriers.*`.

**173** households had a recorded nonempty `health_barriers` answer; **451** households were missing/skipped. All percentages below use the **173 recorded respondents** as the denominator, not all 624.

| Barrier | Weighted % | n / 173 |
|---|---:|---:|
| No nearby facility | 51.01 | 79 |
| Cannot afford consultation | 50.12 | 90 |
| Cannot afford treatment | 32.67 | 73 |
| Cannot afford transportation | 6.38 | 17 |
| Long waiting time | 5.72 | 8 |
| **Any of consultation, treatment, transport costs** | **63.14** | **120** |

Respondents could choose multiple barriers, so columns do not sum to 100%. **Questionnaire skip logic must be checked** before generalizing these rates beyond respondents with recorded answers. Binary zero values in skipped rows were not treated as valid negative responses.

## 3. Drinking-water access

- `rec_piped_water_past_week_yn`: **26.39%** reported **no** piped water received in previous week (**68 of 290** valid responses). **334 of 624** households had missing/skipped responses. Eligibility must be verified; do **not** generalize to all 624 without checking.
- `wash_hwise_drink`: **8.08%** chose `rarely` or `sometimes` (**40 of 624**). Exact questionnaire wording and recall period must be verified before specifying the nature of the difficulty.
- `wash_hwise_worry`: **15.02%** chose `rarely` or `sometimes` (**88 households**); 2 households chose `dnk` or `pnta` and were excluded from the response-based denominator.

## 4. Primary drinking-water sources

Variable: `wash_drinking_water_source` (624 valid responses):

| Primary source | Weighted % | n |
|---|---:|---:|
| Piped to dwelling | 50.99 | 288 |
| Bottled water | 18.99 | 146 |
| Protected well | 11.26 | 69 |
| Well/spring | 8.02 | 49 |
| Tanker truck | 4.70 | 23 |

The source-category indicator categorized **98.99%** as improved. This is **not** a laboratory measure of chemical or microbial safety. The JMP classification was `basic` for **96.31%** of 622 valid responses, which does not establish safely managed drinking water.

## 5. Income-related water vulnerability

Variable `cm_income_total` was valid for **604 / 624** records (currency column indicated USD). Weighted income quartile threshold values were US$500, US$700, and US$970.

| Observed income range (USD, period unverified) | Households with valid income | Weighted water worry % | Weighted drinking-water difficulty % |
|---|---:|---:|---:|
| 0–500 | 211 | 25.81 | 12.26 |
| 550–700 | 132 | 14.94 | 8.07 |
| 720–970 | 119 | 7.36 | 6.09 |
| 1,000–5,000 | 142 | 5.37 | 3.22 |

For water worry, 602 valid substantive responses were used, while 604 valid substantive responses were available for `wash_hwise_drink`. These patterns are **descriptive, not causal**.

## 6. Water expenditure caveat

`hh_water_expenditure_above_5per` was populated for only **204** households: **44.51%** were flagged `yes` (**73 of 204**, unweighted). **420** records were missing/skipped. The applicable denominator and calculation rules need verification; do not use this result as a 624-household prevalence.

## Reproducibility and limitations

Results reported above were produced by locally executed Python scripts provided as console summaries. The repository script recreates the core healthcare findings using the original cleaned workbook; the original workbook and original local script files were **not uploaded**.

Checks remaining:
1. Confirm health and WASH question wordings and skip logic against the workbook's `survey` and `choices` sheets.
2. Confirm weights, sampling strata and PSU definitions in technical documentation.
3. Independently reproduce all tabulations and resolve missingness.
4. If drawing statistical inference, use appropriate survey-design-adjusted uncertainty estimates.
5. Assess agricultural water contamination through actual water samples before proposing a treatment target.

**Do not equate household water-source type or healthcare needs with proven water contamination or waterborne illness.**
