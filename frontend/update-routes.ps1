$file = "src\components\ContentArea.tsx"
$content = Get-Content $file -Raw -Encoding UTF8

# 1. Agregar import de BusinessCardManagement
$oldImport = "import QRManagement from '../pages/QRManagement';"
$newImport = @"
import QRManagement from '../pages/QRManagement';
import BusinessCardManagement from '../pages/BusinessCardManagement';
"@

$content = $content -replace [regex]::Escape($oldImport), $newImport

# 2. Agregar ruta después de /qrcode
$oldRoute = @"
      <Route
        path="/qrcode"
        element={
          <ProtectedRoute>
            <QRManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/perfil"
"@

$newRoute = @"
      <Route
        path="/qrcode"
        element={
          <ProtectedRoute>
            <QRManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/business-card"
        element={
          <ProtectedRoute>
            <BusinessCardManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/perfil"
"@

$content = $content -replace [regex]::Escape($oldRoute), $newRoute

# Guardar el archivo
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "ContentArea.tsx actualizado correctamente" -ForegroundColor Green
