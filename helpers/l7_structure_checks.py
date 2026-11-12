"""Property and small-example checks for Lab 7's ungraded data-structure tasks.

These checks describe required behavior. They do not reconstruct a reference join
or contain a reference group-summary implementation.
"""
import numpy as np
import pandas as pd


def join_practice_tables():
    measurements = pd.DataFrame({
        'participant_id': ['P01', 'P01', 'P02'],
        'session_id': ['visit_A', 'visit_B', 'visit_A'],
        'use_days': [0, 3, 1],
    })
    context = pd.DataFrame({
        'participant_id': ['P01', 'P01', 'P03'],
        'session_id': ['visit_A', 'visit_B', 'visit_A'],
        'context': ['Medical', 'Recreational', 'Medical'],
    })
    return measurements, context


def check_join(joiner):
    left, right = join_practice_tables()
    left_before, right_before = left.copy(deep=True), right.copy(deep=True)
    joined = joiner(left, right)
    assert len(joined) == len(left), 'Keep each measurement row once, including one without context; do not add context-only rows.'
    assert set(left.columns).issubset(joined.columns), 'Keep the measurement columns with their original names.'
    pd.testing.assert_frame_equal(joined[left.columns].reset_index(drop=True), left)
    assert joined['context'].iloc[0] == 'Medical', 'Attach the context for the same visit.'
    assert joined['context'].iloc[1] == 'Recreational', 'Two visits of one person can have different contexts.'
    assert pd.isna(joined['context'].iloc[2]), 'An unmatched measurement must remain visible with missing context.'
    for side in ['measurement', 'context']:
        l = pd.concat([left, left.iloc[[0]]], ignore_index=True) if side == 'measurement' else left
        r = pd.concat([right, right.iloc[[0]]], ignore_index=True) if side == 'context' else right
        try:
            joiner(l, r)
        except pd.errors.MergeError:
            pass
        else:
            raise AssertionError(f'The relationship check should reject a repeated record in the {side} table.')
    pd.testing.assert_frame_equal(left, left_before)
    pd.testing.assert_frame_equal(right, right_before)


def _summary(result, columns, labels):
    assert isinstance(result, pd.DataFrame), 'Return the supplied summary table.'
    assert list(result.columns) == columns, 'Keep the supplied output columns.'
    assert result.index.is_unique and set(result.index) == set(labels), 'Keep one labeled row per group.'


def check_use_summary(summarizer):
    # Reordered labels test alignment. Zero is available; an unanswered outcome is not.
    toy = pd.DataFrame({
        'context': ['B', 'A', 'B', 'A', 'B', 'A', 'C'],
        'usable_days': [0., 2., 5., 0., np.nan, 4., np.nan],
        'any_use': pd.array([False, True, True, False, pd.NA, True, pd.NA], dtype='boolean'),
    })
    original = toy.copy(deep=True)
    result = summarizer(toy)
    _summary(result, ['sampled_n', 'available_n', 'any_use_percent'], ['A', 'B', 'C'])
    assert result.loc['A', 'sampled_n'] == 3 and result.loc['A', 'available_n'] == 3
    assert np.isclose(float(result.loc['A', 'any_use_percent']), 66.66666666666667), 'Count the documented zero in A, too.'
    assert result.loc['B', 'sampled_n'] == 3 and result.loc['B', 'available_n'] == 2
    assert np.isclose(float(result.loc['B', 'any_use_percent']), 50.), 'B has one user, one documented nonuser and one unavailable outcome.'
    assert result.loc['C', 'sampled_n'] == 1 and result.loc['C', 'available_n'] == 0
    assert pd.isna(result.loc['C', 'any_use_percent']), 'A group with no available outcomes has no defined percentage.'
    pd.testing.assert_frame_equal(toy, original)


def check_decision_summary(summarizer):
    toy = pd.DataFrame({
        'population': ['B', 'A', 'B', 'A', 'B', 'A', 'C'],
        'repetition': [1, 1, 2, 2, 3, 3, 1],
        'reject_H0': pd.array([False, True, False, False, pd.NA, pd.NA, pd.NA], dtype='boolean'),
    })
    original = toy.copy(deep=True)
    result = summarizer(toy)
    _summary(result, ['rejections', 'rejection_rate'], ['A', 'B', 'C'])
    assert result.loc['A', 'rejections'] == 1 and np.isclose(float(result.loc['A', 'rejection_rate']), .5), 'A has one rejection among two usable decisions; its third attempt is undefined.'
    assert result.loc['B', 'rejections'] == 0 and result.loc['B', 'rejection_rate'] == 0
    assert result.loc['C', 'rejections'] == 0 and pd.isna(result.loc['C', 'rejection_rate']), 'No usable decisions means an undefined rate, not zero.'
    pd.testing.assert_frame_equal(toy, original)
