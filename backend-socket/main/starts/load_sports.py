import importlib.util
import os

def load_sports():
    modulos_dir = 'main/models/sports_dicts'
    sports = []


    # Recorre los archivos en el directorio de módulos
    for archivo_nombre in os.listdir(modulos_dir):
        # Comprueba si el archivo es un archivo de Python
        if archivo_nombre.endswith('.py'):
            # Ruta completa al archivo
            ruta_archivo = os.path.join(modulos_dir, archivo_nombre)
            # Nombre del módulo (sin la extensión .py)
            nombre_modulo = os.path.splitext(archivo_nombre)[0]
            # Especifica la ubicación del módulo
            especificacion_modulo = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
            # Carga el módulo
            modulo = importlib.util.module_from_spec(especificacion_modulo)
            especificacion_modulo.loader.exec_module(modulo)
            # Agrega el diccionario de deporte a la lista
            sports.append(getattr(modulo, nombre_modulo))

    # Imprime la lista de diccionarios de deportes

    sports_name_list = []
    for sport in sports:
        sports_name_list.append(list(sport.keys())[0])

    # print(sports_name_list)

    return sports, sports_name_list