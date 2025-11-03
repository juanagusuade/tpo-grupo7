"""
Maneja la persistencia de reservas en formato TXT delimitado.

FORMATO: Cada linea es una reserva con campos separados por ";"
         Ejemplo: 12345;67890;54321;25/08/2025;30/08/2025;ACTIVO

VENTAJAS: Liviano, append eficiente, procesamiento linea por linea
DESVENTAJAS: Sin tipado automatico, modificaciones requieren reescritura completa

ESTRATEGIAS:
    - APPEND: Agregar nuevas reservas (rapido)
    - REESCRITURA: Modificar/eliminar reservas (lento pero necesario)

=========================================================================================
"""

import os
from common.constantes import RUTA_RESERVAS, DELIMITADOR
from common.constantes import INDICE_ID_RESERVA, INDICE_ID_CLIENTE, INDICE_ID_DEPARTAMENTO
from common.constantes import INDICE_FECHA_INGRESO, INDICE_FECHA_EGRESO, INDICE_ESTADO
from common.manejo_errores import manejar_error_inesperado

ENTIDAD_PERSISTENCIA_TXT = "Persistencia TXT"


# --- Funciones de Conversion ---

def parsear_de_txt_a_reserva(linea):
    """
    Convierte una linea de texto a lista de reserva.
    
    Parametros:
        linea (str): "12345;67890;54321;25/08/2025;30/08/2025;ACTIVO"
    
    Retorna:
        list: [12345, 67890, 54321, "25/08/2025", "30/08/2025", "ACTIVO"]
    """
    campos = linea.strip().split(DELIMITADOR)
    reserva = [
        int(campos[INDICE_ID_RESERVA]),
        int(campos[INDICE_ID_CLIENTE]),
        int(campos[INDICE_ID_DEPARTAMENTO]),
        str(campos[INDICE_FECHA_INGRESO]),
        str(campos[INDICE_FECHA_EGRESO]),
        str(campos[INDICE_ESTADO])
    ]
    return reserva


def formatear_reserva_txt(reserva_lista):
    """
    Convierte una lista de reserva a linea de texto.
    
    Parametros:
        reserva_lista (list): [12345, 67890, 54321, "25/08/2025", "30/08/2025", "ACTIVO"]
    
    Retorna:
        str: "12345;67890;54321;25/08/2025;30/08/2025;ACTIVO"
    """
    campos_str = [str(campo) for campo in reserva_lista]
    return DELIMITADOR.join(campos_str)


# --- Funciones Internas ---

def leer_datos_txt_interno(ruta_archivo, funcion_parseo):
    """
    Lee archivo TXT linea por linea y convierte a lista de datos.
    
    Parametros:
        ruta_archivo (str): Path al archivo TXT
        funcion_parseo (function): Funcion que convierte linea -> dato
    
    Retorna:
        list: Datos leidos o [] si error
    """
    lista_reservas = []
    archivo = None
    try:
        archivo = open(ruta_archivo, "r", encoding="utf-8")
        linea = archivo.readline()
        while linea:
            if linea.strip():
                reserva = funcion_parseo(linea)
                lista_reservas.append(reserva)
            linea = archivo.readline()
    except FileNotFoundError:
        try:
            archivo_nuevo = open(ruta_archivo, "w", encoding="utf-8")
            archivo_nuevo.close()
        except Exception:
            manejar_error_inesperado(ENTIDAD_PERSISTENCIA_TXT, "crear archivo", "No se pudo crear el archivo.")
    except Exception:
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_TXT, "leer datos", "Error al leer archivo.")
    finally:
        if archivo:
            archivo.close()
    return lista_reservas


def guardar_datos_txt_temporal_interno(ruta_archivo, lista_datos, funcion_formateo):
    """
    Guarda datos usando archivo temporal (seguro para reescritura).
    
    Parametros:
        ruta_archivo (str): Path al archivo final
        lista_datos (list): Datos a guardar
        funcion_formateo (function): Funcion que convierte dato -> linea
    
    Retorna:
        bool: True si OK, False si error
    """
    ruta_tmp = ruta_archivo + ".tmp"
    archivo = None
    try:
        archivo = open(ruta_tmp, "w", encoding="utf-8")
        for dato in lista_datos:
            linea = funcion_formateo(dato)
            archivo.write(linea + "\n")
        archivo.close()
        os.replace(ruta_tmp, ruta_archivo)
        return True
    except Exception:
        if archivo:
            archivo.close()
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_TXT, "guardar datos", "Error al guardar archivo.")
        return False


def agregar_linea_txt_append_interno(ruta_archivo, item, funcion_formateo):
    """
    Agrega una linea al final del archivo (modo append).
    
    Parametros:
        ruta_archivo (str): Path al archivo TXT
        item: Dato individual a agregar
        funcion_formateo (function): Funcion que convierte dato -> linea
    
    Retorna:
        bool: True si OK, False si error
    """
    linea = funcion_formateo(item)
    archivo = None
    try:
        archivo = open(ruta_archivo, "a", encoding="utf-8")
        archivo.write(linea + "\n")
        archivo.close()
        return True
    except Exception:
        if archivo:
            archivo.close()
        manejar_error_inesperado(ENTIDAD_PERSISTENCIA_TXT, "agregar linea", "Error al agregar al archivo.")
        return False


# --- API Publica ---

def leer_reservas():
    """Lee reservas desde TXT."""
    return leer_datos_txt_interno(RUTA_RESERVAS, parsear_de_txt_a_reserva)


def guardar_reservas_txt(lista_reservas):
    """Guarda todas las reservas (reescribe archivo completo)."""
    return guardar_datos_txt_temporal_interno(RUTA_RESERVAS, lista_reservas, formatear_reserva_txt)


def agregar_reserva_txt(reserva_lista):
    """Agrega una reserva al final (modo append, rapido)."""
    return agregar_linea_txt_append_interno(RUTA_RESERVAS, reserva_lista, formatear_reserva_txt)