# main.py
from domain.departamentos import (
    agregar_departamento,
    eliminar_departamento,
    actualizar_departamento,
    departamentos
)


def mostrar_menu():
    print("\n--- MENÚ DEPARTAMENTOS ---")
    print("1. Agregar departamento")
    print("2. Eliminar departamento")
    print("3. Actualizar departamento")
    print("4. Listar departamentos")
    print("5. Salir")


def listar_departamentos():
    if not departamentos:
        print("\nNo hay departamentos registrados.")
        return

    print("\n--- LISTADO DE DEPARTAMENTOS ---")
    for d in departamentos:
        print(
            f"ID: {d['id']} | Ubicación: {d['ubicacion']} | Ambientes: {d['ambientes']} "
            f"| Capacidad: {d['capacidad']} | Estado: {d['estado']} "
            f"| Precio/noche: {d['precio_noche']} | Activo: {d['activo']}"
        )


def main():
    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            ubicacion = input("Ubicación: ")
            ambientes = int(input("Ambientes: "))
            capacidad = int(input("Capacidad: "))
            estado = input("Estado: ")
            precio_noche = float(input("Precio por noche: "))

            if agregar_departamento(ubicacion, ambientes, capacidad, estado, precio_noche):
                print("Departamento agregado correctamente.")

        elif opcion == "2":
            listar_departamentos()
            id_dep = int(input("ID del departamento a eliminar: "))
            if eliminar_departamento(id_dep):
                print("Departamento eliminado.")
            else:
                print("No se encontró ese ID.")

        elif opcion == "3":
            listar_departamentos()
            id_dep = int(input("ID del departamento a actualizar: "))
            ubicacion = input("Nueva ubicación: ")
            ambientes = int(input("Nuevos ambientes: "))
            capacidad = int(input("Nueva capacidad: "))
            estado = input("Nuevo estado: ")
            precio_noche = float(input("Nuevo precio por noche: "))

            if actualizar_departamento(id_dep, ubicacion, ambientes, capacidad, estado, precio_noche):
                print("Departamento actualizado.")
            else:
                print("No se encontró ese ID.")

        elif opcion == "4":
            listar_departamentos()

        elif opcion == "5":
            print("Saliendo")
            break

        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    main()