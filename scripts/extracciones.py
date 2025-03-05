import openpyxl
import pandas as pd
import os

def comprobar_columnas(columnas, columnas_buscar=["Nombre","Usuario","APP","Responsable"]):
    """
        Compara el nombre de las columnas del archivo, en caso de que no encuentre los nombres
        de columna en 'columnas_buscar' retorna False.
    """
    return set(columnas_buscar).issubset(set(columnas))

def archivo_json(ruta):
    """
        Convierte el archivo validado a un formato json.
    """
    messages = [] # se enlistan los posibles problemas al leer el archivo
    data_json = {} # se enlista la informacion contenida en el archivo

    ruta = os.path.abspath(ruta)

    archivo = openpyxl.load_workbook(ruta, read_only=True)

    for nombre_hoja in archivo.sheetnames:
        # para cada hoja en el archivo

        df = pd.read_excel(ruta, sheet_name=nombre_hoja)
        
        columnas = df.columns # obtiene el nombre de columnas de la hoja

        if comprobar_columnas(columnas):
            # en caso de que el nombre de las columnas coincida
            data_json[nombre_hoja] = df.to_json(orient="index")

        else:
            # en caso de que faltaran columnas en la hoja
            messages.append(f"{nombre_hoja} no ha podido ser convertida. Verifique el formato utilizado.")

    messages.append("Archivo procesado!")

    return data_json, messages
        