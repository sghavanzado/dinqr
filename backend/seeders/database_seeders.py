"""
SIGA - Sistema Integral de Gestión de Accesos
Database Seeders - Datos de Prueba

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Seeders para popular la base de datos con datos de prueba.
"""

from extensions import db
from models.user import User, Role, Permission
from models.prestadores import Prestador, Empresa, Local, Historial, CentroNeg, Function, TipoService, LocalService, AreaService
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


class BaseSeeder:
    """Clase base para todos los seeders"""
    
    @staticmethod
    def clear_table(model):
        """Elimina todos los registros de una tabla"""
        try:
            db.session.query(model).delete()
            db.session.commit()
            logger.info(f"✓ Tabla {model.__tablename__} limpiada")
        except Exception as e:
            db.session.rollback()
            logger.error(f"✗ Error limpiando tabla {model.__tablename__}: {e}")
            raise


class RolePermissionSeeder(BaseSeeder):
    """Seeder para roles y permisos"""
    
    @staticmethod
    def run(clear_existing=False):
        """
        Crea roles y permisos en la base de datos.
        
        Args:
            clear_existing: Si True, elimina datos existentes antes de sembrar
        """
        logger.info("=== Iniciando RolePermissionSeeder ===")
        
        if clear_existing:
            BaseSeeder.clear_table(Permission)
            BaseSeeder.clear_table(Role)
        
        # Crear permisos
        permissions_data = [
            ('admin_access', 'Acceso completo al sistema'),
            ('create_user', 'Crear nuevos usuarios'),
            ('update_user', 'Modificar usuarios existentes'),
            ('delete_user', 'Eliminar usuarios'),
            ('view_audit_logs', 'Ver registros de auditoría'),
            ('generate_qr', 'Generar códigos QR'),
            ('delete_qr', 'Eliminar códigos QR'),
            ('view_prestadores', 'Ver prestadores'),
            ('create_prestadores', 'Crear prestadores'),
            ('update_prestadores', 'Actualizar prestadores'),
            ('delete_prestadores', 'Eliminar prestadores'),
        ]
        
        permissions = {}
        for name, desc in permissions_data:
            perm = Permission.query.filter_by(name=name).first()
            if not perm:
                perm = Permission(name=name, description=desc)
                db.session.add(perm)
                logger.info(f"  + Permiso creado: {name}")
            permissions[name] = perm
        
        db.session.commit()
        
        # Crear roles
        roles_data = [
            ('admin', 'Administrador del sistema', [
                'admin_access', 'create_user', 'update_user', 'delete_user',
                'view_audit_logs', 'generate_qr', 'delete_qr', 'view_prestadores',
                'create_prestadores', 'update_prestadores', 'delete_prestadores'
            ]),
            ('operator', 'Operador de sistema', [
                'generate_qr', 'view_prestadores', 'create_prestadores', 'update_prestadores'
            ]),
            ('viewer', 'Usuario de solo lectura', [
                'view_prestadores'
            ]),
            ('user', 'Usuario estándar', [
                'view_prestadores'
            ]),
        ]
        
        for role_name, desc, perm_names in roles_data:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=desc)
                # Asignar permisos al rol
                role.permissions = [permissions[p] for p in perm_names if p in permissions]
                db.session.add(role)
                logger.info(f"  + Rol creado: {role_name} con {len(perm_names)} permisos")
        
        db.session.commit()
        logger.info("=== RolePermissionSeeder completado ===\n")


class UserSeeder(BaseSeeder):
    """Seeder para usuarios de prueba"""
    
    @staticmethod
    def run(count=10, clear_existing=False):
        """
        Crea usuarios de prueba.
        
        Args:
            count: Número de usuarios a crear
            clear_existing: Si True, elimina usuarios existentes
        """
        logger.info(f"===Iniciando UserSeeder ({count} usuarios) ===")
        
        if clear_existing:
            # NO eliminar todos los usuarios, solo los de prueba
            User.query.filter(User.email.like('%@test.com')).delete()
            db.session.commit()
        
        # Obtener roles
        admin_role = Role.query.filter_by(name='admin').first()
        operator_role = Role.query.filter_by(name='operator').first()
        viewer_role = Role.query.filter_by(name='viewer').first()
        user_role = Role.query.filter_by(name='user').first()
        
        if not all([admin_role, operator_role, viewer_role, user_role]):
            logger.error("  ✗ Roles no encontrados. Ejecute RolePermissionSeeder primero.")
            return
        
        # Crear usuario admin principal (si no existe)
        admin = User.query.filter_by(email='admin@siga.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@siga.com',
                name='Administrador',
                last_name='Sistema',
                role=admin_role,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            logger.info(f"  + Usuario admin creado: admin@siga.com / admin123")
        
        # Crear usuarios de prueba
        first_names = ['Juan', 'María', 'Pedro', 'Ana', 'Carlos', 'Lucía', 'Miguel', 'Elena', 'José', 'Laura']
        last_names = ['García', 'Rodríguez', 'Martínez', 'López', 'Sánchez', 'Pérez', 'Gómez', 'Fernández', 'Díaz', 'Torres']
        
        for i in range(count):
            first = random.choice(first_names)
            last = random.choice(last_names)
            username = f"{first.lower()}.{last.lower()}{i}"
            email = f"{username}@test.com"
            
            # Asignar rol aleatorio
            role = random.choice([admin_role, operator_role, viewer_role, user_role])
            
            user = User(
                username=username,
                email=email,
                name=first,
                last_name=last,
                role=role,
                is_active=random.choice([True, True, True, False]),  # 75% activos
                phone_number=f"+244 9{random.randint(10000000, 99999999)}"
            )
            user.set_password('test123')
            db.session.add(user)
            logger.info(f"  + Usuario creado: {email} ({role.name})")
        
        db.session.commit()
        logger.info("=== UserSeeder completado ===\n")


class PrestadorSeeder(BaseSeeder):
    """Seeder para prestadores y empresas"""
    
    @staticmethod
    def run(count_empresas=5, count_prestadores=20, clear_existing=False):
        """
        Crea prestadores, empresas y datos relacionados.
        
        Args:
            count_empresas: Número de empresas a crear
            count_prestadores: Número de prestadores a crear
            clear_existing: Si True, elimina datos existentes
        """
        logger.info(f"=== Iniciando PrestadorSeeder ===")
        
        if clear_existing:
            BaseSeeder.clear_table(Historial)
            BaseSeeder.clear_table(Prestador)
            BaseSeeder.clear_table(Empresa)
            BaseSeeder.clear_table(Local)
            BaseSeeder.clear_table(CentroNeg)
            BaseSeeder.clear_table(Function)
            BaseSeeder.clear_table(TipoService)
            BaseSeeder.clear_table(LocalService)
            BaseSeeder.clear_table(AreaService)
        
        # Crear locales
        locales_data = ['Luanda', 'Benguela', 'Huambo', 'Lobito', 'Cabinda']
        locales = []
        for nome in locales_data:
            local = Local(nome=nome)
            db.session.add(local)
            locales.append(local)
        db.session.commit()
        logger.info(f"  + {len(locales)} locales creados")
        
        # Crear empresas
        empresas_data = [
            ('Sonangol EP', '+244 222 000 100', 'contacto@sonangol.co.ao'),
            ('Total E&P Angola', '+244 222 000 200', 'info@total.co.ao'),
            ('Chevron Angola', '+244 222 000 300', 'contact@chevron.co.ao'),
            ('ENI Angola', '+244 222 000 400', 'info@eni.co.ao'),
            ('BP Angola', '+244 222 000 500', 'contact@bp.co.ao'),
        ]
        empresas = []
        for i in range(count_empresas):
            nome, tel, email = empresas_data[i % len(empresas_data)]
            empresa = Empresa(
                nome=f"{nome} {i+1}" if i >= len(empresas_data) else nome,
                telefono=tel,
                email=email,
                obs=f"Empresa de prueba {i+1}"
            )
            db.session.add(empresa)
            empresas.append(empresa)
        db.session.commit()
        logger.info(f"  + {len(empresas)} empresas creadas")
        
        # Crear centros de negocio
        centros_data = ['Exploración', 'Producción', 'Refinación', 'Distribución', 'Administrativo']
        centros = []
        for nome in centros_data:
            centro = CentroNeg(nome=nome)
            db.session.add(centro)
            centros.append(centro)
        db.session.commit()
        
        # Crear funciones/cargos
        funcoes_data = ['Ingeniero', 'Técnico', 'Operador', 'Supervisor', 'Gerente']
        funcoes = []
        for nome in funcoes_data:
            func = Function(nome=nome)
            db.session.add(func)
            funcoes.append(func)
        db.session.commit()
        
        # Crear tipos de servicio
        tipos_data = ['Mantenimiento', 'Seguridad', 'Limpieza', 'Transporte', 'Consultoría']
        tipos = []
        for nome in tipos_data:
            tipo = TipoService(nome=nome)
            db.session.add(tipo)
            tipos.append(tipo)
        db.session.commit()
        
        # Crear locales de servicio
        locales_serv_data = ['Sede Central', 'Oficina Regional', 'Base Operativa', 'Almacén', 'Campo']
        locales_serv = []
        for nome in locales_serv_data:
            local_serv = LocalService(nome=nome)
            db.session.add(local_serv)
            locales_serv.append(local_serv)
        db.session.commit()
        
        # Crear áreas de servicio
        areas_data = ['Administración', 'Operaciones', 'Logística', 'RRHH', 'IT']
        areas = []
        for nome in areas_data:
            area = AreaService(nome=nome)
            db.session.add(area)
            areas.append(area)
        db.session.commit()
        
        logger.info(f"  + Datos auxiliares creados")
        
        # Crear prestadores
        first_names = ['António', 'João', 'Manuel', 'Francisco', 'José', 'Paulo', 'Carlos', 'Fernando', 'Pedro', 'Miguel']
        last_names = ['Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa']
        
        for i in range(count_prestadores):
            nome = f"{random.choice(first_names)} {random.choice(last_names)}"
            prestador = Prestador(
                nome=nome,
                filiacao=f"Pai de {nome.split()[0]}",
                data_nas=datetime.now().date() - timedelta(days=random.randint(7300, 18250)),  # 20-50 años
                local=random.choice(locales),
                nacionalidade='Angolana',
                bi_pass=f"{random.randint(100000000, 999999999)}BA{random.randint(10, 99)}",
                emissao=datetime.now().date() - timedelta(days=random.randint(30, 1095)),
                validade=datetime.now().date() + timedelta(days=random.randint(30, 1095)),
                local_resid=random.choice(locales_data),
                telefono=f"+244 9{random.randint(10000000, 99999999)}",
                email=f"{nome.replace(' ', '.').lower()}@empresa.co.ao",
                lock=False,
                obs=f"Prestador  de prueba {i+1}",
                empresa=random.choice(empresas)
            )
            db.session.add(prestador)
        
        db.session.commit()
        logger.info(f"  + {count_prestadores} prestadores creados")
        
        logger.info("=== PrestadorSeeder completado ===\n")


def run_all_seeders(clear_existing=False):
    """
    Ejecuta todos los seeders en orden.
    
    Args:
        clear_existing: Si True, limpia datos existentes antes de sembrar
    """
    logger.info("\n" + "="*50)
    logger.info("EJECUTANDO TODOS LOS SEEDERS")
    logger.info("="*50 + "\n")
    
    try:
        RolePermissionSeeder.run(clear_existing=clear_existing)
        UserSeeder.run(count=10, clear_existing=clear_existing)
        PrestadorSeeder.run(count_empresas=5, count_prestadores=20, clear_existing=clear_existing)
        
        logger.info("\n" + "="*50)
        logger.info("✓ TODOS LOS SEEDERS COMPLETADOS EXITOSAMENTE")
        logger.info("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"\n✗ Error ejecutando seeders: {e}")
        db.session.rollback()
        raise
