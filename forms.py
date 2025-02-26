from flask_wtf import FlaskForm
from flask_wtf.file import FileField
import wtforms as wtf

class LoginForm(FlaskForm):
    """
        Utilizado para verificar que un usuario ya esta registrado.
        Return: el Token del usuario si existe.
    """
    username = wtf.StringField('Cuenta Red')
    password = wtf.PasswordField('Password')
    enviar = wtf.SubmitField('Enviar') 

class SubirExtraccionForm(FlaskForm):
    """
        Recibe una archivo excel que contenga una extraccion.
    """
    file = FileField('Seleccionar archivo')
    enviar = wtf.SubmitField('Enviar')