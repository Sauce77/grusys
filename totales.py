import os
import requests
from flask import Blueprint,render_template,request, session, url_for, send_file, redirect
import io
import xlsxwriter

from scripts.totales import obtener_totales,obtener_totales_excel

routes_totales = Blueprint("totales", __name__)

API_URL_EXTRACCION = "https://grc-api.onrender.com/extraccion/"
API_URL_CERTIFICACION = "https://grc-api.onrender.com/certificacion/"

@routes_totales.route("/", methods=["GET", "POST"])
def mostrar_todos_totales():
    """
        Muestra totales de todas las aplicaciones.
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

    json_total_app, json_totales_res = obtener_totales(registros_json)
        
    return render_template("totales/mostrar_totales.html",auth=auth,apps=apps_json,total_app=json_total_app,totales=json_totales_res,app="todos los Aplicativos")

@routes_totales.route("/<app>", methods=["GET","POST"])
def mostrar_app_totales(app):
    """
        Muestra totales de la aplicacion especifica.
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

    json_total_app, json_totales_res = obtener_totales(registros_json)
    return render_template("totales/mostrar_totales.html",auth=auth,apps=apps_json,total_app=json_total_app,totales=json_totales_res,app=app)


@routes_totales.route("/descargar")
def descargar_excel():
    """
        Convierte la informacion JSON de totales 
    """

    # guardamos el archivo a generar en memoria
    output = io.BytesIO()

    try:
        output = obtener_totales_excel({"prenom": "euphories"})
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='mi_archivo_generado.xlsx'
        )

    except Exception as e:
        return f"Hubo un error al descargar: {e}"