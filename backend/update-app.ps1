$file = "app.py"
$content = Get-Content $file -Raw -Encoding UTF8

# Reemplazar import y registro del blueprint
$oldText = @"
    from routes.business_card_routes import business_card_bp
    app.register_blueprint(business_card_bp, url_prefix='/api/business-card')
"@

$newText = @"
    from routes.cv_routes import cv_bp
    app.register_blueprint(cv_bp, url_prefix='/cv')
"@

$content = $content -replace [regex]::Escape($oldText), $newText

# Guardar el archivo
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "app.py actualizado correctamente" -ForegroundColor Green
