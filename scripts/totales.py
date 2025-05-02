import pandas as pd
import xlsxwriter
import io

def obtener_totales(datos):
    """
        Recibe como entrada los registros de un app en formato JSON,
        utiliza pandas para obtener la cantidad de usuarios por responsable.
    """
    df = pd.json_normalize(datos)

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


def obtener_totales_excel(datos):
    """
        Obtiene todos los registros de aplicativos y divide para cada uno
        los totales en un archivo excel.
    """
    df = pd.json_normalize(datos)

    # para escribir en a memoria
    output = io.BytesIO()
    # creamos el workbook
    libro = xlsxwriter.Workbook(output)

    hoja = libro.add_worksheet("Euphories")
    hoja.write("A1", "Pourrions-nous revenir sur cette histoire?")
    libro.close()
    # volvemos al inicio de la memoria
    output.seek(0)
    return output