import pytest

from common.validaciones import validar_numero_decimal, validar_dni, validar_telefono, comparar_fechas_string

def test_validar_decimal():
    posibilidades = ["10", "-10", "10.5", "-10.5", "abc", 12, 12.34]
    resultados_esperados = [True, False, True, False, False, False, False]
    for valor, esperado in zip(posibilidades, resultados_esperados):
        assert validar_numero_decimal(valor) == esperado
        
    
def test_validar_dni():
    resultados= ["1234567", "12345678", "123456", "123456789", "1234abc"]
    resultados_esperados=[True, True, False, False, False]     
    for dni, esperado in zip(resultados, resultados_esperados):
        assert validar_dni(dni) == esperado

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

    # Verificar casos validos
    for telefono in casos_validos:
        assert validar_telefono(telefono) == True, f"Falló con teléfono válido: {telefono}"

    # Verificar casos invalidos
    for telefono in casos_invalidos:
        assert validar_telefono(telefono) == False, f"Falló con teléfono inválido: {telefono}"

def test_comparar_fechas():
    """Comparar dos fechas diferentes y sus resultados"""
    fechaChica = "01/01/2024"
    fechaGrande = "15/01/2024"
    fechaInvalida = "15/15/1515"
    resultadoEsperadoNegativo = -1
    resultadoEsperadoPositivo = 1
    resultadoEsperadoIgual = 0

    resultadoNegativo = comparar_fechas_string(fechaChica, fechaGrande)
    resultadoPositivo = comparar_fechas_string(fechaGrande, fechaChica)
    resultadoIgual = comparar_fechas_string(fechaChica, fechaChica)
    resultadoErroneo = comparar_fechas_string(fechaChica, fechaInvalida)

    assert resultadoNegativo == resultadoEsperadoNegativo
    assert resultadoPositivo == resultadoEsperadoPositivo
    assert resultadoIgual == resultadoEsperadoIgual
    assert resultadoErroneo == None

    with pytest.raises(ValueError):
        comparar_fechas_string(fechaChica, fechaInvalida)  # causa ValueError
