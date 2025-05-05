from extensions import db
from models.user import User

def create_admin():
    """Crea un usuario administrador si no existe."""
    if not User.query.filter_by(username="admin2@example.com").first():
        admin = User(
            username="admin2@example.com ",
            email="admin2@example.com",
            role="admin",
            is_active=True
        )
        admin.set_password("adminpassword")  # Hashea la contraseña correctamente
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado correctamente.")
    else:
        print("El usuario administrador ya existe.")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        create_admin()
