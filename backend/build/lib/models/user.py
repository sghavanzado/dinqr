from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import inspect

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True, index=True)  # Make username nullable
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(512), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(64), nullable=False)
    second_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        return any(permission.name == permission_name for permission in self.role.permissions)

    def is_admin(self):
        return self.has_permission('admin_access')

    def get_permissions(self):
        return [permission.name for permission in self.role.permissions]

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role_id': self.role_id,
            'is_active': self.is_active,
            'name': self.name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

# Modelo de Permiso
class Permission(db.Model):
    __tablename__ = 'permission'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256)) 
    
    def __repr__(self):
        return f'<Permission {self.name}>'

# Modelo de Rol
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission', 
                                 secondary='roles_permissions',
                                 backref=db.backref('roles', lazy='dynamic'))

roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

# Modelo de Registro de Auditoría
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(64), nullable=False)
    target_type = db.Column(db.String(64), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45))
    details = db.Column(db.JSON)

    user = db.relationship('User', backref=db.backref('audit_logs', lazy='dynamic'))

def log_action(user_id, action, target_type, target_id, ip_address=None, details=None):
    """Registra una acción del usuario en el sistema."""
    log = AuditLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        ip_address=ip_address,
        details=details
    )
    db.session.add(log)
    db.session.commit()

# Inicialización de permisos por defecto
def initialize_permissions(app):
    with app.app_context():
        # Check if the Permission table exists using proper inspection
        inspector = inspect(db.engine)
        if not inspector.has_table('permission'):
            app.logger.warning("Permission table does not exist. Skipping permission initialization.")
            return

        required_permissions = [
            ('admin_access', 'Acceso completo al sistema'),
            ('create_user', 'Crear nuevos usuarios'),
            ('update_user', 'Modificar usuarios existentes'),
            ('delete_user', 'Eliminar usuarios'),
            ('view_audit_logs', 'Ver registros de auditoría')
        ]
        
        for perm_name, perm_desc in required_permissions:
            if not Permission.query.filter_by(name=perm_name).first():
                perm = Permission(name=perm_name, description=perm_desc)
                db.session.add(perm)
        
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin', description='Administrador del sistema')
            admin_perms = Permission.query.all()
            admin_role.permissions.extend(admin_perms)
            db.session.add(admin_role)
        
        if not Role.query.filter_by(name='user').first():
            user_role = Role(name='user', description='Usuario estándar')
            db.session.add(user_role)
        
        try:
            db.session.commit()
            app.logger.info("Permissions and roles initialized successfully.")
        except Exception as e:
            app.logger.error(f"Error initializing permissions: {e}")
            db.session.rollback()