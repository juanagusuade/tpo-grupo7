from common.validaciones import validar_numero_decimal, validar_dni




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