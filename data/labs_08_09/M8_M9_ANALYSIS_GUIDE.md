# Analysis guide — v1.0.1

Choose cannabis or alcohol before examining associations. Load blank CSV cells as missing; retain synthetic identifiers as text.

| Exercise | Outcome | Required filter |
|---|---|---|
| M8 one-sample t versus zero | `instructional_mid_nac_arvn_bilateral` | `instructional_mid_analysis_eligible == 1` |
| M8 paired large versus small | `instructional_mid_nac_alrvn_bilateral`, `instructional_mid_nac_asrvn_bilateral` | Same MID filter; pair within participant |
| M8 independent groups (Welch) | Bilateral pooled contrast | `instructional_m8_cannabis_analysis_eligible == 1` or alcohol equivalent; compare selected `*_any_detailed` groups |
| M9 ANOVA | `mr_y_tfmri__sst__csvcg__dsk__pop__rh_beta` | `instructional_m9_cannabis_analysis_eligible == 1` or alcohol equivalent; selected `*_frequency_group` |
| M9 pairwise | Same SST outcome and groups | Three planned ANOVA-pooled comparisons; Bonferroni family alpha .05 |
| M9 stricter sensitivity | Same SST outcome | `instructional_sst_sensitivity_eligible == 1` AND selected `*_report_resolved == 1` |

Frequency groups: cannabis 0 / 1–11 / 12+ days; alcohol 0 / 1–5 / 6+ days in the common synthetic 365-day period. Labels 0/1/2 indicate no/lower/higher use, not clinical severity. Do not require the other substance to be resolved or the other imaging task to be eligible. Avoid whole-table complete-case filtering.

Use effect estimates and intervals alongside p-values. Inspect unequal allocation, group spreads and tails before interpreting the supplied methods. L8 uses Welch for its independent two-group comparison. L9 uses the common within-group variance assumption of its one-way ANOVA model; this is a different assumption, not a reversal of L8's method choice. A favorable SD ratio supports a diagnostic discussion but does not prove equal population variances.

For L9, let N = n0 + n1 + n2. Pool all three groups: MSE = sum[(ng − 1) × sg²] / (N − 3). For each planned pair i,j, use difference = mean_i − mean_j and SE = sqrt[MSE × (1/ni + 1/nj)], with the same error df = N − 3. This is neither a two-group pooled t test recomputed separately for each pair nor a Welch pairwise test.

Evaluate all three planned pairs in these directions: lower − zero (group 1 − group 0), higher − zero (2 − 0) and higher − lower (2 − 1), regardless of the omnibus ANOVA decision. A positive difference means the first-named group has the higher mean. For family alpha .05, adjusted p = min(3 × raw two-sided p, 1). Each adjusted interval is difference ± t_(1−.05/6, N−3) × SE; its individual confidence level is 1−.05/3, approximately 98.333%. The three intervals target simultaneous family coverage of at least 95% under the model assumptions. Do not label these ordinary 95% intervals or select a test because it gives a preferred p-value.

Keep the same outcome, group cutoffs, comparison directions and family in the stricter sensitivity analysis. Report it as a robustness comparison, not another opportunity to claim a discovery. The samples overlap; adjustment within each three-pair family does not control an unrestricted search across substances, samples or outcomes.

Power lesson: plan two-group scenarios d=.10/.20/.30 using reference SST SD .133 PSC, corresponding to .0133/.0266/.0399 PSC. State allocation, alpha, target power and assumptions. This is not observed post hoc power, a clinical threshold, or omnibus ANOVA power.

Interpretation prompts: How does co-use vary across your chosen groups? What changes under stricter eligibility? Which stimulus and response differences enter the stop-versus-go contrast? Why does higher activation not automatically mean better control? What does a nonsignificant result and its interval establish—and what remains uncertain?

Record the chosen substance, eligibility, three-pair family and provisional magnitude before examining associations. Use the chosen magnitude for the three pairs in each of the primary and stricter samples; the other power scenarios are reference material. Interval containment alone is not automatically a formal equivalence test. No observed post hoc power or outcome-dependent choice of margin is required.
