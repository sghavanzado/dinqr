# Configurações do Passe - Employee Pass Configuration

## 📋 Overview
The **Configurações do Passe** module provides comprehensive management of employee pass generation with advanced theming and formatting capabilities. This system allows full CRUD operations on pass themes (visual style, layout, typography) and formats (file type, dimensions, DPI).

## 🎨 Features

### Themes Management
- **Visual Styling**: Primary/secondary colors, text colors, border colors
- **Layout Control**: Horizontal, vertical, compact layouts with custom margins
- **Typography**: Font families and sizes for titles, names, job titles, and info text
- **Graphic Elements**: Logo positioning and sizing, QR code configuration
- **Background Options**: Solid colors, gradients, and image backgrounds

### Format Management
- **Industry Standards**: Support for CR80, CR100, Business Card, Badge, and Mini formats
- **File Types**: PDF, HTML, PNG, SVG output formats
- **Quality Control**: DPI settings, compression options, orientation control
- **Custom Dimensions**: Flexible width/height configuration in millimeters

## 🚀 API Endpoints

### Configuration
- `GET /api/iamc/passes/configuracao` - Get dynamic configuration with available themes, formats, and options

### Themes
- `GET /api/iamc/passes/temas` - List all themes
- `POST /api/iamc/passes/temas` - Create new theme
- `GET /api/iamc/passes/temas/{id}` - Get specific theme
- `PUT /api/iamc/passes/temas/{id}` - Update theme
- `DELETE /api/iamc/passes/temas/{id}` - Delete theme

### Formats
- `GET /api/iamc/passes/formatos` - List all formats
- `POST /api/iamc/passes/formatos` - Create new format
- `GET /api/iamc/passes/formatos/{id}` - Get specific format
- `PUT /api/iamc/passes/formatos/{id}` - Update format
- `DELETE /api/iamc/passes/formatos/{id}` - Delete format

### Pass Generation
- `POST /api/rrhh/passes/gerar` - Generate individual pass with theme/format
- `POST /api/rrhh/passes/lote` - Generate multiple passes
- `GET /api/rrhh/passes/preview/{id}` - Preview pass in HTML

## 📊 Database Tables

### pass_temas_avancado
Stores theme configurations including colors, layout, typography, graphic elements, and background settings.

### pass_formatos_avancado
Stores format configurations including dimensions, file type, quality, and orientation settings.

## 🔧 Standard Card Sizes

| Format | Dimensions (mm) | Description |
|--------|----------------|-------------|
| CR80 | 85.6 × 53.98 | Standard credit card |
| CR100 | 98.5 × 67.0 | Large card |
| BUSINESS | 89.0 × 51.0 | Business card |
| BADGE | 76.2 × 101.6 | Vertical badge |
| MINI | 70.0 × 45.0 | Mini card |

## 🎯 Usage Examples

### Creating a Theme
```json
{
  "nome": "Corporate Blue",
  "cor_primaria": "#1976d2",
  "cor_secundaria": "#e3f2fd",
  "cor_texto": "#000000",
  "layout_tipo": "horizontal",
  "fonte_titulo": "Helvetica-Bold",
  "tamanho_fonte_titulo": 12,
  "fundo_tipo": "solido",
  "fundo_cor": "#ffffff"
}
```

### Creating a Format
```json
{
  "nome": "PDF Standard CR80",
  "extensao": "pdf",
  "descricao": "Standard card for printing",
  "largura": 85.6,
  "altura": 53.98,
  "dpi": 300,
  "orientacao": "horizontal",
  "qualidade": 95
}
```

### Generating a Pass
```json
{
  "funcionario_id": 123,
  "incluir_qr": true,
  "tema_id": 1,
  "formato_id": 1,
  "data_validade": "2025-12-31"
}
```

## 🛠 Development Tools

### Testing
- `python test_endpoints.py` - Test all endpoints
- `python demo_passes_config.py` - Complete workflow demonstration

### Cleanup
- `python cleanup_test_data.py` - Clean test data from database

## 📝 Default Data

The system comes with 4 pre-configured themes:
1. **Corporate Blue** - Professional blue theme
2. **Executive Dark** - Dark gradient theme
3. **Modern Green** - Clean green theme
4. **Elegant Gray** - Sophisticated gray theme

And 5 pre-configured formats:
1. **PDF Standard CR80** - Standard card PDF
2. **PDF Vertical Badge** - Vertical badge PDF
3. **HTML Preview** - Browser preview
4. **PNG High Quality** - Digital image
5. **PDF Business Card** - Business card format

## 🔒 Validation

- Theme names must be unique
- Colors must be valid hex codes (#RRGGBB format)
- Layout types: horizontal, vertical, compact
- File extensions: pdf, html, png, svg
- DPI range: 72-600
- Quality: 1-100%

## 🎨 Frontend Integration

The backend provides complete API support for:
- Dynamic theme/format selection in UI
- Real-time preview capabilities
- Batch pass generation
- Configuration management interface

All endpoints return consistent JSON responses with proper error handling and validation messages.

## 📈 Status

✅ **PRODUCTION READY**
- All backend endpoints implemented and tested
- Database schema created and populated
- Validation and error handling complete
- Demo scripts working
- Ready for frontend integration

---

*Created for DINQR System - Employee Pass Management*
