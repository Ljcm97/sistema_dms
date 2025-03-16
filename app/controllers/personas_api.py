from flask import Blueprint, jsonify
from flask_login import login_required
from app.models.persona import Persona

# Crear blueprint
personas_api_bp = Blueprint('personas_api', __name__, url_prefix='/api')

@personas_api_bp.route('/personas-por-area/<int:area_id>')
@login_required
def personas_por_area(area_id):
    """
    API para obtener las personas de un área específica
    """
    personas = Persona.query.filter_by(area_id=area_id, activo=True).order_by(Persona.nombre, Persona.apellido).all()
    return jsonify([{
        'id': p.id,
        'nombre_completo': p.nombre_completo
    } for p in personas])