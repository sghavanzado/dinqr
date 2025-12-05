# Solución a Errores de Dependencias Frontend
# Error: Could not resolve "./createStyles.js" y similares

# Paso 1: Detener Vite
# Presiona Ctrl+C en la terminal donde corre Vite

# Paso 2: Limpiar node_modules y cache
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
Remove-Item -Recurse -Force .vite -ErrorAction SilentlyContinue

# Paso 3: Reinstalar dependencias
npm install

# Paso 4: Reiniciar Vite
npm run dev

Write-Host "Dependencias reinstaladas. Intenta npm run dev nuevamente." -ForegroundColor Green
