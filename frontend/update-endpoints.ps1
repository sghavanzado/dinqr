$file = "src\components\BusinessCardTable.tsx"
$content = Get-Content $file -Raw -Encoding UTF8

# Actualizar endpoints
$content = $content -replace '/api/business-card/funcionarios-sin-carton', '/cv/funcionarios-sin-cv'
$content = $content -replace '/api/business-card/generar', '/cv/generar'

# Guardar
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "BusinessCardTable.tsx actualizado con nuevos endpoints" -ForegroundColor Green
