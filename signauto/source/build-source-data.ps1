param(
    [string]$SourceRoot = 'E:\sean\max'
)

$ErrorActionPreference = 'Stop'

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw "Source bundle is unavailable at '$SourceRoot'. Mount it or pass -SourceRoot with the folder containing the PSD, LightBurn file, transfer log, and Fonts folder."
}

$lightBurnPath = Join-Path $SourceRoot 'LARGE SIGN.lbrn2'
$photoshopPath = Join-Path $SourceRoot 'lARGE STREET SIGN PSD.psd'
$transferLogPath = Join-Path $SourceRoot 'gude-2026-07-14.log'
$fontRoot = Join-Path $SourceRoot 'Fonts'
$fontFiles = @(
    @{ File = 'times.ttf'; Style = 'Regular'; Weight = 400 },
    @{ File = 'timesbd.ttf'; Style = 'Bold'; Weight = 700 },
    @{ File = 'timesbi.ttf'; Style = 'Bold Italic'; Weight = 700 },
    @{ File = 'timesi.ttf'; Style = 'Italic'; Weight = 400 }
)

$required = @($lightBurnPath, $photoshopPath, $transferLogPath) + ($fontFiles | ForEach-Object { Join-Path $fontRoot $_.File })
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath $_ -PathType Leaf) })
if ($missing.Count -gt 0) {
    throw "Missing source file(s): $($missing -join ', ')"
}

[xml]$lightBurn = Get-Content -Raw -LiteralPath $lightBurnPath
$project = $lightBurn.LightBurnProject
$pathShape = @($project.Shape | Where-Object { $_.Type -eq 'Path' })[0]
if (-not $pathShape) {
    throw 'The LightBurn project does not contain a path shape.'
}

$numberPattern = '[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'
$vertexMatches = [regex]::Matches([string]$pathShape.VertList, "V($numberPattern)\s+($numberPattern)")
if ($vertexMatches.Count -lt 4) {
    throw 'The LightBurn contour could not be decoded.'
}

$transformValues = [regex]::Matches([string]$pathShape.XForm, $numberPattern) | ForEach-Object { [double]$_.Value }
if ($transformValues.Count -ne 6) {
    throw 'The LightBurn contour transform is not a six-value affine transform.'
}
$a, $b, $c, $d, $e, $f = $transformValues

$globalPoints = foreach ($match in $vertexMatches) {
    $x = [double]$match.Groups[1].Value
    $y = [double]$match.Groups[2].Value
    [pscustomobject]@{
        X = ($a * $x) + ($c * $y) + $e
        Y = ($b * $x) + ($d * $y) + $f
    }
}

$minX = ($globalPoints.X | Measure-Object -Minimum).Minimum
$maxX = ($globalPoints.X | Measure-Object -Maximum).Maximum
$minY = ($globalPoints.Y | Measure-Object -Minimum).Minimum
$maxY = ($globalPoints.Y | Measure-Object -Maximum).Maximum
$contourPoints = @($globalPoints | ForEach-Object {
    [ordered]@{
        x = [math]::Round($_.X - $minX, 3)
        y = [math]::Round($_.Y - $minY, 3)
    }
})

$holes = @($project.Shape | Where-Object { $_.Type -eq 'Ellipse' } | ForEach-Object {
    $ellipse = $_
    $values = [regex]::Matches([string]$ellipse.XForm, $numberPattern) | ForEach-Object { [double]$_.Value }
    if ($values.Count -ne 6) {
        throw 'A LightBurn mounting-hole transform is invalid.'
    }
    [ordered]@{
        x = [math]::Round($values[4] - $minX, 3)
        y = [math]::Round($values[5] - $minY, 3)
        radius = [math]::Round([double]$ellipse.Rx, 3)
    }
} | Sort-Object { $_.x })

$fontAudit = @($fontFiles | ForEach-Object {
    $path = Join-Path $fontRoot $_.File
    [ordered]@{
        filename = $_.File
        family = 'Times New Roman'
        style = $_.Style
        weight = $_.Weight
        embeddingFsType = 8
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
    }
})

$sourceData = [ordered]@{
    generatedAt = (Get-Date).ToUniversalTime().ToString('o')
    status = 'VISUAL APPROVED BY MAX 2026-07-14 - OFFICE PRODUCTION CHECK REQUIRED'
    product = [ordered]@{
        title = 'Personalised Mr & Mrs Street Sign Gift'
        handle = 'mr-mrs-personalised-street-sign-gift'
        gid = 'gid://shopify/Product/9702132711763'
        sku = '36961'
        storefrontWidthMm = 570
        storefrontHeightMm = 120
        confirmedFinishedWidthMm = 570
        confirmedFinishedHeightMm = 125
    }
    lightBurn = [ordered]@{
        filename = 'LARGE SIGN.lbrn2'
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $lightBurnPath).Hash
        appVersion = [string]$project.AppVersion
        formatVersion = [string]$project.FormatVersion
        contour = [ordered]@{
            widthMm = [math]::Round($maxX - $minX, 3)
            heightMm = [math]::Round($maxY - $minY, 3)
            vertexCount = $contourPoints.Count
            points = $contourPoints
        }
        mountingHoles = $holes
        cutSettings = [ordered]@{
            speed = [double]$project.CutSetting.speed.Value
            minPower = [double]$project.CutSetting.minPower.Value
            maxPower = [double]$project.CutSetting.maxPower.Value
            passes = [int]$project.CutSetting.numPasses.Value
            runBlower = [bool][int]$project.CutSetting.runBlower.Value
        }
    }
    photoshop = [ordered]@{
        filename = 'lARGE STREET SIGN PSD.psd'
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $photoshopPath).Hash
        auditMethod = 'psd-tools 1.17.4 read-only inspection'
        canvasPx = [ordered]@{ width = 7200; height = 4960 }
        largeSignVisibleBoundsPx = [ordered]@{ left = 231; top = 126; right = 6998; bottom = 1635 }
        visibleAspectRatio = 4.484426
        equivalentHeightAt570Mm = 127.107
        purpose = 'Visible extent is consistent with deliberate print overrun across the black border.'
        overrunInterpretationConfidence = 'Likely'
        approximateTotalHeightOverrunMm = 2.107
        typefacePostScript = 'TimesNewRomanPSMT'
        fauxBold = $true
        verticalScale = 1.4
        mainTextSafeBoundsAt570Mm = [ordered]@{ left = 53.82; right = 518.24; top = 23.75; bottom = 88.94 }
        signatureHeartBoundsAt570Mm = [ordered]@{ left = 187.75; right = 207.63; top = 40.27; bottom = 59.55 }
    }
    transferLog = [ordered]@{
        filename = 'gude-2026-07-14.log'
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $transferLogPath).Hash
        assessment = 'Local resume-cache initialisation failed; supplied source files are present and independently readable.'
    }
    fonts = $fontAudit
    decisions = @(
        [ordered]@{
            code = 'FINISHED_SIZE_CONFIRMED'
            value = '570 x 125 mm'
            source = 'Max clarification on 2026-07-14'
            confidence = 'Accepted for this implementation'
            rationale = 'The LightBurn contour is the accepted finished cut size. The PSD extends to approximately 127.1 mm, consistent with Max''s explanation that black print intentionally overruns the cut border.'
        }
    )
    productionBlockers = @(
        [ordered]@{
            code = 'OFFICE_OUTPUT_VALIDATION_REQUIRED'
            disposition = 'Compare an approved generated order with the real office print and cut result.'
        },
        [ordered]@{
            code = 'PRODUCTION_HANDOFF_NOT_IMPLEMENTED'
            disposition = 'Printer, RIP, nesting, and laser handoff remain outside this preview experiment.'
        }
    )
}

$json = $sourceData | ConvertTo-Json -Depth 20 -Compress
$javascript = "window.DAISY_SOURCE_DATA = $json;`n"
[IO.File]::WriteAllText((Join-Path $sourceDir 'source-data.js'), $javascript, [Text.UTF8Encoding]::new($false))

Write-Output "Built source-data.js: contour=$($contourPoints.Count) vertices; holes=$($holes.Count); LightBurn=$([math]::Round($maxX - $minX, 3)) x $([math]::Round($maxY - $minY, 3)) mm"
