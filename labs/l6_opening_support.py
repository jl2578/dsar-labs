"""Supplied display and descriptive helpers; no student solution or hidden outcomes."""
import numpy as np
import pandas as pd

def show(value):
    """Render in Jupyter; allow the same calculations in a plain Python process."""
    try:
        from IPython.display import display
        display(value)
    except ImportError:
        print(value.to_string() if isinstance(value,(pd.DataFrame,pd.Series)) else value)

def seed_rng(role, operation, n, run=0):
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([6060,role,operation,n,run])))

def summarize_discovery(samples, days_field):
    rows=[]
    for label,sample in samples.items():
        for band in sample['ace_band'].cat.categories:
            band_values=sample.loc[sample['ace_band'].eq(band),days_field]
            values=band_values.dropna()
            n=len(values); k=int(values.gt(0).sum())
            rows.append({'sample':label,'ace_band':str(band),'sample_band_n':len(band_values),
                'usable_n':n,'unavailable_n':int(band_values.isna().sum()),'users':k,
                'any_use_pct':100*k/n if n else np.nan,
                'mean_days_all':float(values.mean()) if n else np.nan,
                'sparse':n<20,'few_users':k<10})
    return pd.DataFrame(rows)

def summarize_coi(samples, coi_field, ace_field):
    """Count fixed ACE10 bands within each historical COI level.

    Each percentage uses only records with both an available ACE10 score and
    the requested COI level. A level with no such records has n=0, zero band
    counts, and missing percentages/mean. No samples or categories are pooled.
    """
    rows=[]
    for label,sample in samples.items():
        coi = pd.to_numeric(sample[coi_field], errors='raise')
        ace = pd.to_numeric(sample[ace_field], errors='raise')
        available_coi, available_ace = coi.dropna(), ace.dropna()
        if not available_coi.isin(range(1,6)).all():
            raise ValueError('Available COI levels must be integers from 1 through 5.')
        if not (np.isfinite(available_ace).all()
                and available_ace.between(0,10).all()
                and available_ace.eq(np.floor(available_ace)).all()):
            raise ValueError('Available ACE10 scores must be integers from 0 through 10.')
        for level in range(1,6):
            values=ace.loc[coi.eq(level)].dropna()
            n=len(values)
            counts = {'0':int(values.eq(0).sum()), '1':int(values.eq(1).sum()),
                      '2_3':int(values.between(2,3).sum()), '4_plus':int(values.ge(4).sum())}
            rows.append({'sample':label,'coi_level':level,'n':n,
                'mean':float(values.mean()) if n else np.nan,
                **{f'n_{band}':count for band,count in counts.items()},
                **{f'pct_{band}':100*count/n if n else np.nan for band,count in counts.items()},
                'sparse':n<20})
    return pd.DataFrame(rows)
