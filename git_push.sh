#!/bin/bash
cd "$(dirname "$0")"
git add .
git commit -m "Actualización automática desde script"
git push origin main
echo "✅ Cambios subidos a GitHub correctamente."
read -p "Presiona Enter para salir..."

