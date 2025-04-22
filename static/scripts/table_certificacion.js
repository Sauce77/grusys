var datosJavaScript = JSON.parse(datosJSON);
var datosJavaScript = JSON.parse(datosJSON);

$(document).ready(function() {

    // construir datatable
    var tabla = $('#tablaRegistros').DataTable({
      data: datosJavaScript,
        columns: [
          { data: 'app' , name: 'app'},
          { data: 'nombre', name: 'nombre'},
          { data: 'usuario', name: 'usuario'},
          { data: 'estatus', name: 'estatus' },
          { data: 'perfil', name: 'perfil' },
          { data: 'fecha_creacion', name: 'fecha_creacion' },
          { data: 'ultimo_acceso', name: 'ultimo_acceso' },
          { data: 'responsable', name: 'responsable' },
          { 
            data: 'requiere_acceso',
                className: 'dt-center', // Opcional: centra el contenido
                render: function (data, type, row) {
                    // Asigna un valor único al checkbox, por ejemplo, el ID del registro
                    if(data === null){
                      return '<input type="checkbox" class="form-check-input" value="' + row.usuario + '" checked>';  
                    }
                    else{
                      return data
                    }
                }
          },
          { data: 'comentarios', name: 'comentarios' },
          { data: 'en_extraccion', name: 'en_extraccion', visible: false},
          { data: 'exenta_baja', name: 'exenta_baja', visible: false},
        ],
        order: [[8, 'desc'], [10, 'asc'], [11, 'asc'], [1, 'asc']],
          rowCallback: function(row, data) {
        
            if (data.en_extraccion === false ) { 
              $(row).css('background-color', 'yellow');
            }
            else if(data.requiere_acceso === "NO"){
              $(row).css('background-color', 'red');
            }
            else if(data.exenta_baja === true){
              $(row).css('background-color', 'lightblue');
            }
          }
    });
});