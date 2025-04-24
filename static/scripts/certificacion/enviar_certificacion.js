var authJSON = JSON.parse(authJSON);

$(document).ready(function(){

    $("#btnEnviar").on("click", function(){
        var json_respuesta = [];

        $('#tablaRegistros').DataTable().rows().every(function(rowIdx, tableLoop, rowLoop){

          // obtenemos datos de la fila actual
          var rowData = this.data();

          var respuesta = {
              "app": rowData["app"],
              "usuario": rowData["usuario"],
              "requiere_acceso": "SI",
              "comentarios": ""
          };

            // obtenemos el componente <tr>
            let fila = $(this.node());
            
            let checkbox = fila.find(".form-check-input")

            if(checkbox.length > 0){
              
              if(checkbox.is(":checked")){
                respuesta.requiere_acceso = "SI";
              }
              else{
                respuesta.requiere_acceso = "NO";
              }

            }// si contiene checkbox

            // caja de comentarios

            let textarea = fila.find("textarea");

            if(textarea.length>0){
              respuesta.comentarios = textarea.val()
            }

            json_respuesta.push(respuesta);
        });
        
        console.log(json_respuesta);
        
        // credenciales
        actToken = authJSON.token;

        //enviar peticion
        fetch('https://grc-api.onrender.com/certificacion/enviar/', {
            method: 'POST',
            headers: {
              'Accept': '*/*',
              'Content-Type': 'application/json',
              'Authorization': `Token ${actToken}`
            },
            body: JSON.stringify(json_respuesta)
          })
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error en la petición: ${response.status}`);
              }
              return response.json();
            })
            .then(data => {
              console.log('Certificacion Enviada', data);
              window.location.reload();
            })
            .catch(error => {
              console.error('Hubo un error:', error);
            });
    });// fin boton enviar
});