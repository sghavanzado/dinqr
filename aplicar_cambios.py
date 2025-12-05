#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para aplicar cambios a MainGrid.tsx de forma segura
"""

import re

# Leer el archivo
with open('frontend/src/components/MainGrid.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# CAMBIO 1: Agregar estados después de funcionariosComQR
pattern1 = r'(const \[funcionariosComQR, setFuncionariosComQR\] = useState<Funcionario\[\]>\(\[\]\);)'
replacement1 = r'\1\r\n  const [funcionariosConQRNormal, setFuncionariosConQRNormal] = useState<string[]>([]);\r\n  const [funcionariosConCV, setFuncionariosConCV] = useState<string[]>([]);'
content = re.sub(pattern1, replacement1, content)

# CAMBIO 2: Agregar funciones antes del useEffect
pattern2 = r'(  };)\r\n\r\n(  // =============================================\r\n  // 🚀 EFFECT PARA CARGAR DATOS AL MONTAR EL COMPONENTE\r\n  // =============================================)'
replacement2 = r'''\1

  // Función para obtener funcionarios con CV
  const fetchFuncionariosConCV = async () => {
    try {
      const response = await axiosInstance.get('/cv/funcionarios-con-cv');
      if (response.status === 200) {
        const idsConCV = response.data.map((f: any) => String(f.id));
        setFuncionariosConCV(idsConCV);
      }
    } catch (error) {
      console.error('Error fetching funcionarios con CV:', error);
    }
  };

  // Función para obtener funcionarios con QR Normal
  const fetchFuncionariosConQRNormal = async () => {
    try {
      const response = await axiosInstance.get('/qr/solo-qr-normal');
      if (response.status === 200) {
        setFuncionariosConQRNormal(response.data.map((id: any) => String(id)));
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

\2'''
content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)

# CAMBIO 3: Actualizar useEffect
pattern3 = r'(useEffect\(\(\) => \{\r\n    fetchDashboardData\(\);  // Cargar estadísticas del dashboard\r\n    fetchFuncionarios\(\);)   // Cargar funcionarios con QR\r\n  \}, \[\]\);'
replacement3 = r'''\1   // Cargar funcionarios con QR
    fetchFuncionariosConCV();
    fetchFuncionariosConQRNormal();
  }, []);'''
content = re.sub(pattern3, replacement3, content)

# Guardar el archivo
with open('frontend/src/components/MainGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK - Cambios aplicados exitosamente a MainGrid.tsx")
print("Ahora debes aplicar manualmente el CAMBIO 4 (seccion de botones)")
