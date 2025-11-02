from domain.reservas import comparar_fechas_string, hay_solapamiento_fechas


def test_comparar_fechas_basico():
    """Test simple: comparar dos fechas diferentes"""
    resultado = comparar_fechas_string("01/01/2024", "15/01/2024")
    assert resultado == -1


def test_solapamiento_mismo_dia():
    """Test simple: verificar que checkout/checkin el mismo dia NO solapa"""
    resultado = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "05/01/2025", "10/01/2025")
    assert resultado == False
