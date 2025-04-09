import openpyxl
import numpy as np
import pandas as pd
import json
import os

from . import expreg

columnas_para_extraccion = ["nombre","usuario","app","responsable"]
columnas_para_json = ["app","responsable","perfil","nombre","usuario","estatus","comentarios"]

def columnas_lower(columnas):
    """
        Convierte una lista de columnas a lowercase.
    """
    return [columna.lower() for columna in columnas]

def comprobar_columnas(columnas, columnas_buscar):
    """
        Compara el nombre de las columnas del archivo, en caso de que no encuentre los nombres
        de columna en 'columnas_buscar' retorna False.
    """
    return set(columnas_buscar).issubset(set(columnas_lower(columnas)))

def serializar_timestamp(obj):
    """
        Permite serializar los objetos timestamp de pandas para ser utilizados con json.
    """
    if pd.isna(obj):
        return None 
    
    if isinstance(obj, pd.Timestamp):
        return obj.strftime('%Y-%m-%d')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def serializar_registro(registro):
    """
        Estructura la informacion del registro para JSON.
    """
    data = {
        "app": None,
        "comentarios": None,
        "en_extraccion": False,
        "estatus": "Activo",
        "fecha_creacion": None,
        "nombre": None,
        "perfil": None,
        "requiere_acceso": None,
        "responsable": None,
        "ultimo_acceso": None,
        "usuario": None
    }

    for col,valor in registro.items():

        # nombre de columna en lowercase
        columna = col.lower()

        # para cada campo en el registro
        if columna in data.keys():
            if pd.isna(valor):
                data[columna] = None
            else:
                data[columna] = valor
        
        else:
            # para columna fecha creacion
            if expreg.col_fecha_creacion(columna):
                # si encuentra, serializar el valor
                data["fecha_creacion"] = serializar_timestamp(valor)

            # para columna ultimo acceso
            if expreg.col_ultimo_acceso(columna):
                # si encuentra, serializar el valor
                data["ultimo_acceso"] = serializar_timestamp(valor)

            if expreg.col_requiere_acceso(columna):
                if pd.isna(valor):
                    data["requiere_acceso"] = None
                else:
                    data["requiere_acceso"] = valor
                

    # el registro creado se encuentra en la extraccion
    data["en_extraccion"] = True

    return data

def archivo_json(ruta):
    """
        Convierte el archivo de extraccion validado a un formato json.
    """
    messages = [] # se enlistan los posibles problemas al leer el archivo
    data_excel = [] # se enlista la informacion contenida en el archivo

    ruta = os.path.abspath(ruta)

    archivo = openpyxl.load_workbook(ruta, read_only=True)

    for nombre_hoja in archivo.sheetnames:
        # para cada hoja en el archivo

        df = pd.read_excel(ruta, sheet_name=nombre_hoja)
        
        columnas = df.columns # obtiene el nombre de columnas de la hoja

        if comprobar_columnas(columnas, columnas_para_extraccion):
            # en caso de que el nombre de las columnas coincida
            
            # obtenemos los campos para cada fila
            for index,fila in df.iterrows():
                data_excel.append(serializar_registro(fila))

        else:
            # en caso de que faltaran columnas en la hoja
            messages.append(f"{nombre_hoja} no ha podido ser convertida. Verifique el formato utilizado.")

    messages.append("Archivo procesado!")

    return data_excel, messages