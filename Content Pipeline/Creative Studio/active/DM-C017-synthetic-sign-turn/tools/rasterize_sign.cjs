const fs = require("fs");
const sharp = require("sharp");

const [input, output] = process.argv.slice(2);
if (!input || !output) {
  throw new Error("Usage: node rasterize_sign.cjs input.svg output.png");
}

sharp(fs.readFileSync(input), { density: 102 })
  .resize(2280, 500, { fit: "fill" })
  .png()
  .toFile(output)
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
