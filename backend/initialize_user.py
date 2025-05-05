from app import create_app
from extensions import db
from models.user import User, Role

def initialize_admin_user():
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar rol admin
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                print("❌ Error: Primero ejecuta initialize_roles.py")
                return

            # Crear usuario admin si no existe
            if User.query.filter_by(email='maikel@ejemplos.com').first():
                print("⚠️  El usuario admin ya existe")
                return

            admin_user = User(
                username='manager',
                email='manager@gts.ao',
                role=admin_role,
                name='Administrador',
                second_name='Local',
                last_name='SNL',
                phone_number='000000000',
                is_active=True
            )
            admin_user.set_password('P@ssw0rd')  # Cambiar en producción
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅  Usuario admin creado exitosamente")
            print(f"👤 Detalles del usuario:")
            print(f"   Email: {admin_user.email}")
            print(f"   Rol: {admin_user.role.name}")
            print(f"   ID: {admin_user.id}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuario admin: {str(e)}")
            raise

if __name__ == '__main__':
    initialize_admin_user()
        