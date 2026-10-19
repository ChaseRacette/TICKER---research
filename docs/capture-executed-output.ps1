# Run from the repository root in PowerShell:
# powershell -ExecutionPolicy Bypass -File docs\capture-executed-output.ps1

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$outputPath = Join-Path $PSScriptRoot 'executed-output.txt'

Set-Location $repoRoot
"Project 1 executed-model output" | Set-Content -LiteralPath $outputPath
"Captured: $(Get-Date -Format o)" | Add-Content -LiteralPath $outputPath
"Repository: $repoRoot" | Add-Content -LiteralPath $outputPath
"" | Add-Content -LiteralPath $outputPath

@(
    'python models\dcf.py',
    'python models\msft_pe_comps.py',
    'python msft_proforma.py',
    'python research\lab-11-sensitivity\msft_sensitivity.py'
) | ForEach-Object {
    "`n=== $_ ===" | Add-Content -LiteralPath $outputPath
    Invoke-Expression $_ 2>&1 | Out-String | Add-Content -LiteralPath $outputPath
}

Write-Host "Saved executed output to $outputPath"
