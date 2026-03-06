/** Exec utility — wraps Bun.spawn with timeout + capture */

import type { ExecResult } from "../types.js";

const DEFAULT_TIMEOUT_MS = 120_000;

export async function exec(
  cmd: string,
  opts: { cwd: string; timeoutMs?: number; env?: Record<string, string> }
): Promise<ExecResult> {
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const start = performance.now();

  const baseEnv: Record<string, string> = {
    ...process.env as Record<string, string>,
    CI: "1",
    RUST_BACKTRACE: "1",
    ...(opts.env ?? {}),
  };

  // Remove undefined values
  const env = Object.fromEntries(
    Object.entries(baseEnv).filter(([, v]) => v !== undefined)
  ) as Record<string, string>;

  const parts = parseCommand(cmd);

  let timedOut = false;

  try {
    const proc = Bun.spawn(parts, {
      cwd: opts.cwd,
      env,
      stdout: "pipe",
      stderr: "pipe",
    });

    const timeoutPromise = new Promise<"timeout">((resolve) =>
      setTimeout(() => resolve("timeout"), timeoutMs)
    );

    const exitPromise = proc.exited;
    const race = await Promise.race([exitPromise, timeoutPromise]);

    if (race === "timeout") {
      timedOut = true;
      proc.kill(9);
      await proc.exited.catch(() => {});
      const ms = Math.round(performance.now() - start);
      return {
        ok: false,
        exitCode: -1,
        stdout: "",
        stderr: `Process timed out after ${timeoutMs}ms`,
        ms,
        timedOut: true,
      };
    }

    const exitCode = race as number;
    const [stdout, stderr] = await Promise.all([
      readStream(proc.stdout),
      readStream(proc.stderr),
    ]);

    const ms = Math.round(performance.now() - start);

    return {
      ok: exitCode === 0,
      exitCode,
      stdout,
      stderr,
      ms,
      timedOut: false,
    };
  } catch (err) {
    const ms = Math.round(performance.now() - start);
    return {
      ok: false,
      exitCode: -1,
      stdout: "",
      stderr: err instanceof Error ? err.message : String(err),
      ms,
      timedOut,
    };
  }
}

function parseCommand(cmd: string): string[] {
  const parts: string[] = [];
  let current = "";
  let inSingle = false;
  let inDouble = false;

  for (let i = 0; i < cmd.length; i++) {
    const ch = cmd[i];
    if (ch === "'" && !inDouble) {
      inSingle = !inSingle;
    } else if (ch === '"' && !inSingle) {
      inDouble = !inDouble;
    } else if (ch === " " && !inSingle && !inDouble) {
      if (current.length > 0) {
        parts.push(current);
        current = "";
      }
    } else {
      current += ch;
    }
  }
  if (current.length > 0) parts.push(current);

  // For commands starting with 'bash', 'sh', 'bun', 'cargo', 'npm', 'git'
  // use them directly. For others, wrap in sh -c.
  const knownBins = ["bash", "sh", "bun", "cargo", "npm", "npx", "git", "node"];
  if (parts.length > 0 && knownBins.includes(parts[0])) {
    return parts;
  }

  return ["sh", "-c", cmd];
}

async function readStream(stream: ReadableStream<Uint8Array> | null): Promise<string> {
  if (!stream) return "";
  try {
    const chunks: Uint8Array[] = [];
    const reader = stream.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) chunks.push(value);
    }
    const decoder = new TextDecoder();
    return chunks.map((c) => decoder.decode(c, { stream: true })).join("");
  } catch {
    return "";
  }
}
