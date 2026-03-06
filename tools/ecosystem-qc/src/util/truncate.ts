/** Truncate strings to safe sizes for report embedding */

const DEFAULT_MAX_BYTES = 16 * 1024; // 16KB

export function truncate(input: string, maxBytes: number = DEFAULT_MAX_BYTES): string {
  if (Buffer.byteLength(input, "utf-8") <= maxBytes) {
    return input;
  }
  // Binary search for the right character count
  let lo = 0;
  let hi = input.length;
  while (lo < hi) {
    const mid = Math.ceil((lo + hi) / 2);
    if (Buffer.byteLength(input.slice(0, mid), "utf-8") <= maxBytes - 30) {
      lo = mid;
    } else {
      hi = mid - 1;
    }
  }
  return input.slice(0, lo) + "\n… [truncated]";
}
