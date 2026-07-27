# svg-to-print-pdf.ps1
#
# Converts an approved Daisy street-sign SVG into a print-ready, correctly-sized
# vector PDF for the Mimaki RasterLink7 hot folder.
#
# WHY IT WORKS THIS WAY
# --------------------
# The obvious approach - re-implement the SVG's text layout and emit PDF path
# operators - was tried and rejected. It produced artwork ~2% wider than the
# approved output because a naive sum of glyph advance widths ignores the font's
# kerning pairs (SAVVAS alone has AV, VV, VA, AS). Measured against the approved
# reference raster that attempt scored a mean luminance error of 78/255 with
# 31.6% of pixels wrong.
#
# Instead this hands the SVG to a renderer that already agrees with the approved
# output: headless Chrome. Same engine, correct kerning, and it loads the SVG's
# own embedded WOFF subset rather than a look-alike system font. Measured against
# the same reference: mean error 0.86/255, 0.32% of pixels - i.e. antialiasing
# only.
#
# The SVG is wrapped in minimal HTML that pins the CSS page box to the sign's
# physical size, so the PDF comes out at true scale with no fitting or margins.
# Output is vector (embedded font program + real paths), not a raster, so it
# stays sharp at the printer's 1200 dpi.
#
# USAGE
#   powershell -NoProfile -ExecutionPolicy Bypass -File svg-to-print-pdf.ps1 `
#       -SvgPath ..\artwork\mr-mrs-large-preview.svg `
#       -PdfPath D:\out\proof.pdf
#
#   Add -ReferencePng ..\artwork\mr-mrs-large-preview.png to also render a raster proof
#   and report the pixel difference against the approved reference.
#
# NOTE: this does not send anything to the printer. Writing the result into the
# RasterLink hot folder is a separate, deliberate step.

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$SvgPath,
  [Parameter(Mandatory=$true)][string]$PdfPath,
  [string]$ReferencePng,
  [int]$TimeBudgetMs = 8000
)

$ErrorActionPreference = 'Stop'

# ------------------------------------------------------------- locate Chrome
$browser = $null
foreach ($c in @(
  'C:\Program Files\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
  'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
)) { if (Test-Path $c) { $browser = $c; break } }
if (-not $browser) { throw 'No Chrome or Edge found - required as the SVG renderer.' }
Write-Host "renderer: $browser"

# --------------------------------------------- read the sign's physical size
# Taken from the SVG itself rather than assumed, so Medium/Small variants work
# without a code change.
[xml]$svg = Get-Content -LiteralPath $SvgPath -Raw
$wAttr = $svg.DocumentElement.GetAttribute('width')
$hAttr = $svg.DocumentElement.GetAttribute('height')
if ($wAttr -notmatch '^([\d.]+)mm$' ) { throw "SVG width '$wAttr' is not in mm - refusing to guess scale." }
$wMm = [double]$Matches[1]
if ($hAttr -notmatch '^([\d.]+)mm$' ) { throw "SVG height '$hAttr' is not in mm - refusing to guess scale." }
$hMm = [double]$Matches[1]
Write-Host ("sign size: {0} x {1} mm" -f $wMm, $hMm)

# Surface build.py's own review flag rather than silently printing a squashed name.
$review = $svg.SelectSingleNode("//*[local-name()='heartManualReviewRequired']")
if ($review -and $review.InnerText -eq 'true') {
  Write-Warning 'heartManualReviewRequired=true in this SVG - extreme name compression. Check before printing.'
}

# ------------------------------------------------------------- build wrapper
$svgInline = (Get-Content -LiteralPath $SvgPath -Raw) -replace '(?s)^.*?(?=<svg)', ''
$html = @"
<!doctype html>
<html><head><meta charset="utf-8"><style>
  @page { size: ${wMm}mm ${hMm}mm; margin: 0; }
  html, body { margin: 0; padding: 0; background: #fff; }
  svg { display: block; width: ${wMm}mm; height: ${hMm}mm; }
</style></head><body>
$svgInline
</body></html>
"@
$tmpHtml = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), ('daisy-sign-' + [System.IO.Path]::GetFileNameWithoutExtension($SvgPath) + '.html'))
[System.IO.File]::WriteAllText($tmpHtml, $html, [System.Text.UTF8Encoding]::new($false))

$pdfDir = Split-Path -Parent $PdfPath
if ($pdfDir -and -not (Test-Path $pdfDir)) { New-Item -ItemType Directory -Force -Path $pdfDir | Out-Null }

# ------------------------------------------------------------------ render
$commonArgs = @('--headless=new','--disable-gpu','--no-sandbox','--hide-scrollbars',
                ('--virtual-time-budget=' + $TimeBudgetMs))
# Paths here routinely contain spaces (e.g. C:\Users\Max Ellison\...). An
# unquoted or unencoded path makes Chrome read the tail as a second URL and fail
# with "Multiple targets are not supported in headless mode".
$pageUri = (New-Object System.Uri($tmpHtml)).AbsoluteUri
$p = Start-Process -FilePath $browser -Wait -PassThru -NoNewWindow -ArgumentList (
  $commonArgs + @('--no-pdf-header-footer', ('--print-to-pdf="' + $PdfPath + '"'), ('"' + $pageUri + '"'))
)
if ($p.ExitCode -ne 0 -or -not (Test-Path $PdfPath)) { throw "PDF generation failed (exit $($p.ExitCode))." }

# ------------------------------------------------------------------ verify
$bytes = [System.IO.File]::ReadAllBytes($PdfPath)
$raw = [System.Text.Encoding]::GetEncoding(28591).GetString($bytes)

$m = [regex]::Match($raw, '/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]')
if (-not $m.Success) { throw 'No MediaBox found in output PDF.' }
$ptW = [double]$m.Groups[3].Value; $ptH = [double]$m.Groups[4].Value
$gotW = $ptW * 25.4 / 72.0; $gotH = $ptH * 25.4 / 72.0
$dW = [Math]::Abs($gotW - $wMm); $dH = [Math]::Abs($gotH - $hMm)
Write-Host ("page: {0:F2} x {1:F2} mm  (target {2} x {3}; delta {4:F3} / {5:F3} mm)" -f $gotW,$gotH,$wMm,$hMm,$dW,$dH)
# Chrome rounds the PDF page box to a whole point, so the error is bounded by
# 1pt = 0.353 mm and grows with page size (0.12 mm on a 125 mm sign, 0.20 mm on a
# 420 mm jig). This is the page box only - CSS lays content out from the page
# origin, so element positions are unaffected, and any residual offset is
# common-mode between the jig and the artwork printed into it, so it cancels.
# 0.4 mm therefore catches a genuinely wrong page size without failing on
# rounding the renderer cannot avoid.
if ($dW -gt 0.4 -or $dH -gt 0.4) { throw "Page size off by more than 0.4 mm - do not print this." }

$fontFiles = ([regex]::Matches($raw,'/FontFile2')).Count + ([regex]::Matches($raw,'/FontFile3')).Count
if ($fontFiles -lt 1) { throw 'No embedded font program in the PDF - a RIP could substitute the font. Refusing.' }
Write-Host ("embedded font programs: {0}   image xobjects: {1}" -f $fontFiles, ([regex]::Matches($raw,'/Subtype\s*/Image')).Count)
Write-Host ("wrote {0} ({1:N0} bytes)" -f $PdfPath, $bytes.Length)

# --------------------------------------------- optional raster proof + diff
if ($ReferencePng) {
  Add-Type -AssemblyName System.Drawing
  $ref = [System.Drawing.Bitmap]::new((Resolve-Path -LiteralPath $ReferencePng).Path)
  $shot = [System.IO.Path]::ChangeExtension($PdfPath, '.proof.png')
  $q = Start-Process -FilePath $browser -Wait -PassThru -NoNewWindow -ArgumentList (
    $commonArgs + @('--force-device-scale-factor=1', ("--window-size=$($ref.Width),$($ref.Height)"),
                    ('--screenshot="' + $shot + '"'), ('"' + $pageUri + '"'))
  )
  if ($q.ExitCode -eq 0 -and (Test-Path $shot)) {
    $mine = [System.Drawing.Bitmap]::new($shot)
    $w = [Math]::Min($ref.Width,$mine.Width); $h = [Math]::Min($ref.Height,$mine.Height)
    $sum = 0.0; $bad = 0
    for ($y=0; $y -lt $h; $y++) { for ($x=0; $x -lt $w; $x++) {
      $a=$ref.GetPixel($x,$y); $b=$mine.GetPixel($x,$y)
      $d=[Math]::Abs((0.299*$a.R+0.587*$a.G+0.114*$a.B)-(0.299*$b.R+0.587*$b.G+0.114*$b.B))
      $sum+=$d; if ($d -gt 64) { $bad++ }
    }}
    $tot = $w*$h
    Write-Host ("proof vs reference: mean {0:F2}/255, {1:F3}% pixels differ" -f ($sum/$tot), (100.0*$bad/$tot))
    if (($sum/$tot) -gt 5.0) { Write-Warning 'Proof differs materially from the approved reference - inspect before printing.' }
    $mine.Dispose()
  }
  $ref.Dispose()
}
