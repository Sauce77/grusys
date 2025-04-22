var authJSON = JSON.parse(authJSON);

$(document).ready(function(){

    $("#btnEnviar").on("click", function(){
        var json_respuesta = [];

        $('#tablaRegistros').DataTable().rows().every(function(rowIdx, tableLoop, rowLoop){
            // obtenemos datos de la fila actual
            var rowData = this.data();

            // obtenemos el componente <tr>
            let $fila = $(this.node());

            // obtenemos el valor del acceso
            var acceso = "SI";
            
            let checkbox = $fila.find('.form-check-input');

            if(checkbox!==null){

                if (checkbox.is(':checked') === false){
                    acceso = "NO";
                }// fin if checked
    
                let textarea = $fila.find('textarea');
                
                var comentarios = textarea.val();
    
                var respuesta = {
                    "app": rowData["app"],
                    "usuario": rowData["usuario"],
                    "requiere_acceso": acceso,
                    "comentarios": comentarios
                };
                
            }

            json_respuesta.push(respuesta);
        });
        

        //enviar peticion
        fetch('https://grc-api.onrender.com/certificacion/enviar/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Token '+authJSON.token
            },
            body: JSON.stringify(json_respuesta),
          })
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error en la petición: ${response.status}`);
              }
              return response.json();
            })
            .then(data => {
              console.log('Certificacion Enviada', data);
            })
            .catch(error => {
              console.error('Hubo un error:', error);
            });
    });// fin boton enviar
});