import pandas as pd

def obtener_totales(datos):
    """
        Recibe como entrada los registros de un app en formato JSON,
        utiliza pandas para obtener la cantidad de usaurios por responsable.
    """
    df = pd.json_normalize(datos)

    # return df.to_html(index=False)

    # obtenemos los responsables
    responsables = df["responsable"].unique()

    totales = []

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
        expresion = r'BAJA POLITICA \d+ DIAS'
        filtro = df_res["comentarios"].str.contains(expresion, regex=True)
        filtro = filtro.fillna(False).astype(bool)
        total_bajas_automaticas = len(df_res[filtro])

        respuesta = {
            "responsable": responsable,
            "total_usuarios": len(df_res),
            "enviado_responsable": total_enviado_responsable,
            "respuesta_responsable": total_respuesta_responsable,
            "baja_automatica": total_bajas_automaticas
        }

        totales.append(respuesta)

    return totales