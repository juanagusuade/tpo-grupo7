import flet as ft
from ui.gui_app import iniciar_app
from domain.clientes import cargar_clientes_desde_archivo, guardar_clientes_a_archivo
from domain.departamentos import cargar_departamentos_desde_archivo, guardar_departamentos_a_archivo
import common.poblador as poblador

def main():
    """Funcion principal del sistema (GUI)"""
    print("Iniciando sistema...")
    
    # Cargar datos iniciales
    print("Cargando datos...")
    cargar_clientes_desde_archivo()
    cargar_departamentos_desde_archivo()
    poblador.poblar_datos_iniciales()

    # Iniciar aplicacion Flet
    print("Abriendo interfaz gráfica...")
    ft.app(target=iniciar_app)

    # Guardar datos al salir (esto se ejecuta cuando se cierra la ventana de Flet)
    print("Guardando datos...")
    guardar_clientes_a_archivo("salir del sistema")
    guardar_departamentos_a_archivo("salir del sistema")
    print("Sistema finalizado.")

if __name__ == "__main__":
    main()
    