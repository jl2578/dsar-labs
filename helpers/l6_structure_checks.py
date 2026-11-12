"""Diagnostic feedback for the two data-structure tasks in Sections 5 and 8.

These checks verify student objects; they do not return completed task objects or
change samples. The notebook keeps its worked demonstrations separate from them.
"""
import numpy as np
import pandas as pd


def check_repeated_table(frame, means_by_n, repetitions):
    if not isinstance(frame, pd.DataFrame):
        raise ValueError('Your Turn 2: construct a DataFrame with one row per repetition.')
    if list(frame.columns) != ['n', 'repetition', 'sample_mean']:
        raise ValueError('Your Turn 2: retain the three columns of the supplied tables; stack their rows.')
    if len(frame) != repetitions * len(means_by_n):
        raise ValueError('Your Turn 2: retain every repetition from both sample sizes.')
    if not frame.index.equals(pd.RangeIndex(len(frame))):
        raise ValueError('Your Turn 2: give the combined table a fresh consecutive row index.')
    if frame['n'].drop_duplicates().tolist() != list(means_by_n):
        raise ValueError('Your Turn 2: retain the supplied sample-size order and labels.')
    for n, rows in frame.groupby('n', sort=False):
        values = means_by_n[n]
        if len(rows) != repetitions or rows['repetition'].tolist() != list(range(1, repetitions + 1)):
            raise ValueError('Your Turn 2: repetition IDs restart at 1 within each sample size; retain their order.')
        if not np.array_equal(rows['sample_mean'].to_numpy(), np.asarray(values)):
            raise ValueError('Your Turn 2: retain the supplied means without sorting, averaging, rounding or redrawing them.')


def check_selected_runs(selected, full, n):
    if not isinstance(selected, pd.DataFrame):
        raise ValueError('Your Turn 2: select rows and retain all result columns.')
    if list(selected.columns) != list(full.columns):
        raise ValueError('Your Turn 2: retain every original column in its original order.')
    if len(selected) != int(full['n'].value_counts().get(n, 0)):
        raise ValueError('Your Turn 2: retain exactly the number of records belonging to this sample size.')
    if not selected['n'].eq(n).all() or not selected.index.is_unique:
        raise ValueError('Your Turn 2: every selected row must have the requested n and an unchanged unique index.')
    if not selected.index.is_monotonic_increasing or not selected.index.isin(full.index).all():
        raise ValueError('Your Turn 2: retain original row indices and their order.')
    if not selected.equals(full.reindex(selected.index)):
        raise ValueError('Your Turn 2: selection must not change any retained value.')


def check_interval_flags(sim, truth, covered):
    if not isinstance(sim, pd.DataFrame) or sim.empty:
        raise ValueError('Your Turn 3: the attempt table must contain at least one row.')
    if not isinstance(covered, pd.Series) or not covered.index.equals(sim.index):
        raise ValueError('Your Turn 3: return one Boolean flag aligned to each attempt, including undefined attempts.')
    if not pd.api.types.is_bool_dtype(covered.dtype) or covered.isna().any():
        raise ValueError('Your Turn 3: each attempt needs a True/False flag, not a missing value or a filtered row.')
    if covered.to_numpy(dtype=bool)[~sim['valid'].to_numpy(dtype=bool)].any():
        raise ValueError('Your Turn 3: an undefined interval cannot count as covering the target.')
    # The notebook's four-category partition check verifies classification.
    # This helper checks shape, alignment, type, and undefined-row behavior.


def check_coverage_rate(classified, rate):
    if classified.empty:
        raise ValueError('Your Turn 3: cannot summarize an empty attempt table.')
    if not np.isscalar(rate) or not np.isfinite(rate):
        raise ValueError('Your Turn 3: calculate a finite scalar proportion from the Boolean column.')
    if not 0 <= rate <= 1:
        raise ValueError('Your Turn 3: a proportion must be between zero and one.')
    if not np.isclose(rate * len(classified), int(classified['covered'].sum()), atol=1e-10, rtol=1e-14):
        raise ValueError('Your Turn 3: count covered attempts against all rows, including undefined attempts.')


def check_coverage_function(classify, summarize):
    """Use a small diagnostic table with a nonconsecutive index and boundary hits."""
    table = pd.DataFrame({'lower':[1., -2., 1.5, np.nan, -1.],
                          'upper':[2., .5, 3., np.nan, 1.],
                          'valid':[True, True, True, False, True]}, index=[8, 2, 11, 4, 6])
    result = classify(table, 1.)
    if not result.index.equals(table.index) or len(result) != len(table):
        raise ValueError('Your Turn 3: classification must preserve every attempt and its row index.')
    summary = summarize(table, 1.)
    expected = {'repetitions':5, 'covered_count':2, 'below_count':1, 'above_count':1,
                'undefined_count':1, 'coverage':.4, 'entirely_below_truth':.2,
                'entirely_above_truth':.2, 'undefined_rate':.2}
    if any(not np.isclose(summary[k], v) for k, v in expected.items()):
        raise ValueError('Your Turn 3: the diagnostic counts and proportions must retain all attempts.')
