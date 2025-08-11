import random
# Matriz de reservas, que relaciona departamentos con clientes.
#ID Reserva (int)[0] - ID Cliente (int)[1] - ID Dpto (int)[2] - Fecha Ingreso (date)[3] - Fecha Egreso (date)[4].
reservas = []

def generar_id_unico(lista):
    id = random.randint(1000, 9999)
    existe_id_igual = True
    while existe_id_igual:
        existe_id_igual = False
        for e in lista:
            if e[0] == id:
                existe_id_igual = True
                id = random.randint(1000, 9999)
                break
    return id

def cargar_reserva(id_cliente, id_departamento, fecha_ingreso, fecha_egreso):
    id_reserva = generar_id_unico(reservas)
    reservas.append([id_reserva, id_cliente, id_departamento, fecha_ingreso, fecha_egreso])
    return id_reserva
