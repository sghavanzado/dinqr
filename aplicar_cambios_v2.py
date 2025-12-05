#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script mejorado para aplicar cambios a MainGrid.tsx
"""

# Leer el archivo
with open('frontend/src/components/MainGrid.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar la línea donde está funcionariosComQR
insert_line = None
for i, line in enumerate(lines):
    if 'const [funcionariosComQR, setFuncionariosComQR] = useState<Funcionario[]>([]);' in line:
        insert_line = i + 1
        break

if insert_line:
    # Insertar los dos nuevos estados
    lines.insert(insert_line, '  const [funcionariosConQRNormal, setFuncionariosConQRNormal] = useState<string[]>([]);\r\n')
    lines.insert(insert_line + 1, '  const [funcionariosConCV, setFuncionariosConCV] = useState<string[]>([]);\r\n')
    print("Estados agregados")

# Encontrar el useEffect y agregar las funciones antes
useeffect_line = None
for i, line in enumerate(lines):
    if 'useEffect(() => {' in line and 'fetchDashboardData' in lines[i+1]:
        useeffect_line = i
        break

if useeffect_line:
    # Insertar las funciones antes del useEffect
    functions = '''
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

'''
    lines.insert(useeffect_line, functions)
    print("Funciones agregadas")
    
    # Actualizar el índice del useEffect
    useeffect_line += functions.count('\n')
    
    # Encontrar el cierre del useEffect y agregar las llamadas
    for i in range(useeffect_line, min(useeffect_line + 10, len(lines))):
        if 'fetchFuncionarios();' in lines[i]:
            lines[i] = lines[i].rstrip() + '\r\n    fetchFuncionariosConCV();\r\n    fetchFuncionariosConQRNormal();\r\n'
            print("useEffect actualizado")
            break

# Guardar el archivo
with open('frontend/src/components/MainGrid.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("OK - Cambios 1, 2 y 3 aplicados exitosamente")
