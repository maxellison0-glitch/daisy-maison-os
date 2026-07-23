import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const batchDir = path.dirname(fileURLToPath(import.meta.url));
const laneDir = path.resolve(batchDir, "../../../..");
const hfExe =
  "C:\\Users\\Max Ellison\\AppData\\Local\\Programs\\nodejs\\node_modules\\@higgsfield\\cli\\vendor\\hf.exe";

const prompt = fs.readFileSync(path.join(batchDir, "prompt.txt"), "utf8");
const startImage = path.join(
  laneDir,
  "working/batches/start-keyframe/v01-white-back-match/outputs/take-01.png",
);
const endImage = path.join(
  laneDir,
  "working/batches/hero-still/v05-approved-product-lock/outputs/take-01.jpg",
);
const imageReferences = [
  path.join(
    laneDir,
    "working/batches/product-calibration/v01-locked-real-sign-edit/outputs/take-03.jpg",
  ),
  path.join(
    laneDir,
    "source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/02-front-to-edge-product-only.jpg",
  ),
  path.join(
    laneDir,
    "source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/03-back-to-edge-product-only.jpg",
  ),
  path.join(
    laneDir,
    "source/real-product-reference-pack/instagram-DPjdseCDbDR/product-only-crops/04-white-back-product-only.jpg",
  ),
];
const videoReference = path.join(
  batchDir,
  "inputs/real-turn-face-excluded.mp4",
);

const required = [
  hfExe,
  startImage,
  endImage,
  ...imageReferences,
  videoReference,
];
for (const item of required) {
  if (!fs.existsSync(item)) {
    throw new Error(`Required input does not exist: ${item}`);
  }
}

const common = [
  "seedance_2_0",
  "--prompt",
  prompt,
  "--aspect_ratio",
  "9:16",
  "--bitrate_mode",
  "high",
  "--duration",
  "8",
  "--generate_audio",
  "false",
  "--genre",
  "auto",
  "--mode",
  "std",
  "--resolution",
  "1080p",
  "--start-image",
  startImage,
  "--end-image",
  endImage,
];
for (const reference of imageReferences) {
  common.push("--image-references", reference);
}
common.push("--video-references", videoReference);

const action = process.argv[2] ?? "quote";
let args;
if (action === "quote") {
  args = ["generate", "cost", ...common, "--json"];
} else if (action === "submit") {
  args = ["generate", "create", ...common, "--json"];
} else if (action === "get") {
  const jobId = process.argv[3];
  if (!jobId) throw new Error("Usage: node run_higgsfield.mjs get <job_id>");
  args = ["generate", "get", jobId, "--json"];
} else {
  throw new Error("Action must be quote, submit or get");
}

const result = spawnSync(hfExe, args, {
  cwd: batchDir,
  encoding: "utf8",
  windowsHide: true,
  maxBuffer: 32 * 1024 * 1024,
});
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
process.exitCode = result.status ?? 1;
