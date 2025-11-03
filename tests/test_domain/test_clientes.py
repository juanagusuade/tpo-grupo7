from domain.clientes import buscar_dni
from common.constantes import DNI_CLIENTE, NOMBRE_CLIENTE

#Lista de clientes solo para usar en los  tests
CLIENTES_DE_PRUEBA = [
    {DNI_CLIENTE: "10000001", NOMBRE_CLIENTE: "Ana"},
    {DNI_CLIENTE: "10000002", NOMBRE_CLIENTE: "Beto"},
    {DNI_CLIENTE: "10000003", NOMBRE_CLIENTE: "Carla"}
]

def test_buscar_dni():

#Test 1: Verifica que el DNI se repite y retorna True

    resultado_true = buscar_dni(CLIENTES_DE_PRUEBA, "10000002")
    
# Test 2: El DNI NO se repite y retorna False 

    resultado_false = buscar_dni(CLIENTES_DE_PRUEBA, "99999999")


    assert resultado_true == True
    assert resultado_false == False





