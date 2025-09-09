from common.utils import *
from domain.clientes import *



#crud
def agregar_cliente():
    nombre = pedir_input_con_validacion("Nombre: ")
    apellido = pedir_input_con_validacion("Apellido: ")
    dni = pedir_input_con_validacion("DNI: ")
    telefono = pedir_input_con_validacion("Telefono: ")

    nuevo_cliente = {
        "id": generar_id_unico_diccionario(clientes, "id"),
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "telefono": telefono,
    }
    clientes.append(nuevo_cliente)
    print(f"Cliente agregado correctamente con el id {nuevo_cliente['id']}")


def listar_clientes():
    if not clientes:
        print("No hay clientes registrados.\n")
        return
    for cliente in clientes:
        print(f"ID: {cliente['id']} - Nombre: {cliente['nombre']} {cliente['apellido']} dni: {cliente['dni']} {cliente['telefono']}")
    print()


def eliminar_cliente():
    if not clientes:
        print("No hay clientes para eliminar.\n")
        return

    id_eliminar = pedir_input_con_validacion("Ingrese el ID del cliente a eliminar: ")

    for i, cliente in enumerate(clientes):
        if str(cliente.get("id")) == str(id_eliminar):
            confirmacion = pedir_input_con_validacion(
                f"¿Confirmás eliminar a {cliente['nombre']} {cliente['apellido']} (ID {cliente['id']})? (s/n): "
            )
            if confirmacion.strip().lower().startswith("s"):
                clientes.pop(i)
                print("Cliente eliminado correctamente.\n")
            else:
                print("Operación cancelada.\n")
            return

# Nueva función para actualizar cliente
def actualizar_cliente():
    if not clientes:
        print("No hay clientes para actualizar.\n")
        return

    id_actualizar = pedir_input_con_validacion("Ingrese el ID del cliente a actualizar: ")

    for cliente in clientes:
        if str(cliente.get("id")) == str(id_actualizar):
            print("Deje vacío para mantener el valor actual.")
            # Usamos input directo para permitir vacío sin romper validaciones
            nuevo_nombre = input(f"Nuevo nombre [{cliente['nombre']}]: ").strip()
            nuevo_apellido = input(f"Nuevo apellido [{cliente['apellido']}]: ").strip()
            nuevo_dni = input(f"Nuevo DNI [{cliente['dni']}]: ").strip()
            nuevo_telefono = input(f"Nuevo teléfono [{cliente['telefono']}]: ").strip()

            if nuevo_nombre:
                cliente['nombre'] = nuevo_nombre
            if nuevo_apellido:
                cliente['apellido'] = nuevo_apellido
            if nuevo_dni:
                cliente['dni'] = nuevo_dni
            if nuevo_telefono:
                cliente['telefono'] = nuevo_telefono

            print("Cliente actualizado correctamente.\n")
            return












def menu_cliente():
    while True:
        print("""
        --- MENÚ DE CLIENTES ---
        1) Agregar cliente
        2) Listar clientes
        3) Eliminar cliente
        4) Actualizar cliente
        0) Salir
        """)
        op = input("Opcion: ")
        if op == "1":
            agregar_cliente()
        elif op == "2":
            listar_clientes()
        elif op == "3":
            eliminar_cliente()
        elif op == "4":
            actualizar_cliente()
        elif op == "0":
            break

if __name__ == "__main__":
    menu_cliente()
