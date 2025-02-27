from flask import Blueprint,render_template,request

from forms import SubirExtraccionForm

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

    if form.validate_on_submit():
        return "Archivo listo!"
    return render_template("subir_extraccion.html", form=form)