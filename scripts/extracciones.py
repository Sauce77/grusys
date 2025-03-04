import openpyxl
import pandas as pd

def comprobar_columnas(columnas, columnas_buscar=["Nombre","Usuario","APP","Responsable"]):
    """
        Compara el nombre de las columnas del archivo, en caso de que no encuentre los nombres
        de columna en 'columnas_buscar' retorna False.
    """
    return set(columnas_buscar).issubset(set(columnas))

def archivo_json(archivo):
    """
        Convierte el archivo validado a un formato json.
    """
    messages = [] # se enlistan los posibles problemas al leer el archivo

    data_json = []

    archivo = openpyxl.load_workbook(archivo, read_only=True)

    for nombre_hoja in archivo.sheetnames:
        # para cada hoja en el archivo

        df = pd.read_excel(archivo, sheet_name=nombre_hoja)
        
        columnas = df.columns # obtiene el nombre de columnas de la hoja

        if comprobar_columnas(columnas):
            # en caso de que el nombre de las columnas coincida
            data_json.append(df.to_json)

        else:
            # en caso de que faltaran columnas en la hoja
            messages.append(f"{nombre_hoja} no ha podido ser convertida. Verifique el formato utilizado.")

    messages.append("Archivo procesado!")

    return data_json, messages
        