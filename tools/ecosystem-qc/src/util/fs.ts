/** Filesystem helpers */

import { existsSync, statSync, readdirSync } from "node:fs";
import { join } from "node:path";

export function pathExists(p: string): boolean {
  return existsSync(p);
}

export function isDir(p: string): boolean {
  try {
    return statSync(p).isDirectory();
  } catch {
    return false;
  }
}

export function isFile(p: string): boolean {
  try {
    return statSync(p).isFile();
  } catch {
    return false;
  }
}

export function listDirs(parent: string): string[] {
  try {
    return readdirSync(parent, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name);
  } catch {
    return [];
  }
}

export function readTextFile(p: string): string | null {
  try {
    return Bun.file(p).text() as unknown as string;
  } catch {
    return null;
  }
}

export async function readTextFileAsync(p: string): Promise<string | null> {
  try {
    return await Bun.file(p).text();
  } catch {
    return null;
  }
}

export function readJsonFile<T = unknown>(p: string): T | null {
  try {
    const text = require("node:fs").readFileSync(p, "utf-8");
    return JSON.parse(text) as T;
  } catch {
    return null;
  }
}
