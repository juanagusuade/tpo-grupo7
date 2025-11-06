from common.entrada_datos import validar_alfabetico

def test_validar_alfabetico():
    # Entradas a probar
    posibilidades = ["Juan123", "123", "juan@arias", "hola!", "Juan-Perez", " ", "juan", "Juan", "JUAN"]

    # Resultados esperados (en el MISMO orden)
    resultados_esperados = [False, False, False, False, False, False, True, True, True]

    # Probar cada caso
    for valor, esperado in zip(posibilidades, resultados_esperados):
        assert validar_alfabetico(valor) == esperado
