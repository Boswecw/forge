type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };

const encoder = new TextEncoder();

function canonicalizeValue(value: JsonValue): string {
  if (value === null) {
    return "null";
  }

  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }

  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new Error("non-finite numbers are not supported in canonical JSON");
    }
    return JSON.stringify(value);
  }

  if (typeof value === "string") {
    return JSON.stringify(value);
  }

  if (Array.isArray(value)) {
    return `[${value.map(canonicalizeValue).join(",")}]`;
  }

  const keys = Object.keys(value).sort();
  const serializedEntries = keys.map((key) => `${JSON.stringify(key)}:${canonicalizeValue(value[key])}`);
  return `{${serializedEntries.join(",")}}`;
}

export function canonicalizeJson(value: JsonValue): Uint8Array {
  const canonicalString = canonicalizeValue(value);
  return encoder.encode(canonicalString);
}
