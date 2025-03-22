import re

def col_fecha_creacion(columna):
    """ 
        Determina si el nombre de la columna corresponde con las variaciones de "Fecha Creacion"
    """
    patron = re.compile(r"(fecha.*creaci(ó|o)n)", re.IGNORECASE)
    if patron.search(columna):
        return True
    return False

def col_ultimo_acceso(columna):
    """ 
        Determina si el nombre de la columna corresponde con las variaciones de "Ultimo Acceso"
    """
    patron = re.compile(r"((ú|u)ltimo.*acceso)", re.IGNORECASE)
    if patron.search(columna):
        return True
    return False

def col_requiere_acceso(columna):
    """ 
        Determina si el nombre de la columna corresponde con las variaciones de "Requiere Acceso"
    """
    patron = re.compile(r"(requiere.*acceso)", re.IGNORECASE)
    if patron.search(columna):
        return True
    return False