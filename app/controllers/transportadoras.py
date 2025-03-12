from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.documento import Transportadora
from app.forms import TransportadoraForm
from sqlalchemy import func

# Crear blueprint
transportadoras_bp = Blueprint('transportadoras', __name__, url_prefix='/transportadoras')

@transportadoras_bp.route('/')
@login_required
def index():
    """
    Lista de transportadoras
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = Transportadora.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(Transportadora.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(Transportadora.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_transportadoras = Transportadora.query.count()
    activas = Transportadora.query.filter_by(activo=True).count()
    
    # Uso de transportadoras
    from app.models.documento import Documento
    transportadoras_uso = db.session.query(
        Transportadora.id,
        Transportadora.nombre,
        func.count(Documento.id).label('num_documentos')
    ).outerjoin(
        Documento, Documento.transportadora_id == Transportadora.id
    ).group_by(
        Transportadora.id, Transportadora.nombre
    ).order_by(
        func.count(Documento.id).desc()
    ).limit(5).all()
    
    return render_template('transportadoras/index.html',
                          title='Gestión de Transportadoras',
                          transportadoras=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_transportadoras=total_transportadoras,
                          activas=activas,
                          transportadoras_uso=transportadoras_uso)

@transportadoras_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear una nueva transportadora
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = TransportadoraForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe una transportadora con el mismo nombre
        if Transportadora.query.filter(func.lower(Transportadora.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe una transportadora con este nombre', 'danger')
            return render_template('transportadoras/crear.html', form=form, title='Crear Transportadora')
        
        # Crear transportadora
        transportadora = Transportadora(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(transportadora)
        db.session.commit()
        
        flash(f'Transportadora {transportadora.nombre} creada correctamente', 'success')
        return redirect(url_for('transportadoras.index'))
    
    return render_template('transportadoras/crear.html', form=form, title='Crear Transportadora')

@transportadoras_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar una transportadora existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    transportadora = Transportadora.query.get_or_404(id)
    form = TransportadoraForm()
    
    if request.method == 'GET':
        form.nombre.data = transportadora.nombre
        form.descripcion.data = transportadora.descripcion
        form.activo.data = transportadora.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otra transportadora con el mismo nombre
        duplicate = Transportadora.query.filter(
            func.lower(Transportadora.nombre) == func.lower(form.nombre.data),
            Transportadora.id != transportadora.id
        ).first()
        
        if duplicate:
            flash('Ya existe otra transportadora con este nombre', 'danger')
            return render_template('transportadoras/editar.html', form=form, transportadora=transportadora, title='Editar Transportadora')
        
        # Actualizar transportadora
        transportadora.nombre = form.nombre.data
        transportadora.descripcion = form.descripcion.data
        transportadora.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Transportadora {transportadora.nombre} actualizada correctamente', 'success')
        return redirect(url_for('transportadoras.index'))
    
    return render_template('transportadoras/editar.html', form=form, transportadora=transportadora, title='Editar Transportadora')

@transportadoras_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar una transportadora
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    transportadora = Transportadora.query.get_or_404(id)
    
    # Verificar si la transportadora está en uso
    if transportadora.documentos.count() > 0:
        flash(f'No se puede eliminar la transportadora {transportadora.nombre} porque está en uso', 'danger')
        return redirect(url_for('transportadoras.index'))
    
    # Guardar nombre para mensaje
    nombre = transportadora.nombre
    
    db.session.delete(transportadora)
    db.session.commit()
    
    flash(f'Transportadora {nombre} eliminada correctamente', 'success')
    return redirect(url_for('transportadoras.index'))