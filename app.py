import os
import requests
import json
from flask import Flask, render_template, jsonify, request
from forms import LoginForm

API_URL = "https://grc-api.onrender.com/"

app = Flask(__name__)
app.config["SECRET_KEY"] = "Famous" # os.environ.get("SECRET_KEY")

@app.route("/" , methods=["GET","POST"])
def root():
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

    return render_template('index.html', formulario=formulario)

if __name__ == "__main__":
    app.run(debug=True)