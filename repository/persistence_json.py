"""
=========================================================================================
MODULO: persistence_json.py
=========================================================================================

Maneja la persistencia de clientes y departamentos en archivos JSON.

FORMATO JSON:
    JSON almacena datos como lista de diccionarios:
    [{"id": 1, "nombre": "Juan", "activo": true}, {...}]

VENTAJAS: Legible, soporte nativo en Python, mantiene tipos de datos
DESVENTAJAS: Sobrescribe todo el archivo, no eficiente para grandes volumenes

=========================================================================================
"""

import json
from common.constantes import RUTA_CLIENTES, RUTA_DEPARTAMENTOS
from common.manejo_errores import manejar_error_inesperado

ENTIDAD_PERSISTENCIA_JSON = "Persistencia JSON"


def leer_datos_json_interno(ruta_archivo):
    """
    Lee datos desde un archivo JSON.
    
    PSEUDOCODIGO:
        intentar:
            abrir archivo en modo lectura
            datos = json.load(archivo)
            cerrar archivo
            retornar datos
        
        si archivo_no_existe:
            retornar []  # Primera ejecucion
        
        si error_json:
            retornar []  # Archivo corrupto
    
    Parametros:
        ruta_archivo (str): Path al archivo JSON
    
    Retorna:
        list: Datos leidos o [] si hay error
    """
    # TODO: Implementar segun pseudocodigo
    return []


def guardar_datos_json_interno(ruta_archivo, lista_datos):
    """
    Guarda datos en un archivo JSON (sobrescribe todo).
    
    PSEUDOCODIGO:
        intentar:
            abrir archivo en modo escritura
            json.dump(lista_datos, archivo, indent=4, ensure_ascii=False)
            cerrar archivo
            retornar True
        
        si error:
            retornar False
    
    Parametros:
        ruta_archivo (str): Path al archivo JSON
        lista_datos (list): Datos a guardar
    
    Retorna:
        bool: True si OK, False si error
    """
    # TODO: Implementar segun pseudocodigo
    return False


# --- API Publica ---

def leer_clientes():
    """Lee clientes desde JSON."""
    # TODO: return leer_datos_json_interno(RUTA_CLIENTES)
    return []


def guardar_clientes(lista_clientes):
    """Guarda clientes en JSON."""
    # TODO: return guardar_datos_json_interno(RUTA_CLIENTES, lista_clientes)
    return False


def leer_departamentos():
    """Lee departamentos desde JSON."""
    # TODO: return leer_datos_json_interno(RUTA_DEPARTAMENTOS)
    return []


def guardar_departamentos(lista_deptos):
    """Guarda departamentos en JSON."""
    # TODO: return guardar_datos_json_interno(RUTA_DEPARTAMENTOS, lista_deptos)
    return False


"""
INTEGRACION:

1. Al iniciar (main.py):
   clientes.clientes = persistence.leer_clientes()
   departamentos.departamentos = persistence.leer_departamentos()

2. Al salir (main.py):
   persistence.guardar_clientes(clientes.clientes)
   persistence.guardar_departamentos(departamentos.departamentos)

3. Guardado periodico (opcional):
   Despues de operaciones criticas, llamar a guardar_clientes() o guardar_departamentos()
"""