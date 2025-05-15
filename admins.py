import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session, url_for
from werkzeug.utils import secure_filename

from forms import SubirExtraccionForm
from scripts.extracciones import archivo_extraccion_json, archivo_exentas_json
from scripts.uploads import subir_archivo

routes_admins = Blueprint("admins", __name__)

API_URL_EXTRACCION = "https://grc-api.onrender.com/extraccion/"
API_URL_CERTIFICACION = "https://grc-api.onrender.com/certificacion/"


@routes_admins.route("/", methods=["GET","POST"])
def root():
    return "Hola"

@routes_admins.route("/registros", methods=["GET","POST"])
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
    url = API_URL_EXTRACCION + "registros/"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_URL_EXTRACCION + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("admins/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo="Todos los registros")


@routes_admins.route("/registros/<app>")
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
    url = API_URL_EXTRACCION + "registros/app/" + app
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_URL_EXTRACCION + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("admins/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo=f"Registros {app}")

@routes_admins.route("admins/extraccion.html", methods=["GET","POST"])
def subir_extraccion():
    """
        Solicita la extraccion para cargar los usuarios.
        Valida un excel y envia la peticion en JSON al API.
    """
    auth = session.get("user")
    messages = []
    
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

            url = API_URL_EXTRACCION + "insertar/"
            response = requests.post(url, headers=headers, json=extraccion_json)

            for message in response.json().values():
                messages.append(message)

    return render_template('admins/subir_extraccion.html', form=form, auth=auth, messages=messages)

@routes_admins.route("/exentar", methods=["GET","POST"])
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
    url = API_URL_EXTRACCION + "exentas/"
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
            url = API_URL_CERTIFICACION + "exentar/"
            response = requests.post(url, headers=headers, json=extraccion_json)
            
            return redirect(url_for('admins.exentar_bajas'))

    return render_template('admins/exentar_bajas.html', form=form, auth=auth, registros=registros_json)

@routes_admins.route("/politica", methods=["GET","POST"])
def aplicar_politica():
    """
        Recibe un archivo de word con apps y cuentas. Se modifica el valor
        exenta_bajas a true.
    """
    auth = session.get("user")

    messages = []

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}',
        'Content-Type': 'application/json'
    }

    if request.method == "POST":
        
        # obtenemos el numero de dias
        dias = request.form["diasPolitica"]
        # convertimos el texto a entero
        num_dias = None
        try:
            num_dias = int(dias)
        except ValueError as e:
            messages.append("Numero ingresado invalido.")

        # obtenemos las celdas marcadas
        apps_seleccionadas = request.form.getlist("apps[]")

        json_politica = {
            "dias": num_dias,
            "apps": []
        }

        # agregamos cada app seleccionado al json_politica

        for app in apps_seleccionadas:
            json_politica["apps"].append({"nombre": app})

        url = API_URL_CERTIFICACION + "politica/"
        respuesta = requests.post(url, headers=headers, json=json_politica)
        respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    
    # peticion para aplicativos
    url = API_URL_EXTRACCION + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("admins/aplicar_politica.html",auth=auth, apps=apps_json)