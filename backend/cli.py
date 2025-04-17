import click
from flask import current_app
from werkzeug.security import generate_password_hash
from models.user import User, Role
import logging

def register_commands(app):
    @app.cli.command('create-admin')
    @click.option('--username', prompt=True)
    @click.option('--email', prompt=True)
    @click.option('--password', prompt=True, hide_input=True)
    def create_admin(username, email, password):
        """Crear usuario administrador inicial"""
        with current_app.app_context():
            app.logger.debug("Iniciando creación de administrador...") #agregar log
            admin_role = Role.query.filter_by(name='admin').first()

            if not admin_role:
                raise Exception('Rol admin no existe. Ejecuta las migraciones primero.')

            if User.query.filter_by(email=email).first():
                raise Exception('El email ya está registrado')

            admin_user = User(
                username=username,
                email=email,
                name='Admin',
                last_name='User',
                role=admin_role
            )
            admin_user.set_password(password)

            db.session.add(admin_user)
            db.session.commit()
            app.logger.debug(f'Administrador {username} creado exitosamente!') #agregar log
            print(f'Administrador {username} creado exitosamente!')

    @app.cli.command('init-db')
    def init_db():
        """Inicializar la base de datos y permisos"""
        with current_app.app_context():
            app.logger.debug("Iniciando inicialización de base de datos...") #agregar log
            db.create_all()
            from models.user import initialize_permissions
            initialize_permissions()
            app.logger.debug('Base de datos y permisos inicializados correctamente') #agregar log.
            print('Base de datos y permisos inicializados correctamente')