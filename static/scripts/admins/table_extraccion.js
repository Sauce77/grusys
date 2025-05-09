var datosJavaScript = JSON.parse(datosJSON);

$(document).ready(function() {

    // construir datatable
    var tabla = $('#tablaExtraccion').DataTable({
      data: datosJavaScript,
        columns: [
          { data: 'app' , name: 'app'},
          { data: 'nombre', name: 'nombre'},
          { data: 'usuario', name: 'usuario'},
          { data: 'estatus', name: 'estatus' },
          { data: 'perfil', name: 'perfil' },
          { data: 'fecha_creacion',
            render: function (data, type, row) {
              // Asigna un valor único al checkbox, por ejemplo, el ID del registro
              if(data === null){
                return 'No disponible';  
              }
              else{
                return data
              }
            }
          },
          { data: 'ultimo_acceso',
            render: function (data, type, row) {
              // Asigna un valor único al checkbox, por ejemplo, el ID del registro
              if(data === null){
                return 'No disponible';  
              }
              else{
                return data
              }
            }
          },
          { data: 'responsable', name: 'responsable' },
          { data: 'requiere_acceso', name: 'requiere_acceso' },
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
              $(row).css('background-color', '#E8785F');
            }
            else if(data.exenta_baja === true){
              $(row).css('background-color', 'lightblue');
            }
          
          }
    });
});