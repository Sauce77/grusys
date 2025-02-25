from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    """
        Utilizado para verificar que un usuario ya esta registrado.
        Return: el Token del usuario si existe.
    """
    username = StringField('CuentaRed')
    password = PasswordField('Password')
    enviar = SubmitField('Enviar') 