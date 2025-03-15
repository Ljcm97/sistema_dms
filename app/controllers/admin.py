from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.usuario import Usuario, Rol
from app.models.persona import Persona
from app.models.area import Area
from app.models.privilegio import Privilegio
from app.forms import UsuarioForm, PersonaForm
from werkzeug.security import generate_password_hash
import datetime

# Crear blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    """
    Panel de administración
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder al panel de administración', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    # Estadísticas para el panel
    num_usuarios = Usuario.query.count()
    num_personas = Persona.query.count()
    num_areas = Area.query.count()
    
    # Usuarios recientes
    usuarios_recientes = Usuario.query.order_by(Usuario.creado_en.desc()).limit(5).all()
    
    return render_template('admin/index.html', 
                           title='Panel de Administración',
                           num_usuarios=num_usuarios,
                           num_personas=num_personas,
                           num_areas=num_areas,
                           usuarios_recientes=usuarios_recientes)

# ==== Gestión de Usuarios ====

@admin_bp.route('/usuarios')
@login_required
def usuarios():
    """
    Lista de usuarios
    """
    page = request.args.get('page', 1, type=int)
    query = Usuario.query.join(Persona).order_by(Persona.nombre, Persona.apellido)
    
    # Filtros de búsqueda
    search = request.args.get('search', '')
    if search:
        query = query.filter(
            Usuario.username.like(f'%{search}%') |
            Persona.nombre.like(f'%{search}%') |
            Persona.apellido.like(f'%{search}%')
        )
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('admin/usuarios.html',
                          title='Gestión de Usuarios',
                          usuarios=pagination.items,
                          pagination=pagination,
                          search=search)

@admin_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    """
    Crear un nuevo usuario
    """
    form = UsuarioForm()
    
    if form.validate_on_submit():
        # Verificar que la persona no tenga ya un usuario
        persona = Persona.query.get(form.persona_id.data)
        if persona.usuario:
            flash(f'La persona {persona.nombre_completo} ya tiene un usuario asignado', 'danger')
            return render_template('admin/crear_usuario.html', form=form, title='Crear Usuario')
        
        # Crear nuevo usuario
        usuario = Usuario(
            username=form.username.data,
            persona_id=form.persona_id.data,
            rol_id=form.rol_id.data,
            activo=form.activo.data
        )
        usuario.password = form.password.data
        
        db.session.add(usuario)
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} creó un nuevo usuario: {usuario.username}')
        flash(f'Usuario {usuario.username} creado correctamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/crear_usuario.html', form=form, title='Crear Usuario')

@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    """
    Editar un usuario existente
    """
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir modificar al usuario actual
    if usuario.id == current_user.id:
        flash('No puedes modificar tu propio usuario desde aquí', 'warning')
        return redirect(url_for('admin.usuarios'))
    
    form = UsuarioForm(usuario_actual=usuario)
    
    if request.method == 'GET':
        form.username.data = usuario.username
        form.persona_id.data = usuario.persona_id
        form.rol_id.data = usuario.rol_id
        form.activo.data = usuario.activo
    
    if form.validate_on_submit():
        # Actualizar usuario
        usuario.username = form.username.data
        usuario.persona_id = form.persona_id.data
        usuario.rol_id = form.rol_id.data
        usuario.activo = form.activo.data
        
        # Actualizar contraseña si se proporcionó
        if form.password.data:
            usuario.password = form.password.data
        
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} modificó al usuario: {usuario.username}')
        flash(f'Usuario {usuario.username} actualizado correctamente', 'success')
        return redirect(url_for('admin.usuarios'))
    
    return render_template('admin/editar_usuario.html', form=form, usuario=usuario, title='Editar Usuario')

@admin_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    """
    Eliminar un usuario
    """
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir eliminar al usuario actual
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin.usuarios'))
    
    # Almacenar información para el mensaje
    username = usuario.username
    
    db.session.delete(usuario)
    db.session.commit()
    
    current_app.logger.info(f'Usuario {current_user.username} eliminó al usuario: {username}')
    flash(f'Usuario {username} eliminado correctamente', 'success')
    return redirect(url_for('admin.usuarios'))

# ==== Gestión de Personas ====

@admin_bp.route('/personas')
@login_required
def personas():
    """
    Lista de personas
    """
    page = request.args.get('page', 1, type=int)
    query = Persona.query.join(Area).order_by(Persona.nombre, Persona.apellido)
    
    # Filtros de búsqueda
    search = request.args.get('search', '')
    if search:
        query = query.filter(
            Persona.nombre.like(f'%{search}%') |
            Persona.apellido.like(f'%{search}%') |
            Persona.email.like(f'%{search}%') |
            Area.nombre.like(f'%{search}%')
        )
    
    # Filtro por área
    area_id = request.args.get('area_id', 0, type=int)
    if area_id > 0:
        query = query.filter(Persona.area_id == area_id)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Lista de áreas para el filtro
    areas = Area.query.order_by(Area.nombre).all()
    
    return render_template('admin/personas.html',
                          title='Gestión de Personas',
                          personas=pagination.items,
                          pagination=pagination,
                          search=search,
                          area_id=area_id,
                          areas=areas)

@admin_bp.route('/personas/crear', methods=['GET', 'POST'])
@login_required
def crear_persona():
    """
    Crear una nueva persona
    """
    form = PersonaForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe una persona con el mismo email
        if form.email.data and Persona.query.filter_by(email=form.email.data).first():
            flash('Ya existe una persona con este email', 'danger')
            return render_template('admin/crear_persona.html', form=form, title='Crear Persona')
        
        # Crear nueva persona
        persona = Persona(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            area_id=form.area_id.data,
            activo=form.activo.data
        )
        
        # Asignar cargo_id solo si no es 0
        if form.cargo_id.data and form.cargo_id.data != 0:
            persona.cargo_id = form.cargo_id.data
        
        db.session.add(persona)
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} creó una nueva persona: {persona.nombre_completo}')
        flash(f'Persona {persona.nombre_completo} creada correctamente', 'success')
        return redirect(url_for('admin.personas'))
    
    return render_template('admin/crear_persona.html', form=form, title='Crear Persona')

@admin_bp.route('/personas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_persona(id):
    """
    Editar una persona existente
    """
    persona = Persona.query.get_or_404(id)
    form = PersonaForm()
    
    if request.method == 'GET':
        form.nombre.data = persona.nombre
        form.apellido.data = persona.apellido
        form.email.data = persona.email
        form.telefono.data = persona.telefono
        form.area_id.data = persona.area_id
        form.activo.data = persona.activo
        if persona.cargo_id:
            form.cargo_id.data = persona.cargo_id
    
    if form.validate_on_submit():
        # Verificar si ya existe otra persona con el mismo email
        if form.email.data and Persona.query.filter(
            Persona.email == form.email.data,
            Persona.id != persona.id
        ).first():
            flash('Ya existe otra persona con este email', 'danger')
            return render_template('admin/editar_persona.html', form=form, persona=persona, title='Editar Persona')
        
        # Actualizar persona
        persona.nombre = form.nombre.data
        persona.apellido = form.apellido.data
        persona.email = form.email.data
        persona.telefono = form.telefono.data
        persona.area_id = form.area_id.data
        persona.activo = form.activo.data
        
        # Asignar cargo_id solo si no es 0, de lo contrario establecer en None
        if form.cargo_id.data and form.cargo_id.data != 0:
            persona.cargo_id = form.cargo_id.data
        else:
            persona.cargo_id = None
        
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} modificó a la persona: {persona.nombre_completo}')
        flash(f'Persona {persona.nombre_completo} actualizada correctamente', 'success')
        return redirect(url_for('admin.personas'))
    
    return render_template('admin/editar_persona.html', form=form, persona=persona, title='Editar Persona')

@admin_bp.route('/personas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_persona(id):
    """
    Eliminar una persona
    """
    persona = Persona.query.get_or_404(id)
    
    # Verificar si la persona tiene un usuario asociado
    if persona.usuario:
        flash(f'No se puede eliminar a {persona.nombre_completo} porque tiene un usuario asociado', 'danger')
        return redirect(url_for('admin.personas'))
    
    # Verificar si la persona está asociada a documentos
    if persona.documentos_actuales.count() > 0:
        flash(f'No se puede eliminar a {persona.nombre_completo} porque está asociada a documentos', 'danger')
        return redirect(url_for('admin.personas'))
    
    # Almacenar información para el mensaje
    nombre_completo = persona.nombre_completo
    
    db.session.delete(persona)
    db.session.commit()
    
    current_app.logger.info(f'Usuario {current_user.username} eliminó a la persona: {nombre_completo}')
    flash(f'Persona {nombre_completo} eliminada correctamente', 'success')
    return redirect(url_for('admin.personas'))

# ==== API para obtener personas por área ====

@admin_bp.route('/api/personas-por-area/<int:area_id>')
@login_required
def api_personas_por_area(area_id):
    """
    API para obtener las personas de un área
    """
    personas = Persona.query.filter_by(area_id=area_id, activo=True).order_by(Persona.nombre, Persona.apellido).all()
    return jsonify([{
        'id': p.id,
        'nombre_completo': p.nombre_completo
    } for p in personas])

@admin_bp.route('/privilegios')
@login_required
def privilegios():
    """
    Gestión de privilegios de usuarios
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Obtener todos los usuarios con sus privilegios
    usuarios = Usuario.query.order_by(Usuario.username).paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Cargar los privilegios manualmente para cada usuario
    for usuario in usuarios.items:
        usuario.privilegio = Privilegio.query.filter_by(usuario_id=usuario.id).first()
    
    return render_template('admin/privilegios.html',
                          title='Gestión de Privilegios',
                          usuarios=usuarios.items,
                          pagination=usuarios)

@admin_bp.route('/privilegios/actualizar/<int:usuario_id>', methods=['POST'])
@login_required
def actualizar_privilegio(usuario_id):
    """
    Actualizar privilegios de un usuario
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para esta acción', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # No se pueden modificar privilegios de superadministradores
    if usuario.is_superadmin():
        flash('No se pueden modificar privilegios de superadministradores', 'warning')
        return redirect(url_for('admin.privilegios'))
    
    # Obtener el privilegio actual o crear uno nuevo
    privilegio = Privilegio.query.filter_by(usuario_id=usuario_id).first()
    if not privilegio:
        privilegio = Privilegio(usuario_id=usuario_id, creado_por=current_user.id)
        db.session.add(privilegio)
    
    # Actualizar privilegios
    puede_registrar = request.form.get('puede_registrar_documentos') == 'on'
    puede_ver = request.form.get('puede_ver_documentos_area') == 'on'
    
    privilegio.puede_registrar_documentos = puede_registrar
    privilegio.puede_ver_documentos_area = puede_ver
    
    db.session.commit()
    
    flash(f'Privilegios del usuario {usuario.username} actualizados correctamente', 'success')
    return redirect(url_for('admin.privilegios'))