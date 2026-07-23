import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const batchDir = dirname(fileURLToPath(import.meta.url));
const laneDir = resolve(batchDir, "..", "..", "..", "..");
const hfExe = join(
  process.env.LOCALAPPDATA,
  "Programs",
  "nodejs",
  "node_modules",
  "@higgsfield",
  "cli",
  "vendor",
  "hf.exe",
);

const prompt = readFileSync(join(batchDir, "prompt.txt"), "utf8")
  .replace(/\s+/g, " ")
  .trim();

const references = [
  join(
    laneDir,
    "working",
    "batches",
    "hero-still",
    "v05-approved-product-lock",
    "outputs",
    "take-01.jpg",
  ),
  join(
    laneDir,
    "source",
    "real-product-reference-pack",
    "instagram-DPjdseCDbDR",
    "product-only-crops",
    "04-white-back-product-only.jpg",
  ),
  join(
    laneDir,
    "source",
    "real-product-reference-pack",
    "instagram-DPjdseCDbDR",
    "product-only-crops",
    "03-back-to-edge-product-only.jpg",
  ),
  join(
    laneDir,
    "source",
    "real-product-reference-pack",
    "instagram-DPjdseCDbDR",
    "product-only-crops",
    "02-front-to-edge-product-only.jpg",
  ),
];

const mode = process.argv[2];
if (!["--quote", "--generate-one"].includes(mode)) {
  throw new Error("Usage: node run_higgsfield.mjs --quote|--generate-one");
}

const command = mode === "--quote" ? "cost" : "create";
const args = [
  "generate",
  command,
  "nano_banana_flash",
  "--prompt",
  prompt,
  ...references.flatMap((reference) => ["--image_references", reference]),
  "--aspect_ratio",
  "9:16",
  "--resolution",
  "1k",
  "--json",
];

const result = spawnSync(hfExe, args, {
  cwd: laneDir,
  encoding: "utf8",
  windowsHide: true,
});

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
process.exit(result.status ?? 1);
