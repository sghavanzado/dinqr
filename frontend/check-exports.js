// Node.js import test
const fs = require('fs');
const path = require('path');

// Read the passesConfig.ts file and check for potential issues
const filePath = path.join(__dirname, 'src', 'services', 'api', 'passesConfig.ts');
const content = fs.readFileSync(filePath, 'utf8');

// Look for the ConfiguracaoAvancada export
const configExportMatch = content.match(/export interface ConfiguracaoAvancada/);
console.log('ConfiguracaoAvancada export found:', !!configExportMatch);

// Check if there are any potential syntax issues
const lines = content.split('\n');
lines.forEach((line, index) => {
  if (line.includes('ConfiguracaoAvancada') && line.includes('export')) {
    console.log(`Line ${index + 1}: ${line.trim()}`);
  }
});

console.log('File analysis complete.');
