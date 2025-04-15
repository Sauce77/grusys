from flask import Blueprint, render_template, session, redirect, url_for
import requests

routes_certificacion = Blueprint("certificacion", __name__)

API_EXTRACCION_URL = "https://grc-api.onrender.com/extraccion/"
API_CERTIFICACION_URL = "https://grc-api.onrender.com/certificacion/"

@routes_certificacion.route("/", methods=["GET", "POST"])
def root():
    return "Certificacion"

@routes_certificacion.route("/registros", methods=["GET", "POST"])
def mostrar_todos_certificacion():
    """
        Muestra todos los registros correspondientes al usuario.
    """

    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    # obtenemos el username de la sesion actual
    data_usuario = auth.get("user")
    username = data_usuario.get("username")

    # peticion para registros
    url = API_CERTIFICACION_URL + "registros/user/" + username
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_EXTRACCION_URL + "apps/" + username
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("certificacion/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo=f"Todos los registros")

@routes_certificacion.route("/registros/<app>", methods=["GET", "POST"])
def mostrar_app_certificacion(app):
    """
        Muestra usuarios separados por aplicativo correspondientes
        al usuario.
    """

    auth = session.get("user")

    if not auth:
        return redirect(url_for('login_user'))

    # cabecera utilizada para la peticion
    headers = {
        'Authorization': f'Token {auth["token"]}'
    }

    # obtenemos el username de la sesion actual
    data_usuario = auth.get("user")
    username = data_usuario.get("username")

    # peticion para registros
    url = API_CERTIFICACION_URL + "registros/" + app + "/" + username
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_EXTRACCION_URL + "apps/" + username
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("certificacion/registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo=f"Registros {app}")