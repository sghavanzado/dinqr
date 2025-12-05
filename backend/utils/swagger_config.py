"""
SIGA - Sistema Integral de Gestión de Accesos
Configuración mejorada de Swagger/OpenAPI

Desarrollado por: Ing. Maikel Cuao
Fecha: 2025
Descripción: Configuración completa de Swagger con documentación detallada, esquemas y autenticación JWT.
"""

from flasgger import Swagger


def configure_swagger(app):
    """
    Configura Swagger/OpenAPI con documentación completa de la API.
    
    Args:
        app: Instancia de Flask
    
    Returns:
        Swagger: Instancia configurada de Swagger
    """
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SIGA - API Sistema Integral de Gestión de Accesos",
            "description": """
API REST para el Sistema Integral de Gestión de Accesos (SIGA).

Permite gestionar:
- Usuarios y autenticación
- Roles y permisos (RBAC)
- Prestadores de servicios
- Generación de códigos QR
- Historial y auditoría

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación.  Para acceder a endpoints protegidos:

1. Obtener token via `/auth/login`
2. Incluir el token en el header: `Authorization: Bearer <token>`

## Rate Limiting

La API tiene límites de tasa de 500 peticiones por hora por IP.

## Contacto

**Desarrollador**: Ing. Maikel Cuao  
**Email**: maikel@hotmail.com
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Ing. Maikel Cuao",
                "email": "maikel@hotmail.com"
            },
            "license": {
                "name": "Proprietary",
                "url": ""
            }
        },
        "host": app.config.get("API_HOST", "localhost:5000"),
        "basePath": "/",
        "schemes": [
            "https" if app.config.get("ENABLE_HTTPS") else "http"
        ],
        "tags": [
            {
                "name": "Autenticación",
                "description": "Endpoints para login, registro y gestión de tokens"
            },
            {
                "name": "Usuarios",
                "description": "CRUD de usuarios del sistema"
            },
            {
                "name": "Roles y Permisos",
                "description": "Gestión de roles y permisos (RBAC)"
            },
            {
                "name": "Códigos QR",
                "description": "Generación, descarga y gestión de códigos QR"
            },
            {
                "name": "Prestadores",
                "description": "Gestión de prestadores de servicios"
            },
            {
                "name": "Configuración",
                "description": "Configuración del sistema y parámetros"
            },
            {
                "name": "Salud",
                "description": "Health checks y estado del sistema"
            }
        ],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "username": {"type": "string", "example": "jdoe"},
                    "email": {"type": "string", "example": "jdoe@example.com"},
                    "name": {"type": "string", "example": "John"},
                    "last_name": {"type": "string", "example": "Doe"},
                    "role_id": {"type": "integer", "example": 1},
                    "is_active": {"type": "boolean", "example": True},
                    "created_at": {"type": "string", "format": "date-time"},
                    "last_login": {"type": "string", "format": "date-time"}
                }
            },
            "Role": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "admin"},
                    "description": {"type": "string", "example": "Administrador del sistema"}
                }
            },
            "Permission": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "name": {"type": "string", "example": "admin_access"},
                    "description": {"type": "string", "example": "Acceso completo al sistema"}
                }
            },
            "Prestador": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "nome": {"type": "string"},
                    "nacionalidade": {"type": "string"},
                    "bi_pass": {"type": "string"},
                    "telefono": {"type": "string"},
                    "email": {"type": "string"},
                    "empresa_id": {"type": "integer"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "Mensaje de error"},
                    "details": {"type": "string", "description": "Detalles adicionales"},
                    "request_id": {"type": "string", "description": "ID único de la petición"}
                }
            },
            "LoginRequest": {
                "type": "object",
                "required": ["email", "password"],
                "properties": {
                    "email": {"type": "string", "example": "admin@siga.com"},
                    "password": {"type": "string", "example": "password123"}
                }
            },
            "LoginResponse": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "refresh_token": {"type": "string"},
                    "user": {"$ref": "#/definitions/User"}
                }
            }
        },
        "responses": {
            "UnauthorizedError": {
                "description": "Token de autenticación faltante o inválido",
                "schema": {
                    "$ref": "#/definitions/Error"
                }
            },
            "ForbiddenError": {
                "description": "Acceso denegado - permisos insuficientes",
                "schema": {
                    "$ref": "#/definitions/Error"
                }
            },
            "NotFoundError": {
                "description": "Recurso no encontrado",
                "schema": {
                    "$ref": "#/definitions/Error"
                }
            },
            "ValidationError": {
                "description": "Error de validación de datos",
                "schema": {
                    "$ref": "#/definitions/Error"
                }
            }
        }
    }
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs",  # Nueva ruta más clara
        "title": "SIGA API Documentation"
    }
    
    # Swagger UI configuration
    swagger_config["ui_params"] = {
        "docExpansion": "list",  # 'none', 'list', 'full'
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "displayOperationId": False
    }
    
    return Swagger(app, template=swagger_template, config=swagger_config)


# Ejemplos de documentación para endpoints (para usar en las rutas)

auth_login_spec = {
    "tags": ["Autenticación"],
    "summary": "Iniciar sesión",
    "description": "Autenticar usuario y obtener tokens JWT",
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "description": "Credenciales de usuario",
            "required": True,
            "schema": {
                "$ref": "#/definitions/LoginRequest"
            }
        }
    ],
    "responses": {
        200: {
            "description": "Login exitoso",
            "schema": {
                "$ref": "#/definitions/LoginResponse"
            }
        },
        401: {
            "description": "Credenciales inválidas",
            "schema": {
                "$ref": "#/definitions/Error"
            }
        }
    }
}

qr_generate_spec = {
    "tags": ["Códigos QR"],
    "summary": "Generar códigos QR",
    "description": "Genera códigos QR para los funcionarios especificados",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["ids"],
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "example": [1, 2, 3]
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "QR codes generados exitosamente",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "qr_generated": {"type": "boolean"},
                        "message": {"type": "string"}
                    }
                }
            }
        },
        401: {"$ref": "#/responses/UnauthorizedError"},
        403: {"$ref": "#/responses/ForbiddenError"},
        400: {"$ref": "#/responses/ValidationError"}
    }
}

users_list_spec = {
    "tags": ["Usuarios"],
    "summary": "Listar usuarios",
    "description": "Obtiene lista de usuarios del sistema con paginación",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "default": 1,
            "description": "Número de página"
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "default": 10,
            "description": "Resultados por página"
        }
    ],
    "responses": {
        200: {
            "description": "Lista de usuarios",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/User"}
            }
        },
        401: {"$ref": "#/responses/UnauthorizedError"},
        403: {"$ref": "#/responses/ForbiddenError"}
    }
}
