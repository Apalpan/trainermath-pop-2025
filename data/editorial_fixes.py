"""Correcciones para entrenamiento; conserva las reconstrucciones fuente intactas."""
from copy import deepcopy


def apply_editorial_fixes(problems):
    bank = deepcopy(problems)
    for p in bank:
        n = p.get('n')
        if n == 6:
            p['enun'] = p['enun'].replace('Se tiene la expresión:', 'Sean A, B, C y n positivos, con B constante. Se tiene la expresión:')
            p['opts'][2] = '<span class="fr"><span class="fn">85</span><span class="fd">112</span></span>'
            p['nota'] = 'Adaptación de entrenamiento: se declara B constante y se corrige la alternativa C, duplicada en la reconstrucción. La clave sigue siendo 85/27.'
        elif n == 24:
            p['opts'][3] = '<span class="fr"><span class="fn">8</span><span class="fd">130</span></span>'
            p['nota'] = 'Adaptación de entrenamiento: se reemplaza la alternativa D duplicada en la reconstrucción. La clave sigue siendo −8/65.'
        elif n == 28:
            p['enun'] = p['enun'].replace('0):', '0, además x ≠ y y x ≠ −y):', 1)
            p['steps'].append({'t':'Conserva el dominio', 'd':'Además de x ≠ 0 e y ≠ 0, se requiere x ≠ y para el cociente interior y x ≠ −y para poder invertirlo. Simplificar no elimina esas restricciones.'})
            p['nota'] = 'Adaptación de entrenamiento: se explicitan todas las restricciones del dominio.'
        elif n == 51:
            p['enun'] = 'Se pinta únicamente la superficie curva exterior de una taza semiesférica de radio 6 cm, sin asa, borde ni base circular. Halla el costo exacto, sin redondear, si pintar cada cm² cuesta S/ 0,2. (Considera π = 3,14).'
            p['steps'][-1] = {'t':'Comprueba superficie y unidades', 'd':'Se pinta una sola superficie curva: 2πr². No se suma el círculo de apertura ni una segunda cara. El área en cm² se multiplica por la tarifa en S/ por cm².'}
            p['nota'] = 'Adaptación de entrenamiento: se precisa qué superficie se pinta y se mantiene la tarifa por cm².'
        elif n == 54:
            p['enun'] = 'En un sorteo se asignan dos premios: $1 000 y $2 000. Se extraen al azar dos boletos distintos, sin reposición, uno por premio. Un mismo comprador puede ganar ambos premios con boletos diferentes. De los 100 boletos vendidos, cinco son míos. ¿Cuál es la probabilidad de que gane $3 000?'
            p['nota'] = 'Adaptación de entrenamiento: se explicita la extracción sin reposición y que un comprador puede recibir ambos premios.'
    return bank
