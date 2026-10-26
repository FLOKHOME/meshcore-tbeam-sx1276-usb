# Windows launcher; Python and Git must be installed.
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py (Join-Path $project 'tools/build.py') @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python (Join-Path $project 'tools/build.py') @args
} else {
    Write-Error 'Python is missing. Install Python 3.11+ and Git for Windows.'
    exit 1
}
exit $LASTEXITCODE
