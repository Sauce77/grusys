from flask import Blueprint,render_template,request, current_app, redirect
import os
from werkzeug.utils import secure_filename

from forms import SubirExtraccionForm
from scripts.extracciones import archivo_json
from scripts.uploads import sobrepasa_archivo_uploads,limitar_archivos_uploads

routes_admin_user = Blueprint("admins", __name__)

API_URL = "https://grc-api.onrender.com/extraccion/"

@routes_admin_user.route("/", methods=["GET","POST"])
def root():
    return "Hola"

@routes_admin_user.route("/extraccion", methods=["GET","POST"])
def subir_extraccion():
    """
        Solicita la extraccion para cargar los usuarios.
        Valida un excel y envia la peticion en JSON al API.
    """
    form=SubirExtraccionForm()

    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        if sobrepasa_archivo_uploads(current_app.config['UPLOAD_FOLDER']):
            limitar_archivos_uploads(current_app.config['UPLOAD_FOLDER'])

    return render_template('subir_extraccion.html', form=form)