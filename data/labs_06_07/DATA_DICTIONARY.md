# Data dictionary: Labs 6–7

All people, places and observations in these tables are fictional: 8,564 synthetic participants, each with one outcome visit (`ses-07A`) and a baseline record (`ses-00A`).
A blank CSV cell means the value is missing. Missing is never the same as zero.
Numbers that stand for categories (policy codes, COI levels, response codes) are labels. Do not add or average them.
**Origin** shows where each variable comes from:
- **ABCD** means the variable uses an ABCD Study name and definition, with synthetic values.
- **Course** means the variable was built for this course and is not an ABCD variable.

## Shared codes

| Codes | Meaning |
| --- | --- |
| Policy category (`le_l_lawsmj__mjlaws__state_indicator`, `instructional_law_code`, `instructional_policy_*_code`) | 1 Recreational · 2 Medical · 3 Low THC/CBD only · 4 No recreational or medical law |
| COI level (`..._national_c5`) | 1 Very low (scores 1–20) · 2 Low (21–40) · 3 Moderate (41–60) · 4 High (61–80) · 5 Very high (81–100) |
| Assessment date | The interview date for the outcome visit, 0–7 days after the visit start. Cannabis questions cover the 30 days before this date. |

## `instructional_analysis.csv`: one row per person, the main analysis table (Lab 6)

This table repeats the key fields from the tables below so that most analyses need no join.

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `participant_id` | ABCD | Text, e.g. `sub-DSAR67R6-00001` | Fictional person ID | Never missing |
| `session_id` | ABCD | `ses-07A` | Outcome visit; one per person | Never missing |
| `ab_g_dyn__visit_dtt` | ABCD | Date | Visit start date | Never missing |
| `ab_g_dyn__visit_age` | ABCD | Years, about 15.7–18.3 | Age at visit start | Never missing |
| `instructional_tlfb_date` | Course | Date | Assessment date (see Shared codes) | Never missing; a date alone does not mean the interview happened |
| `instructional_age_at_assessment` | Course | Years | Age on the assessment date | Never missing |
| `instructional_ace10` | Course | Integer 0–10, categories per person | ACE10 score (see `instructional_ace_categories.csv`) | Blank unless all ten categories are known |
| `instructional_ace_categories_known` | Course | Integer 0–10 | How many of the ten ACE categories could be determined | 0 when ACE was not assessed |
| `instructional_ace_status` | Course | `scored` / `incomplete_categories` / `not_assessed` | Why ACE10 is or is not available | — |
| `fc_y_fes__cohes_mean` | ABCD | 0–1 | Family cohesion score (see `fc_y_fes.csv`) | Blank if fewer than 8 usable items |
| `instructional_cohesion_status` | Course | `scored` / `insufficient_items` / `not_assessed` | Why cohesion is or is not available | — |
| `su_y_tlfb__mj__smoke__1mo_ud` | ABCD | Integer 0–30, days | Days smoking marijuana flower in the 30 days before assessment | 0 is a reported zero; blank is unknown |
| `instructional_cannabis_days_30d` | Course | Integer 0–30, days | Days using any of eight plant-cannabis products in the 30 days before assessment (see `instructional_cannabis.csv`) | 0 is a reported zero; blank is unknown |
| `instructional_cannabis_any_30d` | Course | 0/1 | 1 if `instructional_cannabis_days_30d` > 0, else 0 | Blank when the day count is blank |
| `instructional_smoking_status`, `instructional_cannabis_status` | Course | `observed` / `documented_nonuse` / `unresolved` / `not_assessed` | Whether the flower count (smoking) or the broad count (cannabis) is known, and how | `documented_nonuse` is a confirmed zero |
| `instructional_policy_window_code` | Course | Policy category 1–4 | Cannabis-law category in force for all 30 days before assessment | Blank unless the window is `stable` |
| `instructional_policy_window_status` | Course | `stable` / `transition` / `unmatched_residence` / `not_assessed` | Whether one law category covered the whole window | `transition`: the law changed during the window |
| `instructional_policy_start_code`, `instructional_policy_end_code` | Course | Policy category 1–4 | Law category on the first and last day of the window | Blank when residence is unmatched |
| `le_l_lawsmj__mjlaws__state_indicator` | ABCD | Policy category 1–4 | State cannabis-law category at **baseline**, not at the outcome visit | Blank when residence is unmatched |
| `instructional_context_event` | Course | `ses-00A` | The baseline visit that the neighborhood and law fields describe | — |
| `instructional_area_id` | Course | Text, e.g. `A0286` | Fictional baseline neighborhood | Blank when no area is linked |
| `instructional_coi_vintage` | Course | 2015 | Year of the COI data used for every area | — |
| `le_l_coi__addr1__coi__total__national_score` | ABCD | Integer 1–100 | Child Opportunity Index national score of the baseline neighborhood (higher = more opportunity) | Blank when no area is linked |
| `le_l_coi__addr1__coi__total__national_c5` | ABCD | COI level 1–5 | Five-level version of the score | Blank when no area is linked |
| `instructional_coi_match_status` | Course | `matched` / `unmatched` | Whether a neighborhood record was found | An unmatched person can still have other outcomes |

## `instructional_ace_responses.csv`: one row per person, ACE questions

ACE10 is a course measure based on the CDC/BRFSS adverse childhood experiences questions. It is not an ABCD score or a clinical tool. The questions cover the time from birth to the assessment date or the 18th birthday, whichever came first.

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `instructional_ace_assessed` | Course | True/False | Whether the ACE questions were asked | — |
| `instructional_ace_assessment_date` | Course | Date | Date the ACE questions were answered | Blank if not assessed |
| `instructional_ace_reference_end_exclusive` | Course | Date | End of the ACE time window (the day itself is not included) | — |
| `instructional_ace_q01`–`q04` | Course | 1 Yes · 2 No · 7 Don't know · 9 Declined | Lived with someone with mental illness or suicidality (q01), alcohol problems (q02), drug misuse (q03), or who was incarcerated (q04) | 7 and 9 are not answers; blank if not assessed |
| `instructional_ace_q05` | Course | 1 Yes · 2 No · 8 Parents not married · 7 · 9 | Parents separated or divorced | 8 is not treated as No |
| `instructional_ace_q06`–`q11` | Course | 1 Never · 2 Once · 3 More than once · 7 · 9 | Witnessed violence between household adults (q06); physically hurt by an adult (q07); repeated verbal mistreatment (q08); three sexual-abuse questions (q09–q11) | 7 and 9 are not answers |
| `instructional_ace_q12`, `q13` | Course | 1 Never · 2 A little · 3 Some · 4 Most · 5 All of the time · 7 · 9 | How often an adult made you feel safe and protected (q12) or met your basic needs (q13) | 7 and 9 are not answers |
| `instructional_ace_qNN_status` | Course | `answered` / `unknown` / `declined` / `ambiguous_response` / `not_assessed` | Status of each question's answer | — |

## `instructional_ace_categories.csv`: one row per person, ACE10 categories

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `instructional_ace_cat_*` (10 fields) | Course | 0/1 | One indicator per category. Abuse: emotional (q08 more than once), physical (q07 at least once), sexual (any of q09–q11 at least once). Neglect: emotional (q12 never or a little), physical (q13 never or a little). Household: substance problems (Yes to q02 or q03), mental illness (q01), parental separation (q05), incarceration (q04), witnessed violence (q06 at least once). | One qualifying answer gives 1. A 0 needs every relevant answer to be negative. Otherwise blank. |
| `instructional_ace10` | Course | Integer 0–10 | Sum of the ten indicators | Blank unless all ten are known; never filled in or scaled up |
| `instructional_ace_categories_known`, `instructional_ace_status` | Course | As in the analysis table | — | — |

## `fc_y_fes.csv`: one row per person, family cohesion

**ABCD source:** the youth Family Environment Scale, table `fc_y_fes` ([ABCD documentation](https://docs.abcdstudy.org/latest/documentation/non_imaging/fc.html#fc_y_fes)), Family Cohesion subscale (9 items). The score here is the ABCD summary variable `fc_y_fes__cohes_mean`, *Family Environment Scale [Youth] (Cohesion): Mean*. It follows the ABCD scoring rule ([`compute_fc_y_fes__cohes_mean`](https://software.nbdc-datahub.org/ABCDscores/reference/compute_fc_y_fes__cohes_mean.html)): the mean of items `fc_y_fes__cohes_001`–`009`, excluding 777, with at most one item missing. The values are synthetic.

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `instructional_cohesion_assessed` | Course | True/False | Whether the cohesion questions were asked | — |
| `instructional_cohesion_assessment_date` | Course | Date | Date answered | Blank if not assessed |
| `fc_y_fes__cohes_001`–`009` | ABCD | 0/1, or 777 | The nine cohesion items. 1 is the more cohesive answer. Items are already scored in that direction, so do not reverse any. | 777 is a nonresponse code, not a value; blank if not assessed |
| `fc_y_fes__cohes_mean` | ABCD | 0–1, higher = more cohesion | Mean of the usable items | Blank if fewer than 8 items are usable |
| `instructional_cohesion_status` | Course | `scored` / `insufficient_items` / `not_assessed` | Why the score is or is not available | — |

## `instructional_cannabis.csv`: one row per person, cannabis use (Lab 7)

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `instructional_tlfb_date` | Course | Date | Assessment date | — |
| `instructional_tlfb_assessed` | Course | True/False | Whether the substance-use interview took place | — |
| `su_y_tlfb__mj__smoke__1mo_ud` | ABCD | Integer 0–30, days | Days smoking marijuana flower in the 30 days before assessment | 0 is a reported zero |
| `instructional_cannabis_days_30d` | Course | Integer 0–30, days | Days using any of eight plant-cannabis products: smoked or vaped flower, smoked or vaped concentrates, edibles, tinctures, cannabis drinks, and blunts. A day counts once even if several products were used. CBD-only, synthetic cannabinoids and nicotine-only use are excluded. | 0 is a reported zero; blank is unknown |
| `instructional_cannabis_any_30d` | Course | 0/1 | Any use in the 30 days | Blank when the day count is blank |
| `instructional_smoking_status`, `instructional_cannabis_status` | Course | `observed` / `documented_nonuse` / `unresolved` / `not_assessed` | How the flower count (smoking) or the broad count (cannabis) is known | Only `observed` and `documented_nonuse` have a usable count |

## `instructional_policy_window.csv`: one row per person, cannabis law during the 30-day window (Lab 7)

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `instructional_policy_window_code`, `_status`, `_start_code`, `_end_code` | Course | As in the analysis table | Law category during the window | — |
| `window_start`, `window_end_exclusive` | Course | Date | The 30 days before assessment (the end date is not included) | — |
| `has_transition` | Course | True/False | The law category changed during the window | — |
| `has_history_gap` | Course | True/False | The law history did not cover every day (False for everyone here) | — |

A law category describes the legal setting only. It does not measure whether stores were open, whether young people could buy cannabis, or anyone's personal access.

## `instructional_baseline_link.csv`: one row per person, baseline neighborhood and jurisdiction (Lab 6 join)

| Field | Origin | Values | Meaning | Missing and zeros |
| --- | --- | --- | --- | --- |
| `participant_id` | ABCD | Text | Person ID (no `session_id`: this is the baseline link) | — |
| `baseline_date` | Course | Date | Baseline visit date | — |
| `context_event` | Course | `ses-00A` | Baseline visit | — |
| `instructional_area_id` | Course | Text | Fictional neighborhood; joins to `instructional_context.csv` | Blank when unlinked |
| `instructional_jurisdiction_id` | Course | Text, e.g. `J07` | Fictional state-like jurisdiction; joins to `instructional_policy_history.csv` | Blank when unlinked |
| `coi_match_status`, `policy_match_status` | Course | `matched` / `unmatched` | Whether each link was found | — |

## `instructional_context.csv`: one row per neighborhood (400 rows)

| Field | Origin | Values | Meaning |
| --- | --- | --- | --- |
| `instructional_area_id` | Course | Text | Neighborhood key |
| `instructional_coi_vintage` | Course | 2015 | Year of the COI data |
| `instructional_coi_index_version` | Course | 2.0 | COI version |
| `instructional_coi_geography_vintage` | Course | 2010 | Year of the neighborhood boundaries |
| `instructional_coi_reference` | Course | `national` | Scores are ranked nationally |
| `le_l_coi__addr1__coi__total__national_score`, `..._c5` | ABCD | 1–100; COI level 1–5 | Neighborhood COI score and level |

## `instructional_policy_history.csv`: one row per jurisdiction-period (17 rows)

| Field | Origin | Values | Meaning |
| --- | --- | --- | --- |
| `instructional_jurisdiction_id` | Course | Text | Jurisdiction key |
| `effective_start`, `effective_end_exclusive` | Course | Date | Period during which the law applied (the end date is not included) |
| `instructional_law_code` | Course | Policy category 1–4 | Law category during that period |

## `le_l_coi.csv` and `le_l_lawsmj.csv`: one row per person, baseline (`ses-00A`)

These hold the ABCD-named baseline fields `le_l_coi__addr1__coi__total__national_score` and `..._c5`, and `le_l_lawsmj__mjlaws__state_indicator`, as described above.

## `eligibility_audit.csv`: one row per person per outcome (4 × 8,564 rows)

| Field | Origin | Values | Meaning |
| --- | --- | --- | --- |
| `outcome` | Course | `ace10` / `cohesion` / `broad_cannabis` / `smoking_flower` | Which outcome this row describes |
| `outcome_available`, `availability_status` | Course | True/False; status of that outcome | Whether the outcome has a usable value |
| `outcome_unavailable_reason` | Course | `none` or the status | Why the outcome is unavailable |
| `eligible_l6`, `eligible_l7_medical`, `eligible_l7_recreational` | Course | True/False | Whether this person and outcome belong to the Lab 6 population, or to the Lab 7 Medical or Recreational population |
| `eligible_l6_reason`, `eligible_l7_medical_reason`, `eligible_l7_recreational_reason` | Course | `eligible`, `not_applicable` (outcome not used in that lab), an availability status, a policy-window status, or `outside_selected_policy` | Why the matching flag is True or False |
