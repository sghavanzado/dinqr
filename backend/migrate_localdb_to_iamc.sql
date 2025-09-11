-- Migration script to add localdb tables and data to IAMC database (SQL Server)
-- Execute this script on the IAMC database

-- Create tables if they don't exist

-- 1. Alembic version table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='alembic_version' AND xtype='U')
CREATE TABLE alembic_version (
    version_num NVARCHAR(32) NOT NULL,
    CONSTRAINT PK_alembic_version PRIMARY KEY (version_num)
);

-- 2. Permission table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='permission' AND xtype='U')
CREATE TABLE permission (
    id INT IDENTITY(1,1) NOT NULL,
    name NVARCHAR(64) NOT NULL,
    description NVARCHAR(256),
    CONSTRAINT PK_permission PRIMARY KEY (id),
    CONSTRAINT UQ_permission_name UNIQUE (name)
);

-- 3. Role table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='role' AND xtype='U')
CREATE TABLE [role] (
    id INT IDENTITY(1,1) NOT NULL,
    name NVARCHAR(64) NOT NULL,
    description NVARCHAR(256),
    CONSTRAINT PK_role PRIMARY KEY (id),
    CONSTRAINT UQ_role_name UNIQUE (name)
);

-- 4. Roles permissions junction table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='roles_permissions' AND xtype='U')
CREATE TABLE roles_permissions (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    CONSTRAINT PK_roles_permissions PRIMARY KEY (role_id, permission_id),
    CONSTRAINT FK_roles_permissions_permission FOREIGN KEY (permission_id) REFERENCES permission(id),
    CONSTRAINT FK_roles_permissions_role FOREIGN KEY (role_id) REFERENCES [role](id)
);

-- 5. User table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user' AND xtype='U')
CREATE TABLE [user] (
    id INT IDENTITY(1,1) NOT NULL,
    username NVARCHAR(64),
    email NVARCHAR(120) NOT NULL,
    password_hash NVARCHAR(512) NOT NULL,
    role_id INT NOT NULL,
    is_active BIT DEFAULT 1,
    name NVARCHAR(64) NOT NULL,
    second_name NVARCHAR(64),
    last_name NVARCHAR(64) NOT NULL,
    phone_number NVARCHAR(20),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    last_login DATETIME2,
    login_attempts INT DEFAULT 0,
    locked_until DATETIME2,
    CONSTRAINT PK_user PRIMARY KEY (id),
    CONSTRAINT FK_user_role FOREIGN KEY (role_id) REFERENCES [role](id),
    CONSTRAINT UQ_user_email UNIQUE (email),
    CONSTRAINT UQ_user_username UNIQUE (username)
);

-- 6. Audit log table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audit_log' AND xtype='U')
CREATE TABLE audit_log (
    id INT IDENTITY(1,1) NOT NULL,
    user_id INT NOT NULL,
    action NVARCHAR(64) NOT NULL,
    target_type NVARCHAR(64) NOT NULL,
    target_id INT NOT NULL,
    [timestamp] DATETIME2 NOT NULL DEFAULT GETDATE(),
    ip_address NVARCHAR(45),
    details NVARCHAR(MAX), -- Using NVARCHAR(MAX) instead of JSON for SQL Server compatibility
    CONSTRAINT PK_audit_log PRIMARY KEY (id),
    CONSTRAINT FK_audit_log_user FOREIGN KEY (user_id) REFERENCES [user](id)
);

-- 7. QR codes table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='qr_codes' AND xtype='U')
CREATE TABLE qr_codes (
    id INT IDENTITY(1,1) NOT NULL,
    contact_id NVARCHAR(50) NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    archivo_qr NVARCHAR(255) NOT NULL,
    firma NVARCHAR(64) NOT NULL,
    CONSTRAINT PK_qr_codes PRIMARY KEY (id),
    CONSTRAINT UQ_qr_codes_contact_id UNIQUE (contact_id)
);

-- 8. Settings table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='settings' AND xtype='U')
CREATE TABLE settings (
    id INT IDENTITY(1,1) NOT NULL,
    [key] NVARCHAR(100) NOT NULL,
    value NVARCHAR(MAX) NOT NULL,
    CONSTRAINT PK_settings PRIMARY KEY (id),
    CONSTRAINT UQ_settings_key UNIQUE ([key])
);

-- Insert data (using MERGE or IF NOT EXISTS to avoid duplicates)

-- Insert alembic version
IF NOT EXISTS (SELECT 1 FROM alembic_version WHERE version_num = '12b248eebe64')
    INSERT INTO alembic_version (version_num) VALUES ('12b248eebe64');

-- Insert permissions
SET IDENTITY_INSERT permission ON;

IF NOT EXISTS (SELECT 1 FROM permission WHERE name = 'admin_access')
    INSERT INTO permission (id, name, description) VALUES (1, 'admin_access', 'Acceso completo al sistema');

IF NOT EXISTS (SELECT 1 FROM permission WHERE name = 'create_user')
    INSERT INTO permission (id, name, description) VALUES (2, 'create_user', 'Crear nuevos usuarios');

IF NOT EXISTS (SELECT 1 FROM permission WHERE name = 'update_user')
    INSERT INTO permission (id, name, description) VALUES (3, 'update_user', 'Modificar usuarios existentes');

IF NOT EXISTS (SELECT 1 FROM permission WHERE name = 'delete_user')
    INSERT INTO permission (id, name, description) VALUES (4, 'delete_user', 'Eliminar usuarios');

IF NOT EXISTS (SELECT 1 FROM permission WHERE name = 'view_audit_logs')
    INSERT INTO permission (id, name, description) VALUES (5, 'view_audit_logs', 'Ver registros de auditoría');

SET IDENTITY_INSERT permission OFF;

-- Reseed permission identity
DECLARE @max_permission_id INT;
SELECT @max_permission_id = ISNULL(MAX(id), 0) FROM permission;
DBCC CHECKIDENT ('permission', RESEED, @max_permission_id);

-- Insert roles
SET IDENTITY_INSERT [role] ON;

IF NOT EXISTS (SELECT 1 FROM [role] WHERE name = 'admin')
    INSERT INTO [role] (id, name, description) VALUES (1, 'admin', 'Administrador del sistema');

IF NOT EXISTS (SELECT 1 FROM [role] WHERE name = 'user')
    INSERT INTO [role] (id, name, description) VALUES (2, 'user', 'Usuario estándar');

SET IDENTITY_INSERT [role] OFF;

-- Reseed role identity
DECLARE @max_role_id INT;
SELECT @max_role_id = ISNULL(MAX(id), 0) FROM [role];
DBCC CHECKIDENT ('[role]', RESEED, @max_role_id);

-- Insert roles_permissions
IF NOT EXISTS (SELECT 1 FROM roles_permissions WHERE role_id = 1 AND permission_id = 1)
    INSERT INTO roles_permissions (role_id, permission_id) VALUES (1, 1);
IF NOT EXISTS (SELECT 1 FROM roles_permissions WHERE role_id = 1 AND permission_id = 2)
    INSERT INTO roles_permissions (role_id, permission_id) VALUES (1, 2);
IF NOT EXISTS (SELECT 1 FROM roles_permissions WHERE role_id = 1 AND permission_id = 3)
    INSERT INTO roles_permissions (role_id, permission_id) VALUES (1, 3);
IF NOT EXISTS (SELECT 1 FROM roles_permissions WHERE role_id = 1 AND permission_id = 4)
    INSERT INTO roles_permissions (role_id, permission_id) VALUES (1, 4);
IF NOT EXISTS (SELECT 1 FROM roles_permissions WHERE role_id = 1 AND permission_id = 5)
    INSERT INTO roles_permissions (role_id, permission_id) VALUES (1, 5);

-- Insert users
SET IDENTITY_INSERT [user] ON;

IF NOT EXISTS (SELECT 1 FROM [user] WHERE email = 'maikel@ejemplos.com')
    INSERT INTO [user] (id, username, email, password_hash, role_id, is_active, name, second_name, last_name, phone_number, created_at, updated_at, last_login, login_attempts, locked_until) 
    VALUES (1, 'maikel', 'maikel@ejemplos.com', 'scrypt:32768:8:1$B8TqSC7Desj94YPn$1af3b000a644f0829c16f187aca205d4d5047b5ad66688dd2f576c80558c447ca95ea2800fe424506f898d71d0b36f1a65877d4b633801acb594e7969ef69b06', 1, 1, 'Maikel', 'Cuao', 'Murillo', '922831026', '2025-04-10 09:57:32.170', '2025-04-10 09:57:32.170', NULL, 0, NULL);

SET IDENTITY_INSERT [user] OFF;

-- Reseed user identity
DECLARE @max_user_id INT;
SELECT @max_user_id = ISNULL(MAX(id), 0) FROM [user];
DBCC CHECKIDENT ('[user]', RESEED, @max_user_id);

-- Insert settings
SET IDENTITY_INSERT settings ON;

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'server')
    INSERT INTO settings (id, [key], value) VALUES (1, 'server', '192.168.253.5');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'username')
    INSERT INTO settings (id, [key], value) VALUES (2, 'username', 'sa');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'password')
    INSERT INTO settings (id, [key], value) VALUES (3, 'password', 'Global2020');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'database')
    INSERT INTO settings (id, [key], value) VALUES (4, 'database', 'externaldb');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'outputFolder')
    INSERT INTO settings (id, [key], value) VALUES (5, 'outputFolder', 'C:\Users\maikel.GTS\Pictures\Salida');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'serverDomain')
    INSERT INTO settings (id, [key], value) VALUES (6, 'serverDomain', '192.168.253.5');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'serverPort')
    INSERT INTO settings (id, [key], value) VALUES (7, 'serverPort', '443');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'qrdomain')
    INSERT INTO settings (id, [key], value) VALUES (8, 'qrdomain', '192.168.253.5');

IF NOT EXISTS (SELECT 1 FROM settings WHERE [key] = 'tabela')
    INSERT INTO settings (id, [key], value) VALUES (9, 'tabela', 'sonacard');

SET IDENTITY_INSERT settings OFF;

-- Reseed settings identity
DECLARE @max_settings_id INT;
SELECT @max_settings_id = ISNULL(MAX(id), 0) FROM settings;
DBCC CHECKIDENT ('settings', RESEED, @max_settings_id);
