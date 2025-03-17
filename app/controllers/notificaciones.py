from flask import Blueprint, jsonify, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from flask import current_app
from app import db
from app.models.notificacion import Notificacion
from app.models.documento import Documento

# Crear blueprint
notificaciones_bp = Blueprint('notificaciones', __name__, url_prefix='/notificaciones')

@notificaciones_bp.route('/no-leidas')
@login_required
def no_leidas():
    """
    Obtener notificaciones no leídas del usuario actual
    """
    try:
        current_app.logger.info(f"Obteniendo notificaciones no leídas para el usuario {current_user.id}")
        notificaciones = Notificacion.get_notificaciones_no_leidas(current_user.id)
        current_app.logger.info(f"Se encontraron {len(notificaciones)} notificaciones no leídas")
        
        result = []
        for n in notificaciones:
            result.append({
                'id': n.id,
                'mensaje': n.mensaje,
                'fecha': n.creado_en.strftime('%d/%m/%Y %H:%M'),
                'documento_id': n.documento_id,
                'url': url_for('documentos.detalle_documento', id=n.documento_id) if n.documento_id else '#'
            })
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error al obtener notificaciones: {str(e)}")
        return jsonify([])

@notificaciones_bp.route('/marcar-leida/<int:id>')
@login_required
def marcar_leida(id):
    """
    Marcar una notificación como leída
    """
    try:
        notificacion = Notificacion.query.get_or_404(id)
        
        # Verificar que la notificación pertenezca al usuario
        if notificacion.usuario_id != current_user.id:
            return jsonify({'status': 'error', 'message': 'No tienes permiso para esta acción'}), 403
        
        # Marcar como leída
        Notificacion.marcar_como_leida(id)
        current_app.logger.info(f"Notificación {id} marcada como leída por el usuario {current_user.id}")
        
        # Redireccionar a la URL de la notificación si tiene documento
        if notificacion.documento_id:
            return redirect(url_for('documentos.detalle_documento', id=notificacion.documento_id))
        
        return redirect(url_for('documentos.dashboard'))
    except Exception as e:
        current_app.logger.error(f"Error al marcar notificación como leída: {str(e)}")
        return redirect(url_for('documentos.dashboard'))

@notificaciones_bp.route('/count')
@login_required
def count():
    """
    Retorna solamente el conteo de notificaciones no leídas
    """
    try:
        count = Notificacion.query.filter_by(
            usuario_id=current_user.id,
            leida=False
        ).count()
        
        return jsonify({'count': count})
    except Exception as e:
        current_app.logger.error(f"Error al contar notificaciones: {str(e)}")
        return jsonify({'count': 0})

@notificaciones_bp.route('/todas')
@login_required
def todas():
    """
    Ver todas las notificaciones en una página
    """
    page = request.args.get('page', 1, type=int)
    
    # Obtener todas las notificaciones del usuario
    query = Notificacion.query.filter_by(usuario_id=current_user.id).order_by(Notificacion.creado_en.desc())
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=20,
        error_out=False
    )
    
    return render_template('notificaciones/todas.html',
                          title='Mis Notificaciones',
                          notificaciones=pagination.items,
                          pagination=pagination)