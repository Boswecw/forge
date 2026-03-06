import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const masterPath = path.join(root, "forge-brand", "assets", "anvil-seal.svg");
const decorativePath = path.join(root, "forge-brand", "assets", "anvil-seal-decorative.svg");

const masterSvg = fs.readFileSync(masterPath, "utf8");
const decorativeSvg = fs.readFileSync(decorativePath, "utf8");

const pathRegex = /<path[^>]*\sd="([^"]+)"[^>]*>/g;

function extractPaths(svg) {
  const paths = [];
  let match;
  while ((match = pathRegex.exec(svg)) !== null) {
    paths.push(match[1]);
  }
  return paths;
}

const masterPaths = extractPaths(masterSvg);
const decorativePaths = extractPaths(decorativeSvg);

if (masterPaths.length !== decorativePaths.length) {
  console.error(`Mismatch: master has ${masterPaths.length} paths, decorative has ${decorativePaths.length}.`);
  process.exit(1);
}

for (let i = 0; i < masterPaths.length; i += 1) {
  if (masterPaths[i] !== decorativePaths[i]) {
    console.error(`Mismatch at index ${i}: ${masterPaths[i]} != ${decorativePaths[i]}`);
    process.exit(1);
  }
}

console.log("OK: geometry matches");
