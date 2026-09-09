# Auditoría de material de admisión

## Alcance y privacidad

El corpus se procesa localmente desde `Informacion/`. El índice de recuperación
(`Informacion/_index/`) contiene texto extraído y vectores solo para uso local;
no se publica. `data/source-map.json` guarda únicamente rutas relativas,
paginación, calidad de extracción y etiquetas de cobertura.

## Inventario verificado

- 73 PDF encontrados recursivamente; 42 documentos únicos y 31 copias exactas
  duplicadas.
- Antes de OCR, 31 documentos tenían texto utilizable, 5 texto bajo y 6 no
  exponían texto extraíble. No hubo PDFs corruptos.
- La generación actual usa PyMuPDF como extractor primario y combina OCR local
  de páginas con texto nativo insuficiente. El manifiesto actual registra 868
  segmentos, 287 páginas OCR incorporadas y la advertencia explícita de revisar
  ecuaciones y diagramas. La recuperación sigue siendo TF-IDF por tokens con
  similitud coseno; no son embeddings semánticos.
- La caché local `Informacion/_ocr/` contiene 299 resultados de OCR para 11
  PDFs escaneados o de texto bajo. La confianza media de página es 67/100,
  con 25 páginas bajo 50/100, 148 bajo 70/100 y 7 sin texto. Es cobertura de
  recuperación, no validación matemática de las transcripciones.

## Cobertura para el banco nuevo

| Tema | Evidencia verificable | Familias que permite derivar |
| --- | --- | --- |
| Aritmética | `Informacion/ARITMÉTICA - PRISMA 2025 (1).pdf`, p. 2 (índice visual) | conjuntos, divisibilidad, promedios y mezclas, primos, MCD/MCM, fracciones, combinatoria, probabilidades, PA/PG, porcentajes e interés |
| Álgebra | `Informacion/CIENCIAS PRACTICAS/Practiquemos Semana 1 CC.pdf`, pp. 4-5; `Simulacro Paideia - Semana 3 CC.pdf`, pp. 4-5 | ecuaciones, sistemas, reducción de expresiones, polinomios, divisibilidad y cociente/residuo |
| Geometría | `Informacion/GEOMETRÍA - PRISMA 2025 (1).pdf`, p. 2 (índice visual); `CRP Hora 5 Semana 4 2026.7 LL.pdf`, pp. 1 y 5 | ángulos, triángulos, puntos/líneas notables, semejanza, polígonos, circunferencia, áreas y sólidos |
| Trigonometría | `Informacion/TRIGONOMETRÍA - PRISMA 2025 (1).pdf`, pp. 5-7, 10, 13 y 16 (revisión visual) | razones y ángulos notables, aplicaciones de elevación/depresión, identidades fundamentales y auxiliares, ángulos compuestos y ángulo doble |
| Sucesiones y velocidad aritmética | `Informacion/CIENCIAS PRACTICAS/Practiquemos semana 5 cc.pdf`, pp. 2-3; `CRP Hora 1 Semana 5 2026.7 LL.pdf`, p. 2 | término, razón, suma de PA/PG y simplificación para cálculo mental |
| Porcentajes | `Informacion/CIENCIAS PRACTICAS/Simulacro Paideia - Semana 5 - 2026.7 - LL.pdf`, p. 2 | aumentos/disminuciones sucesivas y variación de área |
| Conteo y conjuntos | `Informacion/CIENCIAS PRACTICAS/CRP Hora 1 Semana 4 2026.7 LL.pdf`, p. 2 | inclusión-exclusión, preferencias y lectura rápida de datos |
| Geometría de examen | `Informacion/CIENCIAS PRACTICAS/Practiquemos semana 4 cc.pdf`, p. 9; `Simulacro Paideia - Semana 3 CC.pdf`, pp. 5 y 7 | diagonales, ángulos de polígonos, inscritos, apotemas, mediatrices y áreas |

Los documentos `CRP Hora 1-5` (semanas 3-5), `Practiquemos` (semanas 1, 4 y
5), `Simulacro Paideia` (semanas 2, 3 y 5) y sus `Claves` aportan una estructura
útil para práctica CEPRE: tema, bloque por hora, semana, simulacro, respuesta y
revisión. El entrenador puede transformar esa estructura en bloques
cronometrados y mezcla intercalada; los tiempos exactos no se infieren porque
los PDFs revisados no los declaran de forma consistente.

## Límites y siguiente tratamiento

- Los libros Prisma de Aritmética (2024/2025), Geometría (2024/2025) y
  Trigonometría (2024/2025) son escaneos. Se revisaron visualmente páginas 1-2
  de las ediciones 2025: Aritmética y Geometría presentan índices legibles, lo
  que respalda las etiquetas de cobertura; el texto de ejercicios requiere OCR
  antes de usarlo como fuente literal.
- `TRIGONOMETRÍA - PRISMA 2025 (1).pdf` es un PDF concatenado. Sus páginas 1-3
  corresponden a Geometría; la p. 4 reinicia con la portada de Trigonometría,
  la p. 5 enumera el temario trigonométrico y la p. 6 muestra ejercicios de
  razones trigonométricas en figuras. Por ello la evidencia de Trigonometría
  debe citar pp. 5-6, nunca las pp. 1-3. La cobertura está verificada a nivel
  de temario y formato, mientras que OCR todavía debe validar el texto de cada
  ejercicio y no sustituye la comprobación de diagramas.
- Las páginas de evidencia específicas son: 6-7 para razones, triángulos y
  figuras; 10 para aplicaciones de elevación/depresión; 13 para identidades
  auxiliares; y 16 para identidades de doble ángulo y reducción. La mención a
  ángulos verticales queda limitada al índice de la p. 5, pues no se verificó
  una página posterior dedicada a esa subfamilia.
- En el OCR local, las fuentes con confianza media más baja son Geometría 2024
  (55.5/100), Trigonometría 2024 (61.3/100) y Trigonometría 2025 (60.8/100).
  Esas cifras no miden corrección de fórmulas ni de diagramas. Los segmentos
  marcados `ocr_needs_formula_review` deben servir para localizar material,
  mientras que los datos y la solución de cada ejercicio nuevo se validan por
  cálculo independiente.
- `SAB seminario 2 CC resuelto.pdf`, `Seminario 1 resuelto.pdf`,
  `Seminario 3 cc.pdf`, `Seminario 4 resuelto CC.pdf` y `Seminario 5.pdf`
  tienen extracción insuficiente; conservarlos como fuentes potenciales, no
  como evidencia textual.
- Diagramas, notación matemática y alternativas complejas pueden degradarse
  en PDF a texto. Toda familia derivada debe ser original, validada
  matemáticamente y no una reproducción del material de academia.

## Uso reproducible

```powershell
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\ingest_material.py
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts\search_material.py 'polígonos regulares ángulos' --limit 8
```

El segundo comando devuelve rutas, página, etiquetas y una vista previa local.
