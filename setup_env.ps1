$envPath = Join-Path $PSScriptRoot ".env"

Write-Host "This creates a local .env file. Do not commit it."
Write-Host "Use a fresh rotated key if you pasted a secret anywhere public."

$databaseUrl = Read-Host "Neon DATABASE_URL"
$groqApiKey = Read-Host "Groq Cloud API key"
$groqModel = Read-Host "Groq model [llama-3.1-8b-instant]"

if ([string]::IsNullOrWhiteSpace($groqModel)) {
    $groqModel = "llama-3.1-8b-instant"
}

$content = @"
DATABASE_URL=$databaseUrl
GROQ_API_KEY=$groqApiKey
GROQ_MODEL=$groqModel
PORT=5000
"@

Set-Content -Path $envPath -Value $content -Encoding UTF8
Write-Host ".env created at $envPath"

