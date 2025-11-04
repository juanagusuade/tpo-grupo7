import pytest
from domain.clientes import buscar_dni
from common.constantes import DNI_CLIENTE, NOMBRE_CLIENTE

#Lista de clientes solo para usar en los  tests
CLIENTES_DE_PRUEBA = [
    {DNI_CLIENTE: "10000001", NOMBRE_CLIENTE: "Ana"},
    {DNI_CLIENTE: "10000002", NOMBRE_CLIENTE: "Beto"},
    {DNI_CLIENTE: "10000003", NOMBRE_CLIENTE: "Carla"}
]

def test_buscar_dni():

    # Test 1: Verifica que el DNI se repite y retorna True
    resultado_true = buscar_dni(CLIENTES_DE_PRUEBA, "10000002")
    
    # Test 2: El DNI NO se repite y retorna False 
    resultado_false = buscar_dni(CLIENTES_DE_PRUEBA, "99999999")
    
    # Test 3: Verifica que se maneje la excepcion con estructura invalida
    lista_invalida = [{"nombre": "Juan"}, {"nombre": "Pedro"}]
    
    # La funcion buscar_dni maneja KeyError internamente y retorna True
    # No lanza excepción, pero podemos verificar que no falla
    resultado_excepcion = buscar_dni(lista_invalida, "12345678")

    assert resultado_true == True
    assert resultado_false == False
    assert resultado_excepcion == True  # Retorna True cuando hay error (por seguridad)


def test_buscar_dni_con_excepcion():
    """Test para verificar que se lance excepcion con datos completamente invalidos"""
    
    # Probar con un tipo de dato que definitivamente cause error
    with pytest.raises((KeyError, IndexError, TypeError)):
        buscar_dni(None, "12345678")  # None causará TypeError





