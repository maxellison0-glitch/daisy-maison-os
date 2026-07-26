# make-imposition.ps1
#
# Composes approved street-sign SVGs onto a single full-bed 610 x 420 mm sheet at
# the positions produced by make-jig.ps1, for any size in bed-layout.json.
#
# WHY ONE COMBINED FILE
# ---------------------
# The alternative - print each sign separately with a per-sign Position offset in
# RasterLink - requires knowing which physical corner is the bed origin and which
# way the Scan/Feed axes run. Baking the signs into one full-bed page at 0,0 makes
# that irrelevant: relative geometry is fixed in the file, and it is the identical
# placement the jig outlines were printed from, so artwork and outlines cannot
# disagree.
#
# Signs are nested as <svg> elements rather than re-drawn, so the approved artwork
# passes through untouched - no re-layout, no re-measuring text.
#
# Fewer signs than the layout holds is fine: they fill POS 1 upward and the
# remaining slots stay empty. White is no ink on this machine, so an unused slot
# costs nothing.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -Command `
#     "& '.\make-imposition.ps1' -Size medium -SignSvgs 'a.svg','b.svg','c.svg' -OutSvg bed1.svg"
#
# Invoke with -Command, NOT -File: -File flattens the string[] parameter into a
# single comma-joined path and every sign is then reported as missing.

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string[]]$SignSvgs,
  [Parameter(Mandatory=$true)][string]$OutSvg,
  [string]$Size = 'large',
  # Overrides for experiments only; production runs pass none of these.
  [int]$Cols = 0,
  [int]$Rows = 0,
  [double]$MarginY = [double]::NaN,
  [double]$GapX    = [double]::NaN,
  [double]$GapY    = [double]::NaN
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'bed-layout.ps1')

$L = Get-DaisyBedLayout -Size $Size -Cols $Cols -Rows $Rows -MarginY $MarginY -GapX $GapX -GapY $GapY
Write-DaisyBedLayout $L

if ($SignSvgs.Count -lt 1 -or $SignSvgs.Count -gt $L.Count) {
  throw ("Give 1 to {0} sign SVGs for the '{1}' layout; got {2}. More than {0} will not fit the bed." -f $L.Count, $L.Size, $SignSvgs.Count)
}

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
[void]$sb.AppendLine(('<!-- Daisy Maison - {0} street-sign imposition for UJF-6042MkII. Print at position 0,0. -->' -f $L.Size))
# xmlns:daisy and xmlns:xlink must be declared here: the nested sign markup
# carries daisy: production metadata and xlink: image refs, and dropping their
# root element would otherwise leave those prefixes undefined.
[void]$sb.AppendLine(('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:daisy="https://daisymaison.co.uk/ns/production" width="{0}mm" height="{1}mm" viewBox="0 0 {0} {1}">' -f $L.BedW,$L.BedH))
[void]$sb.AppendLine('  <rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>')

$idx = 0
foreach ($path in $SignSvgs) {
  $pos = $L.Positions[$idx]
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
  if ([Math]::Abs($blankW - $L.SignW) -gt 0.01 -or [Math]::Abs($blankH - $L.SignH) -gt 0.01) {
    throw ("$path has a {0} x {1} mm blank but the '{2}' layout expects {3} x {4} mm - refusing to scale approved artwork." -f `
      $blankW, $blankH, $L.Size, $L.SignW, $L.SignH)
  }

  # Bleed is ink that deliberately hangs outside the blank. Where two blanks are
  # adjacent, their bleeds must not reach each other or the darker sign prints
  # into its neighbour's edge.
  if ($L.Rows -gt 1 -and $bleed -gt ($L.GapY / 2.0) + 1e-9) {
    throw ("{0} mm bleed exceeds half the {1} mm row gap - stacked signs would overprint each other." -f $bleed, $L.GapY)
  }
  if ($L.Cols -gt 1 -and $bleed -gt ($L.GapX / 2.0) + 1e-9) {
    throw ("{0} mm bleed exceeds half the {1} mm column gap - side-by-side signs would overprint each other." -f $bleed, $L.GapX)
  }

  $order = if ($raw -match '<daisy:orderReference>([^<]+)</daisy:orderReference>') { $Matches[1] } else { 'unknown' }
  if ($raw -match '<daisy:heartManualReviewRequired>true</daisy:heartManualReviewRequired>') {
    Write-Warning "$order has heartManualReviewRequired=true (extreme name compression) - check before printing."
  }

  # inner markup only: drop the prolog/comments and the root <svg ...> wrapper
  $inner = $raw -replace '(?s)^.*?<svg\b[^>]*>', ''
  $inner = $inner -replace '(?s)</svg>\s*$', ''

  # offset by the bleed so the BLANK, not the canvas, lands on the jig coordinate
  $placeX = $pos.X - $bleed
  $placeY = $pos.Y - $bleed
  $bleedNote = if ($bleed -gt 0) { "  (+{0:F1}mm bleed)" -f $bleed } else { '' }
  Write-Host ("  POS {0}: {1,-10} blank at ({2:F1}, {3:F1}) mm{4}" -f $pos.Index, $order, $pos.X, $pos.Y, $bleedNote)
  [void]$sb.AppendLine(('  <svg id="pos-{0}" data-order="{1}" data-bleed-mm="{2:F2}" x="{3:F3}" y="{4:F3}" width="{5}" height="{6}" viewBox="{7:g} {8:g} {5} {6}">' -f `
    $pos.Index, $order, $bleed, $placeX, $placeY, $canvasW, $canvasH, $vbX, $vbY))
  [void]$sb.AppendLine($inner)
  [void]$sb.AppendLine('  </svg>')
}

[void]$sb.AppendLine('</svg>')

$dir = Split-Path -Parent $OutSvg
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($OutSvg, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host ("wrote {0} ({1:N0} bytes, {2} of {3} slot(s) filled)" -f $OutSvg, (Get-Item $OutSvg).Length, $idx, $L.Count)
