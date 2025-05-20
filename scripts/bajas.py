import pandas as pd
import xlsxwriter
from xlsxwriter.utility import cell_autofit_width
import io
import datetime

def formato_bajas(hoja, formatos, df_bajas, app):
    """
        Ingresa las bajas del dataframe dentro de la
        hoja de
    """
    # obtenemos el año actual
    anio_actual = datetime.datetime.now().year

    # agregamos encabezado
    hoja.write(0, 5, "Nissan Renault Finance Mexico", formatos["titulo"])
    hoja.write(1, 5, app, formatos["titulo"])
    hoja.write(2, 5, f"Certificacion de Usuarios {anio_actual}", formatos["titulo"])
    hoja.write(3, 5, "Reporte de Bajas", formatos["titulo"])

    ancho = 0
    for index,(clave, valor) in enumerate(df_bajas.iterrows()):

        # para ajustar el ancho de columna clave
        if len(clave) > ancho:
            ancho = len(clave)

        
def obtener_bajas_excel(bajas_json):
    """
        Utiliza la información del json para constuir una libro de
        excel
    """
    df_bajas = pd.json_normalize(bajas_json)

    output = io.BytesIO()

    libro = xlsxwriter.Workbook(output)

    hoja = libro.add_worksheet("Porky")

    hoja.write(0, 0, "Porky Porky Porky")

    libro.close()

    # volvemos al inicio de la memoria
    output.seek(0)
    return output
    