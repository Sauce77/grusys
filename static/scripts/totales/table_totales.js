var datosJavaScript = JSON.parse(datosJSON);

$(document).ready(function() {

    // construir datatable
    var tabla = $('#tablaTotales').DataTable({
      data: datosJavaScript,
        columns: [
          { data: 'responsable',},
          { data: 'total_usuarios'},
          { data: 'enviado_responsable'},
          { data: 'respuesta_responsable'},
          { data: 'baja_automatica'},
          { data: 'baja_responsable'},
          { data: 'conservar_acceso'}
        ]
    });

});