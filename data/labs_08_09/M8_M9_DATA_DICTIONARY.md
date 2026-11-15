# M8–M9 synthetic teaching dataset dictionary

14 November 2026 · v1.0.1 documentation update · 5,000 synthetic people · one synthetic wave aged 17–18

This is a synthetic teaching dataset, not ABCD participant data or an empirical estimate of age-specific associations. Official-style names identify synthetic analog measures; `instructional_` fields are course-derived. Source calibration combines ses-06A imaging and ses-07A substance/cohesion summaries. Those source sessions are not participant-level visits in this file.

Blank CSV cells mean unavailable/unusable/unresolved, never zero. Imaging values are masked for both unavailable scans and failed primary task quality. Stricter-only exclusions retain primary-eligible imaging values for sensitivity comparisons. Substance counts, any-use and frequency groups are all masked when reports are unresolved. Lifetime status is a separate complete measure and does not resolve the missing detailed report.

## Interpretation and release limitations

- The common 365-day period is a teaching simplification; real TLFB detailed coverage can be shorter.
- MID pooled reward uses equal large/small weights as an explicit synthetic assumption, not verified production GLT coefficients. All-run names do not imply raw runs were simulated. Do not treat this dataset as a release-faithful reconstruction with the transport assumptions documented here.
- SST correct-stop versus correct-go includes stimulus and response-demand differences. Larger activation is not automatically better control.
- These are single-wave observation-scale measures. The dataset does not separate true neural signal from measurement error or provide repeated scans for reliability estimation.
- Cohesion realized median is 7/9 (.778), versus the source .889, despite the population fit and broad tolerance passing. Realized marginals differ from source targets: alcohol SD is about 8.22 versus 7.59, and maximum 230 versus 190. Source extrema are not hard bounds.
- Frequency categories are descriptive, not diagnoses. Co-use differs across groups. Do not assume a frequency gradient; interpret the observed estimates and uncertainty.
- Four ascertainment categories are defined but only observed/unresolved are populated. No provenance was fabricated to populate the other categories. MID behavior, SSRT, urgency, and BAS are omitted pending calibration; there is no invented SSRT-validity flag.

## Analysis filters

M8 one-sample and paired tests use `instructional_mid_analysis_eligible` only. M8 substance-group tests additionally require the relevant substance report, summarized by `instructional_m8_*_analysis_eligible`. M9 primary tests use `instructional_m9_*_analysis_eligible`; stricter sensitivity uses `instructional_sst_sensitivity_eligible == 1` AND the chosen substance's report-resolved flag. Do not require the other task or substance. No whole-table complete-case deletion.

## Field definitions

| Field | Definition | Units/codes | Missingness |
|---|---|---|---|
| `participant_id` | Unique synthetic participant identifier; not a real ABCD identifier | text | Never missing in this release |
| `instructional_wave_id` | Common instructional wave; not an ABCD session code | text | Never missing in this release |
| `instructional_tlfb_window_days` | Fixed teaching window; real detailed TLFB coverage can be shorter | days | Never missing in this release |
| `ab_g_dyn__visit_age` | Synthetic age, uniform 17 <= age < 19; source ages were not provided | years | Never missing in this release |
| `fc_y_fes__cohes_mean` | Synthetic youth family cohesion mean, complete nine-item model; values on ninths | 0–1 | Never missing in this release |
| `instructional_imaging_available` | Common imaging availability indicator; instructional, not official QC | 0=no; 1=yes | Never missing in this release |
| `instructional_mid_analysis_eligible` | MID primary imaging eligibility; does not require substance reports | 0=no; 1=yes | Never missing in this release |
| `instructional_mid_eligibility_reason` | Primary task disposition | eligible / imaging_unavailable / failed_primary_quality | Never missing in this release |
| `instructional_sst_analysis_eligible` | SST primary imaging eligibility; does not require substance reports | 0=no; 1=yes | Never missing in this release |
| `instructional_sst_eligibility_reason` | Primary task disposition | eligible / imaging_unavailable / failed_primary_quality | Never missing in this release |
| `instructional_sst_sensitivity_eligible` | Stricter SST subset; does not require substance report | 0=no; 1=yes | Never missing in this release |
| `instructional_sst_sensitivity_reason` | Stricter subset disposition | eligible / not_primary_eligible / fails_stricter_quality | Never missing in this release |
| `mr_y_tfmri__mid__alrvn__aseg__ab__lh_beta` | NAc left, large reward versus neutral, visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `mr_y_tfmri__mid__asrvn__aseg__ab__lh_beta` | NAc left, small reward versus neutral, visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_arvn_equalweight_lh` | NAc left, pooled reward versus neutral (equal-weight synthetic assumption), visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `mr_y_tfmri__mid__alrvn__aseg__ab__rh_beta` | NAc right, large reward versus neutral, visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `mr_y_tfmri__mid__asrvn__aseg__ab__rh_beta` | NAc right, small reward versus neutral, visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_arvn_equalweight_rh` | NAc right, pooled reward versus neutral (equal-weight synthetic assumption), visit-level all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_alrvn_bilateral` | Bilateral mean of matching hemisphere contrasts | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_asrvn_bilateral` | Bilateral mean of matching hemisphere contrasts | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_arvn_bilateral` | Bilateral mean of matching hemisphere contrasts | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `instructional_mid_nac_large_minus_small` | Bilateral large-reward minus small-reward contrast | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `mr_y_tfmri__sst__csvcg__dsk__pop__rh_beta` | Right pars opercularis, correct stop minus correct go, all-run analog | PSC | Blank when imaging unavailable or task fails primary quality; source truth never exported |
| `su_y_dyn__mj__lt_indicator` | Synthetic lifetime cannabis reported-use status, distinct from detailed-period report | 0=no; 1=yes | Never missing in this release |
| `su_y_tlfb__mj_ud` | Cannabis use days; all forms for cannabis; synthetic fixed 365-day detailed-period analog | integer 0–365 | Blank when that substance report is unresolved |
| `instructional_cannabis_report_resolved` | Resolved detailed-period cannabis report | 0=no; 1=yes | Never missing in this release |
| `instructional_cannabis_ascertainment_status` | Four-level vocabulary: observed / documented_nonuse / unresolved / not_assessed. This release uses only observed and unresolved; routing-specific nonuse and nonassessment were not generated. Observed zero is a valid observed report. | category | Never missing in this release |
| `instructional_cannabis_any_detailed` | Any cannabis use in the fixed detailed period | 0=no; 1=yes | Blank when unresolved |
| `instructional_cannabis_frequency_group` | 0=zero days; 1=1–11 days; 2=12+ days | 0/1/2 descriptive frequency; not severity | Blank when unresolved |
| `instructional_m8_cannabis_analysis_eligible` | M8 substance-group analysis eligibility; primary MID and resolved cannabis | 0/1 | Never missing in this release |
| `instructional_m8_cannabis_eligibility_reason` | First exclusion reason, task checked before report; original flags preserve both reasons | eligible / task_ineligible / substance_unresolved | Never missing in this release |
| `instructional_m9_cannabis_analysis_eligible` | M9 substance-group analysis eligibility; primary SST and resolved cannabis | 0/1 | Never missing in this release |
| `instructional_m9_cannabis_eligibility_reason` | First exclusion reason, task checked before report; original flags preserve both reasons | eligible / task_ineligible / substance_unresolved | Never missing in this release |
| `su_y_dyn__alc__lt_indicator` | Synthetic lifetime alcohol reported-use status, distinct from detailed-period report | 0=no; 1=yes | Never missing in this release |
| `su_y_tlfb__alc_ud` | Alcohol use days; synthetic fixed 365-day detailed-period analog | integer 0–365 | Blank when that substance report is unresolved |
| `instructional_alcohol_report_resolved` | Resolved detailed-period alcohol report | 0=no; 1=yes | Never missing in this release |
| `instructional_alcohol_ascertainment_status` | Four-level vocabulary: observed / documented_nonuse / unresolved / not_assessed. This release uses only observed and unresolved; routing-specific nonuse and nonassessment were not generated. Observed zero is a valid observed report. | category | Never missing in this release |
| `instructional_alcohol_any_detailed` | Any alcohol use in the fixed detailed period | 0=no; 1=yes | Blank when unresolved |
| `instructional_alcohol_frequency_group` | 0=zero days; 1=1–5 days; 2=6+ days | 0/1/2 descriptive frequency; not severity | Blank when unresolved |
| `instructional_m8_alcohol_analysis_eligible` | M8 substance-group analysis eligibility; primary MID and resolved alcohol | 0/1 | Never missing in this release |
| `instructional_m8_alcohol_eligibility_reason` | First exclusion reason, task checked before report; original flags preserve both reasons | eligible / task_ineligible / substance_unresolved | Never missing in this release |
| `instructional_m9_alcohol_analysis_eligible` | M9 substance-group analysis eligibility; primary SST and resolved alcohol | 0/1 | Never missing in this release |
| `instructional_m9_alcohol_eligibility_reason` | First exclusion reason, task checked before report; original flags preserve both reasons | eligible / task_ineligible / substance_unresolved | Never missing in this release |


## Derived-column naming and version history

The two pooled NAc hemisphere summaries are named `instructional_mid_nac_arvn_equalweight_lh` and `instructional_mid_nac_arvn_equalweight_rh`. Each is (large-reward-versus-neutral + small-reward-versus-neutral)/2. Their bilateral average remains `instructional_mid_nac_arvn_bilateral`. They are explicit course derivatives, not verified official pooled contrasts. Values are identical to the pilot; only the two column names changed. All-run wording applies to the source calibration labels, not to simulated raw runs.

Empirical source release/filtering and exact source age distributions were not supplied. The retained official names identify synthetic analogs whose measurement meanings were checked during planning, not recovered real observations. This release is a documented teaching simulation, not a claim of exact ABCD replication. Optional behavioral measures and actual chapter/lab revisions are outside this package.

## v1.0.1 documentation update

The CSV, field names, values and eligibility rules are byte-identical to v1.0. This update clarifies the alcohol definition and the selected analysis methods. Synthetic-data provenance and measurement limitations remain explicit. The separate analysis guide specifies L8 Welch inference and L9 ANOVA-pooled planned pairs.
