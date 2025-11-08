"""
Módulo de servicios que coordina operaciones entre múltiples entidades.
Contiene lógica de negocio que requiere interacción entre clientes, departamentos y reservas.

NOTA: El import de 'reservas' se hace dentro de las funciones para evitar imports circulares,
ya que reservas.py importa clientes.py y departamentos.py, que a su vez importan este módulo.
"""

from common.constantes import (
    INDICE_ID_RESERVA, 
    INDICE_ESTADO, 
    ESTADO_ACTIVO,
    INDICE_ID_DEPARTAMENTO,
    INDICE_FECHA_INGRESO,
    INDICE_FECHA_EGRESO
)
from common.validaciones import comparar_fechas_string
from common.manejo_errores import manejar_error_inesperado

MODULO = "Funciones compartidas"

def cancelar_reservas_activas_de_cliente(id_cliente):
    """
    Cancela todas las reservas activas asociadas a un cliente.
    Se usa antes de dar de baja lógica a un cliente.
    
    Parámetros:
        id_cliente (int): ID del cliente
    
    Retorna:
        int: Cantidad de reservas canceladas
    """
    from domain import reservas
    
    reservas_cliente = reservas.buscar_reservas_por_cliente(id_cliente)
    canceladas = 0
    
    for reserva in reservas_cliente:
        if reserva[INDICE_ESTADO] == ESTADO_ACTIVO:
            if reservas.cancelar_reserva(reserva[INDICE_ID_RESERVA]):
                canceladas += 1
    
    return canceladas


def cancelar_reservas_activas_de_departamento(id_departamento):
    """
    Cancela todas las reservas activas asociadas a un departamento.
    Se usa antes de dar de baja lógica a un departamento.
    
    Parámetros:
        id_departamento (int): ID del departamento
    
    Retorna:
        int: Cantidad de reservas canceladas
    """
    from domain import reservas 
    
    reservas_depto = reservas.buscar_reservas_por_departamento(id_departamento)
    canceladas = 0
    
    for reserva in reservas_depto:
        if reserva[INDICE_ESTADO] == ESTADO_ACTIVO:
            if reservas.cancelar_reserva(reserva[INDICE_ID_RESERVA]):
                canceladas += 1
    
    return canceladas


def verificar_reservas_activas_de_departamento(id_departamento):
    """
    Verifica si un departamento tiene reservas activas.
    Se usa antes de eliminar físicamente un departamento.
    
    Parámetros:
        id_departamento (int): ID del departamento
    
    Retorna:
        bool: True si tiene reservas activas, False en caso contrario
    """
    from domain import reservas
    
    reservas_depto = reservas.buscar_reservas_por_departamento(id_departamento)
    reservas_activas = [r for r in reservas_depto if r[INDICE_ESTADO] == ESTADO_ACTIVO]
    
    return len(reservas_activas) > 0


def verificar_disponibilidad_departamento_en_fechas(id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """
    Verifica si un departamento está disponible en un rango de fechas.
    Permite que el último día de una reserva coincida con el primer día de otra.
    
    Parámetros:
        id_departamento (int): ID del departamento
        fecha_ingreso_str (str): Fecha de ingreso deseada (DD/MM/YYYY)
        fecha_egreso_str (str): Fecha de egreso deseada (DD/MM/YYYY)
    
    Retorna:
        bool: True si está disponible, False si hay solapamiento o error
    """
    from domain import reservas
    
    try:
        todas_reservas = reservas.obtener_todas_las_reservas()
        
        for r in todas_reservas:
            if r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] == ESTADO_ACTIVO:
                comp_inicio_nueva_fin_reserva = comparar_fechas_string(fecha_ingreso_str, r[INDICE_FECHA_EGRESO])
                comp_inicio_reserva_fin_nueva = comparar_fechas_string(r[INDICE_FECHA_INGRESO], fecha_egreso_str)

                if comp_inicio_nueva_fin_reserva is None or comp_inicio_reserva_fin_nueva is None:
                    return False

                # Hay solapamiento si:
                # - La nueva reserva inicia antes que termine la existente Y
                # - La reserva existente inicia antes que termine la nueva
                if comp_inicio_nueva_fin_reserva < 0 and comp_inicio_reserva_fin_nueva < 0:
                    return False

        return True
    except (TypeError, IndexError) as e:
        manejar_error_inesperado(MODULO, "verificar disponibilidad departamento", str(e))
        return False
