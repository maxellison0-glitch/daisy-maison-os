# make-jig.ps1
#
# Builds an N-up positioning jig for the Mimaki UJF-6042MkII bed, for any sign
# size defined in bed-layout.json.
#
# The jig is PRINTED BY THE MIMAKI ITSELF onto paper taped to the bed. That
# matters: because the same machine draws the outlines and later prints the
# artwork, sign positions are known by construction rather than measured, and
# registration cannot drift through a transcription error. It also means the
# physical bed-origin corner never has to be identified - outlines and artwork
# share whatever convention RasterLink uses.
#
# Outlines are the real cut contour lifted from a generated order SVG, not
# approximated rectangles, so a blank either sits inside its outline or it
# visibly doesn't.
#
# Corner ticks sit OUTSIDE each outline so they stay visible once an opaque
# acrylic blank is laid on top - otherwise the guide disappears exactly when you
# need it.
#
# Grid geometry comes from bed-layout.ps1, the same resolver make-imposition.ps1
# uses, so the jig and the artwork printed onto it cannot disagree.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File make-jig.ps1 `
#       -Size large -ContourSvg ..\artwork\orders\DM37201.svg -OutSvg jig-large.svg

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$ContourSvg,
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

# --------------------------------------------- lift the real cut contour
[xml]$src = Get-Content -LiteralPath $ContourSvg -Raw
$ns = New-Object System.Xml.XmlNamespaceManager($src.NameTable)
$ns.AddNamespace('s','http://www.w3.org/2000/svg')
$plate = $src.DocumentElement.SelectSingleNode("//s:path[@id='outer-plate']", $ns)
if (-not $plate) { throw "No outer-plate contour found in $ContourSvg" }
$d = $plate.d
$vtx = ([regex]::Matches($d,'[-\d.]+,[-\d.]+')).Count
Write-Host ("contour: {0} vertices from {1}" -f $vtx, (Split-Path -Leaf $ContourSvg))

# The contour is authored in the sign's own 0..W x 0..H space, so it can be placed
# by translation alone - no scaling, which would silently change the blank size
# the jig claims to represent. This check is also what stops a Large contour being
# used to cut a Medium jig: the sizes simply will not match.
$vb = ($src.DocumentElement.viewBox -split '\s+') | Where-Object { $_ -ne '' }
if ([Math]::Abs([double]$vb[2] - $L.SignW) -gt 0.01 -or [Math]::Abs([double]$vb[3] - $L.SignH) -gt 0.01) {
  throw ("Contour source is {0}x{1} mm but the '{2}' layout expects {3}x{4} mm - refusing to scale the blank outline. Generate the contour with build.py --size {2}." -f `
    $vb[2], $vb[3], $L.Size, $L.SignW, $L.SignH)
}
# A bled sign has a negative viewBox origin. The jig must trace the BLANK, so
# using a bled SVG would draw outlines 4 mm oversize on every edge.
if ([double]$vb[0] -ne 0 -or [double]$vb[1] -ne 0) {
  throw ("Contour source has a non-zero viewBox origin ({0},{1}) - that is a bled SVG. The jig must trace the blank, so use the pre-bleed artwork." -f $vb[0], $vb[1])
}

# ------------------------------------------------------------------ emit SVG
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
[void]$sb.AppendLine(('<!-- Daisy Maison - {0}-up {1} positioning jig for UJF-6042MkII. Print on paper taped to the bed at position 0,0. -->' -f $L.Count, $L.Size))
[void]$sb.AppendLine(('<svg xmlns="http://www.w3.org/2000/svg" width="{0}mm" height="{1}mm" viewBox="0 0 {0} {1}">' -f $L.BedW,$L.BedH))
[void]$sb.AppendLine('  <rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>')

foreach ($pos in $L.Positions) {
  $x = $pos.X; $y = $pos.Y; $n = $pos.Index
  [void]$sb.AppendLine(('  <g id="position-{0}" transform="translate({1:F3} {2:F3})">' -f $n,$x,$y))
  # blank outline - stroked only, minimal ink
  [void]$sb.AppendLine(('    <path d="{0}" fill="none" stroke="#010101" stroke-width="0.4"/>' -f $d))
  [void]$sb.AppendLine('  </g>')
  # corner ticks placed outside the outline so they survive a blank being laid on top
  $t = 8.0; $off = 3.0
  foreach ($c in @(@(0,0,-1,-1), @($L.SignW,0,1,-1), @(0,$L.SignH,-1,1), @($L.SignW,$L.SignH,1,1))) {
    $cx = $x + [double]$c[0] + ([double]$c[2] * $off)
    $cy = $y + [double]$c[1] + ([double]$c[3] * $off)
    [void]$sb.AppendLine(('  <path d="M {0:F2} {1:F2} h {2:F2} M {0:F2} {1:F2} v {3:F2}" stroke="#010101" stroke-width="0.5" fill="none"/>' -f `
      $cx, $cy, ([double]$c[2] * $t), ([double]$c[3] * $t)))
  }
  # position label, clear of the blank footprint
  [void]$sb.AppendLine(('  <text x="{0:F2}" y="{1:F2}" font-family="Arial,Helvetica,sans-serif" font-size="6" fill="#010101">POS {2}</text>' -f `
    ($x + 2), ($y - 3.5), $n))
  Write-Host ("  POS {0} (col {1}, row {2}): ({3:F1}, {4:F1}) -> ({5:F1}, {6:F1}) mm" -f `
    $n, $pos.Col, $pos.Row, $x, $y, ($x + $L.SignW), ($y + $L.SignH))
}

# bed reference caption - confirms the print landed where RasterLink claimed, and
# records which layout this sheet is a jig FOR.
[void]$sb.AppendLine(('  <text x="4" y="{0:F1}" font-family="Arial,Helvetica,sans-serif" font-size="5" fill="#010101">DAISY {1}-UP JIG  {2}  bed {3}x{4}mm  sign {5}x{6}mm  X {7:F1}  Y {8:F1}/{9:F1}</text>' -f `
  ($L.BedH - 3), $L.Count, $L.Size.ToUpperInvariant(), $L.BedW, $L.BedH, $L.SignW, $L.SignH, $L.MarginX, $L.MarginY, $L.GapY))
[void]$sb.AppendLine('</svg>')

$dir = Split-Path -Parent $OutSvg
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($OutSvg, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host ("wrote {0} ({1:N0} bytes)" -f $OutSvg, (Get-Item $OutSvg).Length)
