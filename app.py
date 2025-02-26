import os
import requests
import json
from flask import Flask, render_template, jsonify, request, redirect
from forms import LoginForm

from admin_user import routes_admin_user

API_URL = "https://grc-api.onrender.com/"

app = Flask(__name__)
app.config["SECRET_KEY"] = "Famous" # os.environ.get("SECRET_KEY")

# registrar modulos de rutas
app.register_blueprint(routes_admin_user, url_prefix='/admins')

@app.route("/" , methods=["GET","POST"])
def root():
    """
        Muestra landing page de aplicacion
    """
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login_user():
    """
        Autentificar un usuario medinate username, password.
        Retorna: JWT
    """
    formulario = LoginForm()

    url = API_URL+"accounts/login/"

    if request.method == 'POST':
    # Lógica para peticiones POST
        try:
            datos_formulario = request.form # Obtiene los datos del cuerpo de la petición
            datos_json = {key: value for key, value in datos_formulario.items()}
            
            response = requests.post(url, json=datos_json)
            response.raise_for_status()
            
            return render_template("user_info.html", data=response.json()), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), response.status_code if hasattr(response, 'status_code') else 500

    return render_template('login.html', formulario=formulario)

if __name__ == "__main__":
    app.run(debug=True)