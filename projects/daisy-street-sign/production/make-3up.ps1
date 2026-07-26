# make-3up.ps1
#
# Composes up to three approved street-sign SVGs onto a single full-bed
# 610 x 420 mm sheet at the jig positions produced by make-jig.ps1.
#
# WHY ONE COMBINED FILE
# ---------------------
# The alternative - print each sign separately with a per-sign Position offset in
# RasterLink - requires knowing which physical corner is the bed origin and which
# way the Scan/Feed axes run. Baking the three signs into one full-bed page at
# 0,0 makes that irrelevant: relative geometry is fixed in the file, and it is
# the identical placement the jig outlines were printed from, so artwork and
# outlines cannot disagree.
#
# Signs are nested as <svg> elements rather than re-drawn, so the approved
# artwork passes through untouched - no re-layout, no re-measuring text.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File make-3up.ps1 `
#       -SignSvgs a.svg,b.svg,c.svg -OutSvg 3up.svg

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string[]]$SignSvgs,
  [Parameter(Mandatory=$true)][string]$OutSvg,
  [double]$BedW = 610.0,
  [double]$BedH = 420.0,
  [double]$SignW = 570.0,
  [double]$SignH = 125.0,
  [double]$MarginY = 12.5,
  [double]$GapY = 10.0
)

$ErrorActionPreference = 'Stop'

if ($SignSvgs.Count -lt 1 -or $SignSvgs.Count -gt 3) {
  throw "Give 1 to 3 sign SVGs; got $($SignSvgs.Count). Three is the bed maximum (4 signs need more area than the bed has)."
}
$marginX = ($BedW - $SignW) / 2.0

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
[void]$sb.AppendLine('<!-- Daisy Maison - three-up street-sign imposition for UJF-6042MkII. Print at position 0,0. -->')
# xmlns:daisy and xmlns:xlink must be declared here: the nested sign markup
# carries daisy: production metadata and xlink: image refs, and dropping their
# root element would otherwise leave those prefixes undefined.
[void]$sb.AppendLine(('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:daisy="https://daisymaison.co.uk/ns/production" width="{0}mm" height="{1}mm" viewBox="0 0 {0} {1}">' -f $BedW,$BedH))
[void]$sb.AppendLine('  <rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>')

$idx = 0
foreach ($path in $SignSvgs) {
  $idx++
  $raw = Get-Content -LiteralPath $path -Raw

  # Confirm each sign really is the size this layout assumes. A Medium or Mini SVG
  # silently scaled into a Large slot would be an expensive mistake.
  if ($raw -notmatch 'width="([\d.]+)mm"\s+height="([\d.]+)mm"') { throw "Cannot read mm size from $path" }
  $canvasW = [double]$Matches[1]; $canvasH = [double]$Matches[2]

  # A bled sign (production/add-bleed.py) has a negative viewBox origin: the canvas
  # is larger than the blank by the bleed on every side. Read the bleed from that
  # origin and place the BLANK on the jig coordinate, letting the extra ink hang
  # outside it - otherwise every sign would sit shifted by the bleed amount.
  if ($raw -notmatch 'viewBox="(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)"') { throw "Cannot read viewBox from $path" }
  $vbX = [double]$Matches[1]; $vbY = [double]$Matches[2]
  $bleed = -$vbX
  if ([Math]::Abs($vbX - $vbY) -gt 0.001) { throw ("$path has an asymmetric viewBox origin ({0},{1}) - unexpected." -f $vbX,$vbY) }
  if ($bleed -lt 0) { throw ("$path has a positive viewBox origin ({0}) - unexpected." -f $vbX) }

  $blankW = $canvasW - 2 * $bleed
  $blankH = $canvasH - 2 * $bleed
  if ([Math]::Abs($blankW - $SignW) -gt 0.01 -or [Math]::Abs($blankH - $SignH) -gt 0.01) {
    throw ("$path has a {0} x {1} mm blank but this layout expects {2} x {3} mm - refusing to scale approved artwork." -f $blankW,$blankH,$SignW,$SignH)
  }

  $order = if ($raw -match '<daisy:orderReference>([^<]+)</daisy:orderReference>') { $Matches[1] } else { 'unknown' }
  if ($raw -match '<daisy:heartManualReviewRequired>true</daisy:heartManualReviewRequired>') {
    Write-Warning "$order has heartManualReviewRequired=true (extreme name compression) - check before printing."
  }

  # inner markup only: drop the prolog/comments and the root <svg ...> wrapper
  $inner = $raw -replace '(?s)^.*?<svg\b[^>]*>', ''
  $inner = $inner -replace '(?s)</svg>\s*$', ''

  $y = $MarginY + ($idx - 1) * ($SignH + $GapY)
  # offset by the bleed so the BLANK, not the canvas, lands on the jig coordinate
  $placeX = $marginX - $bleed
  $placeY = $y - $bleed
  $bleedNote = if ($bleed -gt 0) { "  (+{0:F1}mm bleed)" -f $bleed } else { '' }
  Write-Host ("  POS {0}: {1,-10} blank at ({2:F1}, {3:F1}) mm{4}" -f $idx, $order, $marginX, $y, $bleedNote)
  [void]$sb.AppendLine(('  <svg id="pos-{0}" data-order="{1}" data-bleed-mm="{2:F2}" x="{3:F3}" y="{4:F3}" width="{5}" height="{6}" viewBox="{7:g} {8:g} {5} {6}">' -f `
    $idx, $order, $bleed, $placeX, $placeY, $canvasW, $canvasH, $vbX, $vbY))
  [void]$sb.AppendLine($inner)
  [void]$sb.AppendLine('  </svg>')
}

[void]$sb.AppendLine('</svg>')

$dir = Split-Path -Parent $OutSvg
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($OutSvg, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host ("wrote {0} ({1:N0} bytes, {2} sign(s))" -f $OutSvg, (Get-Item $OutSvg).Length, $idx)
