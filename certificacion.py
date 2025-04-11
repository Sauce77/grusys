from flask import Blueprint, render_template, session, redirect, url_for
import requests

routes_certificacion = Blueprint("certificacion", __name__)

API_URL = "https://grc-api.onrender.com/extraccion/"

@routes_certificacion.route("/", methods=["GET", "POST"])
def root():
    return "Certificacion"

@routes_certificacion.route("/<app>")
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
    url = API_URL + "registros/" + app + "/" + username
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    registros_json = respuesta.json()

    # peticion para aplicativos
    url = API_URL + "apps"
    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()  # Lanza una excepción para códigos de error 4xx o 5xx
    apps_json = respuesta.json()

    return render_template("registros.html", auth=auth, registros=registros_json, apps=apps_json, titulo=f"Registros {app}")