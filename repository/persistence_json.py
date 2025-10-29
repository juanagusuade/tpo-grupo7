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
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        # Primera ejecución, archivo no existe todavía
        return []
    except json.JSONDecodeError:
        # Archivo corrupto o vacío
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_JSON, "leer datos JSON", "Archivo JSON corrupto")
        return []
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_JSON, "leer datos JSON", f"Error inesperado: {str(e)}")
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
    try:
        # Crear directorio si no existe
        import os
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(lista_datos, archivo, indent=4, ensure_ascii=False)
            return True
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_JSON, "guardar datos JSON", f"Error al escribir archivo: {str(e)}")
        return False


# --- API Publica ---

def leer_clientes():
    """Lee clientes desde JSON."""
    return leer_datos_json_interno(RUTA_CLIENTES)


def guardar_clientes(lista_clientes):
    """Guarda clientes en JSON."""
    return guardar_datos_json_interno(RUTA_CLIENTES, lista_clientes)


def leer_departamentos():
    """
    Lee departamentos desde archivo JSON.
    
    Retorna:
        list: Lista de diccionarios con departamentos o [] si no existe/error
    """
    return leer_datos_json_interno(RUTA_DEPARTAMENTOS)


def guardar_departamentos(lista_deptos):
    """
    Guarda departamentos en archivo JSON.
    
    Parametros:
        lista_deptos (list): Lista de diccionarios con departamentos
    
    Retorna:
        bool: True si se guardó correctamente, False si hubo error
    """
    return guardar_datos_json_interno(RUTA_DEPARTAMENTOS, lista_deptos)


def inicializar_datos_departamentos():
    """
    Función de utilidad para cargar departamentos al iniciar el sistema.
    
    Retorna:
        list: Lista de departamentos cargados desde JSON
    """
    try:
        departamentos_cargados = leer_departamentos()
        if departamentos_cargados:
            print(f"Se cargaron {len(departamentos_cargados)} departamentos desde archivo JSON")
        else:
            print("No se encontraron departamentos guardados, iniciando con lista vacía")
        return departamentos_cargados
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_JSON, "inicializar departamentos", str(e))
        return []


def guardar_cambios_departamentos(lista_deptos, operacion=""):
    """
    Función de utilidad para guardar cambios en departamentos con mensajes informativos.
    
    Parametros:
        lista_deptos (list): Lista de departamentos a guardar
        operacion (str): Descripción de la operación realizada
    
    Retorna:
        bool: True si se guardó correctamente
    """
    try:
        if guardar_departamentos(lista_deptos):
            mensaje = f"Departamentos guardados correctamente"
            if operacion:
                mensaje += f" despues de {operacion}"
            print(mensaje)
            return True
        else:
            print("Error al guardar departamentos")
            return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_JSON, "guardar cambios departamentos", str(e))
        return False


"""
INTEGRACION:

1. Al iniciar (main.py):
   clientes.clientes = persistence.leer_clientes()
   departamentos.departamentos = persistence.inicializar_datos_departamentos()

2. Al salir (main.py):
   persistence.guardar_clientes(clientes.clientes)
   persistence.guardar_departamentos(departamentos.departamentos)

3. Guardado después de operaciones críticas (recomendado):
   - Después de agregar: persistence.guardar_cambios_departamentos(departamentos.departamentos, "agregar departamento")
   - Después de actualizar: persistence.guardar_cambios_departamentos(departamentos.departamentos, "actualizar departamento")
   - Después de eliminar: persistence.guardar_cambios_departamentos(departamentos.departamentos, "eliminar departamento")

4. Ejemplo de integración en domain/departamentos.py:
   from repository.persistence_json import guardar_cambios_departamentos
   
   def agregar_departamento(...):
       # lógica existente
       resultado = # True/False
       if resultado:
           guardar_cambios_departamentos(departamentos, "agregar departamento")
       return resultado
"""