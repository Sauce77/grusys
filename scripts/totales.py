import pandas as pd
import xlsxwriter
from xlsxwriter.utility import cell_autofit_width
import io

def obtener_totales(df):
    """
        Recibe como entrada los registros de un app en formato JSON,
        utiliza pandas para obtener la cantidad de usuarios por responsable.
    """
    # obtenemos totales de aplicacion

    # obtenemos el numero de usuarios a certificar
    # necesita agregar campo enviado_responsable a los registros
    total_respuestas_app = len(df["requiere_acceso"].isnull())

    # obtenemos bajas automaticas de aplicacion
    expresion_baja_politica = r'BAJA POLITICA \d+ DIAS'
    filtro_bajas_politica = df["comentarios"].str.contains(expresion_baja_politica, regex=True, na=False)
    total_bajas_automaticas_app = len(df[filtro_bajas_politica])

    # obtenemos bajas responsable de aplicacion
    df_bajas = df[df["requiere_acceso"]=="NO"]
    total_bajas_responsable_app = len(df_bajas[~filtro_bajas_politica])

    total_app = {
        "total_usuarios": len(df),
        "total_respuestas": total_respuestas_app,
        "bajas_automaticas": total_bajas_automaticas_app,
        "bajas_responsable": total_bajas_responsable_app
    }

    # obtenemos los responsables
    responsables = df["responsable"].unique()

    total_responsables = []

    for responsable in responsables:

        # filtramos el df para cada responsable
        df_res = df[df["responsable"]==responsable]

        # obtenemos el numero de usuarios a certificar
        # necesita agregar campo enviado_responsable a los registros
        total_enviado_responsable = len(df_res["requiere_acceso"].isnull())

        # obtenemos el numero de respuestas del responsable
        total_respuesta_responsable = len(df_res["requiere_acceso"].isnull())

        # obtenemos el total de bajas automaticas
        # revisamos si los comentarios coincide con BAJA POLITICA n DIAS
        expresion_baja_politica = r'BAJA POLITICA \d+ DIAS'
        filtro_bajas_politica = df_res["comentarios"].str.contains(expresion_baja_politica, regex=True, na=False)
        total_bajas_automaticas = len(df_res[filtro_bajas_politica])

        # obtenemos el total de bajas responsable
        df_bajas_res = df_res[df_res["requiere_acceso"]=="NO"]
        total_bajas_responsable = len(df_bajas_res[~filtro_bajas_politica])

        # obtenemos total conservar acceso
        total_conservar_acceso = len(df_res[df_res["requiere_acceso"]=="SI"])

        respuesta = {
            "responsable": responsable,
            "total_usuarios": len(df_res),
            "enviado_responsable": total_enviado_responsable,
            "respuesta_responsable": total_respuesta_responsable,
            "baja_automatica": total_bajas_automaticas,
            "baja_responsable": total_bajas_responsable,
            "conservar_acceso": total_conservar_acceso
        }

        total_responsables.append(respuesta)

    return total_app, total_responsables

def formato_totales(hoja, formatos, total_app, totales_responsables):
    """
        Ingresa los totales de la aplicacion en un formato
        de la hoja elegida.
    """
    
    ancho = 0
    for index,(clave, valor) in enumerate(total_app.items()):

        # para ajustar el ancho de columna clave
        if len(clave) > ancho:
            ancho = len(clave)

        # titulo sin guion bajo y en mayusculas
        titulo = clave.replace("_"," ").upper()

        # ingresamos titulo
        hoja.write(index+1, 0, titulo, formatos["titulo"])
        # ingresamos cifra
        hoja.write(index+1, 2, valor, formatos["cifra"])

    # ajustamos ancho de columna titulos
    hoja.set_column(0,0,ancho+7)

    # agregamos el encabezado
    for index in range(4):
        hoja.write(6, index, "", formatos["encabezado"])
    hoja.write_string(6, 0, "Responsable", formatos["encabezado"])

    # agrega resultados por responsable

    # obtenemos el numero de resultados por responsable
    filas_responsable = len(totales_responsables[0])

    for index,total in enumerate(totales_responsables):

        hoja.write(8+(index*filas_responsable), 0, total["responsable"], formatos["texto"])
        for index_fila, (clave, valor) in enumerate(total.items()):

            if clave == "responsable":
                continue

            hoja.write(8+(index*filas_responsable)+index_fila-1, 2, valor, formatos["cifra"])

def obtener_totales_excel(registros_json):
    """
        Obtiene todos los registros de aplicativos y divide para cada uno
        los totales en un archivo excel.
    """
    df_registros = pd.json_normalize(registros_json)

    # para escribir en a memoria
    output = io.BytesIO()
    # creamos el workbook
    libro = xlsxwriter.Workbook(output)

    formatos = {
        "titulo": libro.add_format({'bold':True, 'bg_color': '#E8E8E8', 'font_size': 12}),
        "encabezado": libro.add_format({'bg_color': '#000000', 'color': '#FFFFFF', 'font_size': 14}),
        "cifra": libro.add_format({'bg_color': '#B4CBFB', 'border': 1, 'font_size': 12}),
        "texto": libro.add_format({'font_size': 11})
    }

    # Se registran los totales de toda la extraccion
    hoja = libro.add_worksheet("Extraccion")

    totales_todo, totales_todo_responsable = obtener_totales(df_registros)

    formato_totales(hoja, formatos, totales_todo, totales_todo_responsable)

    # obtenemos el nombre de las apps
    apps = df_registros["app"].unique()

    # una hoja para cada app de totales
    for app in apps:
        # filtramos registro por aplicacion
        df_app = df_registros[df_registros["app"] == app]

        # obtenemos totales del app
        totales_app, totales_app_responsable = obtener_totales(df_app)

        # creamos hoja de la app
        hoja = libro.add_worksheet(app)

        # insertamos formato totales
        formato_totales(hoja,formatos,totales_app,totales_app_responsable)


    libro.close()
    # volvemos al inicio de la memoria
    output.seek(0)
    return output