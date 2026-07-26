# recolour-sign.ps1
#
# Produces a recoloured copy of an approved street-sign SVG.
#
# WHY A POST-PROCESS AND NOT A build.py CHANGE
# --------------------------------------------
# build.py owns the audited geometry: the real 409-vertex cut contour, the PSD-
# derived metrics, and the locked heart+ampersand signature unit. Colour is
# orthogonal to all of that, so it is safer to transform the finished SVG than to
# add colour branching inside the generator and risk the approved geometry.
#
# Edits are made by ELEMENT ID via the XML DOM, never by string-replacing
# "#010101". A blind replace would also hit the mounting-hole strokes, any future
# element sharing the colour, and the metadata block - and would silently do the
# wrong thing the first time a design gained a second black element.
#
# The heart is deliberately untouched. It is a raster asset and part of the locked
# signature; the red heart is the same on every colourway.
#
# USAGE
#   powershell -NoProfile -ExecutionPolicy Bypass -File recolour-sign.ps1 `
#       -SvgPath ..\artwork\orders\DM37805.svg -OutPath out\DM37805-grass.svg `
#       -Colourway Grass
#
#   ...or set colours independently:
#       -BorderColour '#68893C' -TextColour '#010101'
#
# Shopify's Family street sign (SKU 36965) carries a `Colour border` attribute
# whose values map onto -Colourway directly (black, grass, grey, ...).

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$SvgPath,
  [Parameter(Mandatory=$true)][string]$OutPath,
  # Named colourway - sets border and text together, which is how the source
  # artwork does it. Explicit -BorderColour/-TextColour override it.
  [string]$Colourway,
  [string]$BorderColour,
  [string]$TextColour,
  [string]$PanelColour = '#FFFFFF',
  # The mounting holes are PHYSICAL holes in the acrylic. build.py draws them as
  # stroked circles, which prints black rings around a hole - ink that should not
  # be there. Max confirmed 2026-07-26 they are to be disregarded on every
  # mock-up, so removal is the default. Pass -KeepMountingHoles only to reproduce
  # an old proof.
  [switch]$KeepMountingHoles,
  # The red heart belongs to the Mr & Mrs Personalised Street Sign (SKU 36961)
  # ONLY. Every other street sign product omits it, even when the customer's text
  # happens to contain an ampersand.
  [switch]$RemoveHeart
)

$ErrorActionPreference = 'Stop'

# Exact values recovered from the production PSD text-engine data and validated
# against the known-good Large spec, which returns #010101.
$PALETTE = @{
  'black'     = '#010101'
  'grey'      = '#7C7C7C'
  'gray'      = '#7C7C7C'
  'sage'      = '#9AA192'
  'grass'     = '#68893C'
  'blue'      = '#799CAA'
  'lightsage' = '#BEC0A9'
  'blush'     = '#EBC3C3'
  'duskypink' = '#CB9CA5'
}

function Resolve-Colour([string]$v, [string]$what) {
  if (-not $v) { return $null }
  $key = ($v -replace '[\s_-]', '').ToLower()
  if ($PALETTE.ContainsKey($key)) { return $PALETTE[$key] }
  if ($v -match '^#[0-9A-Fa-f]{6}$') { return $v.ToUpper() }
  throw ("$what '$v' is neither a known colourway nor a #RRGGBB hex. Known: " + (($PALETTE.Keys | Sort-Object) -join ', '))
}

if ($Colourway) {
  $c = Resolve-Colour $Colourway 'Colourway'
  if (-not $BorderColour) { $BorderColour = $c }
  if (-not $TextColour)   { $TextColour   = $c }
}
if (-not $BorderColour) { $BorderColour = '#010101' }
if (-not $TextColour)   { $TextColour   = '#010101' }
$BorderColour = Resolve-Colour $BorderColour 'BorderColour'
$TextColour   = Resolve-Colour $TextColour   'TextColour'
$PanelColour  = Resolve-Colour $PanelColour  'PanelColour'

Write-Host ("border {0} | text {1} | panel {2}" -f $BorderColour, $TextColour, $PanelColour)

[xml]$svg = Get-Content -LiteralPath $SvgPath -Raw
$ns = New-Object System.Xml.XmlNamespaceManager($svg.NameTable)
$ns.AddNamespace('s','http://www.w3.org/2000/svg')
$ns.AddNamespace('daisy','https://daisymaison.co.uk/ns/production')

$changed = 0
function Set-Attr($node, [string]$name, [string]$value, [string]$label) {
  if (-not $node) { return }
  $old = $node.GetAttribute($name)
  if ($old -and $old -ne 'none' -and $old -ne $value) {
    $node.SetAttribute($name, $value)
    Write-Host ("  {0,-22} {1} -> {2}  ({3})" -f $label, $old, $value, $name)
    $script:changed++
  }
}

# --- frame ------------------------------------------------------------------
Set-Attr ($svg.DocumentElement.SelectSingleNode("//s:path[@id='outer-plate']", $ns)) 'fill' $BorderColour 'outer-plate'

# --- panel ------------------------------------------------------------------
Set-Attr ($svg.DocumentElement.SelectSingleNode("//s:path[@id='inset-panel']", $ns)) 'fill' $PanelColour 'inset-panel'

# --- mounting holes ---------------------------------------------------------
# Removed by default: they are holes drilled in the acrylic, so a printed ring
# just puts ink where the material is absent.
foreach ($id in @('mounting-hole-left','mounting-hole-right')) {
  $n = $svg.DocumentElement.SelectSingleNode("//s:circle[@id='$id']", $ns)
  if (-not $n) { continue }
  if ($KeepMountingHoles) {
    Set-Attr $n 'fill'   $PanelColour  $id
    Set-Attr $n 'stroke' $BorderColour $id
  } else {
    [void]$n.ParentNode.RemoveChild($n)
    Write-Host ("  {0,-22} REMOVED (physical hole - no ink)" -f $id)
    $changed++
  }
}

# --- text -------------------------------------------------------------------
# Every run, including the ampersand: they must stay a single visual colour.
foreach ($t in $svg.DocumentElement.SelectNodes("//s:text", $ns)) {
  $label = if ($t.GetAttribute('id')) { $t.GetAttribute('id') } else { 'text' }
  Set-Attr $t 'fill'   $TextColour $label
  Set-Attr $t 'stroke' $TextColour $label
}

# --- the heart --------------------------------------------------------------
$heart = $svg.DocumentElement.SelectSingleNode("//s:image[@id='signature-heart']", $ns)
if (-not $heart) {
  Write-Warning 'No signature-heart found - is this really an approved sign SVG?'
} elseif ($RemoveHeart) {
  [void]$heart.ParentNode.RemoveChild($heart)
  Write-Host '  signature-heart        REMOVED (non Mr & Mrs product)'
  $changed++
  # The ampersand keeps its own signatureHorizontalScale, which exists to seat the
  # heart. Without the heart that scale is no longer serving anything, so the
  # ampersand may sit slightly narrow relative to the rest of the line. Flagged
  # rather than silently adjusted, because changing it means touching build.py's
  # approved layout.
  Write-Warning 'Heart removed but the ampersand retains signatureHorizontalScale from build.py. Check spacing on any sign whose text contains "&".'
} else {
  Write-Host '  signature-heart        kept (Mr & Mrs signature asset)'
}

if ($changed -eq 0) {
  Write-Warning 'Nothing changed - the requested colours already match the source.'
}

# --- record provenance in the daisy: metadata -------------------------------
$prod = $svg.DocumentElement.SelectSingleNode("//daisy:production", $ns)
if ($prod) {
  foreach ($pair in @(@('colourway', $(if ($Colourway) { $Colourway } else { 'custom' })),
                      @('borderColour', $BorderColour),
                      @('textColour', $TextColour),
                      @('panelColour', $PanelColour),
                      @('recolouredBy', 'production/recolour-sign.ps1'))) {
    $el = $svg.CreateElement('daisy', $pair[0], 'https://daisymaison.co.uk/ns/production')
    $el.InnerText = $pair[1]
    [void]$prod.AppendChild($el)
  }
} else {
  Write-Warning 'No daisy:production metadata block - colour provenance not recorded.'
}

$dir = Split-Path -Parent $OutPath
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
$svg.Save($OutPath)
Write-Host ("wrote {0} ({1:N0} bytes, {2} attribute(s) changed)" -f $OutPath, (Get-Item $OutPath).Length, $changed)
