from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from app.models.usuario import Usuario
from app.forms import LoginForm, CambiarPasswordForm
import datetime

# Crear blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Vista para el inicio de sesión
    """
    # Si el usuario ya está autenticado, redirigir a página principal
    if current_user.is_authenticated:
        return redirect(url_for('documentos.dashboard'))
    
    # Eliminar mensajes flash pendientes de login
    session.pop('_flashes', None)
    
    form = LoginForm()
    
    # Si el formulario se envió y es válido
    if form.validate_on_submit():
        # Buscar el usuario
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        # Verificar usuario y contraseña
        if usuario is None or not usuario.verify_password(form.password.data):
            flash('Usuario o contraseña incorrectos', 'danger')
            current_app.logger.warning(f'Intento de acceso fallido para el usuario: {form.username.data}')
            return render_template('auth/login.html', form=form)
        
        # Verificar si el usuario está activo
        if not usuario.activo:
            flash('Esta cuenta está desactivada. Contacte al administrador.', 'warning')
            current_app.logger.warning(f'Intento de acceso a cuenta desactivada: {usuario.username}')
            return render_template('auth/login.html', form=form)
        
        # Iniciar sesión
        login_user(usuario, remember=form.remember_me.data)
        usuario.update_ultimo_acceso()
        
        current_app.logger.info(f'Usuario {usuario.username} ha iniciado sesión')
        
        # Redireccionar directamente al dashboard, ignorando el parámetro next
        return redirect(url_for('documentos.dashboard'))
    
    return render_template('auth/login.html', form=form, title='Iniciar Sesión')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Vista para cerrar sesión
    """
    current_app.logger.info(f'Usuario {current_user.username} ha cerrado sesión')
    logout_user()
    
    # Eliminar todos los mensajes flash pendientes
    session.pop('_flashes', None)
    
    # Agregar un solo mensaje de cierre de sesión
    flash('Has cerrado sesión correctamente', 'info')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Vista para cambiar contraseña
    """
    form = CambiarPasswordForm()
    
    if form.validate_on_submit():
        # Verificar contraseña actual
        if not current_user.verify_password(form.password_actual.data):
            flash('La contraseña actual es incorrecta', 'danger')
            return render_template('auth/cambiar_password.html', form=form)
        
        # Cambiar contraseña
        current_user.password = form.password.data
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} ha cambiado su contraseña')
        flash('Tu contraseña ha sido actualizada', 'success')
        return redirect(url_for('documentos.dashboard'))
    
    return render_template('auth/cambiar_password.html', form=form, title='Cambiar Contraseña')

# Middleware para verificar permisos de superadministrador
@auth_bp.before_app_request
def before_request():
    """
    Verificar permisos antes de cada solicitud
    """
    # Si la solicitud es para acceder a una ruta estática o de login/logout, ignoramos la verificación
    if not request.endpoint or 'static' in request.path or request.endpoint in ['auth.login', 'auth.logout']:
        return
    
    # Lista de rutas de la API que no deben activar mensajes flash
    api_routes = ['api.', 'notificaciones.']
    is_api_route = any(request.endpoint.startswith(route) for route in api_routes) if request.endpoint else False
        
    # Lista de rutas que requieren permisos de superadministrador
    admin_routes = [
        'admin.index',
        'admin.usuarios',
        'admin.crear_usuario',
        'admin.editar_usuario',
        'admin.eliminar_usuario',
        'admin.personas',
        'admin.crear_persona',
        'admin.editar_persona',
        'admin.eliminar_persona'
    ]
    
    # Si la ruta actual requiere permisos de superadministrador
    if request.endpoint and (request.endpoint in admin_routes or any(request.endpoint.startswith(route + '.') for route in admin_routes)):
        # Si el usuario no está autenticado o no es superadministrador
        if not current_user.is_authenticated or not current_user.is_superadmin():
            flash('No tienes permisos para acceder a esta área', 'danger')
            current_app.logger.warning(f'Intento de acceso no autorizado a {request.endpoint} por {current_user.username if current_user.is_authenticated else "usuario anónimo"}')
            return redirect(url_for('documentos.dashboard'))