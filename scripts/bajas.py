import pandas as pd
import xlsxwriter
from xlsxwriter.utility import cell_autofit_width
import io
import datetime
        
def obtener_bajas_excel(bajas_json):
    """
        Utiliza la información del json para constuir una libro de
        excel
    """
    df_bajas = pd.json_normalize(bajas_json)

    output = io.BytesIO()

    libro = xlsxwriter.Workbook(output)

    formatos = {
        "titulo1": libro.add_format({'bold':True, 'font_size': 20, 'align': 'center', 'locked': True}),
        "titulo2": libro.add_format({'bold':True, 'font_size': 16, 'align': 'center', 'locked': True}),
        "encabezado": libro.add_format({'bold':True, 'bg_color': '#000000', 'color': '#FFFFFF', 'font_size': 14, 'locked': True}),
        "baja": libro.add_format({'bg_color': '#E8785F', 'border': 1, 'font_size': 12, 'locked': True}),
        "texto": libro.add_format({'font_size': 11})
    }

    # obtenemos apps 
    apps = df_bajas["app"].unique()

    # para cada app
    for app in apps:

        # creamos una hoja para la app
        hoja = libro.add_worksheet(app)

        # obtenemos el año actual
        anio_actual = datetime.datetime.now().year

        # agregamos encabezado
        hoja.write(0, 5, "Nissan Renault Finance Mexico", formatos["titulo1"])
        hoja.write(1, 5, app, formatos["titulo2"])
        hoja.write(2, 5, f"Certificacion de Usuarios {anio_actual}", formatos["titulo2"])
        hoja.write(3, 5, "Reporte de Bajas", formatos["titulo2"])

        # obtenemos dataframe del app
        df_bajas_app = df_bajas[df_bajas["app"] == app]

        # agregamos nombres de las columnas
        nombres_columnas = ["APP", "Nombre", "Usuario", "Estatus", "Perfil", "Fecha Creacion", "Ultimo Acceso", "Responsable", "Requiere Acceso", "Comentarios"]
        
        # almacenamos ancho de columnas
        ancho_columna = []

        for index, columna in enumerate(nombres_columnas):
            # agregamos ancho de columna
            ancho_columna.append(len(columna))

            hoja.write(4, index, columna, formatos["encabezado"])


        # ingresamos valores de la fila del app
        for index_fila, fila in df_bajas_app.iterrows():

            for index_columna, columna in enumerate(nombres_columnas):

                # convertimos el nombre de la columna al de dataframe
                nombre_columna_df = columna.replace(" ","_").lower()

                # actualizamos el ancho de la columna
                if ancho_columna[index_columna] < len(fila[nombre_columna_df]):
                    ancho_columna[index_columna] = len(fila[nombre_columna_df])

                # ingresamos datos de la fila
                hoja.write(5 + index_fila, index_columna, fila[nombre_columna_df], formatos["baja"])
        
        # actualizamos los anchos de columnas
        for index, ancho in enumerate(ancho_columna):
            # ajustamos ancho de columna titulos
            hoja.set_column(index,index,ancho + 7)

    libro.close()

    # volvemos al inicio de la memoria
    output.seek(0)
    return output
    