# common/manejo_errores.py

from .constantes import COLOR_ROJO, COLOR_AMARILLO, COLOR_RESET

def manejar_error_inesperado(entidad, operacion, mensaje_personalizado=None):
    """
    Imprime un mensaje de error estandarizado para excepciones inesperadas.

    Args:
        entidad (str): El módulo o entidad donde ocurrió el error (ej: 'Reservas').
        operacion (str): Describe la acción que se estaba realizando (ej: 'agregar reserva').
        mensaje_personalizado (str, opcional): Un string con detalles adicionales.
    """
    print(f"\n{COLOR_ROJO}¡ERROR INESPERADO EN {entidad.upper()}!{COLOR_RESET}")
    print(f"Ocurrió un problema durante la operación de '{operacion}'.")

    if mensaje_personalizado:
        print(f"{COLOR_AMARILLO}Informacion adicional: {mensaje_personalizado}{COLOR_RESET}")

    print("Por favor, verifica los datos ingresados.")