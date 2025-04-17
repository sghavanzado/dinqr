import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  Grid,
  Container,
  Typography,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Autocomplete,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import { 
  locationService, 
  unitService, 
  taxService, 
  supplierService, 
  clientService, 
  invoiceService, 
  productService 
} from '../api/apiService';

interface InvoiceItem {
  product_code: string;
  description: string;
  quantity: string;
  unit_of_measure: string;
  unit_price: string;
  discount: string;
  tax: string;
  total: number;
}

const NovaFatura = () => {
  // Estados principales
  const [formData, setFormData] = useState({
    invoice_number: '',
    issue_date: new Date().toISOString().split('T')[0],
    seller_id: '',
    seller_name: '',
    seller_address: '',
    seller_tax_id: '',
    client_id: '',
    client_name: '',
    client_address: '',
    client_tax_id: '',
    payment_terms: '30 días',
    currency: 'EUR',
    notes: '',
    country: '',
    province: '',
  });

  // Estados para datos y filtrado
  const [clients, setClients] = useState<any[]>([]);
  const [filteredClients, setFilteredClients] = useState<any[]>([]);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [filteredSuppliers, setFilteredSuppliers] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<any[]>([]);
  const [invoiceItems, setInvoiceItems] = useState<InvoiceItem[]>([]);
  
  // Estados para UI y carga
  const [totals, setTotals] = useState({
    subtotal: 0,
    totalTaxes: 0,
    totalDiscounts: 0,
    grandTotal: 0,
  });
  const [productDialogOpen, setProductDialogOpen] = useState(false);
  const [productFormData, setProductFormData] = useState({
    product_code: '',
    description: '',
    quantity: '',
    unit_of_measure: '',
    unit_price: '',
    discount: '0',
    tax: '21',
  });
  const [countries, setCountries] = useState<any[]>([]);
  const [provinces, setProvinces] = useState<any[]>([]);
  const [units, setUnits] = useState<any[]>([]);
  const [taxTypes, setTaxTypes] = useState<any[]>([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [loading, setLoading] = useState({
    clients: false,
    suppliers: false,
    products: false,
    searchProducts: false,
  });

  // Inicialización
  useEffect(() => {
    const initializeInvoice = async () => {
      try {
        const lastNumber = localStorage.getItem('lastInvoiceNumber') || '0';
        const nextNumber = parseInt(lastNumber) + 1;
        const invoiceNumber = `FA${nextNumber.toString().padStart(4, '0')}`;
        
        setFormData(prev => ({
          ...prev,
          invoice_number: invoiceNumber
        }));

        await Promise.all([
          fetchClients(),
          fetchSuppliers(),
          fetchProducts(),
          fetchCountries(),
          fetchUnits(),
          fetchTaxTypes()
        ]);
      } catch (error) {
        console.error('Error inicializando factura:', error);
      }
    };

    initializeInvoice();
  }, []);

  // Fetch de datos
  const fetchClients = async () => {
    setLoading(prev => ({ ...prev, clients: true }));
    try {
      const data = await clientService.getClients();
      setClients(data);
      setFilteredClients(data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    } finally {
      setLoading(prev => ({ ...prev, clients: false }));
    }
  };

  const fetchSuppliers = async () => {
    setLoading(prev => ({ ...prev, suppliers: true }));
    try {
      const data = await supplierService.getSuppliers();
      setSuppliers(data);
      setFilteredSuppliers(data);
    } catch (error) {
      console.error('Error fetching suppliers:', error);
    } finally {
      setLoading(prev => ({ ...prev, suppliers: false }));
    }
  };

  const fetchProducts = async () => {
    setLoading(prev => ({ ...prev, products: true }));
    try {
      const data = await productService.getProducts();
      setProducts(data);
      setFilteredProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(prev => ({ ...prev, products: false }));
    }
  };

  const fetchCountries = async () => {
    try {
      const data = await locationService.getCountries();
      setCountries(data);
    } catch (error) {
      console.error('Error fetching countries:', error);
    }
  };

  const fetchProvinces = async (countryId: string) => {
    try {
      const data = await locationService.getProvinces(Number(countryId));
      setProvinces(data);
    } catch (error) {
      console.error('Error fetching provinces:', error);
    }
  };

  const fetchUnits = async () => {
    try {
      const data = await unitService.getUnits();
      setUnits(data);
    } catch (error) {
      console.error('Error fetching units:', error);
    }
  };

  const fetchTaxTypes = async () => {
    try {
      const data = await taxService.getTaxTypes();
      setTaxTypes(data);
    } catch (error) {
      console.error('Error fetching tax types:', error);
    }
  };

  // Funciones de filtrado
  const filterClients = (inputValue: string) => {
    const filtered = clients.filter(client =>
      client.nif.toLowerCase().includes(inputValue.toLowerCase()) ||
      client.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredClients(filtered);
  };

  const filterSuppliers = (inputValue: string) => {
    const filtered = suppliers.filter(supplier =>
      supplier.nif.toLowerCase().includes(inputValue.toLowerCase()) ||
      supplier.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredSuppliers(filtered);
  };

  const filterProducts = async (inputValue: string) => {
    setLoading(prev => ({ ...prev, searchProducts: true }));
    try {
      let filtered;
      if (inputValue.length > 2) {
        const data = await productService.searchProducts(inputValue);
        filtered = data;
      } else {
        filtered = products.filter(product =>
          product.sku.toLowerCase().includes(inputValue.toLowerCase()) ||
          product.name.toLowerCase().includes(inputValue.toLowerCase())
        );
      }
      setFilteredProducts(filtered);
    } catch (error) {
      console.error('Error filtering products:', error);
    } finally {
      setLoading(prev => ({ ...prev, searchProducts: false }));
    }
  };

  // Handlers de selección
  const handleClientSelect = (event: any, value: any) => {
    if (value) {
      setFormData(prev => ({
        ...prev,
        client_id: value.id,
        client_name: value.name,
        client_address: value.address,
        client_tax_id: value.nif,
      }));
      setErrors(prev => ({ ...prev, client_id: '' }));
    } else {
      setFormData(prev => ({
        ...prev,
        client_id: '',
        client_name: '',
        client_address: '',
        client_tax_id: '',
      }));
    }
  };

  const handleSupplierSelect = (event: any, value: any) => {
    if (value) {
      setFormData(prev => ({
        ...prev,
        seller_id: value.id,
        seller_name: value.name,
        seller_address: value.address,
        seller_tax_id: value.nif,
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        seller_id: '',
        seller_name: '',
        seller_address: '',
        seller_tax_id: '',
      }));
    }
  };

  const handleProductSelect = (event: any, value: any) => {
    if (value) {
      setProductFormData(prev => ({
        ...prev,
        product_code: value.sku,
        description: value.name,
        unit_of_measure: value.unit,
        unit_price: value.price.toString(),
      }));
    } else {
      setProductFormData(prev => ({
        ...prev,
        product_code: '',
        description: '',
        unit_of_measure: '',
        unit_price: '',
      }));
    }
  };

  // Validación y envío
  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.client_id) {
      newErrors.client_id = 'Seleccione un cliente';
    }
    
    if (invoiceItems.length === 0) {
      newErrors.items = 'Añada al menos un producto';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddProduct = () => {
    const quantity = parseFloat(productFormData.quantity) || 0;
    const unitPrice = parseFloat(productFormData.unit_price) || 0;
    const discount = parseFloat(productFormData.discount) || 0;
    const taxRate = parseFloat(productFormData.tax) || 0;

    if (quantity <= 0 || unitPrice <= 0) {
      setErrors(prev => ({ ...prev, product: 'Cantidad y precio deben ser mayores a 0' }));
      return;
    }

    const subtotal = quantity * unitPrice;
    const discountAmount = subtotal * (discount / 100);
    const taxableAmount = subtotal - discountAmount;
    const taxAmount = taxableAmount * (taxRate / 100);
    const total = taxableAmount + taxAmount;

    const newItem: InvoiceItem = {
      ...productFormData,
      total: total,
    };

    setInvoiceItems(prev => [...prev, newItem]);
    setTotals(prev => ({
      subtotal: prev.subtotal + subtotal,
      totalDiscounts: prev.totalDiscounts + discountAmount,
      totalTaxes: prev.totalTaxes + taxAmount,
      grandTotal: prev.grandTotal + total,
    }));

    setProductDialogOpen(false);
    setProductFormData({
      product_code: '',
      description: '',
      quantity: '',
      unit_of_measure: '',
      unit_price: '',
      discount: '0',
      tax: '21',
    });
    setErrors(prev => ({ ...prev, product: '', items: '' }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError('');
    setSubmitSuccess(false);

    if (!validateForm()) {
      return;
    }

    try {
      const invoiceData = {
        ...formData,
        items: invoiceItems,
        subtotal: totals.subtotal,
        total_discount: totals.totalDiscounts,
        total_tax: totals.totalTaxes,
        total_amount: totals.grandTotal,
      };

      const response = await invoiceService.createInvoice(invoiceData);
      
      if (response.success) {
        const currentNumber = parseInt(formData.invoice_number.replace('FA', ''));
        localStorage.setItem('lastInvoiceNumber', currentNumber.toString());
        
        const nextNumber = currentNumber + 1;
        const nextInvoiceNumber = `FA${nextNumber.toString().padStart(4, '0')}`;
        
        setFormData(prev => ({
          ...prev,
          invoice_number: nextInvoiceNumber,
          client_id: '',
          client_name: '',
          client_address: '',
          client_tax_id: '',
          notes: '',
        }));
        
        setInvoiceItems([]);
        setTotals({
          subtotal: 0,
          totalTaxes: 0,
          totalDiscounts: 0,
          grandTotal: 0,
        });
        
        setSubmitSuccess(true);
      }
    } catch (error) {
      console.error('Error guardando factura:', error);
      setSubmitError('Error al guardar la factura. Por favor intente nuevamente.');
    }
  };

  const handleCountryChange = (e: any) => {
    const countryId = e.target.value;
    setSelectedCountry(countryId);
    fetchProvinces(countryId);
    setFormData(prev => ({ ...prev, country: countryId, province: '' }));
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Nueva Factura
      </Typography>

      {submitError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {submitError}
        </Alert>
      )}

      {submitSuccess && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Factura creada exitosamente
        </Alert>
      )}

      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          {/* Header Section */}
          <Grid item xs={12} md={6}>
            <TextField
              label="Número de Factura"
              value={formData.invoice_number}
              fullWidth
              InputProps={{ readOnly: true }}
            />
            <TextField
              label="Fecha de Emisión"
              type="date"
              fullWidth
              value={formData.issue_date}
              sx={{ mt: 2 }}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          {/* Supplier Info */}
          <Grid item xs={12} md={6}>
            <Autocomplete
              options={filteredSuppliers}
              getOptionLabel={(option) => `${option.nif} - ${option.name}`}
              onInputChange={(event, newInputValue) => {
                filterSuppliers(newInputValue);
              }}
              onChange={handleSupplierSelect}
              loading={loading.suppliers}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Buscar Proveedor por NIF o Nombre"
                  fullWidth
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loading.suppliers ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <MenuItem {...props} key={option.id}>
                  <div>
                    <div><strong>{option.nif}</strong></div>
                    <div>{option.name}</div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>{option.address}</div>
                  </div>
                </MenuItem>
              )}
            />
            {formData.seller_id && (
              <Box sx={{ 
                mt: 1, 
                p: 2, 
                border: '1px solid #eee', 
                borderRadius: 1,
                backgroundColor: '#f9f9f9'
              }}>
                <Typography variant="subtitle2" gutterBottom>
                  Información del Proveedor
                </Typography>
                <Typography variant="body2">
                  <strong>Nombre:</strong> {formData.seller_name}
                </Typography>
                <Typography variant="body2">
                  <strong>Dirección:</strong> {formData.seller_address}
                </Typography>
                <Typography variant="body2">
                  <strong>NIF:</strong> {formData.seller_tax_id}
                </Typography>
              </Box>
            )}
          </Grid>

          {/* Client Info */}
          <Grid item xs={12} md={6}>
            <Autocomplete
              options={filteredClients}
              getOptionLabel={(option) => `${option.nif} - ${option.name}`}
              onInputChange={(event, newInputValue) => {
                filterClients(newInputValue);
              }}
              onChange={handleClientSelect}
              loading={loading.clients}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Buscar Cliente por NIF o Nombre"
                  fullWidth
                  error={!!errors.client_id}
                  helperText={errors.client_id}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {loading.clients ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <MenuItem {...props} key={option.id}>
                  <div>
                    <div><strong>{option.nif}</strong></div>
                    <div>{option.name}</div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>{option.address}</div>
                  </div>
                </MenuItem>
              )}
            />
            {formData.client_id && (
              <Box sx={{ 
                mt: 1, 
                p: 2, 
                border: '1px solid #eee', 
                borderRadius: 1,
                backgroundColor: '#f9f9f9'
              }}>
                <Typography variant="subtitle2" gutterBottom>
                  Información del Cliente
                </Typography>
                <Typography variant="body2">
                  <strong>Nombre:</strong> {formData.client_name}
                </Typography>
                <Typography variant="body2">
                  <strong>Dirección:</strong> {formData.client_address}
                </Typography>
                <Typography variant="body2">
                  <strong>NIF:</strong> {formData.client_tax_id}
                </Typography>
              </Box>
            )}
          </Grid>

          {/* Location Info */}
          <Grid item xs={12} md={6}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  select
                  label="País"
                  fullWidth
                  value={formData.country}
                  onChange={handleCountryChange}
                >
                  {countries.map((country) => (
                    <MenuItem key={country.id} value={country.id}>
                      {country.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={6}>
                <TextField
                  select
                  label="Provincia"
                  fullWidth
                  value={formData.province}
                  onChange={(e) => setFormData(prev => ({ ...prev, province: e.target.value }))}
                  disabled={!formData.country}
                >
                  {provinces.map((province) => (
                    <MenuItem key={province.id} value={province.id}>
                      {province.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>
          </Grid>

          {/* Notes */}
          <Grid item xs={12}>
            <TextField
              label="Notas"
              fullWidth
              multiline
              rows={2}
              value={formData.notes}
              onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
            />
          </Grid>

          {/* Product Table */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Productos/Servicios</Typography>
              <Button
                variant="contained"
                onClick={() => setProductDialogOpen(true)}
              >
                Añadir Producto
              </Button>
            </Box>
            
            {errors.items && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {errors.items}
              </Alert>
            )}
            
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Código</TableCell>
                    <TableCell>Descripción</TableCell>
                    <TableCell align="right">Cantidad</TableCell>
                    <TableCell>Unidad</TableCell>
                    <TableCell align="right">P. Unitario</TableCell>
                    <TableCell align="right">Descuento (%)</TableCell>
                    <TableCell align="right">IVA (%)</TableCell>
                    <TableCell align="right">Total</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {invoiceItems.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item.product_code}</TableCell>
                      <TableCell>{item.description}</TableCell>
                      <TableCell align="right">{item.quantity}</TableCell>
                      <TableCell>{item.unit_of_measure}</TableCell>
                      <TableCell align="right">{parseFloat(item.unit_price).toFixed(2)}</TableCell>
                      <TableCell align="right">{item.discount}</TableCell>
                      <TableCell align="right">{item.tax}</TableCell>
                      <TableCell align="right">
                        {item.total.toLocaleString('es-ES', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>

          {/* Totals Section */}
          <Grid item xs={12} md={6}>
            <Box sx={{ 
              p: 3, 
              border: '1px solid #eee', 
              borderRadius: 1,
              backgroundColor: '#f9f9f9'
            }}>
              <Typography variant="h6" gutterBottom>
                Resumen de Factura
              </Typography>
              <Grid container spacing={1}>
                <Grid item xs={6}>
                  <Typography>Subtotal:</Typography>
                </Grid>
                <Grid item xs={6} textAlign="right">
                  <Typography>
                    {totals.subtotal.toLocaleString('es-ES', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </Typography>
                </Grid>

                <Grid item xs={6}>
                  <Typography>Descuentos:</Typography>
                </Grid>
                <Grid item xs={6} textAlign="right">
                  <Typography>
                    {(-totals.totalDiscounts).toLocaleString('es-ES', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </Typography>
                </Grid>

                <Grid item xs={6}>
                  <Typography>Impuestos:</Typography>
                </Grid>
                <Grid item xs={6} textAlign="right">
                  <Typography>
                    {totals.totalTaxes.toLocaleString('es-ES', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </Typography>
                </Grid>

                <Grid item xs={6}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    Total:
                  </Typography>
                </Grid>
                <Grid item xs={6} textAlign="right">
                  <Typography variant="subtitle1" fontWeight="bold">
                    {totals.grandTotal.toLocaleString('es-ES', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          </Grid>

          {/* Form Actions */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button
                type="button"
                variant="outlined"
                onClick={() => {
                  setInvoiceItems([]);
                  setTotals({
                    subtotal: 0,
                    totalTaxes: 0,
                    totalDiscounts: 0,
                    grandTotal: 0,
                  });
                }}
              >
                Limpiar Productos
              </Button>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
              >
                Guardar Factura
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>

      {/* Add Product Dialog */}
      <Dialog open={productDialogOpen} onClose={() => setProductDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Añadir Producto/Servicio</DialogTitle>
        <DialogContent>
          {errors.product && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {errors.product}
            </Alert>
          )}
          
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <Autocomplete
                options={filteredProducts}
                getOptionLabel={(option) => `${option.sku} - ${option.name}`}
                onInputChange={(event, newInputValue) => {
                  filterProducts(newInputValue);
                }}
                onChange={handleProductSelect}
                loading={loading.searchProducts}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Buscar Producto por Código o Nombre"
                    fullWidth
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {loading.searchProducts ? <CircularProgress color="inherit" size={20} /> : null}
                          {params.InputProps.endAdornment}
                        </>
                      ),
                    }}
                  />
                )}
                renderOption={(props, option) => (
                  <MenuItem {...props} key={option.id}>
                    <div>
                      <div><strong>{option.sku}</strong></div>
                      <div>{option.name}</div>
                      <div style={{ fontSize: '0.8rem', color: '#666' }}>
                        Precio: {option.price.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })} | 
                        Stock: {option.stock} | 
                        Unidad: {option.unit}
                      </div>
                    </div>
                  </MenuItem>
                )}
              />
            </Grid>

            {productFormData.product_code && (
              <Grid item xs={12}>
                <Box sx={{ 
                  p: 2, 
                  border: '1px solid #eee', 
                  borderRadius: 1,
                  backgroundColor: '#f9f9f9'
                }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Información del Producto Seleccionado
                  </Typography>
                  <Grid container spacing={1}>
                    <Grid item xs={4}>
                      <Typography variant="body2">
                        <strong>Código:</strong> {productFormData.product_code}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2">
                        <strong>Precio:</strong> {productFormData.unit_price} €
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2">
                        <strong>Unidad:</strong> {productFormData.unit_of_measure}
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="body2">
                        <strong>Descripción:</strong> {productFormData.description}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </Grid>
            )}

            <Grid item xs={6} sm={4}>
              <TextField
                label="Cantidad"
                type="number"
                fullWidth
                value={productFormData.quantity}
                onChange={(e) => setProductFormData(prev => ({ ...prev, quantity: e.target.value }))}
                inputProps={{ min: "0", step: "1" }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <TextField
                label="Descuento (%)"
                type="number"
                fullWidth
                value={productFormData.discount}
                onChange={(e) => setProductFormData(prev => ({ ...prev, discount: e.target.value }))}
                inputProps={{ min: "0", max: "100", step: "1" }}
              />
            </Grid>
            <Grid item xs={6} sm={4}>
              <TextField
                label="IVA (%)"
                select
                fullWidth
                value={productFormData.tax}
                onChange={(e) => setProductFormData(prev => ({ ...prev, tax: e.target.value }))}
              >
                {taxTypes.map((tax) => (
                  <MenuItem key={tax.id} value={tax.rate}>
                    {tax.name} ({tax.rate}%)
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setProductDialogOpen(false);
            setErrors(prev => ({ ...prev, product: '' }));
          }}>Cancelar</Button>
          <Button onClick={handleAddProduct} color="primary" variant="contained">
            Añadir a Factura
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default NovaFatura;