from ui.menu_cliente import menu_cliente
from ui.menu_depto import menu_departamento
from common.utils import pedir_input_con_validacion



def menu_principal():
    while True:
        print("\n" + "=" * 50)
        print(" SISTEMA DE GESTIÓN — MENÚ PRINCIPAL")
        print("=" * 50)
        print("1) Menú de Clientes")
        print("2) Menú de Departamentos")
        #FALTARIA RESERVAS
        print("0) Salir")
        opcion = pedir_input_con_validacion("Elegí una opción: ").strip()

        if opcion == "1":
                menu_cliente()
        elif opcion == "2":
                  menu_departamento()
        elif opcion == "3":
            print("Aca irian reservas xd")
        elif opcion == "0":
            print("Gracias por utilizar el sistema")
            break
        else:
            print("Opción inválida, pruebe de nuevo.")

if __name__ == "__main__":
    menu_principal()