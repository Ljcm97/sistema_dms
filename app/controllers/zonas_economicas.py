from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.zona_economica import ZonaEconomica
from app.forms import ZonaEconomicaForm
from sqlalchemy import func

# Crear blueprint
zonas_bp = Blueprint('zonas', __name__, url_prefix='/zonas')

@zonas_bp.route('/')
@login_required
def index():
    """
    Lista de zonas económicas
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = ZonaEconomica.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(ZonaEconomica.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(ZonaEconomica.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_zonas = ZonaEconomica.query.count()
    activas = ZonaEconomica.query.filter_by(activo=True).count()
    
    return render_template('zonas/index.html',
                          title='Gestión de Zonas Económicas',
                          zonas=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_zonas=total_zonas,
                          activas=activas)

@zonas_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear una nueva zona económica
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = ZonaEconomicaForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe una zona con el mismo nombre
        if ZonaEconomica.query.filter(func.lower(ZonaEconomica.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe una zona económica con este nombre', 'danger')
            return render_template('zonas/crear.html', form=form, title='Crear Zona Económica')
        
        # Crear zona económica
        zona = ZonaEconomica(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(zona)
        db.session.commit()
        
        flash(f'Zona económica {zona.nombre} creada correctamente', 'success')
        return redirect(url_for('zonas.index'))
    
    return render_template('zonas/crear.html', form=form, title='Crear Zona Económica')

@zonas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar una zona económica existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    zona = ZonaEconomica.query.get_or_404(id)
    form = ZonaEconomicaForm()
    
    if request.method == 'GET':
        form.nombre.data = zona.nombre
        form.descripcion.data = zona.descripcion
        form.activo.data = zona.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otra zona con el mismo nombre
        duplicate = ZonaEconomica.query.filter(
            func.lower(ZonaEconomica.nombre) == func.lower(form.nombre.data),
            ZonaEconomica.id != zona.id
        ).first()
        
        if duplicate:
            flash('Ya existe otra zona económica con este nombre', 'danger')
            return render_template('zonas/editar.html', form=form, zona=zona, title='Editar Zona Económica')
        
        # Actualizar zona económica
        zona.nombre = form.nombre.data
        zona.descripcion = form.descripcion.data
        zona.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Zona económica {zona.nombre} actualizada correctamente', 'success')
        return redirect(url_for('zonas.index'))
    
    return render_template('zonas/editar.html', form=form, zona=zona, title='Editar Zona Económica')

@zonas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar una zona económica
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    try:
        zona = ZonaEconomica.query.get_or_404(id)
        
        # Guardar nombre para mensaje
        nombre = zona.nombre
        
        db.session.delete(zona)
        db.session.commit()
        
        current_app.logger.info(f'Usuario {current_user.username} eliminó la zona económica: {nombre}')
        flash(f'Zona económica {nombre} eliminada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al eliminar zona económica {id}: {str(e)}')
        flash(f'Error al eliminar la zona económica: {str(e)}', 'danger')
    
    return redirect(url_for('zonas.index'))