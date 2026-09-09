# Banco generado de práctica CEPRE

`data/generated_bank.py` expone `PROBLEMS_GENERATED`: 400 ejercicios originales
deterministas numerados desde 1001. Son 50 familias matemáticamente distintas con
8 variantes cada una. Las variantes fortalecen rapidez de reconocimiento y cálculo;
no se presentan como 400 conceptos matemáticos distintos.

Cada ejercicio conserva tema, subtema, dificultad de 1 a 3 estrellas, tiempo meta,
pasos, idea, pista, trampa y referencia de fuente. Las referencias son de temario y
páginas revisadas; el contenido es nuevo y no reproduce texto de los PDF.

Cobertura: aritmética y razonamiento numérico (divisibilidad, fracciones,
porcentajes, conteo, conjuntos y patrones), álgebra (ecuaciones, sistemas,
polinomios, funciones y desigualdades), geometría (áreas, Pitágoras, polígonos, circunferencia y
sólidos), probabilidad/estadística elemental y trigonometría. El módulo separado
`data/trigonometry_bank.py` aporta 48 ejercicios (6 familias × 8) de razones,
tangente para altura/sombra, identidades fundamentales, cofunciones, ángulo doble
y suma de ángulos. Su evidencia es `TRIGONOMETRÍA - PRISMA 2025 (1).pdf`, p. 5
(índice temático), pp. 6-7 (razones), p. 10 (aplicaciones) y p. 16 (ángulos
compuestos y doble ángulo); los enunciados son originales.

Verificación: ejecutar `python scripts/validate_bank.py`. El script recalcula la
respuesta desde los parámetros de cada ejercicio con `Fraction` cuando corresponde,
y revisa esquema, alternativas únicas, índice correcto, cantidad de pasos y rangos
de nivel/tiempo. No hay truncamiento de resultados no enteros.
Para trigonometría, ejecutar también `python scripts/validate_trigonometry.py`;
recalcula razones, identidades y fórmulas de suma/doble ángulo con fracciones
exactas.

La validación final exige también **448 conjuntos de parámetros matemáticos
distintos**. Cambiar un prefijo del enunciado no cuenta como caso nuevo. Los
parámetros se mantienen en rangos de entrenamiento humano, y las alternativas de
seno/coseno y probabilidad respetan sus dominios.

## Ampliación por temario Prisma 2026-2

`data/syllabus_additions.py` incorpora 96 casos (12 familias × 8), IDs 1501–1596:
decimales, valor posicional decimal, factorización, funciones aplicadas,
programación lineal, inecuaciones cuadráticas, valor absoluto, triángulos
notables, grados/radianes, reducción de cuadrante, ecuaciones y funciones
trigonométricas. Cada unidad del mapa de 55 unidades tiene al menos un caso.

El total es 544 nuevos más 62 originales = 606. Se excluyen del entrenamiento
5 originales duplicados y 10 complementarios (8 conversiones a bases no
decimales, un sistema no lineal y una ley de cosenos); siguen en Estudio.
El banco elegible es 591.

La taxonomía final la aplica `data/curriculum.py` desde `data/syllabus-map.json`.
Progresiones y sucesiones se muestran en Números y Operaciones; combinatoria y
probabilidad en Estadística. Los validadores independientes están en
`scripts/audit-math-independent.py` y `scripts/audit-syllabus-independent.py`.

55 unidades con casos no equivalen a dominio de todas sus subhabilidades:
por ejemplo, S01 incluye tablas simples y cálculos estadísticos, no todos los
tipos de gráficos. Los niveles y tiempos son objetivos pedagógicos por calibrar.
