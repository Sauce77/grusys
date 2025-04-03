import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session, url_for
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
    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

    url = API_URL + "all/"

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx

    datos_json = respuesta.json()
    return render_template("registros.html", auth=auth, data=datos_json, titulo="Todos los registros")


@routes_admin_user.route("/registros/<app>")
def mostrar_app_registros(app):
    """
        Muestra usuarios separados por aplicativo.
    """

    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

    url = API_URL + "registros/" + app

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx

    datos_json = respuesta.json()
    return render_template("registros.html", auth=auth, data=datos_json)

@routes_admin_user.route("/extraccion", methods=["GET","POST"])
def subir_extraccion():
    """
        Solicita la extraccion para cargar los usuarios.
        Valida un excel y envia la peticion en JSON al API.
    """
    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

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

            extraccion_json, messages = archivo_json(file_path)
        
            # cabecera utilizada para la peticion
            headers = {
                'Authorization': f'Token {auth["token"]}',
                'Content-Type': 'application/json'
            }

            url = API_URL + "insertar/"
            response = requests.post(url, headers=headers, json=extraccion_json)
            
            if response.status_code == 200:
                return response.content
            
            return response.content
            
        if sobrepasa_archivo_uploads(current_app.config['UPLOAD_FOLDER']):
            limitar_archivos_uploads(current_app.config['UPLOAD_FOLDER'])

    return render_template('subir_extraccion.html', form=form, auth=auth)