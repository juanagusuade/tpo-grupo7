from domain.reservas import comparar_fechas_string, hay_solapamiento_fechas


def test_comparar_fechas():
    """Test simple: comparar dos fechas diferentes"""
    fechaChica = "01/01/2024"
    fechaGrande = "15/01/2024"
    resultadoEsperadoNegativo = -1
    resultadoEsperadoPositivo = 1

    resultadoNegativo = comparar_fechas_string(fechaChica, fechaGrande)
    resultadoPositivo = comparar_fechas_string(fechaGrande, fechaChica)

    assert resultadoNegativo == resultadoEsperadoNegativo
    assert resultadoPositivo == resultadoEsperadoPositivo


def test_solapamiento_mismo_dia():
    """Test simple: verificar que checkout/checkin el mismo dia NO solapa"""
    no_solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "05/01/2025", "10/01/2025")
    solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "04/01/2025", "10/01/2025")

    assert no_solapados == False
    assert solapados == True


# quiero probar listar_clientes_activos:
#     primero hago una lista de clientes con distintos estados
#     hago otra lista con los clientes ya filtrados
#     llamo a la funcion de listar_clientes_activos con la lista grande
#     asserteo que el resultado de la funcion es igual a la de los clientes filtrados

