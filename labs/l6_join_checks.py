"""Supplied feedback for the historical lookup and supplied Lab 6 eligibility flags."""
from pathlib import Path

import pandas as pd


_AUDIT_OUTCOMES = {"adversity": "ace10", "cohesion": "cohesion"}


def check_context_lookup(context):
    """Check basic source-table properties; key properties await the student's list."""
    assert isinstance(context, pd.DataFrame) and not context.empty, "The supplied context lookup is empty."
    assert context.columns.is_unique, "The supplied lookup repeats a column name."
    assert not context.duplicated().any(), "The supplied lookup contains a repeated full record."


def check_join_keys(join_keys, link_rows, context):
    """Check the submitted key's table properties without storing the answer list."""
    assert isinstance(join_keys, list) and all(isinstance(key, str) for key in join_keys), (
        "Supply the geographic lookup columns as a list of field names."
    )
    assert len(join_keys) >= 2 and len(join_keys) == len(set(join_keys)), (
        "Use distinct fields for the declared geographic identity and historical source period."
    )
    assert all(key in link_rows.columns and key in context.columns for key in join_keys), (
        "Every proposed joining field must exist in both source tables."
    )
    assert context[join_keys].notna().all().all(), "The proposed lookup key has a missing value."
    assert not context.duplicated(join_keys).any(), "The proposed key does not identify one lookup record."


def check_release_eligibility(data_path, choice, eligible_ids):
    """Compare IDs with the supplied eligible_l6 flags, without rebuilding the student's filter."""
    assert choice in _AUDIT_OUTCOMES, "Choose one of the assigned L6 outcomes."
    audit = pd.read_csv(
        Path(data_path) / "eligibility_audit.csv",
        usecols=["participant_id", "session_id", "outcome", "eligible_l6"],
    )
    selected = audit.loc[audit["outcome"].eq(_AUDIT_OUTCOMES[choice])]
    assert len(selected) and selected["session_id"].eq("ses-07A").all(), (
        "The eligibility audit does not identify the expected outcome visit."
    )
    assert selected["participant_id"].is_unique, "The eligibility audit repeats a participant for this outcome."
    assert pd.api.types.is_bool_dtype(selected["eligible_l6"].dtype), (
        "The eligibility flags must contain Boolean values."
    )
    assert selected["eligible_l6"].notna().all(), "The eligibility audit has an unavailable flag."
    submitted = pd.Series(list(eligible_ids), dtype="string")
    assert submitted.notna().all() and submitted.is_unique, "The selected roster must contain one record per participant."
    expected = set(selected.loc[selected["eligible_l6"], "participant_id"])
    assert set(submitted) == expected, (
        "Your roster disagrees with the supplied eligibility audit. Recheck the chosen outcome, "
        "report availability, usable zeros, and whether context completeness was added to eligibility."
    )

