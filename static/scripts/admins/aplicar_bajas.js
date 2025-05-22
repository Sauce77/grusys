var authJSON = JSON.parse(authJSON);
var datosJavaScript = JSON.parse(datosJSON);

$(document).ready(function(){

    $("#btnBajas").on("click", function(){

        // credenciales
        actToken = authJSON.token;
        console.log(datosJavaScript)

        //enviar peticion
        fetch('https://grc-api.onrender.com/extraccion/borrar/', {
            method: 'DELETE',
            headers: {
              'Accept': '*/*',
              'Content-Type': 'application/json',
              'Authorization': `Token ${actToken}`
            },
            body: datosJavaScript
          })
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error en la petición: ${response.status}`);
              }
              return response.json();
            })
            .then(data => {
              console.log('Registros Eliminados.', data);
              window.location.reload();
            })
            .catch(error => {
              console.error('Hubo un error:', error);
            });
    });// fin boton enviar
});