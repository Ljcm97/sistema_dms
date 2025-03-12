from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.documento import TipoDocumento
from app.forms import TipoDocumentoForm
from sqlalchemy import func

# Crear blueprint
tipos_bp = Blueprint('tipos', __name__, url_prefix='/tipos')

@tipos_bp.route('/')
@login_required
def index():
    """
    Lista de tipos de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = TipoDocumento.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(TipoDocumento.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(TipoDocumento.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_tipos = TipoDocumento.query.count()
    activos = TipoDocumento.query.filter_by(activo=True).count()
    
    # Uso de tipos de documento
    from app.models.documento import Documento
    tipos_uso = db.session.query(
        TipoDocumento.id,
        TipoDocumento.nombre,
        func.count(Documento.id).label('num_documentos')
    ).outerjoin(
        Documento, Documento.tipo_documento_id == TipoDocumento.id
    ).group_by(
        TipoDocumento.id, TipoDocumento.nombre
    ).order_by(
        func.count(Documento.id).desc()
    ).limit(5).all()
    
    return render_template('tipos/index.html',
                          title='Gestión de Tipos de Documento',
                          tipos=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_tipos=total_tipos,
                          activos=activos,
                          tipos_uso=tipos_uso)

@tipos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear un nuevo tipo de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = TipoDocumentoForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe un tipo con el mismo nombre
        if TipoDocumento.query.filter(func.lower(TipoDocumento.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe un tipo de documento con este nombre', 'danger')
            return render_template('tipos/crear.html', form=form, title='Crear Tipo de Documento')
        
        # Crear tipo de documento
        tipo = TipoDocumento(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(tipo)
        db.session.commit()
        
        flash(f'Tipo de documento {tipo.nombre} creado correctamente', 'success')
        return redirect(url_for('tipos.index'))
    
    return render_template('tipos/crear.html', form=form, title='Crear Tipo de Documento')

@tipos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar un tipo de documento existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    tipo = TipoDocumento.query.get_or_404(id)
    form = TipoDocumentoForm()
    
    if request.method == 'GET':
        form.nombre.data = tipo.nombre
        form.descripcion.data = tipo.descripcion
        form.activo.data = tipo.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otro tipo con el mismo nombre
        duplicate = TipoDocumento.query.filter(
            func.lower(TipoDocumento.nombre) == func.lower(form.nombre.data),
            TipoDocumento.id != tipo.id
        ).first()
        
        if duplicate:
            flash('Ya existe otro tipo de documento con este nombre', 'danger')
            return render_template('tipos/editar.html', form=form, tipo=tipo, title='Editar Tipo de Documento')
        
        # Actualizar tipo de documento
        tipo.nombre = form.nombre.data
        tipo.descripcion = form.descripcion.data
        tipo.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Tipo de documento {tipo.nombre} actualizado correctamente', 'success')
        return redirect(url_for('tipos.index'))
    
    return render_template('tipos/editar.html', form=form, tipo=tipo, title='Editar Tipo de Documento')

@tipos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar un tipo de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    tipo = TipoDocumento.query.get_or_404(id)
    
    # Verificar si el tipo está en uso
    if tipo.documentos.count() > 0:
        flash(f'No se puede eliminar el tipo de documento {tipo.nombre} porque está en uso', 'danger')
        return redirect(url_for('tipos.index'))
    
    # Guardar nombre para mensaje
    nombre = tipo.nombre
    
    db.session.delete(tipo)
    db.session.commit()
    
    flash(f'Tipo de documento {nombre} eliminado correctamente', 'success')
    return redirect(url_for('tipos.index'))