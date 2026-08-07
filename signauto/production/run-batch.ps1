# run-batch.ps1
#
# THE ONE COMMAND. Orders in, print-ready PDFs out.
#
#   powershell -NoProfile -ExecutionPolicy Bypass -File production\run-batch.ps1 `
#       -OrdersJson orders.json -OutDir production\print\2026-07-27
#
# It chains every stage in order and stops dead on the first failure, because a
# half-finished bed that still produces a PDF is how the wrong thing gets printed:
#
#   build.py          order text -> SVG at the exact blank size
#   recolour-sign.ps1 SKU -> heart decision + colourway; strips mounting holes
#   add-bleed.py      mandatory 4 mm bleed on every border
#   make-imposition   N-up onto the 610 x 420 bed (3 Large, 3 Medium, 8 Small)
#   make-jig.ps1      matching paper jig for the same bed
#   svg-to-print-pdf  headless Chrome -> PDF at true mm
#
# It does NOT touch the printer unless -SendToPrinter is passed - see
# docs\OPERATIONS.md.
#
# INPUT
# -----
# Either the manifest from scripts\plan-batch.py, or a plain array:
#
#   [ { "order":"DM37694", "sku":"36961", "size":"Large",
#       "line1":"MR & MRS NICHOLS",
#       "line2":"FROM THIS DAY FORWARD... 14TH SEPTEMBER 2024",
#       "colour":"Black" } ]
#
# Signs are grouped into beds by size + colourway, because one bed is one print
# run at one ink setup. A part-full bed is still produced and is reported as such -
# it is a real decision whether to print it or wait for more orders, and that
# decision is Max's, not this script's.

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$OrdersJson,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [double]$BleedMm = 4.0,
  # Emit the per-sign intermediates too. Off by default so OutDir holds only what
  # goes to the printer.
  [switch]$KeepIntermediates,
  # Copy each finished bed PDF into the RasterLink7 hot folder. OFF BY DEFAULT
  # and deliberately a separate act: everything before this point is reversible,
  # and this is the step that puts ink on acrylic. Only pass it once the PDFs
  # have been checked and real blanks are sitting on a printed jig.
  [switch]$SendToPrinter,
  [string]$HotFolder = 'C:\MijCtrl\Hot\UJF6042MkII'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$HERE = $PSScriptRoot
$PROJ = Split-Path -Parent $HERE
. (Join-Path $HERE 'bed-layout.ps1')

function Invoke-Stage([string]$Label, [scriptblock]$Body) {
  & $Body
  if ($LASTEXITCODE -ne 0) { throw "$Label failed with exit code $LASTEXITCODE" }
}

# --- read the orders --------------------------------------------------------
if (-not (Test-Path -LiteralPath $OrdersJson)) { throw "No such orders file: $OrdersJson" }
$payload = Get-Content -LiteralPath $OrdersJson -Raw | ConvertFrom-Json

# Accept a bare array, or plan-batch.py's manifest (batches -> positions).
$signs = @()
if ($payload -is [array]) {
  $signs = $payload
} elseif ($payload.PSObject.Properties.Name -contains 'batches') {
  foreach ($b in $payload.batches) { $signs += $b.positions }
} elseif ($payload.PSObject.Properties.Name -contains 'signs') {
  $signs = $payload.signs
} else {
  throw "Unrecognised orders JSON. Expected an array, or a plan-batch.py manifest with .batches."
}
if (-not $signs -or $signs.Count -eq 0) { throw "No signs found in $OrdersJson - nothing to print." }

# Expand quantity>1 into separate physical signs; each one occupies a bed slot.
$expanded = @()
foreach ($s in $signs) {
  $qty = 1
  if ($s.PSObject.Properties.Name -contains 'quantity' -and $s.quantity) { $qty = [int]$s.quantity }
  for ($i = 1; $i -le $qty; $i++) { $expanded += $s }
}
$signs = $expanded

# --- validate before generating anything ------------------------------------
# Every sign is checked up front. Failing on sign 7 of 8 after six Chrome renders
# wastes minutes and leaves a confusing half-populated OutDir.
$problems = @()
for ($i = 0; $i -lt $signs.Count; $i++) {
  $s = $signs[$i]
  $where = "sign $($i+1)"
  if ($s.PSObject.Properties.Name -contains 'order' -and $s.order) { $where = $s.order }
  foreach ($f in 'sku','size','line1') {
    if (($s.PSObject.Properties.Name -notcontains $f) -or -not $s.$f) { $problems += "$where : missing '$f'" }
  }
  if ($s.PSObject.Properties.Name -contains 'size' -and $s.size) {
    if ($s.size.ToString().ToLower() -notin @('large','medium','small')) {
      $problems += "$where : size '$($s.size)' is not Large, Medium or Small"
    }
  }
}
if ($problems.Count) { throw ("Refusing to run:`n  " + ($problems -join "`n  ")) }

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$work = Join-Path $OutDir '_work'
New-Item -ItemType Directory -Force -Path $work | Out-Null

# --- group into beds: one bed = one SIZE. Colour does not split a bed. -------
# Border colour is artwork, not a machine setting: the Mimaki lays CMYK onto
# white acrylic, so a grass sign and a blush sign on the same bed are simply two
# different images in one print run with no re-setup between them. Splitting by
# colourway used to force a part bed per colour - eight colourways could mean
# eight half-empty beds and eight print runs to place a dozen signs. Only the
# physical blank size changes the layout, so only size groups a bed.
$groups = @{}
foreach ($s in $signs) {
  $key = $s.size.ToString().ToLower()
  if (-not $groups.ContainsKey($key)) { $groups[$key] = @() }
  $groups[$key] += $s
}

Write-Host ("`n{0} sign(s) -> {1} size group(s)" -f $signs.Count, $groups.Count)

$beds = @()
foreach ($size in ($groups.Keys | Sort-Object)) {
  $layout  = Get-DaisyBedLayout -Size $size
  $perBed  = $layout.Count
  $members = $groups[$size]

  Write-Host ("`n=== {0} : {1} sign(s), {2} per bed ===" -f $size, $members.Count, $perBed)

  for ($start = 0; $start -lt $members.Count; $start += $perBed) {
    $slice   = @($members[$start..([Math]::Min($start + $perBed, $members.Count) - 1)])
    $bedNo   = $beds.Count + 1
    $bedName = "bed{0:D2}-{1}" -f $bedNo, $size
    # Report the colours actually on this bed, since one bed can now carry several.
    $colours = @($slice | ForEach-Object {
      if (($_.PSObject.Properties.Name -contains 'colour') -and $_.colour) { $_.colour.ToString() } else { 'Black' }
    } | Sort-Object -Unique)
    Write-Host ("  {0}: {1} of {2} slots  [{3}]" -f $bedName, $slice.Count, $perBed, ($colours -join ', '))

    # --- per sign: generate, style, bleed ---
    $bled = @()
    $plain = @()
    foreach ($s in $slice) {
      # Shopify order names arrive as "#DM37869". Strip the leading hash rather
      # than substituting it, or every file and every stamped order id reads
      # "_DM37869" and stops matching what the order actually says.
      $id  = if ($s.PSObject.Properties.Name -contains 'order' -and $s.order) { ($s.order -replace '^#', '') -replace '[^\w.-]', '_' } else { "sign$($bled.Count+1)" }
      $stem = "{0}-{1}" -f $bedName, $id
      $raw  = Join-Path $work "$stem-raw.svg"
      $sty  = Join-Path $work "$stem-styled.svg"
      $ble  = Join-Path $work "$stem-bleed.svg"
      # A blank line 2 MUST be passed as the --no-line2 switch, never as ''.
      # PowerShell 5.1 drops empty arguments to native commands, so '' would leave
      # build.py on its wedding-date default and print a wedding subtitle on a
      # house sign. Caught in testing on "THE POTTING SHED".
      $l2 = ''
      if (($s.PSObject.Properties.Name -contains 'line2') -and $s.line2) { $l2 = $s.line2.ToString() }

      Invoke-Stage "build.py ($id)" {
        if ($l2) { python (Join-Path $PROJ 'artwork\build.py') --size $size --out $raw $id $s.line1 $l2 | Out-Null }
        else     { python (Join-Path $PROJ 'artwork\build.py') --size $size --out $raw --no-line2 $id $s.line1 | Out-Null }
      }

      # Colour is read PER SIGN, not per bed. When a bed was one colourway the
      # group's colour was the same for every member, so taking it from the group
      # was correct by accident. A mixed bed makes that wrong: it would paint the
      # whole bed in whichever colour the first order happened to use.
      $signCol = ''
      if (($s.PSObject.Properties.Name -contains 'colour') -and $s.colour) { $signCol = $s.colour.ToString() }

      $rcArgs = @('-SvgPath', $raw, '-OutPath', $sty, '-Sku', $s.sku.ToString())
      if ($signCol) { $rcArgs += @('-Colourway', $signCol) }
      Invoke-Stage "recolour-sign ($id)" { powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $HERE 'recolour-sign.ps1') @rcArgs | Out-Null }

      Invoke-Stage "add-bleed ($id)" { python (Join-Path $HERE 'add-bleed.py') $sty $ble $BleedMm | Out-Null }

      $bled  += $ble
      $plain += $sty
      Write-Host ("    {0,-14} {1}" -f $id, $s.line1)
    }

    # --- bed: impose the bled artwork, and cut a jig from the UNBLED contour ---
    # The jig must trace the real blank. Handing it a bled SVG would trace an
    # outline 4 mm oversize and the blanks would rattle in their slots -
    # make-jig.ps1 rejects a negative viewBox origin for exactly this reason.
    $bedSvg = Join-Path $OutDir "$bedName.svg"
    $jigSvg = Join-Path $OutDir "$bedName-jig.svg"
    $quoted = ($bled | ForEach-Object { "'" + $_.Replace("'","''") + "'" }) -join ','
    Invoke-Stage "make-imposition ($bedName)" {
      powershell -NoProfile -ExecutionPolicy Bypass -Command `
        "& '$((Join-Path $HERE 'make-imposition.ps1').Replace("'","''"))' -Size $size -SignSvgs $quoted -OutSvg '$bedSvg'" | Out-Null
    }
    Invoke-Stage "make-jig ($bedName)" {
      powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $HERE 'make-jig.ps1') -Size $size -ContourSvg $plain[0] -OutSvg $jigSvg | Out-Null
    }

    # --- PDFs ---
    foreach ($svg in @($bedSvg, $jigSvg)) {
      $pdf = [IO.Path]::ChangeExtension($svg, '.pdf')
      Invoke-Stage "svg-to-print-pdf ($([IO.Path]::GetFileName($svg)))" {
        powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $HERE 'svg-to-print-pdf.ps1') -SvgPath $svg -PdfPath $pdf |
          Select-String -Pattern 'page:' | ForEach-Object { "      " + $_.Line.Trim() }
      }
    }

    $beds += [pscustomobject]@{
      bed      = $bedName
      size     = $size
      colours  = $colours
      signs    = $slice.Count
      capacity = $perBed
      full     = ($slice.Count -eq $perBed)
      artwork  = [IO.Path]::ChangeExtension($bedSvg, '.pdf')
      jig      = [IO.Path]::ChangeExtension($jigSvg, '.pdf')
      orders   = @($slice | ForEach-Object { if ($_.PSObject.Properties.Name -contains 'order') { $_.order } else { '' } })
    }
  }
}

if (-not $KeepIntermediates) { Remove-Item -Recurse -Force -LiteralPath $work }

# --- manifest ---------------------------------------------------------------
# Written last, so its existence means every stage above succeeded.
$manifest = [pscustomobject]@{
  outDir      = (Resolve-Path -LiteralPath $OutDir).Path
  source      = (Resolve-Path -LiteralPath $OrdersJson).Path
  bleedMm     = $BleedMm
  signCount   = $signs.Count
  beds        = $beds
  manualStep  = 'Press ENTER on the printer panel for every job - the head heater is faulty and never reaches temperature.'
  nextAction  = 'Check each PDF, print the jig, dry-fit real blanks, then copy the artwork PDF to the RasterLink7 hot folder.'
}
$manifestPath = Join-Path $OutDir 'run-manifest.json'
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

# --- optional handoff to RasterLink7 ----------------------------------------
# Only the ARTWORK goes to the hot folder, never the jig. The jig is printed
# once per fresh bed as its own deliberate job; sweeping it in here would queue
# outlines to print straight onto acrylic blanks, which has nearly happened
# before. RasterLink imports within ~5 seconds and the file disappears from the
# folder - that disappearance is the confirmation, not a dialog.
if ($SendToPrinter) {
  if (-not (Test-Path -LiteralPath $HotFolder)) {
    throw "Hot folder '$HotFolder' does not exist. Is RasterLink7 installed and running on this machine? Nothing was sent; the PDFs in $OutDir are unaffected."
  }
  Write-Host "`nCopying artwork to $HotFolder"
  foreach ($b in $beds) {
    if (-not (Test-Path -LiteralPath $b.artwork)) { throw "Missing artwork PDF for $($b.bed) - refusing to send a partial batch." }
    Copy-Item -LiteralPath $b.artwork -Destination $HotFolder -Force
    Write-Host ("  sent {0}" -f (Split-Path -Leaf $b.artwork))
  }
  Write-Host "`nIn RasterLink7: select the job, Alt+X, RIP and Print, Start, page at 0,0."
  Write-Host 'Use 600x900 VD / 12 pass - NOT the default a fresh profile assigns.'
  Write-Host 'Then press ENTER on the printer panel. The head heater is faulty, so it never clears itself.'
}

Write-Host "`n---------------------------------------------------------------"
Write-Host ("{0} sign(s) on {1} bed(s):" -f $signs.Count, $beds.Count)
foreach ($b in $beds) {
  $flag = if ($b.full) { 'FULL' } else { "PART ($($b.signs)/$($b.capacity))" }
  Write-Host ("  {0,-20} {1,-12} {2}" -f $b.bed, $flag, ($b.colours -join ', '))
}
$part = @($beds | Where-Object { -not $_.full })
if ($part.Count) {
  Write-Host ("`n{0} bed(s) are not full. Printing a part bed wastes acrylic; holding it delays those orders. Your call." -f $part.Count)
}
Write-Host "`nManifest: $manifestPath"
if ($SendToPrinter) {
  Write-Host ("{0} artwork PDF(s) are in the hot folder. The ENTER press on the panel is still yours." -f $beds.Count)
} else {
  Write-Host 'Nothing has been sent to the printer. Re-run with -SendToPrinter once the PDFs are checked.'
}
