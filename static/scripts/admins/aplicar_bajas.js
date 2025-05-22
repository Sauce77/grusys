var authJSON = JSON.parse(authJSON);

var jsonData = JSON.parse(datosJSON);

$(document).ready(function(){

    $("#btnBajas").on("click", function(){

        // credenciales
        actToken = authJSON.token;
        console.log(jsonData)

        //enviar peticion
        fetch('https://grc-api.onrender.com/extraccion/batch/', {
            method: 'POST',
            headers: {
              'Accept': '*/*',
              'Content-Type': 'application/json',
              'Authorization': `Token ${actToken}`
            },
            body: JSON.stringify(jsonData)
          })
            .then(response => {
              if (!response.ok) {
                throw new Error(`Error en la petición: ${response.status}`);
              }
              return response.body;
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