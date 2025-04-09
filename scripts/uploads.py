import os
from flask import current_app
from werkzeug.utils import secure_filename

LIMITE_UPLOADS = 3

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

    # si el numero de archivos es menor al limite
    if len(archivos) < LIMITE_UPLOADS:
        return 
    
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

def subir_archivo(file, carpeta):
    """
        Recibe un archivo como parametro, en caso de poder subirse
        se retorna la ruta del archivo subido
    """
    if file.filename == "":
        return "No valid."
    
    filename = secure_filename(file.filename)
    # se construye la ruta de la carpeta a subir
    folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], carpeta)
    # crea las carpetas en caso de que no existan
    os.makedirs(folder_path, exist_ok=True)
    # construimos la ruta completa al archivo
    file_path = os.path.join(folder_path, filename)
    # guardamos el archivo en la ruta completa
    file.save(file_path)

    limitar_archivos_uploads(folder_path)

    return file_path