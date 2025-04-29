import os
import requests
from flask import Blueprint,render_template,request, current_app, redirect, jsonify, session, url_for

routes_totales = Blueprint("totales", __name__)

@routes_totales.route("/", methods=["GET","POST"])
def root():
    return "Totales"