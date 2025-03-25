import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session
from werkzeug.utils import secure_filename

from forms import SubirExtraccionForm
from scripts.extracciones import archivo_json
from scripts.uploads import sobrepasa_archivo_uploads,limitar_archivos_uploads,archivo_reciente

routes_admin_user = Blueprint("admins", __name__)

API_URL = "https://grc-api.onrender.com/extraccion/"

@routes_admin_user.route("/", methods=["GET","POST"])
def root():
    return "Hola"

@routes_admin_user.route("/registros", methods=["GET","POST"])
def mostrar_todos_registros():
    """
        Muestra todos los registros de la base de datos
    """
    url = API_URL + "all/"

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {session.get("Token")}'
    }

    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx

    datos_json = respuesta.json()
    return datos_json

@routes_admin_user.route("/extraccion", methods=["GET","POST"])
def subir_extraccion():
    """
        Solicita la extraccion para cargar los usuarios.
        Valida un excel y envia la peticion en JSON al API.
    """
    form=SubirExtraccionForm()

    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            data_json, messages = archivo_json(file_path)

            # cabecera utilizada para la peticion
            headers = {
                'Authorization': f'Token {session.get("Token")}',
                'Content-Type': 'application/json'
            }

            url = API_URL + "insertar/"
            response = requests.post(url, headers=headers, json=data_json)
            response.raise_for_status()
            
            if response.status_code == 200:
                return "Informacion enviada!"
            
            return "Server Error", response.status_code
            
        if sobrepasa_archivo_uploads(current_app.config['UPLOAD_FOLDER']):
            limitar_archivos_uploads(current_app.config['UPLOAD_FOLDER'])

    return render_template('subir_extraccion.html', form=form)