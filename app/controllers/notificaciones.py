from flask import Blueprint, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.notificacion import Notificacion

# Crear blueprint
notificaciones_bp = Blueprint('notificaciones', __name__, url_prefix='/notificaciones')

@notificaciones_bp.route('/no-leidas')
@login_required
def no_leidas():
    """
    Obtener notificaciones no leídas del usuario actual
    """
    notificaciones = Notificacion.get_notificaciones_no_leidas(current_user.id)
    return jsonify([{
        'id': n.id,
        'mensaje': n.mensaje,
        'fecha': n.creado_en.strftime('%d/%m/%Y %H:%M'),
        'documento_id': n.documento_id,
        'url': url_for('documentos.detalle_documento', id=n.documento_id) if n.documento_id else '#'
    } for n in notificaciones])

@notificaciones_bp.route('/marcar-leida/<int:id>')
@login_required
def marcar_leida(id):
    """
    Marcar una notificación como leída
    """
    notificacion = Notificacion.query.get_or_404(id)
    
    # Verificar que la notificación pertenezca al usuario
    if notificacion.usuario_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'No tienes permiso para esta acción'}), 403
    
    # Marcar como leída
    Notificacion.marcar_como_leida(id)
    
    # Redireccionar a la URL de la notificación si tiene documento
    if notificacion.documento_id:
        return redirect(url_for('documentos.detalle_documento', id=notificacion.documento_id))
    
    return redirect(url_for('documentos.dashboard'))