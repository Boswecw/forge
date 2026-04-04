"""Property-based tests using Hypothesis."""

from __future__ import annotations

import re

from hypothesis import given, settings
from hypothesis import strategies as st

from forge_contract_core.identity import compute_idempotency_key, verify_idempotency_key
from forge_contract_core.refs import InvalidRefError, format_reference, parse_reference

# ── Idempotency key stability ──────────────────────────────────────────────────

@given(
    family=st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=1, max_size=64),
    artifact_id=st.uuids().map(str),
    version=st.integers(min_value=1, max_value=100),
    lineage_root_id=st.uuids().map(str),
)
@settings(max_examples=200)
def test_idempotency_key_always_64_hex_chars(family, artifact_id, version, lineage_root_id):
    key = compute_idempotency_key(family, artifact_id, version, lineage_root_id)
    assert len(key) == 64
    assert re.fullmatch(r"[0-9a-f]{64}", key) is not None


@given(
    family=st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=1, max_size=64),
    artifact_id=st.uuids().map(str),
    version=st.integers(min_value=1, max_value=100),
    lineage_root_id=st.uuids().map(str),
)
@settings(max_examples=200)
def test_idempotency_key_stable_for_same_inputs(family, artifact_id, version, lineage_root_id):
    k1 = compute_idempotency_key(family, artifact_id, version, lineage_root_id)
    k2 = compute_idempotency_key(family, artifact_id, version, lineage_root_id)
    assert k1 == k2


@given(
    family=st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=1, max_size=64),
    artifact_id=st.uuids().map(str),
    version=st.integers(min_value=1, max_value=100),
    lineage_root_id=st.uuids().map(str),
)
@settings(max_examples=200)
def test_verify_idempotency_key_roundtrip(family, artifact_id, version, lineage_root_id):
    key = compute_idempotency_key(family, artifact_id, version, lineage_root_id)
    assert verify_idempotency_key(key, family, artifact_id, version, lineage_root_id)


# ── Reference grammar roundtrip ────────────────────────────────────────────────

_FAMILY_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,127}$")
_UUID_STRATEGY = st.uuids().map(str)
_FAMILY_STRATEGY = st.from_regex(r"[a-z][a-z0-9_]{0,30}", fullmatch=True)


@given(
    family=_FAMILY_STRATEGY,
    artifact_id=_UUID_STRATEGY,
    version=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=200)
def test_reference_roundtrip(family: str, artifact_id: str, version: int):
    formatted = format_reference(family, artifact_id, version)
    parsed = parse_reference(formatted)
    assert parsed.family == family
    assert parsed.artifact_id == artifact_id
    assert parsed.version == version
    assert str(parsed) == formatted


@given(raw=st.text(min_size=0, max_size=256))
@settings(max_examples=300)
def test_invalid_references_raise_or_parse(raw: str):
    """Parsing never crashes — it either succeeds or raises InvalidRefError."""
    try:
        ref = parse_reference(raw)
        # If it parses, it must roundtrip
        assert str(ref) == raw
    except InvalidRefError:
        pass  # Expected for most random strings
