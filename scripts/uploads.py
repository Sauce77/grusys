import os

LIMITE_UPLOADS = 3

def sobrepasa_archivo_uploads(carpeta):
    """
        Cuenta la cantidad de archivos que se encuentran en la
        carpeta ingresada. Retorna el True si la cantidad de 
        archivos es mayor al limite, de lo contrario, retorna 
        false.
    """
    num_archivos = 0
    for f in os.listdir(carpeta):
        if os.path.isfile(os.path.join(carpeta, f)):
            num_archivos += 1

            # si el numero de archivos es mayor al limite
            if num_archivos > LIMITE_UPLOADS:
                return True

    return False

def limitar_archivos_uploads(carpeta):
    """
        Limita la cantidad de archivos almacenados en la carpeta uploads.
        En caso de sobrepasar, elimina los archivos mas antiguos.
    """
    archivos = []
    for f in os.listdir(carpeta):
        if os.path.isfile(os.path.join(carpeta, f)):
            # se anade el archivo a la lista
            archivos.append(os.path.join(carpeta, f))

    # ordenar por tiempo de modificacion
    archivos.sort(key=os.path.getmtime)

    # se remueven los archivo antiguos
    while len(archivos) > LIMITE_UPLOADS:
        archivo_a_eliminar = archivos.pop(0)
        os.remove(archivo_a_eliminar)


def archivo_reciente(carpeta):
    """
        Retorna la ruta del archivo mas reciente en la carpeta
        indicada.
    """
    archivos = []
    for f in os.listdir(carpeta):
        if os.path.isfile(os.path.join(carpeta, f)):
            # se anade el archivo a la lista
            archivos.append(os.path.join(carpeta, f))

    # ordenar por tiempo de modificacion
    archivos.sort(key=os.path.getmtime)

    return archivos[-1]
