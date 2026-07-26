# make-jig.ps1
#
# Builds a three-up positioning jig for the Mimaki UJF-6042MkII bed.
#
# The jig is PRINTED BY THE MIMAKI ITSELF onto paper taped to the bed. That
# matters: because the same machine draws the outlines and later prints the
# artwork, sign positions are known by construction rather than measured, and
# registration cannot drift through a transcription error. It also means the
# physical bed-origin corner never has to be identified - outlines and artwork
# share whatever convention RasterLink uses.
#
# Outlines are the real 409-vertex cut contour lifted from a generated order
# SVG, not approximated rectangles, so a blank either sits inside its outline or
# it visibly doesn't.
#
# Corner ticks sit OUTSIDE each outline so they stay visible once an opaque
# acrylic blank is laid on top - otherwise the guide disappears exactly when you
# need it.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File make-jig.ps1 `
#       -ContourSvg ..\artwork\orders\DM37201.svg -OutSvg ..\production\jig-3up.svg

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$ContourSvg,
  [Parameter(Mandatory=$true)][string]$OutSvg,
  [double]$BedW = 610.0,
  [double]$BedH = 420.0,
  [double]$SignW = 570.0,
  [double]$SignH = 125.0,
  [int]$Rows = 3,
  [double]$MarginY = 12.5,
  [double]$GapY = 10.0
)

$ErrorActionPreference = 'Stop'

# ------------------------------------------------------------- sanity checks
$marginX = ($BedW - $SignW) / 2.0
if ($marginX -lt 0) { throw "Sign width $SignW mm exceeds bed width $BedW mm." }
$needed = ($Rows * $SignH) + (2 * $MarginY) + (($Rows - 1) * $GapY)
if ($needed -gt $BedH) {
  throw ("Layout needs {0:F1} mm but the bed is {1} mm. Reduce rows, margin or gap." -f $needed, $BedH)
}
# Area check - catches an impossible request before any geometry is emitted.
$areaUsed = $Rows * $SignW * $SignH
if ($areaUsed -gt ($BedW * $BedH)) {
  throw ("{0} signs need {1:N0} mm2 but the bed is only {2:N0} mm2." -f $Rows, $areaUsed, ($BedW*$BedH))
}
Write-Host ("bed {0} x {1} mm | {2} signs of {3} x {4} | X margin {5:F1} mm | Y {6:F1}/{7:F1}" -f `
  $BedW,$BedH,$Rows,$SignW,$SignH,$marginX,$MarginY,$GapY)
Write-Host ("bed utilisation: {0:F1}%" -f (100.0 * $areaUsed / ($BedW*$BedH)))

# --------------------------------------------- lift the real cut contour
[xml]$src = Get-Content -LiteralPath $ContourSvg -Raw
$ns = New-Object System.Xml.XmlNamespaceManager($src.NameTable)
$ns.AddNamespace('s','http://www.w3.org/2000/svg')
$plate = $src.DocumentElement.SelectSingleNode("//s:path[@id='outer-plate']", $ns)
if (-not $plate) { throw "No outer-plate contour found in $ContourSvg" }
$d = $plate.d
$vtx = ([regex]::Matches($d,'[-\d.]+,[-\d.]+')).Count
Write-Host ("contour: {0} vertices from {1}" -f $vtx, (Split-Path -Leaf $ContourSvg))

# The contour is authored in the sign's own 0..570 x 0..125 space, so it can be
# placed by translation alone - no scaling, which would silently change the
# blank size the jig claims to represent.
$vb = ($src.DocumentElement.viewBox -split '\s+') | Where-Object { $_ -ne '' }
if ([double]$vb[2] -ne $SignW -or [double]$vb[3] -ne $SignH) {
  throw ("Contour source is {0}x{1} but SignW/SignH are {2}x{3} - refusing to scale the blank outline." -f $vb[2],$vb[3],$SignW,$SignH)
}

# ------------------------------------------------------------------ emit SVG
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
[void]$sb.AppendLine('<!-- Daisy Maison - three-up positioning jig for UJF-6042MkII. Print on paper taped to the bed. -->')
[void]$sb.AppendLine(('<svg xmlns="http://www.w3.org/2000/svg" width="{0}mm" height="{1}mm" viewBox="0 0 {0} {1}">' -f $BedW,$BedH))
[void]$sb.AppendLine('  <rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>')

for ($i = 0; $i -lt $Rows; $i++) {
  $x = $marginX
  $y = $MarginY + $i * ($SignH + $GapY)
  $n = $i + 1
  [void]$sb.AppendLine(('  <g id="position-{0}" transform="translate({1:F3} {2:F3})">' -f $n,$x,$y))
  # blank outline - stroked only, minimal ink
  [void]$sb.AppendLine(('    <path d="{0}" fill="none" stroke="#010101" stroke-width="0.4"/>' -f $d))
  [void]$sb.AppendLine('  </g>')
  # corner ticks placed outside the outline so they survive a blank being laid on top
  $t = 8.0; $off = 3.0
  foreach ($c in @(@(0,0,-1,-1), @($SignW,0,1,-1), @(0,$SignH,-1,1), @($SignW,$SignH,1,1))) {
    $cx = $x + [double]$c[0] + ([double]$c[2] * $off)
    $cy = $y + [double]$c[1] + ([double]$c[3] * $off)
    [void]$sb.AppendLine(('  <path d="M {0:F2} {1:F2} h {2:F2} M {0:F2} {1:F2} v {3:F2}" stroke="#010101" stroke-width="0.5" fill="none"/>' -f `
      $cx, $cy, ([double]$c[2] * $t), ([double]$c[3] * $t)))
  }
  # position label, clear of the blank footprint
  [void]$sb.AppendLine(('  <text x="{0:F2}" y="{1:F2}" font-family="Arial,Helvetica,sans-serif" font-size="6" fill="#010101">POS {2}</text>' -f `
    ($x + 2), ($y - 3.5), $n))
  Write-Host ("  position {0}: top-left ({1:F1}, {2:F1}) -> ({3:F1}, {4:F1}) mm" -f $n,$x,$y,($x+$SignW),($y+$SignH))
}

# bed reference marks - confirm the print landed where RasterLink claimed
[void]$sb.AppendLine(('  <text x="4" y="{0:F1}" font-family="Arial,Helvetica,sans-serif" font-size="5" fill="#010101">DAISY 3-UP JIG  bed {1}x{2}mm  sign {3}x{4}mm  X margin {5:F1}  Y {6:F1}/{7:F1}</text>' -f `
  ($BedH - 3), $BedW, $BedH, $SignW, $SignH, $marginX, $MarginY, $GapY))
[void]$sb.AppendLine('</svg>')

$dir = Split-Path -Parent $OutSvg
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllText($OutSvg, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host ("wrote {0} ({1:N0} bytes)" -f $OutSvg, (Get-Item $OutSvg).Length)
