$ErrorActionPreference = 'Stop'
try {
    $codeyUrl = 'http://127.0.0.1:8765'
    $codeyEnv = Join-Path $PSScriptRoot '.env'
    if (Test-Path -LiteralPath $codeyEnv) {
        $codeySetting = Get-Content -LiteralPath $codeyEnv | Where-Object { $_ -match '^BETTER_AUTH_URL=' } | Select-Object -Last 1
        if ($codeySetting) { $codeyUrl = $codeySetting.Substring(16).Trim().Trim('"').Trim("'") }
    }
    try { $health = Invoke-RestMethod -Uri "$codeyUrl/api/health" -TimeoutSec 2 }
    catch { Write-Host 'Codey is already stopped.'; exit 0 }
    if ($health.app -ne 'codey') { throw 'This address is being used by another app.' }
    if ($health.version -eq 3) {
        $codeyPort = ([uri]$codeyUrl).Port
        $codeyControl = Get-Content -LiteralPath (Join-Path $PSScriptRoot ".runtime/control-$codeyPort.json") -Raw | ConvertFrom-Json
        if ($codeyControl.url -ne $codeyUrl) { throw 'The saved server address does not match this app.' }
        $codeyHeaders = @{'Origin'=$codeyUrl; 'X-Codey-Request'='1'; 'X-Codey-Control'=$codeyControl.token}
    } else {
        # Stop a running v1/v2 server during the local upgrade.
        $course = Invoke-RestMethod -Uri "$codeyUrl/api/course" -TimeoutSec 3
        $codeyHeaders = @{'X-Codey-Token'=$course.token}
    }
    Invoke-RestMethod -Method Post -Uri "$codeyUrl/api/shutdown" -ContentType 'application/json' -Headers $codeyHeaders -Body '{}' -TimeoutSec 5 | Out-Null
    Write-Host 'Codey stopped. Saved account progress remains in SQLite; guest progress remains in your browser.'
} catch { Write-Host $_.Exception.Message -ForegroundColor Red; exit 1 }
