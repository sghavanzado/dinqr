#!/bin/bash
cd "$(dirname "$0")"
git pull origin main
echo "✅ Cambios descargados correctamente."
read -p "Presiona Enter para salir..."

