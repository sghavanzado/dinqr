# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Obtener la ruta del directorio actual
block_cipher = None
current_dir = os.path.dirname(os.path.abspath(SPEC))

# Datos adicionales que necesita la aplicación
datas = []

# Incluir templates y archivos estáticos
datas += [(os.path.join(current_dir, 'static'), 'static')]
datas += [(os.path.join(current_dir, 'migrations'), 'migrations')]
datas += [(os.path.join(current_dir, 'data'), 'data')]

# Incluir archivos de configuración
config_files = [
    'config.py',
    'extensions.py',
    'windows_service.py',
    'waitress_server.py'
]

for config_file in config_files:
    if os.path.exists(os.path.join(current_dir, config_file)):
        datas += [(os.path.join(current_dir, config_file), '.')]

# Módulos ocultos que PyInstaller podría no detectar automáticamente
hiddenimports = [
    'flask',
    'flask_cors',
    'flask_jwt_extended',
    'flask_limiter',
    'flask_talisman',
    'flask_migrate',
    'flask_sqlalchemy',
    'flasgger',
    'waitress',
    'sqlalchemy',
    'psycopg2',
    'pyodbc',
    'qrcode',
    'PIL',
    'PIL.Image',
    'dotenv',
    'logging.handlers',
    'uuid',
    'pathlib',
    'alembic',
    'alembic.config',
    'routes.auth_routes',
    'routes.user_routes',
    'routes.qr_routes',
    'routes.settings_routes',
    'routes.health_check',
    'routes.route_qrdata',
    'models.user',
    'models.qrdata',
    'models.settings',
    'services.qr_service',
    'utils.api_helpers',
    'utils.db_utils',
    'utils.decorators',
    # Configuration modules
    'config',
    # Windows Service modules
    'win32service',
    'win32serviceutil',
    'win32event',
    'win32api',
    'win32con',
    'servicemanager',
    'pywintypes',
    'pythoncom',
    'win32timezone',
    'win32security',
    'win32process',
    'win32gui',
    'win32clipboard',
    'win32pipe',
    'win32file',
    'win32evtlog',
    'win32evtlogutil',
    'windows_service',
    'waitress_server',
    # Threading modules for waitress_server
    'threading',
    'time',
    # Additional Windows modules for admin verification
    'ctypes',
    'winreg',
    'win32security',
]

# Recopilar submódulos de Flask y SQLAlchemy
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('sqlalchemy')
hiddenimports += collect_submodules('alembic')
hiddenimports += collect_submodules('waitress')

# Recopilar submódulos de pywin32 específicamente
try:
    hiddenimports += collect_submodules('win32serviceutil')
    hiddenimports += collect_submodules('win32service')
    hiddenimports += collect_submodules('pywintypes')
    hiddenimports += collect_submodules('pythoncom')
except:
    print("Warning: Could not collect pywin32 submodules")

# Datos de pywin32 si están disponibles
try:
    datas += collect_data_files('pywintypes')
    datas += collect_data_files('pythoncom')
except:
    print("Warning: Could not collect pywin32 data files")

# Datos de paquetes
datas += collect_data_files('flask')
datas += collect_data_files('flasgger')
datas += collect_data_files('alembic')

# Buscar y incluir DLLs de pywin32
import site
pywin32_binaries = []
try:
    for site_pkg in site.getsitepackages():
        pywin32_dll_path = os.path.join(site_pkg, 'pywin32_system32')
        if os.path.exists(pywin32_dll_path):
            for dll_file in os.listdir(pywin32_dll_path):
                if dll_file.endswith('.dll'):
                    pywin32_binaries.append((os.path.join(pywin32_dll_path, dll_file), '.'))
            break
    print(f"Found {len(pywin32_binaries)} pywin32 DLL files")
except Exception as e:
    print(f"Warning: Could not find pywin32 DLLs: {e}")

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=pywin32_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='generadorqr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
