import { createHash } from "node:crypto";

export function sha256Prefixed(input: Uint8Array): string {
  const digest = createHash("sha256").update(input).digest("hex");
  return `sha256:${digest}`;
}
