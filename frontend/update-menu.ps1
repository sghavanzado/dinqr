$file = "src\components\MenuContent.tsx"
$content = Get-Content $file -Raw -Encoding UTF8

# Buscar y reemplazar el bloque children
$oldText = @"
    children: [
      {
        id: '2.1',
        label: 'Gerar Code',
        icon: ReceiptLongOutlinedIcon,
        to: '/qrcode',
      },
    ],
"@

$newText = @"
    children: [
      {
        id: '2.1',
        label: 'Gerar Code',
        icon: ReceiptLongOutlinedIcon,
        to: '/qrcode',
      },
      {
        id: '2.2',
        label: 'Gerar CV',
        icon: ReceiptLongOutlinedIcon,
        to: '/business-card',
      },
    ],
"@

$content = $content -replace [regex]::Escape($oldText), $newText

# Guardar el archivo
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "MenuContent.tsx actualizado correctamente" -ForegroundColor Green
