from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import wtforms as wtf
from wtforms.validators import ValidationError
import openpyxl

class LoginForm(FlaskForm):
    """
        Utilizado para verificar que un usuario ya esta registrado.
        Return: el Token del usuario si existe.
    """
    username = wtf.StringField(render_kw={"class":"form-control"})
    password = wtf.PasswordField(render_kw={"class":"form-control"})
    enviar = wtf.SubmitField('Enviar', render_kw={"class":"btn btn-primary"}) 

class SubirExtraccionForm(FlaskForm):
    """
        Recibe una archivo excel que contenga una extraccion.
    """
    file = FileField('Seleccionar archivo')
    enviar = wtf.SubmitField('Enviar')

    def validate_file(self, field):
        if field.data:
            try:
                openpyxl.load_workbook(field.data)
            except openpyxl.utils.exceptions.InvalidFileException:
                raise ValidationError("El archivo no es compatible con Excel.")