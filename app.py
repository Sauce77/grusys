import os
import requests
import json
from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from forms import LoginForm

from endpoints.admins import routes_admins
from endpoints.certificacion import routes_certificacion
from endpoints.totales import routes_totales

API_URL = "https://grc-api.onrender.com/"

app = Flask(__name__)
app.config["SECRET_KEY"] = "Famous" # os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# registrar modulos de rutas
app.register_blueprint(routes_admins, url_prefix='/admins')
app.register_blueprint(routes_certificacion, url_prefix='/certificacion')
app.register_blueprint(routes_totales, url_prefix="/totales")

@app.route("/" , methods=["GET","POST"])
def index():
    """
        Muestra landing page de aplicacion
    """
    user = session.get("user")
    return render_template("index.html", auth=user)

@app.route("/login", methods=["GET","POST"])
def login_user():
    """
        Autentificar un usuario medinate username, password.
        Retorna: JWT
    """
    form= LoginForm()

    url = API_URL + "accounts/login/"

    if request.method == 'POST':
    # Lógica para peticiones POST
        try:
            datos_formulario = request.form # Obtiene los datos del cuerpo de la petición
            datos_json = {key: value for key, value in datos_formulario.items()}
            
            response = requests.post(url, json=datos_json)
            response.raise_for_status()

            login_json = response.json()

            session["user"] = login_json
            
            return redirect(url_for('index'))

        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), response.status_code if hasattr(response, 'status_code') else 500

    return render_template('accesos/login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)