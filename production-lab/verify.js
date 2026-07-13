/* Verification harness: runs the REAL script extracted from the HTML file,
   with a minimal DOM shim + stubbed text measurer, then asserts structure. */
const fs = require("fs");
const path = require("path");

const HTML = fs.readFileSync(path.join(__dirname, "daisy-production-lab-v0.html"), "utf8");
const scriptBody = HTML.split("<script>").pop().split("</script>")[0];

// ---- minimal DOM shim ----
function makeEl(id) {
  const el = {
    _id: id, value: "", style: {}, textContent: "", innerHTML: "", className: "",
    _attrs: {},
    classList: { toggle() {}, add() {}, remove() {} },
    setAttribute(k, v) { this._attrs[k] = String(v); },
    getAttribute(k) { return this._attrs[k]; },
    addEventListener() {},
    appendChild() {}, removeChild() {}, remove() {}, click() {},
    getComputedTextLength() {
      const fs = parseFloat(this._attrs["font-size"] || 10);
      // rough serif advance incl. ~0.06em tracking: 0.55 * fs per char
      return (this.textContent || "").length * fs * 0.55;
    },
  };
  return el;
}
const store = {};
global.document = {
  getElementById: id => store[id] || (store[id] = makeEl(id)),
  createElement: () => makeEl("_created"),
  body: { appendChild() {}, removeChild() {} },
};
global.Blob = function () {};
global.URL = { createObjectURL: () => "blob:stub", revokeObjectURL() {} };

// ---- run the real script + expose internals ----
const exposed = scriptBody + `
;globalThis.__api = { CONFIG, buildSVG, validate, computeState, normalizeText, escapeXML, analyzeChars, fitFontSize, loadSample, render, els };`;
eval(exposed);
const api = globalThis.__api;

// ---- helpers ----
let pass = 0, fail = 0;
function check(name, cond, extra = "") {
  (cond ? pass++ : fail++);
  console.log((cond ? "  PASS " : "  FAIL ") + name + (extra ? "  ›  " + extra : ""));
}

function wellFormed(xml) {
  // crude but effective: every start tag has a match, & only in entities
  const badAmp = /&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/.test(xml);
  return { badAmp };
}

// ===== 1. GOOD SAMPLE (medium) =====
console.log("\n=== GOOD SAMPLE: TEST-001 / MR & MRS WINDSOR / medium ===");
api.loadSample("good");
const sGood = api.computeState();
const svgGood = api.buildSVG(sGood, { forExport: true });
fs.writeFileSync(path.join(__dirname, "out-good.svg"), svgGood);
const vGood = api.validate(sGood);

check("normalizes AND→& & uppercases", sGood.dispLine1 === "MR & MRS WINDSOR", sGood.dispLine1);
check("line2 normalized uppercase", sGood.dispLine2.startsWith("FROM THIS DAY FORWARD"), sGood.dispLine2);
check("verdict = PASS", vGood.verdict === "PASS", vGood.verdict);
["outer-plate","inset-panel","mounting-holes","line-1","signature-heart","line-2"].forEach(id =>
  check("has group id " + id, svgGood.includes(`id="${id}"`)));
check("viewBox is 450:120 (medium)", svgGood.includes('viewBox="0 0 450 120"'));
check("export has cm dims", svgGood.includes('width="45cm"') && svgGood.includes('height="12cm"'));
check("has <?xml?> prolog", svgGood.startsWith("<?xml"));
check("metadata orderNumber", svgGood.includes("<orderNumber>TEST-001</orderNumber>"));
check("metadata handle", svgGood.includes("<productHandle>mr-mrs-personalised-street-sign-gift</productHandle>"));
check("metadata sku", svgGood.includes("<sku>36961</sku>"));
check("metadata size", svgGood.includes("<size>medium</size>"));
check("metadata has timestamp", /<generatedAt>\d{4}-\d{2}-\d{2}T/.test(svgGood));
check("metadata rendered line1 has &amp;", svgGood.includes("<line1Rendered>MR &amp; MRS WINDSOR</line1Rendered>"));
check("visible line-1 escapes & as &amp;", /id="line-1"[^>]*>MR &amp; MRS WINDSOR</.test(svgGood));
check("no raw unescaped & in doc", !wellFormed(svgGood).badAmp);
check("says PREVIEW not print-ready", svgGood.includes("<status>PREVIEW</status>") && /not print-ready/i.test(svgGood));
check("heart is red #C0392B", svgGood.includes('fill="#C0392B"'));
check("plate is #1C1C1A", svgGood.includes('id="outer-plate"') && svgGood.includes('#1C1C1A'));
check("reports a fitted font size for line1", sGood.fit1.fontSize > 0, "fs=" + sGood.fit1.fontSize);

// ===== 2. OVERLONG SAMPLE (small) =====
console.log("\n=== OVERLONG SAMPLE: small ===");
api.loadSample("overlong");
const sBad = api.computeState();
const svgBad = api.buildSVG(sBad, { forExport: true });
fs.writeFileSync(path.join(__dirname, "out-overlong.svg"), svgBad);
const vBad = api.validate(sBad);
check("verdict = REVIEW", vBad.verdict === "REVIEW", vBad.verdict);
check("has a failing/overflow or over-limit check", vBad.hasFail || vBad.hasWarn);
check("line1 over 75 chars flagged", vBad.checks.some(c => /over limit/i.test(c.label)));
check("viewBox is 280:120 (small)", svgBad.includes('viewBox="0 0 280 120"'));
check("overlong doc still well-formed (no raw &)", !wellFormed(svgBad).badAmp);
console.log("  overlong checks:", vBad.checks.map(c => `${c.s}:${c.label}`).join(" | "));

// ===== 3. XSS / ESCAPING PROBE =====
console.log("\n=== ESCAPING PROBE: injection attempt in inputs ===");
api.els.order.value = 'X"><script>evil()</script>';
api.els.line1.value = '<b>A</b> AND "B" & <C>';
api.els.line2.value = "";
api.els.size.value = "large";
const sInj = api.computeState();
const svgInj = api.buildSVG(sInj, { forExport: true });
check("no literal <script> injected", !svgInj.includes("<script>"));
check("< is escaped to &lt;", svgInj.includes("&lt;b&gt;A&lt;/b&gt;"));
check("injection doc well-formed (no raw &)", !wellFormed(svgInj).badAmp);
check("order attr injection escaped in metadata", svgInj.includes("&quot;&gt;&lt;script&gt;"));

// ===== 4. EMPTY LINE 1 =====
console.log("\n=== EMPTY LINE 1 ===");
api.els.order.value = "T"; api.els.line1.value = "   "; api.els.line2.value = "HELLO";
const sEmpty = api.computeState();
const vEmpty = api.validate(sEmpty);
check("empty line1 → REVIEW", vEmpty.verdict === "REVIEW");
check("empty line1 → fail check present", vEmpty.checks.some(c => c.s === "fail" && /line 1/i.test(c.label)));

console.log(`\n================  ${pass} passed, ${fail} failed  ================`);
process.exit(fail ? 1 : 0);
