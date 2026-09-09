<#
Loads environment variables from .env in the workspace root
and runs installation + makemigrations + migrate + runserver.

Usage: run this script from the project root in PowerShell.
Ensure you created a .env file (see .env.example) before running.
#>

$envFile = Join-Path $PSScriptRoot '.env'
if (-Not (Test-Path $envFile)) {
    Write-Error ".env not found at $envFile. Create it from .env.example and fill values before running."
    exit 1
}

Get-Content $envFile | ForEach-Object {
    $_ = $_.Trim()
    if ($_ -eq '' -or $_.StartsWith('#')) { return }
    $parts = $_ -split('=',2)
    if ($parts.Length -ne 2) { return }
    $name = $parts[0].Trim()
    $value = $parts[1].Trim()
    # Remove surrounding quotes if any
    if ($value.StartsWith('"') -and $value.EndsWith('"')) { $value = $value.Trim('"') }
    if ($value.StartsWith("'") -and $value.EndsWith("'")) { $value = $value.Trim("'") }
    Write-Host "Setting env: $name"
    Set-Item -Path Env:\$name -Value $value
}

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Making migrations..."
python manage.py makemigrations

Write-Host "Applying migrations..."
python manage.py migrate

Write-Host "Starting development server at http://127.0.0.1:8000"
python manage.py runserver
