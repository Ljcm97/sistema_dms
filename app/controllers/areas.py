from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.area import Area
from app.forms import AreaForm
from sqlalchemy import func

# Crear blueprint
areas_bp = Blueprint('areas', __name__, url_prefix='/areas')

@areas_bp.route('/')
@login_required
def index():
    """
    Lista de áreas
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = Area.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(Area.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(Area.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_areas = Area.query.count()
    activas = Area.query.filter_by(activo=True).count()
    
    # Uso de áreas
    from app.models.persona import Persona
    areas_uso = db.session.query(
        Area.id,
        Area.nombre,
        func.count(Persona.id).label('num_personas')
    ).outerjoin(
        Persona, Persona.area_id == Area.id
    ).group_by(
        Area.id, Area.nombre
    ).order_by(
        func.count(Persona.id).desc()
    ).limit(5).all()
    
    return render_template('areas/index.html',
                          title='Gestión de Áreas',
                          areas=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_areas=total_areas,
                          activas=activas,
                          areas_uso=areas_uso)

@areas_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear una nueva área
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = AreaForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe un área con el mismo nombre
        if Area.query.filter(func.lower(Area.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe un área con este nombre', 'danger')
            return render_template('areas/crear.html', form=form, title='Crear Área')
        
        # Crear área
        area = Area(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(area)
        db.session.commit()
        
        flash(f'Área {area.nombre} creada correctamente', 'success')
        return redirect(url_for('areas.index'))
    
    return render_template('areas/crear.html', form=form, title='Crear Área')

@areas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar un área existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    area = Area.query.get_or_404(id)
    form = AreaForm()
    
    if request.method == 'GET':
        form.nombre.data = area.nombre
        form.descripcion.data = area.descripcion
        form.activo.data = area.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otra área con el mismo nombre
        duplicate = Area.query.filter(
            func.lower(Area.nombre) == func.lower(form.nombre.data),
            Area.id != area.id
        ).first()
        
        if duplicate:
            flash('Ya existe otra área con este nombre', 'danger')
            return render_template('areas/editar.html', form=form, area=area, title='Editar Área')
        
        # Actualizar área
        area.nombre = form.nombre.data
        area.descripcion = form.descripcion.data
        area.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Área {area.nombre} actualizada correctamente', 'success')
        return redirect(url_for('areas.index'))
    
    return render_template('areas/editar.html', form=form, area=area, title='Editar Área')

@areas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar un área
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    area = Area.query.get_or_404(id)
    
    # Verificar si el área está en uso por personas
    if area.personas.count() > 0:
        flash(f'No se puede eliminar el área {area.nombre} porque está asignada a personas', 'danger')
        return redirect(url_for('areas.index'))
    
    # Verificar si el área está en uso por documentos
    if area.documentos_actuales.count() > 0:
        flash(f'No se puede eliminar el área {area.nombre} porque está asignada a documentos', 'danger')
        return redirect(url_for('areas.index'))
    
    # Guardar nombre para mensaje
    nombre = area.nombre
    
    db.session.delete(area)
    db.session.commit()
    
    flash(f'Área {nombre} eliminada correctamente', 'success')
    return redirect(url_for('areas.index'))