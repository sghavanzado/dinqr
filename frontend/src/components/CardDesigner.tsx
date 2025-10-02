import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  ButtonGroup,
  IconButton,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Add as AddIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
  Undo as UndoIcon,
  Redo as RedoIcon,
  TextFields as TextIcon,
  Image as ImageIcon,
  QrCode as QrCodeIcon,
  Palette as PaletteIcon,
  FlipToFront as FrontIcon,
  FlipToBack as BackIcon,
  ExpandMore as ExpandMoreIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { Stage, Layer, Rect, Text as KonvaText, Image as KonvaImage, Transformer } from 'react-konva';
import useImage from 'use-image';

// Constantes para o tamanho do passe CR80
const CARD_WIDTH_MM = 85.6;
const CARD_HEIGHT_MM = 54;
const SCALE_FACTOR = 10; // Para ter uma boa resolução na tela
const CANVAS_WIDTH = CARD_WIDTH_MM * SCALE_FACTOR; // 856px
const CANVAS_HEIGHT = CARD_HEIGHT_MM * SCALE_FACTOR; // 540px

// Tipos para elementos do design
interface DesignElement {
  id: string;
  type: 'text' | 'image' | 'qr' | 'background';
  x: number;
  y: number;
  width: number;
  height: number;
  rotation?: number;
  properties: {
    text?: string;
    fontSize?: number;
    fontFamily?: string;
    fill?: string;
    align?: string;
    src?: string;
    backgroundColor?: string;
    backgroundImage?: string;
  };
}

interface CardDesign {
  id: string;
  name: string;
  front: DesignElement[];
  back: DesignElement[];
  createdAt: Date;
  updatedAt: Date;
}

interface CardDesignerProps {
  open: boolean;
  onClose: () => void;
  onSave: (design: CardDesign) => void;
  initialDesign?: CardDesign;
}

// Componente para elementos de texto
const TextElement: React.FC<{
  element: DesignElement;
  isSelected: boolean;
  onSelect: () => void;
  onChange: (changes: Partial<DesignElement>) => void;
}> = ({ element, isSelected, onSelect, onChange }) => {
  const textRef = useRef<any>();
  const transformerRef = useRef<any>();

  useEffect(() => {
    if (isSelected && transformerRef.current && textRef.current) {
      transformerRef.current.nodes([textRef.current]);
      transformerRef.current.getLayer()?.batchDraw();
    }
  }, [isSelected]);

  return (
    <>
      <KonvaText
        ref={textRef}
        id={element.id}
        x={element.x}
        y={element.y}
        width={element.width}
        height={element.height}
        text={element.properties.text || 'Texto'}
        fontSize={element.properties.fontSize || 16}
        fontFamily={element.properties.fontFamily || 'Arial'}
        fill={element.properties.fill || '#000000'}
        align={element.properties.align || 'left'}
        draggable
        onClick={onSelect}
        onTap={onSelect}
        onDragEnd={(e) => {
          onChange({
            x: e.target.x(),
            y: e.target.y(),
          });
        }}
        onTransformEnd={(e) => {
          const node = textRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          onChange({
            x: node.x(),
            y: node.y(),
            width: Math.max(5, node.width() * scaleX),
            height: Math.max(5, node.height() * scaleY),
            rotation: node.rotation(),
          });

          node.scaleX(1);
          node.scaleY(1);
        }}
      />
      {isSelected && (
        <Transformer
          ref={transformerRef}
          boundBoxFunc={(oldBox, newBox) => {
            // Limitar o tamanho mínimo
            if (newBox.width < 5 || newBox.height < 5) {
              return oldBox;
            }
            return newBox;
          }}
        />
      )}
    </>
  );
};

// Componente para elementos de imagem
const ImageElement: React.FC<{
  element: DesignElement;
  isSelected: boolean;
  onSelect: () => void;
  onChange: (changes: Partial<DesignElement>) => void;
}> = ({ element, isSelected, onSelect, onChange }) => {
  const [image] = useImage(element.properties.src || '');
  const imageRef = useRef<any>();
  const transformerRef = useRef<any>();

  useEffect(() => {
    if (isSelected && transformerRef.current && imageRef.current) {
      transformerRef.current.nodes([imageRef.current]);
      transformerRef.current.getLayer()?.batchDraw();
    }
  }, [isSelected]);

  return (
    <>
      <KonvaImage
        ref={imageRef}
        id={element.id}
        x={element.x}
        y={element.y}
        width={element.width}
        height={element.height}
        image={image}
        draggable
        onClick={onSelect}
        onTap={onSelect}
        onDragEnd={(e) => {
          onChange({
            x: e.target.x(),
            y: e.target.y(),
          });
        }}
        onTransformEnd={(e) => {
          const node = imageRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          onChange({
            x: node.x(),
            y: node.y(),
            width: Math.max(5, node.width() * scaleX),
            height: Math.max(5, node.height() * scaleY),
            rotation: node.rotation(),
          });

          node.scaleX(1);
          node.scaleY(1);
        }}
      />
      {isSelected && (
        <Transformer
          ref={transformerRef}
          boundBoxFunc={(oldBox, newBox) => {
            if (newBox.width < 5 || newBox.height < 5) {
              return oldBox;
            }
            return newBox;
          }}
        />
      )}
    </>
  );
};

// Componente principal CardDesigner
const CardDesigner: React.FC<CardDesignerProps> = ({
  open,
  onClose,
  onSave,
  initialDesign,
}) => {
  // Estados principais
  const [currentSide, setCurrentSide] = useState<'front' | 'back'>('front');
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null);
  const [design, setDesign] = useState<CardDesign>(() => {
    if (initialDesign) return initialDesign;
    
    return {
      id: `design_${Date.now()}`,
      name: 'Novo Design',
      front: [
        {
          id: 'bg_front',
          type: 'background',
          x: 0,
          y: 0,
          width: CANVAS_WIDTH,
          height: CANVAS_HEIGHT,
          properties: {
            backgroundColor: '#ffffff',
          },
        },
      ],
      back: [
        {
          id: 'bg_back',
          type: 'background',
          x: 0,
          y: 0,
          width: CANVAS_WIDTH,
          height: CANVAS_HEIGHT,
          properties: {
            backgroundColor: '#ffffff',
          },
        },
      ],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
  });

  // Refs
  const stageRef = useRef<any>();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Estados da interface
  const [activeTab, setActiveTab] = useState(0);
  const [designName, setDesignName] = useState(design.name);

  // Elementos da face atual
  const currentElements = design[currentSide];
  const selectedElement = currentElements.find(el => el.id === selectedElementId);

  // Funções utilitárias
  const generateId = () => `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  const updateElement = (elementId: string, changes: Partial<DesignElement>) => {
    setDesign(prev => ({
      ...prev,
      [currentSide]: prev[currentSide].map(el =>
        el.id === elementId ? { ...el, ...changes } : el
      ),
      updatedAt: new Date(),
    }));
  };

  const addElement = (type: DesignElement['type'], properties: Partial<DesignElement> = {}) => {
    const newElement: DesignElement = {
      id: generateId(),
      type,
      x: 50,
      y: 50,
      width: type === 'text' ? 200 : 100,
      height: type === 'text' ? 40 : 100,
      properties: {
        ...(type === 'text' && {
          text: 'Novo Texto',
          fontSize: 16,
          fontFamily: 'Arial',
          fill: '#000000',
          align: 'left',
        }),
        ...(type === 'image' && {
          src: '',
        }),
        ...(type === 'qr' && {
          text: 'https://exemplo.com',
        }),
        ...properties.properties,
      },
      ...properties,
    };

    setDesign(prev => ({
      ...prev,
      [currentSide]: [...prev[currentSide], newElement],
      updatedAt: new Date(),
    }));

    setSelectedElementId(newElement.id);
  };

  const deleteElement = (elementId: string) => {
    if (elementId.startsWith('bg_')) return; // Não permitir deletar fundo

    setDesign(prev => ({
      ...prev,
      [currentSide]: prev[currentSide].filter(el => el.id !== elementId),
      updatedAt: new Date(),
    }));

    if (selectedElementId === elementId) {
      setSelectedElementId(null);
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const src = e.target?.result as string;
        addElement('image', {
          properties: { src },
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    const updatedDesign = {
      ...design,
      name: designName,
      updatedAt: new Date(),
    };
    onSave(updatedDesign);
  };

  const handleExportPNG = () => {
    if (stageRef.current) {
      const uri = stageRef.current.toDataURL();
      const link = document.createElement('a');
      link.download = `${designName}_${currentSide}.png`;
      link.href = uri;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  // Renderização dos elementos no canvas
  const renderElements = () => {
    return currentElements.map(element => {
      if (element.type === 'background') {
        return (
          <Rect
            key={element.id}
            x={element.x}
            y={element.y}
            width={element.width}
            height={element.height}
            fill={element.properties.backgroundColor || '#ffffff'}
          />
        );
      }

      if (element.type === 'text') {
        return (
          <TextElement
            key={element.id}
            element={element}
            isSelected={selectedElementId === element.id}
            onSelect={() => setSelectedElementId(element.id)}
            onChange={(changes) => updateElement(element.id, changes)}
          />
        );
      }

      if (element.type === 'image') {
        return (
          <ImageElement
            key={element.id}
            element={element}
            isSelected={selectedElementId === element.id}
            onSelect={() => setSelectedElementId(element.id)}
            onChange={(changes) => updateElement(element.id, changes)}
          />
        );
      }

      return null;
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth={false}
      fullWidth
      PaperProps={{
        sx: {
          width: '95vw',
          height: '90vh',
          maxWidth: '1400px',
        },
      }}
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="h6">Designer de Passes</Typography>
            <TextField
              size="small"
              value={designName}
              onChange={(e) => setDesignName(e.target.value)}
              placeholder="Nome do design"
              sx={{ minWidth: 200 }}
            />
          </Box>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ p: 0, overflow: 'hidden' }}>
        <Box sx={{ display: 'flex', height: '100%' }}>
          {/* Painel lateral esquerdo */}
          <Paper sx={{ width: 300, borderRadius: 0, overflow: 'auto' }}>
            <Box sx={{ p: 2 }}>
              {/* Controles de face */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Face do Passe
                </Typography>
                <ButtonGroup fullWidth variant="outlined">
                  <Button
                    startIcon={<FrontIcon />}
                    variant={currentSide === 'front' ? 'contained' : 'outlined'}
                    onClick={() => {
                      setCurrentSide('front');
                      setSelectedElementId(null);
                    }}
                  >
                    Frente
                  </Button>
                  <Button
                    startIcon={<BackIcon />}
                    variant={currentSide === 'back' ? 'contained' : 'outlined'}
                    onClick={() => {
                      setCurrentSide('back');
                      setSelectedElementId(null);
                    }}
                  >
                    Verso
                  </Button>
                </ButtonGroup>
              </Box>

              {/* Ações rápidas */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Adicionar Elementos
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Button
                    startIcon={<TextIcon />}
                    variant="outlined"
                    size="small"
                    onClick={() => addElement('text')}
                  >
                    Texto
                  </Button>
                  <Button
                    startIcon={<ImageIcon />}
                    variant="outlined"
                    size="small"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    Imagem
                  </Button>
                  <Button
                    startIcon={<QrCodeIcon />}
                    variant="outlined"
                    size="small"
                    onClick={() => addElement('qr')}
                  >
                    QR Code
                  </Button>
                </Box>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  style={{ display: 'none' }}
                  onChange={handleImageUpload}
                />
              </Box>

              {/* Propriedades do elemento selecionado */}
              {selectedElement && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Propriedades do Elemento
                  </Typography>
                  
                  {selectedElement.type === 'text' && (
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      <TextField
                        label="Texto"
                        size="small"
                        value={selectedElement.properties.text || ''}
                        onChange={(e) => updateElement(selectedElement.id, {
                          properties: { ...selectedElement.properties, text: e.target.value }
                        })}
                      />
                      
                      <FormControl size="small">
                        <InputLabel>Fonte</InputLabel>
                        <Select
                          value={selectedElement.properties.fontFamily || 'Arial'}
                          onChange={(e) => updateElement(selectedElement.id, {
                            properties: { ...selectedElement.properties, fontFamily: e.target.value }
                          })}
                        >
                          <MenuItem value="Arial">Arial</MenuItem>
                          <MenuItem value="Helvetica">Helvetica</MenuItem>
                          <MenuItem value="Times New Roman">Times New Roman</MenuItem>
                          <MenuItem value="Courier New">Courier New</MenuItem>
                        </Select>
                      </FormControl>

                      <Box>
                        <Typography variant="caption">Tamanho da Fonte</Typography>
                        <Slider
                          value={selectedElement.properties.fontSize || 16}
                          min={8}
                          max={72}
                          step={1}
                          onChange={(_, value) => updateElement(selectedElement.id, {
                            properties: { ...selectedElement.properties, fontSize: value as number }
                          })}
                          valueLabelDisplay="auto"
                        />
                      </Box>

                      <Box>
                        <Typography variant="caption">Cor do Texto</Typography>
                        <TextField
                          type="color"
                          size="small"
                          fullWidth
                          value={selectedElement.properties.fill || '#000000'}
                          onChange={(e) => updateElement(selectedElement.id, {
                            properties: { ...selectedElement.properties, fill: e.target.value }
                          })}
                        />
                      </Box>

                      <FormControl size="small">
                        <InputLabel>Alinhamento</InputLabel>
                        <Select
                          value={selectedElement.properties.align || 'left'}
                          onChange={(e) => updateElement(selectedElement.id, {
                            properties: { ...selectedElement.properties, align: e.target.value }
                          })}
                        >
                          <MenuItem value="left">Esquerda</MenuItem>
                          <MenuItem value="center">Centro</MenuItem>
                          <MenuItem value="right">Direita</MenuItem>
                        </Select>
                      </FormControl>
                    </Box>
                  )}

                  {selectedElement.type === 'background' && (
                    <Box>
                      <Typography variant="caption">Cor de Fundo</Typography>
                      <TextField
                        type="color"
                        size="small"
                        fullWidth
                        value={selectedElement.properties.backgroundColor || '#ffffff'}
                        onChange={(e) => updateElement(selectedElement.id, {
                          properties: { ...selectedElement.properties, backgroundColor: e.target.value }
                        })}
                      />
                    </Box>
                  )}

                  {selectedElement.id && !selectedElement.id.startsWith('bg_') && (
                    <Button
                      color="error"
                      variant="outlined"
                      size="small"
                      fullWidth
                      onClick={() => deleteElement(selectedElement.id)}
                      sx={{ mt: 2 }}
                    >
                      Eliminar Elemento
                    </Button>
                  )}
                </Box>
              )}
            </Box>
          </Paper>

          {/* Área do canvas */}
          <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            {/* Barra de ferramentas */}
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button startIcon={<UndoIcon />} size="small" disabled>
                    Desfazer
                  </Button>
                  <Button startIcon={<RedoIcon />} size="small" disabled>
                    Refazer
                  </Button>
                </Box>
                
                <Typography variant="body2" color="text.secondary">
                  {currentSide === 'front' ? 'Frente' : 'Verso'} • CR80 (85,6mm × 54mm)
                </Typography>
              </Box>
            </Box>

            {/* Canvas */}
            <Box
              sx={{
                flex: 1,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                backgroundColor: '#f5f5f5',
                overflow: 'auto',
                p: 2,
              }}
            >
              <Box
                sx={{
                  border: '2px solid #ccc',
                  borderRadius: 2,
                  overflow: 'hidden',
                  boxShadow: 3,
                }}
              >
                <Stage
                  ref={stageRef}
                  width={CANVAS_WIDTH}
                  height={CANVAS_HEIGHT}
                  onMouseDown={(e) => {
                    // Deselecionar se clicar no fundo
                    if (e.target === e.target.getStage()) {
                      setSelectedElementId(null);
                    }
                  }}
                  onTouchStart={(e) => {
                    if (e.target === e.target.getStage()) {
                      setSelectedElementId(null);
                    }
                  }}
                >
                  <Layer>
                    {renderElements()}
                  </Layer>
                </Stage>
              </Box>
            </Box>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Button onClick={onClose}>
          Cancelar
        </Button>
        <Button
          startIcon={<DownloadIcon />}
          onClick={handleExportPNG}
          variant="outlined"
        >
          Exportar PNG
        </Button>
        <Button
          startIcon={<SaveIcon />}
          onClick={handleSave}
          variant="contained"
        >
          Guardar Design
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CardDesigner;
