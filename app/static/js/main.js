// Función para cargar personas por área con mejor manejo de errores y feedback visual
function cargarPersonasPorArea(selectArea, selectPersona) {
    const areaId = $(selectArea).val();
    const $personaSelect = $(selectPersona);
    
    // Mostrar indicador de carga
    $personaSelect.prop('disabled', true);
    $personaSelect.empty(); // Limpiar opciones existentes
    $personaSelect.append('<option value="">Cargando personas...</option>');
    
    // Verificar que el selector de área existe y tiene un valor válido
    if (!areaId || areaId <= 0) {
        $personaSelect.empty();
        $personaSelect.append('<option value="">-- Seleccione primero un área --</option>');
        $personaSelect.prop('disabled', false);
        return;
    }
    
    console.log(`Cargando personas para área ID: ${areaId}`);
    
    // Realizar la petición AJAX con mejor manejo de errores
    $.ajax({
        url: `/api/personas-por-area/${areaId}`,
        method: 'GET',
        dataType: 'json',
        timeout: 10000, // 10 segundos de timeout
        success: function(data) {
            // Limpiar opciones existentes
            $personaSelect.empty();
            
            // Siempre agregar la opción por defecto
            $personaSelect.append('<option value="">-- Seleccione --</option>');
            
            if (data && data.length > 0) {
                // Agregar opciones de personas
                $.each(data, function(index, persona) {
                    $personaSelect.append(`<option value="${persona.id}">${persona.nombre_completo}</option>`);
                });
                console.log(`Cargadas ${data.length} personas para el área ${areaId}`);
            } else {
                // Solo agregar un mensaje de "No hay personas" si no hay datos
                console.log('No se encontraron personas para esta área');
                $personaSelect.append('<option value="" disabled>No hay personas en esta área</option>');
            }
            
            // Habilitar el selector
            $personaSelect.prop('disabled', false);
        },
        error: function(xhr, status, error) {
            console.error(`Error al cargar personas: ${error}`, xhr.responseText);
            $personaSelect.empty();
            $personaSelect.append('<option value="">-- Error al cargar personas --</option>');
            $personaSelect.prop('disabled', false);
            
            // Intentar con rutas alternativas
            fallbackLoadPersonas(areaId, $personaSelect);
        }
    });
}

// Función de respaldo para cargar personas cuando falla la API principal
function fallbackLoadPersonas(areaId, $personaSelect) {
    // Intenta usar la ruta alternativa para obtener personas
    $.ajax({
        url: `/admin/api/personas-por-area/${areaId}`,
        method: 'GET',
        dataType: 'json',
        timeout: 8000,
        success: function(data) {
            $personaSelect.empty();
            $personaSelect.append('<option value="">-- Seleccione --</option>');
            
            if (data && data.length > 0) {
                $.each(data, function(index, persona) {
                    $personaSelect.append(`<option value="${persona.id}">${persona.nombre_completo || persona.nombre}</option>`);
                });
            } else {
                $personaSelect.append('<option value="" disabled>No hay personas en esta área</option>');
            }
            $personaSelect.prop('disabled', false);
        },
        error: function() {
            // Si también falla, intenta con la última ruta de respaldo
            hacerCargaManual(areaId, $personaSelect);
        }
    });
}

// Función de respaldo para cargar personas utilizando fetch y la ruta de admin
function hacerCargaManual(areaId, $personaSelect) {
    console.log("Intentando carga manual para el área: " + areaId);
    
    $personaSelect.empty();
    $personaSelect.append('<option value="">-- Seleccione --</option>');
    
    // Intentamos una solución alternativa usando fetch
    fetch(`/personas_api/personas-por-area/${areaId}`)
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('No se pudo obtener datos de respaldo');
    })
    .then(data => {
        if (data && data.length > 0) {
            data.forEach(persona => {
                $personaSelect.append(`<option value="${persona.id}">${persona.nombre_completo}</option>`);
            });
        } else {
            $personaSelect.append('<option value="" disabled>No hay personas disponibles</option>');
        }
    })
    .catch(error => {
        console.error('Error en carga manual:', error);
        $personaSelect.append('<option value="" disabled>No se pudieron cargar personas</option>');
    })
    .finally(() => {
        $personaSelect.prop('disabled', false);
    });
}

// Funciones para confirmar acciones importantes
function confirmarEliminacion(event, mensaje = '¿Está seguro de que desea eliminar este elemento?') {
    if (!confirm(mensaje)) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Función para cargar notificaciones con mejor manejo de errores y feedback
function cargarNotificaciones() {
    console.log("Cargando notificaciones...");
    
    // Mostrar indicador de carga
    $('#notificacionesLoading').show();
    $('#noNotificaciones').hide();
    $('#notificacionesList').empty();
    
    $.ajax({
        url: '/notificaciones/no-leidas',
        type: 'GET',
        dataType: 'json',
        timeout: 5000,
        success: function(data) {
            console.log("Notificaciones recibidas:", data);
            
            const $notificacionesList = $('#notificacionesList');
            const $notificacionesCount = $('#notificacionesCount');
            const $notificacionesTotalCount = $('#notificacionesTotalCount');
            const $noNotificaciones = $('#noNotificaciones');
            
            // Ocultar indicador de carga
            $('#notificacionesLoading').hide();
            
            // Actualizar contadores
            if (data && data.length > 0) {
                $notificacionesCount.text(data.length).show();
                $notificacionesTotalCount.text(data.length);
                $noNotificaciones.hide();
                
                // Agregar notificaciones
                data.forEach(function(notificacion) {
                    const $item = $('<li>').addClass('dropdown-item notification-item unread');
                    const $link = $('<a>').attr('href', notificacion.url)
                        .addClass('notification-link')
                        .data('id', notificacion.id);
                    
                    const $content = $('<div>').addClass('notification-content');
                    $content.append($('<div>').addClass('notification-message').text(notificacion.mensaje));
                    $content.append($('<div>').addClass('notification-time').text(notificacion.fecha));
                    
                    $link.append($content);
                    $item.append($link);
                    $notificacionesList.append($item);
                });
                
                // Agregar evento para marcar como leída
                $('.notification-link').click(function(e) {
                    const id = $(this).data('id');
                    console.log("Marcando como leída la notificación:", id);
                    $.get('/notificaciones/marcar-leida/' + id);
                });
            } else {
                $notificacionesCount.hide();
                $notificacionesTotalCount.text("0");
                $noNotificaciones.show();
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al cargar notificaciones:", status, error);
            $('#notificacionesLoading').hide();
            $('#noNotificaciones').text('Error al cargar notificaciones').show();
        }
    });
}

// Función para actualizar solo el contador de notificaciones
function actualizarContadorNotificaciones() {
    $.ajax({
        url: '/notificaciones/count',
        type: 'GET',
        dataType: 'json',
        timeout: 3000,
        success: function(data) {
            const $notificacionesCount = $('#notificacionesCount');
            if (data.count > 0) {
                $notificacionesCount.text(data.count).show();
            } else {
                $notificacionesCount.hide();
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al actualizar contador de notificaciones:", status, error);
        }
    });
}

// Inicialización de eventos para notificaciones
$(document).ready(function() {
    // ... otras inicializaciones ...
    
    // Iniciar carga de notificaciones
    setTimeout(cargarNotificaciones, 1000);
    
    // Actualizar contador cada 30 segundos
    setInterval(actualizarContadorNotificaciones, 30000);
    
    // Cargar notificaciones completas cada 2 minutos
    setInterval(cargarNotificaciones, 120000);
    
    // Cargar notificaciones al hacer clic en el icono
    $('#notificacionesLink').click(function() {
        cargarNotificaciones();
    });
});

// Refresca el contador de notificaciones cada minuto sin recargar toda la lista
function actualizarContadorNotificaciones() {
    $.getJSON('/notificaciones/count', function(data) {
        const $notificacionesCount = $('#notificacionesCount');
        if (data.count > 0) {
            $notificacionesCount.text(data.count).show();
        } else {
            $notificacionesCount.hide();
        }
    });
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
    
    // Cargar automáticamente personas al abrir modales o cuando la página se carga con valores predeterminados
    if ($('#area_destino_id').length && $('#area_destino_id').val() > 0) {
        cargarPersonasPorArea('#area_destino_id', '#persona_destino_id');
    }
    
    if ($('#area_origen_id').length && $('#area_origen_id').val() > 0) {
        cargarPersonasPorArea('#area_origen_id', '#persona_origen_id');
    }
    
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
    
    // Cargar notificaciones al iniciar
    cargarNotificaciones();
    
    // Actualizar contador cada 30 segundos
    setInterval(actualizarContadorNotificaciones, 30000);
    
    // Recargar notificaciones completas cada 2 minutos
    setInterval(cargarNotificaciones, 120000);
    
    // Cargar notificaciones al hacer clic en el icono
    $('#notificacionesLink').click(function() {
        cargarNotificaciones();
    });
});

// Asegurar que los selects siempre se abran hacia abajo
$(document).ready(function() {
    // Prevenir que los selects se abran hacia arriba
    $('.form-select').on('shown.bs.select', function() {
        var dropdownMenu = $(this).next('.dropdown-menu');
        dropdownMenu.css({
            'top': '100%',
            'bottom': 'auto',
            'transform': 'none'
        });
    });
});