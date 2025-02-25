import os
import requests
import json
from flask import Flask, render_template, jsonify
from forms import LoginForm

API_URL = "https://grc-api.onrender.com/accounts/login/"

app = Flask(__name__)
app.config["SECRET_KEY"] = "Famous" # os.environ.get("SECRET_KEY")

@app.route("/" , methods=["GET","POST"])
def root():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        datos = {
            "username": formulario.username.data,
            "password": formulario.password.data
        }
        
        json_data = jsonify(datos)

        headers = {'Content-Type': 'application/json'}
        respuesta = requests.post(API_URL, data=json_data, headers=headers)
    
        respuesta.raise_for_status()

        return respuesta.text

        


    return render_template('index.html', formulario=formulario)

if __name__ == "__main__":
    app.run(debug=True)