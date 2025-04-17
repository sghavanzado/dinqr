from app import create_app
from extensions import db
from models.user import Permission, Role

def initialize_roles_and_permissions():
    # Crear aplicación y contexto
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existen datos
            if Role.query.first() or Permission.query.first():
                print("⚠️  Ya existen roles y permisos en la base de datos")
                return

            # Crear permisos básicos
            permissions = [
                Permission(name='admin_access', description='Acceso completo al sistema'),
                Permission(name='create_user', description='Crear nuevos usuarios'),
                Permission(name='update_user', description='Modificar usuarios existentes'),
                Permission(name='delete_user', description='Eliminar usuarios'),
                Permission(name='view_audit_logs', description='Ver registros de auditoría')
            ]

            db.session.bulk_save_objects(permissions)
            
            # Crear rol de administrador con todos los permisos
            admin_role = Role(name='admin', description='Administrador del sistema')
            admin_role.permissions = permissions
            
            db.session.add(admin_role)

            # Crear rol de usuario estándar sin permisos adicionales
            user_role = Role(name='user', description='Usuario estándar')
            db.session.add(user_role)
            
            db.session.commit()
            
            print("✅  Roles y permisos inicializados exitosamente")
            print(f"🔑 Rol admin creado con {len(permissions)} permisos")
            print("🔑 Rol user creado sin permisos adicionales")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inicializando roles: {str(e)}")
            raise

if __name__ == '__main__':
    initialize_roles_and_permissions()
