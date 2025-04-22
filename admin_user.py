import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session, url_for
from werkzeug.utils import secure_filename

from forms import SubirExtraccionForm
from scripts.extracciones import archivo_extraccion_json, archivo_exentas_json
from scripts.uploads import subir_archivo

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

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    # peticion para registros
    url = API_URL + "registros/"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_URL + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("admins/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo="Todos los registros")


@routes_admin_user.route("/registros/<app>")
def mostrar_app_registros(app):
    """
        Muestra usuarios separados por aplicativo.
    """

    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    # peticion para registros
    url = API_URL + "registros/app/" + app
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_URL + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("admins/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo=f"Registros {app}")

@routes_admin_user.route("admins/extraccion.html", methods=["GET","POST"])
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

        file = request.files.get("file")
        
        # si el archivo esta vacio 
        if file is None:
            return redirect(url_for('subir_extraccion'))

        # obtenemos la ruta del archivo
        file_path = subir_archivo(file, 'extracciones')
        
        # si la direccion es valida
        if file_path != "No valid.":

            extraccion_json, messages = archivo_extraccion_json(file_path)
        
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

    return render_template('admins/subir_extraccion.html', form=form, auth=auth)

@routes_admin_user.route("/exentar", methods=["GET","POST"])
def exentar_bajas():
    """
        Recibe un archivo de word con apps y cuentas. Se modifica el valor
        exenta_bajas a true.
    """
    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))
    
    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}',
        'Content-Type': 'application/json'
    }

    # peticion para mostrar cuentas exentas
    url = API_URL + "exentas/"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    registros_json = response.json()

    form=SubirExtraccionForm()

    if request.method == "POST":
    
        file = request.files.get("file")
        
        # si el archivo esta vacio 
        if file is None:
            return redirect(url_for('exentar_bajas'))

        # obtenemos la ruta del archivo
        file_path = subir_archivo(file, 'cuentas_exentas')
        
        # si la direccion es valida
        if file_path != "No valid.":

            extraccion_json, messages = archivo_exentas_json(file_path)

            # peticion para exentar cuentas
            url = API_URL + "exentar/"
            response = requests.post(url, headers=headers, json=extraccion_json)
            
            if response.status_code == 200:
                return response.content
            
            return response.content

    return render_template('admins/exentar_bajas.html', form=form, auth=auth, registros=registros_json)
