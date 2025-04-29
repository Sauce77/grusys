import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session, url_for

from scripts.totales import obtener_totales

routes_totales = Blueprint("totales", __name__)

API_URL_EXTRACCION = "https://grc-api.onrender.com/extraccion/"
API_URL_CERTIFICACION = "https://grc-api.onrender.com/certificacion/"

@routes_totales.route("/<app>", methods=["GET","POST"])
def root(app):

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

    return obtener_totales(registros_json)
    # tabla = obtener_totales(registros_json)
    # return render_template("totales/mostrar_totales.html",auth=auth,tabla=tabla)