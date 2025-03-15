from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.cargo import Cargo
from app.forms import CargoForm
from sqlalchemy import func

# Crear blueprint
cargos_bp = Blueprint('cargos', __name__, url_prefix='/cargos')

@cargos_bp.route('/')
@login_required
def index():
    """
    Lista de cargos
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = Cargo.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(Cargo.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(Cargo.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_cargos = Cargo.query.count()
    activos = Cargo.query.filter_by(activo=True).count()
    
    # Uso de cargos
    from app.models.persona import Persona
    cargos_uso = db.session.query(
        Cargo.id,
        Cargo.nombre,
        func.count(Persona.id).label('num_personas')
    ).outerjoin(
        Persona, Persona.cargo_id == Cargo.id
    ).group_by(
        Cargo.id, Cargo.nombre
    ).order_by(
        func.count(Persona.id).desc()
    ).limit(5).all()
    
    return render_template('cargos/index.html',
                          title='Gestión de Cargos',
                          cargos=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_cargos=total_cargos,
                          activos=activos,
                          cargos_uso=cargos_uso)

@cargos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear un nuevo cargo
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = CargoForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe un cargo con el mismo nombre
        if Cargo.query.filter(func.lower(Cargo.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe un cargo con este nombre', 'danger')
            return render_template('cargos/crear.html', form=form, title='Crear Cargo')
        
        # Crear cargo
        cargo = Cargo(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(cargo)
        db.session.commit()
        
        flash(f'Cargo {cargo.nombre} creado correctamente', 'success')
        return redirect(url_for('cargos.index'))
    
    return render_template('cargos/crear.html', form=form, title='Crear Cargo')

@cargos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar un cargo existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    cargo = Cargo.query.get_or_404(id)
    form = CargoForm()
    
    if request.method == 'GET':
        form.nombre.data = cargo.nombre
        form.descripcion.data = cargo.descripcion
        form.activo.data = cargo.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otro cargo con el mismo nombre
        duplicate = Cargo.query.filter(
            func.lower(Cargo.nombre) == func.lower(form.nombre.data),
            Cargo.id != cargo.id
        ).first()
        
        if duplicate:
            flash('Ya existe otro cargo con este nombre', 'danger')
            return render_template('cargos/editar.html', form=form, cargo=cargo, title='Editar Cargo')
        
        # Actualizar cargo
        cargo.nombre = form.nombre.data
        cargo.descripcion = form.descripcion.data
        cargo.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Cargo {cargo.nombre} actualizado correctamente', 'success')
        return redirect(url_for('cargos.index'))
    
    return render_template('cargos/editar.html', form=form, cargo=cargo, title='Editar Cargo')

@cargos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar un cargo
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    try:
        cargo = Cargo.query.get_or_404(id)
        
        # Verificar si el cargo está en uso por personas
        if cargo.personas.count() > 0:
            flash(f'No se puede eliminar el cargo {cargo.nombre} porque está asignado a personas', 'danger')
            return redirect(url_for('cargos.index'))
        
        # Guardar nombre para mensaje
        nombre = cargo.nombre
        
        db.session.delete(cargo)
        db.session.commit()
        
        flash(f'Cargo {nombre} eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('cargos.index'))