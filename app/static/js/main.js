// Función para cargar personas por área
function cargarPersonasPorArea(selectArea, selectPersona) {
    const areaId = $(selectArea).val();
    if (areaId > 0) {
        $.getJSON(`/api/personas-por-area/${areaId}`, function(data) {
            const $personaSelect = $(selectPersona);
            $personaSelect.empty();
            $personaSelect.append('<option value="0">-- Seleccione --</option>');
            
            $.each(data, function(index, persona) {
                $personaSelect.append(`<option value="${persona.id}">${persona.nombre}</option>`);
            });
        });
    } else {
        $(selectPersona).empty();
        $(selectPersona).append('<option value="0">-- Seleccione --</option>');
    }
}

// Funciones para confirmar acciones importantes
function confirmarEliminacion(event, mensaje = '¿Está seguro de que desea eliminar este elemento?') {
    if (!confirm(mensaje)) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Inicialización cuando el documento está listo
$(document).ready(function() {
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Configurar selectores dependientes de área-persona
    $('#area_destino_id, #area_origen_id').change(function() {
        const personaSelect = $(this).attr('id').replace('area', 'persona');
        cargarPersonasPorArea('#' + $(this).attr('id'), '#' + personaSelect);
    });
    
    // Configurar botones de eliminación
    $('.btn-eliminar').click(function(e) {
        return confirmarEliminacion(e, '¿Está seguro de que desea eliminar este elemento? Esta acción no se puede deshacer.');
    });
});