from flask import Blueprint, jsonify, current_app
from flask_login import login_required
from app.models.persona import Persona
from app import db

# Crear blueprint
personas_api_bp = Blueprint('personas_api', __name__, url_prefix='/api')

@personas_api_bp.route('/personas-por-area/<int:area_id>')
@login_required
def personas_por_area(area_id):
    """
    API para obtener las personas de un área específica
    """
    try:
        # Usar una consulta más detallada y agregar logging
        current_app.logger.info(f"Buscando personas para el área ID: {area_id}")
        
        # Verificar si el área existe
        from app.models.area import Area
        area = Area.query.get(area_id)
        if not area:
            current_app.logger.warning(f"El área con ID {area_id} no existe")
            return jsonify([])
            
        personas = Persona.query.filter_by(area_id=area_id, activo=True).order_by(Persona.nombre, Persona.apellido).all()
        
        # Agregar logging para depuración
        current_app.logger.info(f"Se encontraron {len(personas)} personas para el área {area.nombre} (ID: {area_id})")
        
        result = []
        for p in personas:
            current_app.logger.debug(f"Persona: {p.id} - {p.nombre} {p.apellido} - Área: {p.area_id}")
            result.append({
                'id': p.id,
                'nombre_completo': f"{p.nombre} {p.apellido}"
            })
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error al obtener personas por área: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    
@personas_api_bp.route('/diagnostico-personas')
@login_required
def diagnostico_personas():
    """
    Endpoint para diagnóstico - muestra todas las personas y sus áreas
    """
    try:
        from app.models.area import Area
        
        # Obtener todas las áreas
        areas = Area.query.all()
        areas_data = {area.id: area.nombre for area in areas}
        
        # Obtener todas las personas
        personas = Persona.query.all()
        
        result = {
            'total_personas': len(personas),
            'areas': {area_id: {'nombre': nombre, 'personas': []} for area_id, nombre in areas_data.items()},
            'personas_sin_area': []
        }
        
        # Organizar personas por área
        for persona in personas:
            persona_data = {
                'id': persona.id,
                'nombre': persona.nombre,
                'apellido': persona.apellido,
                'nombre_completo': persona.nombre_completo,
                'area_id': persona.area_id,
                'activo': persona.activo
            }
            
            if persona.area_id in result['areas']:
                result['areas'][persona.area_id]['personas'].append(persona_data)
            else:
                result['personas_sin_area'].append(persona_data)
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error en diagnóstico de personas: {str(e)}")
        return jsonify({"error": str(e)}), 500