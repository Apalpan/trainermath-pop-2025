# TrainerMath · Temario Prisma y Anzan interactivo

Entrega para Brenda Sofía, 9 de septiembre de 2026.
Aplicación: https://apalpan.github.io/trainermath-pop-2025/

## Cambios funcionales

- Anzan conserva cifras de 1 a 9; 5, 10, 15 o 20 cifras por ronda.
- Velocidad escrita con coma o punto: 0,25–5 segundos en pasos de 0,05.
  Accesos directos 0,75 / 1,25 / 1,5 / 1,75. Modo automático o avance con flecha.
- Preparación 3–2–1 con Aecodito, cancelable y pausable. Es preparación para
  concentrarse, no una carga de datos simulada.
- Pantalla de concentración con degradado ciruela/rosa, cifra luminosa y grande,
  animación breve de aparición, pausa, reinicio y salida visibles.
- Teclado de calculadora para responder, borrar y limpiar; también admite teclado
  físico. En pantalla táctil no se abre automáticamente el teclado del sistema.
- Sonido suave opcional por cifra, desactivado inicialmente. Si el navegador no
  permite audio, explica el problema y continúa en silencio. Pausar no repite el tono.
- Nueva selección por área y unidad, con mapa desplegable del temario.
- Simulacros con las cinco áreas matemáticas y cuotas visibles. Se conserva el
  reloj absoluto, la revisión al entregar y el progreso local anterior.

## Qué temario se aplicó

Fuente de organización: página 4 del archivo aportado por el usuario
`TEMARIO PUCP - EVALUACIÓN DEL TALENTO 2026-2.pdf`, material de **Prisma**.
Se conserva en `Informacion/`, fuera de Git y del despliegue. El nombre del archivo
no lo convierte en una publicación oficial de PUCP.

La clasificación elegida es: Números y Operaciones, Álgebra, Geometría,
Estadística y Trigonometría. Las progresiones PA/PG corresponden a Números y
Operaciones en este documento, y Probabilidad/Combinatoria a Estadística.

La [página oficial de admisión PUCP](https://admision.pucp.edu.pe/guia-del-postulante/modalidades-de-admision/evaluacion-del-talento-r)
enlaza al [temario oficial por competencias](https://admision.pucp.net/temas-priorizados/).
Allí las progresiones pertenecen a Regularidad, equivalencia y cambio. La diferencia
entre ambas taxonomías se explica en la aplicación. El mapa `data/syllabus-map.json`
conserva la correspondencia por ejercicio y la referencia de página.

## Banco y auditoría matemática

**606 casos:** 544 nuevos en 68 familias y 62 originales. El sorteo utiliza
**591 preguntas**: aparta 5 copias originales declaradas y 10 casos complementarios
(8 conversiones a bases no decimales, un sistema no lineal y una ley de cosenos).
Los complementarios siguen accesibles en Estudio.

Se añadieron 96 ejercicios en 12 unidades antes sin casos: decimales, sistema
decimal, factorización, aplicaciones de funciones, programación lineal,
inecuaciones cuadráticas, valor absoluto, triángulos notables, medidas angulares,
reducción de cuadrante, ecuaciones y funciones trigonométricas.

La comprobación independiente recalcula claves y condiciones del banco nuevo.
La revisión detectó y corrigió también:

| Caso | Corrección |
| --- | --- |
| Original 6 | B constante y variables positivas; alternativa duplicada sustituida |
| Original 24 | Alternativa duplicada sustituida |
| Original 28 | Dominio completo del cociente algebraico |
| Original 33 | Extremo 2 abierto en el intervalo dibujado |
| Original 51 | Una superficie curva, tarifa por cm² y costo exacto |
| Original 54 | Dos boletos sin reposición y posibilidad de ambos premios |
| Nuevos de valor posicional | El dígito consultado existe una vez en la posición correcta |
| Nuevos de reducción trigonométrica | Referencias de 120° y 150° corregidas en la explicación |

Los IDs y las claves originales se conservan. Las seis correcciones originales
no alteran respuestas anteriores. Los niveles nuevos se asignan por complejidad,
y se muestran soluciones trigonométricas explícitas con ambos ángulos.

## Evidencia reproducible

| Comprobación | Estado y alcance |
| --- | --- |
| Claves, dominios y alternativas | PASS: `validate_bank.py`, `validate_trigonometry.py`, `validate_syllabus_additions.py` |
| Auditoría matemática independiente | PASS: `audit-math-independent.py`, `audit-syllabus-independent.py` |
| Selección, tiempos, pausa, importación, migración | PASS: 17 escenarios de `test-engine.cjs` |
| Banco sin repetición hasta agotarlo | PASS: 591 elegibles en 30 sesiones sucesivas, `test-real-bank.cjs` |
| Cinco áreas en 20/30/40 preguntas y todos los niveles | PASS: 100 semillas por combinación, `test-exam-coverage.cjs` |
| 55 unidades, clasificación y progreso anterior | PASS: `test-curriculum.cjs` |
| Práctica, examen, respaldo y errores | PASS: `smoke-browser.cjs`, `smoke-browser-extra.cjs` |
| Anzan, velocidad real 0,75 s, flecha, pausas y calculadora | PASS: `test-anzan.cjs`, `smoke-rose-anzan.cjs` |
| Audio, cancelación y doble envío | PASS: `test-anzan-audio.cjs`; AudioContext instrumentado y nativo Chromium |
| Responsive, teclado, nombres accesibles y movimiento reducido | PASS: capturas 320/375 px y escritorio; snapshot ARIA y modo de contraste forzado |
| Contraste de texto/acción | PASS: acción 6,66:1; secundario 6,08:1; principal 14,55:1 |
| Rendimiento de laboratorio | DOMContentLoaded ≈212 ms; CLS 0; sin solicitudes adicionales. LCP no reportado por este Chromium; sin CWV de campo ni INP |
| HTML sin conexión | PASS: apertura file:// con navegador sin red |

Pruebas de navegador requieren Playwright y servidor local en puerto 8768.
Las capturas e informes están en `output/` (no publicados). Para reconstruir:
`python build.py`. Para repetir las verificaciones, ejecutar los scripts citados.

## Alcance y límites

- Hay casos en las 55 unidades. No es cobertura exhaustiva de cada subhabilidad,
  y algunas unidades tienen pocos ejercicios. La tabla siguiente lo hace visible.
- Matemática es el alcance de este entrenador. No incluye la sección de Lectura
  del folleto ni afirma reproducir la distribución oficial de una convocatoria.
- 22 originales contienen figuras; la auditoría estructural específica cubre la
  figura 33. La inspección visual de las demás figuras de fuente es parcial.
- Los tiempos y niveles son metas de entrenamiento por calibrar con Brenda. No
  hay evidencia todavía de mejora de velocidad en un examen real.
- El audio nativo funciona en Chromium de prueba; no se escuchó un parlante físico.
  Compatibilidad y sonido en el celular real de Brenda requieren uso real.
- El progreso permanece en este navegador; no hay sincronización entre dispositivos.
- Material local: 74 PDF, 43 únicos, 31 duplicados, 875 fragmentos TF-IDF y 287
  páginas recuperadas por OCR. La indexación es local, sin embeddings remotos.

## Disponibilidad por unidad

Los conteos incluyen casos directos y de apoyo; excluyen duplicados declarados y
complementarios. Representan ejercicios disponibles, no dominio de la usuaria.

| Área | Unidad | Casos |
| --- | --- | ---: |
| Números y Operaciones | Razones | 1 |
| Números y Operaciones | Regla de tres | 16 |
| Números y Operaciones | Operaciones combinadas | 8 |
| Números y Operaciones | Número decimal | 8 |
| Números y Operaciones | Sistema decimal | 8 |
| Números y Operaciones | Conteo de números y cifras | 9 |
| Números y Operaciones | Divisibilidad | 17 |
| Números y Operaciones | Números primos | 8 |
| Números y Operaciones | Máximo Común Divisor y Mínimo Común Múltiplo | 19 |
| Números y Operaciones | Fracciones | 18 |
| Números y Operaciones | Regla del tanto por ciento | 10 |
| Números y Operaciones | Aplicaciones comerciales del tanto por ciento | 16 |
| Números y Operaciones | Interés Simple y Compuesto | 8 |
| Números y Operaciones | Promedios | 34 |
| Números y Operaciones | Conjuntos | 8 |
| Números y Operaciones | Conversión de unidades y notación científica | 1 |
| Números y Operaciones | Progresión aritmética y geométrica | 35 |
| Números y Operaciones | Series y sucesiones | 16 |
| Álgebra | Teoría de exponentes | 10 |
| Álgebra | Polinomios | 9 |
| Álgebra | Productos notables | 8 |
| Álgebra | División algebraica | 1 |
| Álgebra | Factorización | 8 |
| Álgebra | Fracciones algebraicas | 1 |
| Álgebra | Ecuaciones de primer y segundo grado | 22 |
| Álgebra | Sistema de ecuaciones de primer grado | 16 |
| Álgebra | Planteo de ecuaciones | 11 |
| Álgebra | Inecuaciones de primer grado | 1 |
| Álgebra | Funciones: lineal afín y cuadrática | 1 |
| Álgebra | Aplicaciones de funciones | 8 |
| Álgebra | Racionalización | 1 |
| Álgebra | Programación lineal | 8 |
| Álgebra | Inecuaciones de segundo grado | 8 |
| Álgebra | Valor absoluto | 8 |
| Geometría | Segmentos, ángulos y ángulos entre paralelas | 2 |
| Geometría | Propiedades fundamentales de los triángulos | 1 |
| Geometría | Triángulos rectángulos notables | 8 |
| Geometría | Líneas y puntos notables en el triángulo | 2 |
| Geometría | Congruencia de triángulos | 1 |
| Geometría | Cuadriláteros: trapezoides, trapecios y paralelogramos | 1 |
| Geometría | Líneas y ángulos en la circunferencia | 8 |
| Geometría | Polígonos | 24 |
| Geometría | Proporcionalidad de segmentos y semejanza de triángulos | 8 |
| Geometría | Relaciones métricas en el triángulo rectángulo | 8 |
| Geometría | Áreas triangulares, cuadrangulares y circulares | 20 |
| Geometría | Poliedros regulares, prismas, pirámides, cilindros, cono y esfera | 12 |
| Estadística | Tablas y gráficos estadísticos | 18 |
| Estadística | Análisis Combinatorio | 17 |
| Estadística | Probabilidades | 20 |
| Trigonometría | Sistemas de medidas angulares | 8 |
| Trigonometría | Razones trigonométricas | 16 |
| Trigonometría | Identidades trigonométricas de ángulos simples, compuestos, doble y mitad | 32 |
| Trigonometría | Reducción al primer cuadrante | 8 |
| Trigonometría | Ecuaciones trigonométricas | 8 |
| Trigonometría | Funciones trigonométricas | 8 |
