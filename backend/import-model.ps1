$file = "app.py"
$content = Get-Content $file -Raw -Encoding UTF8

# Buscar la línea "from models.user import initialize_permissions"
# y agregar después el import del modelo cv_code
$oldText = "from models.user import initialize_permissions"
$newText = @"
from models.user import initialize_permissions
from models.cv_code import CVCode  # Importar modelo para Flask-Migrate
"@

$content = $content -replace [regex]::Escape($oldText), $newText

# Guardar
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "Modelo CVCode importado en app.py" -ForegroundColor Green
