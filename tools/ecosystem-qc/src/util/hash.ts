/** SHA-256 file hashing using Bun's native crypto */

import { readFileSync } from "node:fs";

export function sha256File(filePath: string): string {
  try {
    const data = readFileSync(filePath);
    const hasher = new Bun.CryptoHasher("sha256");
    hasher.update(data);
    return hasher.digest("hex");
  } catch {
    return "ERROR_HASH_FAILED";
  }
}
