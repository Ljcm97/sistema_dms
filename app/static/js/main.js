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
    $('#area_destino_id, #area_origen_id, #entrada_area_destino_id, #salida_area_origen_id').change(function() {
        const personaSelect = $(this).attr('id').replace('area', 'persona');
        cargarPersonasPorArea('#' + $(this).attr('id'), '#' + personaSelect);
    });
    
    // Cargar automáticamente personas al abrir modales
    $('#modalEntrada').on('shown.bs.modal', function() {
        cargarPersonasPorArea('#entrada_area_destino_id', '#entrada_persona_destino_id');
    });
    
    $('#modalSalida').on('shown.bs.modal', function() {
        cargarPersonasPorArea('#salida_area_origen_id', '#salida_persona_origen_id');
    });
    
    // Configurar botones de eliminación
    $('.btn-eliminar').click(function(e) {
        return confirmarEliminacion(e, '¿Está seguro de que desea eliminar este elemento? Esta acción no se puede deshacer.');
    });
});

// Función para cargar notificaciones
function cargarNotificaciones() {
    $.getJSON('/notificaciones/no-leidas', function(data) {
        const $notificacionesList = $('#notificacionesList');
        const $notificacionesCount = $('#notificacionesCount');
        const $noNotificaciones = $('#noNotificaciones');
        
        // Limpiar lista excepto encabezado y divisor
        $notificacionesList.find('li:not(.dropdown-header):not(.dropdown-divider)').remove();
        
        if (data.length > 0) {
            $notificacionesCount.text(data.length).show();
            $noNotificaciones.hide();
            
            // Agregar notificaciones
            data.forEach(function(notificacion) {
                const $item = $('<li>').addClass('dropdown-item notification-item');
                const $link = $('<a>').attr('href', notificacion.url)
                    .addClass('text-dark text-decoration-none')
                    .data('id', notificacion.id);
                
                const $content = $('<div>').addClass('d-flex flex-column');
                $content.append($('<small>').addClass('text-muted').text(notificacion.fecha));
                const $content = $('<div>').addClass('d-flex flex-column');
                $content.append($('<small>').addClass('text-muted').text(notificacion.fecha));
                $content.append($('<span>').text(notificacion.mensaje));
                
                $link.append($content);
                $item.append($link);
                $notificacionesList.append($item);
                
                // Agregar evento para marcar como leída
                $link.click(function(e) {
                    $.get('/notificaciones/marcar-leida/' + notificacion.id);
                });
            });
        } else {
            $notificacionesCount.hide();
            $noNotificaciones.show();
        }
    });
}

// Inicialización cuando el documento está listo
$(document).ready(function() {
    // Código existente...
    
    // Cargar notificaciones al iniciar
    cargarNotificaciones();
    
    // Cargar notificaciones cada 30 segundos
    setInterval(cargarNotificaciones, 30000);
});