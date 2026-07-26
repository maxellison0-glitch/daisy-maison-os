# bed-layout.ps1
#
# Shared layout resolver. Dot-source it, then call Get-DaisyBedLayout.
#
# WHY THIS EXISTS
# ---------------
# The jig outlines and the artwork imposed onto them are produced by two separate
# scripts. If each carried its own copy of the geometry, a single edit to one of
# them would silently misregister every sign on the bed - and you would not find
# out until the acrylic was already printed. Both now derive positions from the
# same function reading the same JSON, so they cannot drift apart.
#
# Positions fill row-major: left to right, then top to bottom.
# Cols = 1 reproduces the original single-column behaviour exactly.
#
#   . "$PSScriptRoot\bed-layout.ps1"
#   $layout = Get-DaisyBedLayout -Size medium

# No Set-StrictMode here: this file is dot-sourced, so any mode it sets would leak
# into the calling script's scope and change how unrelated code behaves.

function Get-DaisyBedLayout {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory=$true)][string]$Size,
    # Every override below defaults to "unset" and falls back to the JSON profile.
    # They exist for experiments; production runs should pass none of them.
    [int]$Cols = 0,
    [int]$Rows = 0,
    [double]$MarginY = [double]::NaN,
    [double]$GapX    = [double]::NaN,
    [double]$GapY    = [double]::NaN,
    [double]$BedW    = [double]::NaN,
    [double]$BedH    = [double]::NaN,
    [string]$ProfilePath
  )

  $ErrorActionPreference = 'Stop'
  if (-not $ProfilePath) { $ProfilePath = Join-Path $PSScriptRoot 'bed-layout.json' }
  if (-not (Test-Path -LiteralPath $ProfilePath)) { throw "Bed layout profile not found: $ProfilePath" }

  $cfg = Get-Content -LiteralPath $ProfilePath -Raw | ConvertFrom-Json
  $key = $Size.ToLowerInvariant()
  $known = $cfg.sizes.PSObject.Properties.Name
  if ($known -notcontains $key) {
    throw ("Unknown size '{0}'. bed-layout.json defines: {1}" -f $Size, ($known -join ', '))
  }
  $p = $cfg.sizes.$key

  $signW = [double]$p.signWidthMm
  $signH = [double]$p.signHeightMm
  if ($Cols -le 0) { $Cols = [int]$p.cols }
  if ($Rows -le 0) { $Rows = [int]$p.rows }
  if ([double]::IsNaN($MarginY)) { $MarginY = [double]$p.marginY }
  if ([double]::IsNaN($GapX))    { $GapX    = [double]$p.gapX }
  if ([double]::IsNaN($GapY))    { $GapY    = [double]$p.gapY }
  if ([double]::IsNaN($BedW))    { $BedW    = [double]$cfg.bed.widthMm }
  if ([double]::IsNaN($BedH))    { $BedH    = [double]$cfg.bed.heightMm }

  # X margin is derived, never configured: the signs are centred across the bed so
  # a misconfigured margin cannot push artwork off one edge.
  $marginX = ($BedW - ($Cols * $signW) - (($Cols - 1) * $GapX)) / 2.0
  $neededH = (2 * $MarginY) + ($Rows * $signH) + (($Rows - 1) * $GapY)

  # 1e-6 tolerance: both current layouts fill the bed to the millimetre, and binary
  # doubles must not turn an exact fit into a spurious failure.
  if ($marginX -lt -1e-6) {
    throw ("{0}: {1} column(s) of {2} mm plus gaps need {3:F1} mm but the bed is {4} mm wide." -f `
      $key, $Cols, $signW, ($BedW - 2*$marginX), $BedW)
  }
  if ($neededH -gt ($BedH + 1e-6)) {
    throw ("{0}: {1} row(s) need {2:F1} mm but the bed is {3} mm deep. Reduce rows, margin or gap." -f `
      $key, $Rows, $neededH, $BedH)
  }
  if ($marginX -lt 0) { $marginX = 0.0 }

  $positions = @()
  $n = 0
  for ($r = 0; $r -lt $Rows; $r++) {
    for ($c = 0; $c -lt $Cols; $c++) {
      $n++
      $positions += [pscustomobject]@{
        Index = $n
        Col   = $c + 1
        Row   = $r + 1
        X     = $marginX + $c * ($signW + $GapX)
        Y     = $MarginY + $r * ($signH + $GapY)
      }
    }
  }

  [pscustomobject]@{
    Size        = $key
    Machine     = $cfg.bed.machine
    BedW        = $BedW
    BedH        = $BedH
    SignW       = $signW
    SignH       = $signH
    Cols        = $Cols
    Rows        = $Rows
    Count       = $positions.Count
    MarginX     = $marginX
    MarginY     = $MarginY
    GapX        = $GapX
    GapY        = $GapY
    Utilisation = 100.0 * ($positions.Count * $signW * $signH) / ($BedW * $BedH)
    Positions   = $positions
  }
}

function Write-DaisyBedLayout {
  param([Parameter(Mandatory=$true)]$Layout)
  Write-Host ("{0} | bed {1} x {2} mm | {3} sign(s) of {4} x {5} mm ({6} col x {7} row)" -f `
    $Layout.Size.ToUpperInvariant(), $Layout.BedW, $Layout.BedH, $Layout.Count, $Layout.SignW, $Layout.SignH, $Layout.Cols, $Layout.Rows)
  Write-Host ("  margins X {0:F1} / Y {1:F1} mm | gaps X {2:F1} / Y {3:F1} mm | bed utilisation {4:F1}%" -f `
    $Layout.MarginX, $Layout.MarginY, $Layout.GapX, $Layout.GapY, $Layout.Utilisation)
}
