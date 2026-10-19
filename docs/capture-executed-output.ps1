# Run from the repository root in PowerShell:
# powershell -ExecutionPolicy Bypass -File docs\capture-executed-output.ps1

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$outputPath = Join-Path $PSScriptRoot 'executed-output.txt'
$temporaryOutputPath = Join-Path $PSScriptRoot 'executed-output.tmp.txt'

Set-Location $repoRoot
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not available. Install Python 3, reopen the terminal, then rerun this script."
}

"Project 1 executed-model output" | Set-Content -LiteralPath $temporaryOutputPath
"Captured: $(Get-Date -Format o)" | Add-Content -LiteralPath $temporaryOutputPath
"Repository: $repoRoot" | Add-Content -LiteralPath $temporaryOutputPath
"" | Add-Content -LiteralPath $temporaryOutputPath

$commands = @(
    @{ Label = 'python models\dcf.py'; Arguments = @('models\dcf.py') },
    @{ Label = 'python models\msft_pe_comps.py'; Arguments = @('models\msft_pe_comps.py') },
    @{ Label = 'python msft_proforma.py'; Arguments = @('msft_proforma.py') },
    @{ Label = 'python research\lab-11-sensitivity\msft_sensitivity.py'; Arguments = @('research\lab-11-sensitivity\msft_sensitivity.py') }
)

foreach ($command in $commands) {
    "`n=== $($command.Label) ===" | Add-Content -LiteralPath $temporaryOutputPath
    $ErrorActionPreference = 'Continue'
    & python @($command.Arguments) 2>&1 | Out-String | Add-Content -LiteralPath $temporaryOutputPath
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -ne 0) {
        Remove-Item -LiteralPath $temporaryOutputPath -ErrorAction SilentlyContinue
        throw "Model command failed: $($command.Label)"
    }
}

Move-Item -LiteralPath $temporaryOutputPath -Destination $outputPath -Force
Write-Host "Saved executed output to $outputPath"
