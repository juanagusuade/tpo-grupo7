def crear_matriz():
    datos = []
    continuar = "si"
    while continuar == "si":  # Construyo las filas
        id_cliente = len(datos) + 1
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = int(input("DNI: "))
        telefono = int(input("Telefono: "))
        fila = [id_cliente, nombre, apellido, dni, telefono]
        datos.append(fila)
        continuar = input("¿Desea cargar otro cliente? (si/no): ")
    return datos


def imprimir_datos(encabezados, matriz):
    filas = len(matriz)

    if filas == 0:
        print("No hay datos cargados:")
        return
    columnas = len(matriz[0])
    for titulo in encabezados:
        print(titulo, end="\t")
    print()
    for fila in range(filas):
        for columna in range(columnas):
            print(matriz[fila][columna], end="\t")
        print()


# Programa principal
titulos = ["ID Cliente", "Nombre", "Apellido", "DNI", "Telefono"]

matriz_clientes = crear_matriz()
print(matriz_clientes)
imprimir_datos(titulos, matriz_clientes)