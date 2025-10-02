/**
 * Script de prueba para verificar los endpoints de la API
 */

async function testApiEndpoints() {
  const API_BASE = '/api/iamc/passes';
  
  console.log('=== PRUEBA DE ENDPOINTS DE PASSES API ===');
  
  const endpoints = [
    `${API_BASE}/configuracao`,
    `${API_BASE}/temas`,
    `${API_BASE}/formatos`
  ];
  
  for (const endpoint of endpoints) {
    try {
      console.log(`\n🔄 Probando: ${endpoint}`);
      
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      console.log(`📊 Status: ${response.status} ${response.statusText}`);
      console.log(`📋 Headers:`, Object.fromEntries(response.headers.entries()));
      
      const contentType = response.headers.get('content-type');
      
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        console.log(`✅ JSON Response:`, data);
      } else {
        const text = await response.text();
        console.log(`❌ Non-JSON Response (first 200 chars):`, text.substring(0, 200));
      }
      
    } catch (error) {
      console.error(`❌ Error en ${endpoint}:`, error);
    }
    
    console.log('─'.repeat(50));
  }
}

// Ejecutar las pruebas cuando se carga la página
if (typeof window !== 'undefined') {
  // En el navegador
  document.addEventListener('DOMContentLoaded', testApiEndpoints);
} else {
  // En Node.js (si se ejecuta con node)
  testApiEndpoints();
}

export { testApiEndpoints };
