// types.ts
export interface ProductFormType {
    sku: string;
    name: string;
    description: string;
    price: number;
    unit: string;
    category: string;
    expiration_date?: string;
    image_url?: string;
    attributes?: Record<string, unknown>;
    stock: number;
    location?: string;
  }
  
  export interface ProductFormErrors {
    sku?: string;
    name?: string;
    description?: string;
    price?: string;
    unit?: string;
    category?: string;
    stock?: string;
    location?: string;
    // ... otros campos de error
  }