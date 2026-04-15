# Implementation Pack D — Rev 3 JSON Schemas (Slice 00)

Owner: Charlie
Scope: All JSON Schemas for the Eco-Stat Telemetry Eval Loop (Rev 3). These schemas are stricter than the Slice 00 placeholders and match later slices.

Put these files in: `signalforge/schemas/`

---

## Common conventions

- Every artifact MUST include:
  - `schema_version` (string, e.g. "v1")
  - `kind` (string, matches filename stem)
  - `run_id` (string)
  - `commit_sha` (string)
  - `generated_at` (string, ISO 8601)

---

## `risk_heatmap.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "weights", "targets"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "risk_heatmap"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "weights": {
      "type": "object",
      "additionalProperties": false,
      "required": ["w_churn", "w_deps", "w_tests", "w_violations", "w_history"],
      "properties": {
        "w_churn": {"type": "number"},
        "w_deps": {"type": "number"},
        "w_tests": {"type": "number"},
        "w_violations": {"type": "number"},
        "w_history": {"type": "number"}
      }
    },
    "targets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["target_id", "path", "risk_raw", "risk_norm", "components"],
        "properties": {
          "target_id": {"type": "string"},
          "path": {"type": "string"},
          "risk_raw": {"type": "number"},
          "risk_norm": {"type": "number"},
          "components": {
            "type": "object",
            "additionalProperties": false,
            "required": ["churn", "deps", "tests", "violations", "history"],
            "properties": {
              "churn": {"type": "number"},
              "deps": {"type": "number"},
              "tests": {"type": "number"},
              "violations": {"type": "number"},
              "history": {"type": "number"}
            }
          }
        }
      }
    }
  }
}
```

---

## `context_slices.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "tau", "expansion_lines", "slices"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "context_slices"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "tau": {"type": "number"},
    "expansion_lines": {"type": "integer", "minimum": 0},
    "slices": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["slice_id", "target_id", "path", "line_start", "line_end", "risk_norm", "reason", "diff_hunk_hash"],
        "properties": {
          "slice_id": {"type": "string"},
          "target_id": {"type": "string"},
          "path": {"type": "string"},
          "line_start": {"type": "integer", "minimum": 1},
          "line_end": {"type": "integer", "minimum": 1},
          "risk_norm": {"type": "number"},
          "reason": {"type": "string"},
          "diff_hunk_hash": {"type": "string"}
        }
      }
    }
  }
}
```

---

## `review_findings.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "reviewers", "findings"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "review_findings"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "reviewers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["reviewer_id", "type", "seed"],
        "properties": {
          "reviewer_id": {"type": "string"},
          "type": {"type": "string"},
          "seed": {"type": "integer"},
          "prompt_id": {"type": ["string", "null"]},
          "model": {"type": ["string", "null"]}
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "finding_id", "defect_key", "target_id", "path", "line_start", "line_end",
          "severity", "confidence", "violation_category", "summary", "reviewer_id", "evidence_hash"
        ],
        "properties": {
          "finding_id": {"type": "string"},
          "defect_key": {"type": "string"},
          "target_id": {"type": "string"},
          "path": {"type": "string"},
          "line_start": {"type": "integer", "minimum": 1},
          "line_end": {"type": "integer", "minimum": 1},
          "severity": {"type": "string"},
          "confidence": {"type": "number"},
          "violation_category": {"type": "string"},
          "summary": {"type": "string"},
          "reviewer_id": {"type": "string"},
          "evidence_hash": {"type": "string"}
        }
      }
    }
  }
}
```

---

## `telemetry_matrix.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version", "kind", "run_id", "commit_sha", "generated_at",
    "methods", "targets", "matrix", "method_health", "avg_pairwise_corr", "k_eff", "fail_closed", "provenance"
  ],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "telemetry_matrix"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "methods": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "targets": {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "matrix": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": {
          "anyOf": [
            {"type": "integer", "enum": [0, 1]},
            {"type": "null"}
          ]
        }
      }
    },
    "method_health": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["method_id", "status"],
        "properties": {
          "method_id": {"type": "string"},
          "status": {"type": "string", "enum": ["OK", "FAILED", "SKIPPED"]},
          "error_summary": {"type": ["string", "null"]},
          "files_scanned": {"type": ["integer", "null"], "minimum": 0},
          "findings_count": {"type": ["integer", "null"], "minimum": 0},
          "min_scan_coverage": {"type": ["number", "null"]}
        }
      }
    },
    "avg_pairwise_corr": {"type": "number"},
    "k_eff": {"type": "number"},
    "fail_closed": {"type": "boolean"},
    "provenance": {
      "type": "object",
      "additionalProperties": {"type": "string"}
    }
  }
}
```

---

## `occupancy_snapshot.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "per_target"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "occupancy_snapshot"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "per_target": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": false,
        "required": ["risk_bucket", "psi_prior", "psi_post", "detected_any", "p_by_method_used", "methods_included_in_update"],
        "properties": {
          "risk_bucket": {"type": "string"},
          "psi_prior": {"type": "number"},
          "psi_post": {"type": "number"},
          "detected_any": {"type": "boolean"},
          "p_by_method_used": {"type": "object", "additionalProperties": {"type": "number"}},
          "methods_included_in_update": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

---

## `capture_estimate.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "S_obs", "R", "q_summary", "chao1", "ice", "chosen", "estimate_confidence", "k_eff", "k_eff_threshold"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "capture_estimate"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "S_obs": {"type": "integer", "minimum": 0},
    "R": {"type": "integer", "minimum": 1},
    "q_summary": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 0}},
    "chao1": {
      "type": "object",
      "additionalProperties": false,
      "required": ["S_est", "f1", "f2", "guard_rule"],
      "properties": {
        "S_est": {"type": "number"},
        "f1": {"type": "integer", "minimum": 0},
        "f2": {"type": "integer", "minimum": 0},
        "guard_rule": {"type": "string"}
      }
    },
    "ice": {
      "type": "object",
      "additionalProperties": false,
      "required": ["S_est", "S_infr", "S_freq", "N_infr", "C_ICE", "M_infr", "gamma2"],
      "properties": {
        "S_est": {"type": "number"},
        "S_infr": {"type": "integer", "minimum": 0},
        "S_freq": {"type": "integer", "minimum": 0},
        "N_infr": {"type": "integer", "minimum": 0},
        "C_ICE": {"type": "number"},
        "M_infr": {"type": "integer", "minimum": 0},
        "gamma2": {"type": "number"}
      }
    },
    "chosen": {
      "type": "object",
      "additionalProperties": false,
      "required": ["S_est", "N_hidden", "safety_margin", "N_hidden_guarded", "rule"],
      "properties": {
        "S_est": {"type": "number"},
        "N_hidden": {"type": "number"},
        "safety_margin": {"type": "number"},
        "N_hidden_guarded": {"type": "number"},
        "rule": {"type": "string"}
      }
    },
    "estimate_confidence": {"type": "string", "enum": ["LOW", "NORMAL"]},
    "k_eff": {"type": "number"},
    "k_eff_threshold": {"type": "number"}
  }
}
```

---

## `calibration_report.schema.json` (optional artifact)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "posteriors"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "calibration_report"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "posteriors": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": {
          "type": "object",
          "additionalProperties": false,
          "required": ["alpha", "beta", "mean", "success", "trial"],
          "properties": {
            "alpha": {"type": "number"},
            "beta": {"type": "number"},
            "mean": {"type": "number"},
            "success": {"type": "integer", "minimum": 0},
            "trial": {"type": "integer", "minimum": 0}
          }
        }
      }
    }
  }
}
```

---

## `hazard_map.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "betas", "per_target"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "hazard_map"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "betas": {
      "type": "object",
      "additionalProperties": false,
      "required": ["beta0", "beta1", "beta2", "beta3", "beta4"],
      "properties": {
        "beta0": {"type": "number"},
        "beta1": {"type": "number"},
        "beta2": {"type": "number"},
        "beta3": {"type": "number"},
        "beta4": {"type": "number"}
      }
    },
    "per_target": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "additionalProperties": false,
        "required": ["hazard_probability", "features"],
        "properties": {
          "hazard_probability": {"type": "number"},
          "features": {"type": "object", "additionalProperties": {"type": "number"}}
        }
      }
    }
  }
}
```

---

## `merge_decision.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "decision", "reasons", "thresholds", "summary"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "merge_decision"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "decision": {"type": "string", "enum": ["ALLOW", "MORE_REVIEW", "BLOCK"]},
    "reasons": {"type": "array", "items": {"type": "string"}},
    "thresholds": {"type": "object", "additionalProperties": true},
    "summary": {"type": "object", "additionalProperties": true}
  }
}
```

---

## `evidence_bundle.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "kind", "run_id", "commit_sha", "generated_at", "ordered_artifacts", "artifact_hashes", "chain_hashes", "final_chain_hash", "config_sha256"],
  "properties": {
    "schema_version": {"type": "string"},
    "kind": {"const": "evidence_bundle"},
    "run_id": {"type": "string"},
    "commit_sha": {"type": "string"},
    "generated_at": {"type": "string"},
    "ordered_artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["kind", "path"],
        "properties": {
          "kind": {"type": "string"},
          "path": {"type": "string"}
        }
      }
    },
    "artifact_hashes": {"type": "array"},
    "chain_hashes": {"type": "array", "items": {"type": "string"}},
    "final_chain_hash": {"type": "string"},
    "config_sha256": {"type": "string"}
  }
}
```

