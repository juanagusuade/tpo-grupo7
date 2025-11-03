from domain.reservas import comparar_fechas_string, hay_solapamiento_fechas

def test_comparar_fechas():
    """Comparar dos fechas diferentes"""
    fechaMenor = "01/01/2024"
    fechaMayor = "15/01/2024"
    fechaErronea = "15/15/1515"

    resultadoEsperadoNegativo = -1
    resultadoEsperadoPositivo = 1
    resultadoEsperadoIgual = 0
    resultadoEsperadoErroneo = None

    resultadoNegativo = comparar_fechas_string(fechaMenor, fechaMayor)
    resultadoPositivo = comparar_fechas_string(fechaMayor, fechaMenor)
    resultadoIgual = comparar_fechas_string(fechaMenor, fechaMenor)
    resultadoErroneo = comparar_fechas_string(fechaErronea, fechaErronea)

    assert resultadoNegativo == resultadoEsperadoNegativo
    assert resultadoPositivo == resultadoEsperadoPositivo
    assert resultadoIgual == resultadoEsperadoIgual
    assert resultadoErroneo == resultadoEsperadoErroneo


def test_solapamiento_mismo_dia():
    """Verificar que checkout/checkin el mismo dia NO solapa"""
    no_solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "05/01/2025", "10/01/2025")
    solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "04/01/2025", "10/01/2025")

    assert no_solapados == False
    assert solapados == True
