# Text Element Structure Fix Test

The error `TypeError: Cannot read properties of undefined (reading 'text')` at `CardDesigner.tsx:136:34` indicates that `element.properties` is undefined when the TextElement component tries to access `element.properties.text`.

## Changes Made:

### 1. Fixed CardDesigner.tsx TextElement (Line 136)
- Added optional chaining (`?.`) to safely access properties
- Changed from `element.properties.text` to `element.properties?.text`

### 2. Fixed PassesConfig.tsx Initial Design Structure
- Updated the initial design creation to use proper structure that matches CardDesigner expectations
- Text elements now have `properties` object containing `text`, `fontSize`, `fontFamily`, `fill`, `align`
- Background elements now have proper `properties` object with `backgroundColor`

## Structure Before (causing error):
```javascript
{
  id: 'text-nome',
  type: 'text',
  content: '{{nome}}',  // ❌ Wrong structure
  fontSize: 10,         // ❌ Should be in properties
  fill: '#000000'       // ❌ Should be in properties
}
```

## Structure After (correct):
```javascript
{
  id: 'text-nome',
  type: 'text',
  name: 'Nome do Funcionário',
  x: 20,
  y: 30,
  width: 200,
  height: 40,
  properties: {           // ✅ Correct structure
    text: '{{nome}}',     // ✅ Text content
    fontSize: 10,         // ✅ Font size
    fontFamily: 'Helvetica-Bold',
    fill: '#000000',
    align: 'left'
  },
  asociation: 'nome'
}
```

## Expected Result:
- Text elements should now render without errors
- CardDesigner should open successfully with existing themes
- No more `Cannot read properties of undefined (reading 'text')` errors

## Backend Save Error:
The 400 BAD REQUEST error when saving themes needs additional investigation. The frontend is sending the correct structure, but the backend might be having validation issues with the design field structure.
