$ErrorActionPreference = 'Stop'
try {
    $pyroomUrl = 'http://127.0.0.1:8765'
    try { $health = Invoke-RestMethod -Uri "$pyroomUrl/api/health" -TimeoutSec 2 }
    catch { Write-Host 'Pyroom is already stopped.'; exit 0 }
    if ($health.app -ne 'pyroom') { throw 'Port 8765 is being used by another app.' }
    $course = Invoke-RestMethod -Uri "$pyroomUrl/api/course" -TimeoutSec 3
    Invoke-RestMethod -Method Post -Uri "$pyroomUrl/api/shutdown" -ContentType 'application/json' -Headers @{'X-Pyroom-Token' = $course.token} -Body '{}' -TimeoutSec 5 | Out-Null
    Write-Host 'Pyroom stopped. Your browser keeps your saved progress.'
} catch { Write-Host $_.Exception.Message -ForegroundColor Red; exit 1 }
