#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports/neuroforge-verification"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PYTHON = ROOT / "neuroforge_backend/.venv/bin/python"
TEST_PATH = "neuroforge_backend/tests/test_analytics_phase_3_0.py::test_dimension_trends"
TEST_FILE = ROOT / "neuroforge_backend/tests/test_analytics_phase_3_0.py"
MODELS_FILE = ROOT / "neuroforge_backend/database/models.py"

TIMESTAMP = REPORT_DIR / "slice_39k_analytics_first_failure_detail_probe.timestamp"
PYTEST_OUT = REPORT_DIR / "slice_39k_dimension_trends_first_failure_detail.txt"
SIGNALS_TSV = REPORT_DIR / "slice_39k_dimension_trends_failure_signals.tsv"
CONTEXT_MD = REPORT_DIR / "slice_39k_dimension_trends_source_context.md"
JSON_REPORT = REPORT_DIR / "slice_39k_analytics_first_failure_detail_probe.json"
STATUS = REPORT_DIR / "slice_39k_status.env"
ACCEPTANCE = REPORT_DIR / "slice_39k_ANALYTICS_FIRST_FAILURE_DETAIL_PROBE_ACCEPTANCE.md"

stamp = datetime.now().astimezone().isoformat(timespec="seconds")
TIMESTAMP.write_text(stamp + "\n", encoding="utf-8")


def run(cmd: list[str], *, timeout: int | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONPATH": str(ROOT)},
        )
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or ""
        return 124, f"{out}\n{err}\n[TIMEOUT] command exceeded {timeout} seconds\n"


def slice_around_lines(text: str, pattern: str, before: int = 25, after: int = 60) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.search(pattern, line):
            start = max(0, idx - before)
            end = min(len(lines), idx + after + 1)
            return "\n".join(f"{i + 1}: {lines[i]}" for i in range(start, end))
    return ""


def collect_signal_lines(text: str) -> list[dict[str, str]]:
    patterns = [
        r"^=+ (FAILURES|ERRORS|short test summary info)",
        r"FAILED ",
        r"ERROR ",
        r"AssertionError",
        r"TypeError",
        r"AttributeError",
        r"IntegrityError",
        r"OperationalError",
        r"StatementError",
        r"ResponseValidationError",
        r"RequestValidationError",
        r"KeyError",
        r"IndexError",
        r"ValueError",
        r"E\s+assert ",
        r"E\s+.*==.*",
        r"EvaluationMetric",
        r"dimension_trends",
        r"metric_name",
        r"model_id",
        r"eval_metric_id",
        r"status_code",
        r"response\.json",
        r"404",
        r"422",
        r"500",
    ]
    rx = re.compile("|".join(f"(?:{p})" for p in patterns))
    rows: list[dict[str, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if rx.search(line):
            rows.append({"line": str(idx), "text": line[:600]})
    return rows


def get_constructor_sanity() -> dict[str, object]:
    sanity_code = r'''
from neuroforge_backend.database.models import EvaluationMetric
m = EvaluationMetric(inference_id="slice-39k", metric_name="coherence", model_id=None, score=0.91)
print("eval_metric_id=" + str(getattr(m, "eval_metric_id", None)))
print("model_id=" + str(getattr(m, "model_id", None)))
print("dimension=" + str(getattr(m, "dimension", None)))
print("metric_name=" + str(getattr(m, "metric_name", None)))
print("score=" + str(getattr(m, "score", None)))
'''
    rc, out = run([str(PYTHON), "-c", sanity_code], timeout=30)
    return {"returncode": rc, "output": out}


sanity = get_constructor_sanity()

cmd = [
    str(PYTHON),
    "-m",
    "pytest",
    "-vv",
    "-s",
    "--tb=long",
    "-x",
    TEST_PATH,
]
first_rc, first_out = run(cmd, timeout=180)
PYTEST_OUT.write_text(first_out, encoding="utf-8")

signals = collect_signal_lines(first_out)
with SIGNALS_TSV.open("w", encoding="utf-8") as fh:
    fh.write("line\ttext\n")
    for row in signals:
        fh.write(f"{row['line']}\t{row['text'].replace(chr(9), ' ')}\n")

failure_context = (
    slice_around_lines(first_out, r"^=+ (FAILURES|ERRORS)")
    or slice_around_lines(first_out, r"AssertionError|TypeError|AttributeError|IntegrityError|OperationalError|ResponseValidationError|RequestValidationError")
    or slice_around_lines(first_out, r"FAILED|ERROR")
    or "[NO_FAILURE_CONTEXT_MATCHED]"
)

source_context = ""
if TEST_FILE.exists():
    test_text = TEST_FILE.read_text(encoding="utf-8", errors="replace")
    source_context = slice_around_lines(test_text, r"def test_dimension_trends", before=20, after=120)

model_context = ""
if MODELS_FILE.exists():
    model_text = MODELS_FILE.read_text(encoding="utf-8", errors="replace")
    model_context = slice_around_lines(model_text, r"class EvaluationMetric", before=10, after=90)

CONTEXT_MD.write_text(
    "# Slice 39K Analytics First Failure Detail Probe\n\n"
    f"Timestamp: `{stamp}`\n\n"
    "## Constructor Sanity Output\n\n"
    "```text\n" + str(sanity["output"]) + "\n```\n\n"
    "## Failure Context\n\n"
    "```text\n" + failure_context + "\n```\n\n"
    "## Test Source Context: test_dimension_trends\n\n"
    "```python\n" + (source_context or "[NOT_FOUND]") + "\n```\n\n"
    "## Model Source Context: EvaluationMetric\n\n"
    "```python\n" + (model_context or "[NOT_FOUND]") + "\n```\n",
    encoding="utf-8",
)

# Classify the next likely repair posture from the captured output.
text = first_out
if first_rc == 0:
    bucket = "dimension_trends_first_target_passed"
    posture = "proceed to full analytics test gate"
elif "IntegrityError" in text and "eval_metric_id" in text:
    bucket = "evaluation_metric_pk_default_persistence_contract"
    posture = "repair EvaluationMetric PK/default persistence contract"
elif "NOT NULL constraint failed: evaluation_metrics.model_id" in text or ("IntegrityError" in text and "model_id" in text):
    bucket = "evaluation_metric_model_id_default_persistence_contract"
    posture = "repair EvaluationMetric model_id default persistence contract"
elif "TypeError" in text and "metric_name" in text and "invalid keyword" in text:
    bucket = "evaluation_metric_constructor_alias_contract"
    posture = "repair constructor alias contract"
elif "AssertionError" in text and ("status_code" in text or "404" in text or "422" in text or "500" in text):
    bucket = "analytics_endpoint_response_status_contract"
    posture = "repair analytics endpoint/status contract"
elif "AssertionError" in text:
    bucket = "analytics_dimension_trends_assertion_contract"
    posture = "inspect expected vs actual payload shape"
elif first_rc == 124:
    bucket = "analytics_dimension_trends_timeout_or_hang"
    posture = "probe fixture/runtime wait boundary"
else:
    bucket = "analytics_dimension_trends_unclassified_failure"
    posture = "inspect detailed failure context before repair"

report = {
    "stamp": stamp,
    "slice": "39K",
    "probe_result": "PASS" if sanity["returncode"] == 0 and PYTEST_OUT.exists() else "FAIL",
    "constructor_sanity_returncode": sanity["returncode"],
    "first_targeted_returncode": first_rc,
    "target_test": TEST_PATH,
    "classified_bucket": bucket,
    "recommended_posture": posture,
    "files": {
        "timestamp": str(TIMESTAMP.relative_to(ROOT)),
        "pytest_output": str(PYTEST_OUT.relative_to(ROOT)),
        "signals_tsv": str(SIGNALS_TSV.relative_to(ROOT)),
        "context_md": str(CONTEXT_MD.relative_to(ROOT)),
        "json_report": str(JSON_REPORT.relative_to(ROOT)),
        "status_env": str(STATUS.relative_to(ROOT)),
        "acceptance": str(ACCEPTANCE.relative_to(ROOT)),
    },
    "signals_count": len(signals),
}
JSON_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

STATUS.write_text(
    "STAMP={stamp}\n"
    "SLICE_39K_RESULT={result}\n"
    "CONSTRUCTOR_SANITY_RETURNCODE={sanity_rc}\n"
    "FIRST_TARGETED_RETURNCODE={first_rc}\n"
    "CLASSIFIED_BUCKET={bucket}\n"
    "RECOMMENDED_POSTURE={posture}\n"
    "TARGETED_PYTEST={pytest_out}\n"
    "SIGNALS_TSV={signals}\n"
    "CONTEXT_MD={context}\n".format(
        stamp=stamp,
        result=report["probe_result"],
        sanity_rc=sanity["returncode"],
        first_rc=first_rc,
        bucket=bucket,
        posture=posture.replace(" ", "_"),
        pytest_out=str(PYTEST_OUT.relative_to(ROOT)),
        signals=str(SIGNALS_TSV.relative_to(ROOT)),
        context=str(CONTEXT_MD.relative_to(ROOT)),
    ),
    encoding="utf-8",
)

ACCEPTANCE.write_text(
    "# Slice 39K — Analytics First Failure Detail Probe Acceptance\n\n"
    f"Timestamp: `{stamp}`\n\n"
    "## Result\n\n"
    f"- Probe result: `{report['probe_result']}`\n"
    f"- Constructor sanity return code: `{sanity['returncode']}`\n"
    f"- First targeted return code: `{first_rc}`\n"
    f"- Classified bucket: `{bucket}`\n"
    f"- Recommended posture: `{posture}`\n\n"
    "## Evidence Files\n\n"
    f"- `{TIMESTAMP.relative_to(ROOT)}`\n"
    f"- `{PYTEST_OUT.relative_to(ROOT)}`\n"
    f"- `{SIGNALS_TSV.relative_to(ROOT)}`\n"
    f"- `{CONTEXT_MD.relative_to(ROOT)}`\n"
    f"- `{JSON_REPORT.relative_to(ROOT)}`\n"
    f"- `{STATUS.relative_to(ROOT)}`\n\n"
    "## Acceptance Meaning\n\n"
    "This slice is a probe only. A passing slice means the first post-39J analytics failure was captured, classified, and written to evidence. It does not mean the analytics test passed.\n\n"
    "## Next Slice Rule\n\n"
    "Repair only the classified bucket reported by `slice_39k_status.env`. Do not combine endpoint, fixture, model, and analytics assertion repairs in one slice.\n",
    encoding="utf-8",
)

print(f"[SLICE_39K_RESULT] {report['probe_result']}")
print(f"[CONSTRUCTOR_SANITY_RETURNCODE] {sanity['returncode']}")
print(f"[FIRST_TARGETED_RETURNCODE] {first_rc}")
print(f"[CLASSIFIED_BUCKET] {bucket}")
print(f"[RECOMMENDED_POSTURE] {posture}")
print(f"[TARGETED_PYTEST] {PYTEST_OUT.relative_to(ROOT)}")
print(f"[CONTEXT_MD] {CONTEXT_MD.relative_to(ROOT)}")
