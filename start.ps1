param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$pyroomUrl = 'http://127.0.0.1:8765'
$pyroomRoot = $PSScriptRoot

function Test-Pyroom {
    try {
        $health = Invoke-RestMethod -Uri "$pyroomUrl/api/health" -TimeoutSec 2
        return $health.app -eq 'pyroom'
    } catch { return $false }
}

try {
    if (Test-Pyroom) {
        if (-not $NoBrowser) { Start-Process $pyroomUrl }
        exit 0
    }
    $pyroomPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (-not (Test-Path -LiteralPath $pyroomPython)) {
        $pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
        if ($pythonCommand -and $pythonCommand.Source -notlike '*WindowsApps*') {
            $pyroomPython = $pythonCommand.Source
        } else {
            throw 'Python could not be found. Install Python 3.12 or newer, then install pandas with: python -m pip install pandas'
        }
    }
    $pyroomWork = Join-Path (Split-Path (Split-Path $pyroomRoot -Parent) -Parent) 'work\pyroom-runtime'
    New-Item -ItemType Directory -Path $pyroomWork -Force | Out-Null
    $pyroomProcess = Start-Process -FilePath $pyroomPython -ArgumentList @('"' + (Join-Path $pyroomRoot 'server.py') + '"') -WorkingDirectory $pyroomRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $pyroomWork 'server.log') -RedirectStandardError (Join-Path $pyroomWork 'server-error.log')
    $pyroomProcess.Id | Set-Content -LiteralPath (Join-Path $pyroomWork 'server.pid')
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        if (Test-Pyroom) {
            if (-not $NoBrowser) { Start-Process $pyroomUrl }
            Write-Host 'Pyroom is open in your browser. Use Stop Pyroom.cmd when you are finished.'
            exit 0
        }
        if ($pyroomProcess.HasExited) { break }
        Start-Sleep -Milliseconds 300
    }
    throw "Pyroom could not start. See $pyroomWork\server-error.log. Port 8765 may already be in use."
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
