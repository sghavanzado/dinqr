#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para actualizar useEffect
"""

# Leer el archivo
with open('frontend/src/components/MainGrid.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar useEffect
old_useeffect = '''  useEffect(() => {
    fetchDashboardData();  // Cargar estadísticas del dashboard
    fetchFuncionarios();   // Cargar funcionarios con QR
  }, []);'''

new_useeffect = '''  useEffect(() => {
    fetchDashboardData();  // Cargar estadísticas del dashboard
    fetchFuncionarios();   // Cargar funcionarios con QR
    fetchFuncionariosConCV();
    fetchFuncionariosConQRNormal();
  }, []);'''

if old_useeffect in content:
    content = content.replace(old_useeffect, new_useeffect)
    print("useEffect actualizado correctamente")
else:
    print("ERROR: No se encontro el useEffect")

# Guardar
with open('frontend/src/components/MainGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Completado!")
