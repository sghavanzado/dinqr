# CardDesigner Theme Editing Fix

## Issues Fixed

### 1. MUI Grid Migration Warnings
**Problem**: Console warnings about deprecated Grid props (`xs`, `sm`, `md`)
**Solution**: Updated all Grid components to use the new `size` prop format

**Files Changed**:
- `frontend/src/components/funcionarios/SearchFilter.tsx`
- `frontend/src/pages/rrhh/PassesConfig.tsx`

**Before**:
```tsx
<Grid xs={12} sm={6} md={4}>
```

**After**:
```tsx
<Grid size={{ xs: 12, sm: 6, md: 4 }}>
```

### 2. CardDesigner Not Loading Existing Themes
**Problem**: When clicking "Editar" on an existing theme, CardDesigner always opened as a new design instead of loading the selected theme's design.

**Root Cause**: The `initialDesign` calculation was happening before the `temaEditando` state was properly set.

**Solution**:
1. Added `designerInitialDesign` state to manage the initial design separately
2. Modified `abrirDialogTema()` to prepare the initial design before opening CardDesigner
3. Added `useEffect` in CardDesigner to handle changes to `initialDesign` prop
4. Used `setTimeout` to ensure state synchronization

**Key Changes**:

```tsx
// New state for managing initial design
const [designerInitialDesign, setDesignerInitialDesign] = useState<any>(undefined);

// Updated abrirDialogTema function
const abrirDialogTema = (tema?: TemaAvancado) => {
  if (tema) {
    setTemaEditando(tema);
    setFormTema(tema);
    
    // Prepare initial design based on existing data or create from theme properties
    let initialDesign = tema.design ? 
      convertExistingDesign(tema.design) : 
      createDesignFromTheme(tema);
    
    setDesignerInitialDesign(initialDesign);
    
    setTimeout(() => {
      setDesignerAberto(true);
    }, 100);
  }
};
```

```tsx
// CardDesigner now properly handles initialDesign changes
useEffect(() => {
  if (initialDesign && initialDesign.id !== design.id) {
    setDesign(initialDesign);
    setDesignName(initialDesign.name);
    setSelectedElementId(null);
  }
}, [initialDesign, design.id]);
```

### 3. State Management Improvements
- Added proper cleanup when closing CardDesigner
- Improved synchronization between theme editing state and CardDesigner state
- Added debugging logs to track state changes

## Testing
After these changes:
1. ✅ MUI Grid warnings should be eliminated
2. ✅ Clicking "Editar" on an existing theme should open CardDesigner with the correct design
3. ✅ Creating new themes should work normally
4. ✅ State should be properly cleaned up when closing dialogs

## Console Logs
The debugging logs now show:
- `🔧 Editando tema existente:` when editing starts
- `✅ Tema tiene design guardado` or `⚡ Tema NO tiene design` based on existing data
- `🚀 Abrindo CardDesigner para edição com design:` when CardDesigner opens
- `🔄 CardDesigner: Actualizando design con initialDesign:` when design is loaded
