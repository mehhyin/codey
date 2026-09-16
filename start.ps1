param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$codeyUrl = 'http://127.0.0.1:8765'
$codeyEnv = Join-Path $PSScriptRoot '.env'
if (Test-Path -LiteralPath $codeyEnv) {
    $codeySetting = Get-Content -LiteralPath $codeyEnv | Where-Object { $_ -match '^BETTER_AUTH_URL=' } | Select-Object -Last 1
    if ($codeySetting) { $codeyUrl = $codeySetting.Substring(16).Trim().Trim('"').Trim("'") }
}
function Test-Codey {
    try { $health = Invoke-RestMethod -Uri "$codeyUrl/api/health" -TimeoutSec 2; return $health.app -eq 'codey' -and $health.version -eq 3 }
    catch { return $false }
}
try {
    if (Test-Codey) { if (-not $NoBrowser) { Start-Process $codeyUrl }; exit 0 }
    foreach ($required in @('.env','build/server/index.js','build/web/index.html','.runtime/pyodide/runtime.json')) {
        if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $required))) { throw 'Finish the first-time setup in README.md, then open Start Codey.cmd again.' }
    }
    $codeyNode = Join-Path $env:ProgramFiles 'nodejs/node.exe'
    if (-not (Test-Path -LiteralPath $codeyNode)) { $codeyNode = (Get-Command node.exe -ErrorAction Stop).Source }
    $codeyWork = Join-Path $PSScriptRoot '.runtime'
    $codeyProcess = Start-Process -FilePath $codeyNode -ArgumentList @('--env-file-if-exists=.env','build/server/index.js') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $codeyWork 'server.log') -RedirectStandardError (Join-Path $codeyWork 'server-error.log')
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        if (Test-Codey) {
            if (-not $NoBrowser) { Start-Process $codeyUrl }
            Write-Host "Codey is ready at $codeyUrl. Use Stop Codey.cmd when finished."
            exit 0
        }
        if ($codeyProcess.HasExited) { break }
        Start-Sleep -Milliseconds 300
    }
    throw 'Codey could not start. Check .runtime/server-error.log. Stop an older Codey server before trying again.'
} catch { Write-Host $_.Exception.Message -ForegroundColor Red; exit 1 }
