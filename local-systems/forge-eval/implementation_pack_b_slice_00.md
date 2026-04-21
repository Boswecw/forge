# Implementation Pack B — Slice 00.5 Evidence Crate (forge_evidence) + Notes

Owner: Charlie
Scope: Slice 00.5a Rust binary `forge-evidence` implementing canonicalization + hashing + hashchain.

Key properties:
- Sorted keys
- UTF-8
- Reject NaN/Infinity
- **Float sanitization:** round and print floats to exactly 8 decimal places (configurable)

---

## Folder layout

```
forge_evidence/
  Cargo.toml
  src/
    main.rs
  tests/
    golden_canonicalize.rs
```

---

## `forge_evidence/Cargo.toml`

```toml
[package]
name = "forge_evidence"
version = "0.1.0"
edition = "2024"

[dependencies]
anyhow = "1"
clap = { version = "4", features = ["derive"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sha2 = "0.10"
hex = "0.4"
```

---

## `forge_evidence/src/main.rs`

```rust
use anyhow::{anyhow, Context, Result};
use clap::{Parser, Subcommand};
use serde::Deserialize;
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::fs;
use std::io::{Read, Write};

#[derive(Parser)]
#[command(name = "forge-evidence")]
#[command(about = "Deterministic evidence utilities (canonicalize, sha256, artifact-id, hashchain).")]
struct Cli {
    #[command(subcommand)]
    cmd: Cmd,

    /// Float precision for canonicalization
    #[arg(long, default_value_t = 8)]
    float_precision: usize,
}

#[derive(Subcommand)]
enum Cmd {
    Canonicalize,
    Sha256,
    ArtifactId {
        #[arg(long)]
        kind: String,
    },
    Hashchain {
        #[arg(long)]
        manifest: String,
    },
}

#[derive(Debug, Deserialize)]
struct ManifestEntry {
    kind: String,
    path: String,
}

fn read_stdin_bytes() -> Result<Vec<u8>> {
    let mut buf = Vec::new();
    std::io::stdin().read_to_end(&mut buf)?;
    Ok(buf)
}

fn sha256_hex(bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(bytes);
    hex::encode(h.finalize())
}

fn round_f64(x: f64, precision: usize) -> f64 {
    let factor = 10_f64.powi(precision as i32);
    (x * factor).round() / factor
}

fn write_canonical_json<W: Write>(w: &mut W, v: &Value, precision: usize) -> Result<()> {
    match v {
        Value::Null => w.write_all(b"null")?,
        Value::Bool(b) => {
            if *b {
                w.write_all(b"true")?
            } else {
                w.write_all(b"false")?
            }
        }
        Value::Number(n) => {
            if let Some(f) = n.as_f64() {
                if !f.is_finite() {
                    return Err(anyhow!("Non-finite float encountered"));
                }
                if (f.fract().abs() < f64::EPSILON)
                    && f >= (i64::MIN as f64)
                    && f <= (i64::MAX as f64)
                {
                    let i = f as i64;
                    w.write_all(i.to_string().as_bytes())?;
                } else {
                    let rf = round_f64(f, precision);
                    let s = format!("{:.*}", precision, rf);
                    w.write_all(s.as_bytes())?;
                }
            } else if let Some(i) = n.as_i64() {
                w.write_all(i.to_string().as_bytes())?;
            } else if let Some(u) = n.as_u64() {
                w.write_all(u.to_string().as_bytes())?;
            } else {
                return Err(anyhow!("Unsupported number representation"));
            }
        }
        Value::String(s) => {
            let escaped = serde_json::to_string(s)?;
            w.write_all(escaped.as_bytes())?;
        }
        Value::Array(arr) => {
            w.write_all(b"[")?;
            for (idx, item) in arr.iter().enumerate() {
                if idx > 0 {
                    w.write_all(b",")?;
                }
                write_canonical_json(w, item, precision)?;
            }
            w.write_all(b"]")?;
        }
        Value::Object(map) => {
            w.write_all(b"{")?;
            let mut keys: Vec<&String> = map.keys().collect();
            keys.sort();
            for (idx, k) in keys.iter().enumerate() {
                if idx > 0 {
                    w.write_all(b",")?;
                }
                let key_json = serde_json::to_string(*k)?;
                w.write_all(key_json.as_bytes())?;
                w.write_all(b":")?;
                let val = map.get(*k).expect("key exists");
                write_canonical_json(w, val, precision)?;
            }
            w.write_all(b"}")?;
        }
    }
    Ok(())
}

fn canonicalize_bytes(json_bytes: &[u8], precision: usize) -> Result<Vec<u8>> {
    let v: Value = serde_json::from_slice(json_bytes).context("Invalid JSON input")?;
    let mut out = Vec::<u8>::new();
    write_canonical_json(&mut out, &v, precision)?;
    Ok(out)
}

fn artifact_id(kind: &str, canonical_bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(kind.as_bytes());
    h.update([0u8]);
    h.update(canonical_bytes);
    hex::encode(h.finalize())
}

fn cmd_canonicalize(precision: usize) -> Result<()> {
    let input = read_stdin_bytes()?;
    let canon = canonicalize_bytes(&input, precision)?;
    std::io::stdout().write_all(&canon)?;
    Ok(())
}

fn cmd_sha256() -> Result<()> {
    let input = read_stdin_bytes()?;
    let hex = sha256_hex(&input);
    println!("{hex}");
    Ok(())
}

fn cmd_artifact_id(kind: &str, precision: usize) -> Result<()> {
    let input = read_stdin_bytes()?;
    let canon = canonicalize_bytes(&input, precision)?;
    let id = artifact_id(kind, &canon);
    println!("{id}");
    Ok(())
}

fn cmd_hashchain(manifest_path: &str, precision: usize) -> Result<()> {
    let manifest_bytes = fs::read(manifest_path).with_context(|| format!("Read manifest: {manifest_path}"))?;

    let entries: Vec<ManifestEntry> = match serde_json::from_slice::<Value>(&manifest_bytes)? {
        Value::Array(_) => serde_json::from_slice(&manifest_bytes)?,
        Value::Object(_) => {
            #[derive(Deserialize)]
            struct Wrap {
                artifacts: Vec<ManifestEntry>,
            }
            serde_json::from_slice::<Wrap>(&manifest_bytes)?.artifacts
        }
        _ => return Err(anyhow!("Manifest must be array or object with artifacts[]")),
    };

    let mut artifact_hashes = Vec::new();
    let mut chain = Vec::new();
    let prev0 = [0u8; 32];
    chain.push(hex::encode(prev0));

    for e in entries.iter() {
        let raw = fs::read(&e.path).with_context(|| format!("Read artifact: {}", e.path))?;
        let canon = canonicalize_bytes(&raw, precision)?;
        let a_hash_hex = sha256_hex(&canon);

        let prev_bytes = hex::decode(chain.last().unwrap())?;
        let a_hash_bytes = hex::decode(&a_hash_hex)?;

        let mut h = Sha256::new();
        h.update(prev_bytes);
        h.update([0u8]);
        h.update(a_hash_bytes);
        let next = h.finalize();
        chain.push(hex::encode(next));

        artifact_hashes.push(serde_json::json!({
            "kind": e.kind,
            "path": e.path,
            "artifact_sha256": a_hash_hex
        }));
    }

    let out = serde_json::json!({
        "schema_version": "v1",
        "manifest": entries.iter().map(|e| serde_json::json!({"kind": e.kind, "path": e.path})).collect::<Vec<_>>(),
        "artifact_hashes": artifact_hashes,
        "chain_hashes": chain,
        "final_chain_hash": chain.last().unwrap(),
    });

    println!("{}", serde_json::to_string_pretty(&out)?);
    Ok(())
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.cmd {
        Cmd::Canonicalize => cmd_canonicalize(cli.float_precision),
        Cmd::Sha256 => cmd_sha256(),
        Cmd::ArtifactId { kind } => cmd_artifact_id(&kind, cli.float_precision),
        Cmd::Hashchain { manifest } => cmd_hashchain(&manifest, cli.float_precision),
    }
}
```

---

## `forge_evidence/tests/golden_canonicalize.rs`

```rust
use std::io::Write;
use std::process::{Command, Stdio};

#[test]
fn canonicalize_sorts_keys_and_sanitizes_floats() {
    let mut child = Command::new(env!("CARGO_BIN_EXE_forge-evidence"))
        .arg("--float-precision")
        .arg("8")
        .arg("canonicalize")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("spawn forge-evidence");

    {
        let stdin = child.stdin.as_mut().unwrap();
        // Out-of-order keys, floats requiring fixed precision
        write!(stdin, r#"{"b":0.5,"a":1.234567891,"c":[3,2,1]}"#).unwrap();
    }

    let out = child.wait_with_output().expect("wait");
    assert!(out.status.success());

    let s = String::from_utf8(out.stdout).unwrap();
    // keys must be sorted (a before b before c)
    assert!(s.starts_with("{\"a\":"));
    // floats must be printed with exactly 8 decimals
    assert!(s.contains("1.23456789"));
    assert!(s.contains("0.50000000"));
}
```

---

## Build/run

```bash
cd forge_evidence
cargo test

echo '{"b":0.5,"a":1.2}' | cargo run -- canonicalize
```

---

## Notes for next slice

- Slice 00.5b (Python wrapper) will shell out to this binary.
- Slice 07 will build a manifest and call `forge-evidence hashchain`.
- Ghost-tool guard (files_scanned=0 + findings=0 ⇒ FAILED) belongs in Slice 03.5 method_health.

