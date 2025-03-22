import openpyxl
import numpy as np
import pandas as pd
import json
import os

from . import expreg

columnas_para_extraccion = ["nombre","usuario","app","responsable"]
columnas_para_json = ["app","responsable","area","perfil","nombre","usuario","estatus","fecha_creacion","ultimo_acceso","requiere_acceso","comentarios"]

def comprobar_columnas(columnas, columnas_buscar):
    """
        Compara el nombre de las columnas del archivo, en caso de que no encuentre los nombres
        de columna en 'columnas_buscar' retorna False.
    """
    lower_columnas = [columna.lower() for columna in columnas]
    return set(columnas_buscar).issubset(set(lower_columnas))

def serializar_timestamp(obj):
    """
        Permite serializar los objetos timestamp de pandas para ser utilizados con json.
    """
    if pd.isna(obj):
        return None 
    
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def serializar_registro(registro):
    """
        Estructura la informacion del registro para JSON.
    """
    data = {}

    for col,valor in registro.items():
        
        columna = col.lower()

        if expreg.col_fecha_creacion(columna):
            data["fecha_creacion"] = serializar_timestamp(valor)
        elif expreg.col_ultimo_acceso(columna):
            data["ultimo_acceso"] = serializar_timestamp(valor)
        elif expreg.col_requiere_acceso(columna):
            if pd.isna(valor):
                data["requiere_acceso"] = None
            else:
                data["requiere_acceso"] = valor
        else:
            # si no es un columna fecha o acceso
            if columna in columnas_para_json:
                # si la columna se encuentra en el json
                if pd.isna(valor):
                    data[columna] = None
                    
                else:
                    data[columna] = valor

    return data

def archivo_json(ruta):
    """
        Convierte el archivo validado a un formato json.
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
        