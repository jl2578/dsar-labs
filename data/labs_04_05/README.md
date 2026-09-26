# Labs 4–5 synthetic instructional data

These six CSVs support the student-facing Lab 4 and Lab 5 notebooks. They are synthetic instructional records, not ABCD participant data. The `sub-DSAR45M` identifiers are unique to this cohort; they must not be joined to Labs 1–3 records.

| File | Use |
| --- | --- |
| `gn_y_genrel.csv` | Family and twin links for Labs 4–5 |
| `su_y_tlfb.csv` | Alcohol and cannabis use days for Labs 4–5 |
| `mh_y_upps.csv` | Negative-urgency measure for Lab 4 |
| `nc_y_nihtb.csv` | Optional Lab 4 trait transfer |
| `instructional_pgs.csv` | Synthetic externalizing score for Lab 5 |
| `mh_p_cbcl.csv` | Optional Lab 5 Section 10 transfer |

Each use-day measure in `su_y_tlfb.csv` has a small share of blank responses at each session. A blank means unavailable, not zero use days. Alcohol and cannabis availability can differ for the same participant, and twin-pair analyses retain pairs with both outcomes available.
