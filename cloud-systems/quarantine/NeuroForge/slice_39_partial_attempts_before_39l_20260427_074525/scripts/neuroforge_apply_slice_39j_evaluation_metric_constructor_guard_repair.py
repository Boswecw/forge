#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "neuroforge_backend/database/models.py"
REPORT_DIR = ROOT / "reports/neuroforge-verification"

FIRST_TEST_OUT = REPORT_DIR / "slice_39j_dimension_trends_targeted_pytest.txt"
FULL_TEST_OUT = REPORT_DIR / "slice_39j_analytics_phase_3_0_targeted_pytest.txt"
TIMESTAMP = REPORT_DIR / "slice_39j_evaluation_metric_constructor_guard_repair.timestamp"
JSON_REPORT = REPORT_DIR / "slice_39j_evaluation_metric_constructor_guard_repair.json"
STATUS = REPORT_DIR / "slice_39j_status.env"
ACCEPTANCE = REPORT_DIR / "slice_39j_EVALUATION_METRIC_CONSTRUCTOR_GUARD_REPAIR_ACCEPTANCE.md"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().astimezone().isoformat(timespec="seconds")
TIMESTAMP.write_text(stamp + "\n", encoding="utf-8")

if not MODELS.exists():
    raise SystemExit(f"[FAIL] Missing expected model file: {MODELS}")

text = MODELS.read_text(encoding="utf-8")
original = text
changes: list[str] = []

# Import uuid4 for constructor/default generation.
if "from uuid import uuid4" not in text:
    text = text.replace(
        "from datetime import datetime\n",
        "from datetime import datetime\nfrom uuid import uuid4\n",
        1,
    )
    changes.append("added_uuid4_import")

# Keep/restore Slice 39 metric_name alias compatibility.
if "from sqlalchemy.orm import relationship, synonym" not in text:
    text = text.replace(
        "from sqlalchemy.orm import relationship\n",
        "from sqlalchemy.orm import relationship, synonym\n",
        1,
    )
    changes.append("added_synonym_import")

# Isolate the EvaluationMetric class block.
class_match = re.search(
    r"(?ms)^class EvaluationMetric\(Base\):\n(?P<body>.*?)(?=^class \w+\(Base\):|\Z)",
    text,
)
if not class_match:
    raise SystemExit("[FAIL] Could not locate EvaluationMetric class block")

class_start, class_end = class_match.span()
class_text = text[class_start:class_end]

# Add metric_name synonym after dimension if missing.
if 'metric_name = synonym("dimension")' not in class_text:
    dim_pattern = re.compile(
        r'(?m)^(?P<indent>\s*)dimension\s*=\s*Column\(String\(50\),\s*nullable=False\)(?P<comment>[^\n]*)\n'
    )
    dim_match = dim_pattern.search(class_text)
    if not dim_match:
        raise SystemExit("[FAIL] Could not locate EvaluationMetric.dimension column")
    insert = (
        dim_match.group(0)
        + f'{dim_match.group("indent")}# Compatibility alias for analytics constructor contract.\n'
        + f'{dim_match.group("indent")}metric_name = synonym("dimension")\n'
    )
    class_text = class_text[: dim_match.start()] + insert + class_text[dim_match.end() :]
    changes.append("added_metric_name_synonym")

# Add Python-side default to eval_metric_id column, regardless of minor column shape differences.
eval_line_pattern = re.compile(r'(?m)^(?P<indent>\s*)eval_metric_id\s*=\s*Column\((?P<body>[^\n]*)\)\s*$')
eval_match = eval_line_pattern.search(class_text)
if not eval_match:
    raise SystemExit("[FAIL] Could not locate EvaluationMetric.eval_metric_id column")
if "default=" not in eval_match.group("body"):
    body = eval_match.group("body").rstrip()
    new_line = f'{eval_match.group("indent")}eval_metric_id = Column({body}, default=lambda: str(uuid4()))'
    class_text = class_text[: eval_match.start()] + new_line + class_text[eval_match.end() :]
    changes.append("added_eval_metric_id_column_default")

# Add Python-side default to model_id column, without assuming the exact existing column shape.
model_line_pattern = re.compile(r'(?m)^(?P<indent>\s*)model_id\s*=\s*Column\((?P<body>[^\n]*)\)\s*$')
model_match = model_line_pattern.search(class_text)
if not model_match:
    raise SystemExit("[FAIL] Could not locate EvaluationMetric.model_id column")
if "default=" not in model_match.group("body"):
    body = model_match.group("body").rstrip()
    new_line = f'{model_match.group("indent")}model_id = Column({body}, default="unknown_model")'
    class_text = class_text[: model_match.start()] + new_line + class_text[model_match.end() :]
    changes.append("added_model_id_column_default")

# Constructor guard: maps metric_name -> dimension, generates missing IDs, and preserves TypeError on unknown kwargs.
constructor_marker = "def __init__(self, **kwargs):"
if constructor_marker not in class_text:
    indent = "    "
    constructor = f'''
{indent}def __init__(self, **kwargs):
{indent}    # Compatibility guard for legacy analytics fixture/runtime construction.
{indent}    if "metric_name" in kwargs and "dimension" not in kwargs:
{indent}        kwargs["dimension"] = kwargs.pop("metric_name")
{indent}    else:
{indent}        kwargs.pop("metric_name", None)
{indent}
{indent}    if not kwargs.get("eval_metric_id"):
{indent}        kwargs["eval_metric_id"] = str(uuid4())
{indent}    if kwargs.get("model_id") is None:
{indent}        kwargs["model_id"] = "unknown_model"
{indent}
{indent}    valid_keys = {{prop.key for prop in self.__mapper__.attrs}}
{indent}    for key, value in kwargs.items():
{indent}        if key not in valid_keys:
{indent}            raise TypeError(f"{{key!r}} is an invalid keyword argument for {{self.__class__.__name__}}")
{indent}        setattr(self, key, value)
'''
    # Prefer inserting before the relationships section, otherwise before the end of the class block.
    rel_match = re.search(r'(?m)^\s*#\s*Relationships\s*$', class_text)
    if rel_match:
        insert_at = rel_match.start()
        class_text = class_text[:insert_at].rstrip() + "\n" + constructor + "\n" + class_text[insert_at:]
    else:
        class_text = class_text.rstrip() + "\n" + constructor + "\n"
    changes.append("added_constructor_guard")

text = text[:class_start] + class_text + text[class_end:]

if text != original:
    MODELS.write_text(text, encoding="utf-8")

python_bin = ROOT / "neuroforge_backend/.venv/bin/python"
if not python_bin.exists():
    raise SystemExit(f"[FAIL] Missing expected Python interpreter: {python_bin}")

def run_pytest(args: list[str], outfile: Path) -> int:
    cmd = [str(python_bin), "-m", "pytest", *args]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    outfile.write_text(proc.stdout, encoding="utf-8")
    return proc.returncode

first_rc = run_pytest(
    ["-q", "-x", "neuroforge_backend/tests/test_analytics_phase_3_0.py::test_dimension_trends"],
    FIRST_TEST_OUT,
)

full_rc: int | None = None
if first_rc == 0:
    full_rc = run_pytest(
        ["-q", "neuroforge_backend/tests/test_analytics_phase_3_0.py"],
        FULL_TEST_OUT,
    )
else:
    FULL_TEST_OUT.write_text(
        "Full analytics pytest was not run because the first targeted analytics test still failed.\n",
        encoding="utf-8",
    )

if first_rc != 0:
    result = "FAIL"
elif full_rc == 0:
    result = "PASS"
else:
    result = "PARTIAL"

report = {
    "stamp": stamp,
    "result": result,
    "repair_scope": "EvaluationMetric constructor guard and persistence defaults",
    "changed_model_file": str(MODELS.relative_to(ROOT)),
    "changes": changes,
    "first_test_returncode": first_rc,
    "full_test_returncode": full_rc,
    "first_test_output": str(FIRST_TEST_OUT.relative_to(ROOT)),
    "full_test_output": str(FULL_TEST_OUT.relative_to(ROOT)),
    "status": str(STATUS.relative_to(ROOT)),
}
JSON_REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

STATUS.write_text(
    "\n".join(
        [
            f"STAMP={stamp}",
            f"SLICE_39J_RESULT={result}",
            "REPAIR_SCOPE=EvaluationMetric_constructor_guard_and_persistence_defaults",
            f"FIRST_TEST_RETURNCODE={first_rc}",
            f"FULL_TEST_RETURNCODE={'' if full_rc is None else full_rc}",
            f"FIRST_TEST_OUTPUT={FIRST_TEST_OUT.relative_to(ROOT)}",
            f"FULL_TEST_OUTPUT={FULL_TEST_OUT.relative_to(ROOT)}",
            f"JSON_REPORT={JSON_REPORT.relative_to(ROOT)}",
            "",
        ]
    ),
    encoding="utf-8",
)

acceptance = f"""# Slice 39J — EvaluationMetric Constructor Guard Repair

Generated: {stamp}

## Result

`{result}`

## Scope

This repair is intentionally bounded to `neuroforge_backend/database/models.py`.

It aligns `EvaluationMetric` with the analytics constructor/persistence contract by:

- accepting `metric_name=` as a compatibility alias for canonical `dimension`
- generating `eval_metric_id` when constructors omit it
- preserving a bounded `model_id` fallback when constructors omit or pass `None`
- preserving TypeError behavior for unknown constructor keys

## Verification

| Check | Return Code |
| --- | ---: |
| `test_dimension_trends` | {first_rc} |
| `test_analytics_phase_3_0.py` | {"" if full_rc is None else full_rc} |

## Evidence Files

- `{TIMESTAMP.relative_to(ROOT)}`
- `{FIRST_TEST_OUT.relative_to(ROOT)}`
- `{FULL_TEST_OUT.relative_to(ROOT)}`
- `{JSON_REPORT.relative_to(ROOT)}`
- `{STATUS.relative_to(ROOT)}`

## Posture

Commit this slice only if the result is `PASS`.

If the result is `PARTIAL` or `FAIL`, inspect the targeted pytest output before committing.
"""
ACCEPTANCE.write_text(acceptance, encoding="utf-8")

print(f"[SLICE_39J_RESULT] {result}")
print(f"[FIRST_TEST_RETURNCODE] {first_rc}")
print(f"[FULL_TEST_RETURNCODE] {'' if full_rc is None else full_rc}")
print(f"[STATUS] {STATUS.relative_to(ROOT)}")
