from common.validaciones import comparar_fechas_string
from domain.reservas import hay_solapamiento_fechas

def test_solapamiento_mismo_dia():
    """Verificar que checkout/checkin el mismo dia NO solapa"""
    no_solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "05/01/2025", "10/01/2025")
    solapados = hay_solapamiento_fechas("01/01/2025", "05/01/2025", "04/01/2025", "10/01/2025")

    assert no_solapados == False
    assert solapados == True

