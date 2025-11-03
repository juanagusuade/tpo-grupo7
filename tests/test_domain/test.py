import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.entrada_datos import validar_alfabetico

def test_validar_alfabetico():
    # Entradas a probar
    posibilidades = ["Juan123", "123", "juan@arias", "hola!", "Juan-Perez", " ", "juan", "Juan", "JUAN"]

    # Resultados esperados (en el MISMO orden)
    resultados_esperados = [False, False, False, False, False, False, True, True, True]

    # Probar cada caso
    for valor, esperado in zip(posibilidades, resultados_esperados):
        assert validar_alfabetico(valor) == esperado


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.validaciones import validar_telefono


def test_validar_telefono():



    casos_validos = [
        "1234567",
        "12345678",
        "011 4567-8901",
        "(011) 4567-8901",
        "+54 11 4567-8901",
        "011.4567.8901",
        "(011)4567-8901",
        "1234567890",
    ]


    casos_invalidos = [
        "123456",
        "12345",
        "",
        "123-45",
        "1234567abc",
        "1234567@",
        "1234567#890",
        "1234567*890",
    ]


    for telefono in casos_validos:
        assert validar_telefono(telefono) == True, f"Falló con teléfono válido: {telefono}"

    # Verificar casos inválidos
    for telefono in casos_invalidos:
        assert validar_telefono(telefono) == False, f"Falló con teléfono inválido: {telefono}"


