# TrainerMath · Brenda Sofía

Entrenamiento de precisión, velocidad y criterio para admisión. **606 ejercicios**:
544 nuevos en 68 familias matemáticas y los 62 originales POP 2025, con sus
soluciones y figuras. Las cinco copias declaradas del examen original se conservan
para estudio. También se apartan 10 casos complementarios al temario:
**591 preguntas elegibles** para práctica y simulacros.

**Aplicación:** [Abrir TrainerMath](https://apalpan.github.io/trainermath-pop-2025/)

## Uso

- **Inicio:** identidad rosa pastel para Brenda Sofía, logo matemático Σ y Aecodito
  oficial con consejos interactivos. Animaciones breves con respeto a movimiento reducido.
- **Práctica:** área y unidad del temario, estrellas, cantidad y enfoque (variedad, adaptativo, velocidad
  o repaso). Prioriza preguntas no vistas y distintas familias; recicla las más
  antiguas solo al agotar el filtro. El repaso recupera errores de forma deliberada.
- **Aprendizaje:** pista opcional, atajo, trampa habitual y solución con revelado
  progresivo. La explicación no aumenta el tiempo de resolución.
- **Anzan:** cifras del 1 al 9, cantidad 5/10/15/20; velocidad editable entre 0,25 y
  5 segundos en pasos de 0,05. Acepta coma o punto, con accesos 0,75/1,25/1,5/1,75.
  Presentación automática o flecha derecha/Espacio. Preparación 3–2–1 con Aecodito,
  pantalla de concentración con degradados, sonido opcional por cifra y calculadora
  táctil para responder. Pausa, reinicio y salida; se detiene al ocultar la pestaña.
  Este calentamiento no modifica las métricas de ejercicios CEPRE.
- **Examen CEPRE:** elegir estrellas, preguntas y minutos. Siempre incluye las cinco
  áreas matemáticas de la ruta Prisma; muestra las cuotas antes y los resultados por área después.
  Prioriza preguntas nuevas dentro de cada área y recicla al agotar esa área.
  Las cuotas se ajustan al banco disponible en el nivel. Cambiar respuestas, marcar y navegar;
  las soluciones se muestran después de entregar. El reloj total persiste al
  recargar y la entrega es automática al vencer el tiempo.
- **Revisión:** errores, respuestas con pista y aciertos fuera del tiempo objetivo.
- **Teclado:** A–D o 1–4 responden en la sesión visible; flechas navegan el examen;
  Escape cancela el diálogo de entrega.
- **Respaldo:** exportar e importar el progreso desde el pie de la aplicación.

Los tiempos son **metas pedagógicas**, pendientes de calibración con uso real.
El simulacro es configurable y no afirma reproducir una convocatoria o escala
oficial CEPRE. La mejora real se evalúa comparando precisión y tiempo a igual tema
y nivel durante varias sesiones.

El perfil es local, sin contraseña ni autenticación remota. No hay sincronización
entre dispositivos. Se conserva la clave antigua `tm_pop2025_v1` y se migra su
progreso al nuevo almacenamiento `trainermath_brenda_v3`. No se atribuyen tiempos
inventados a intentos antiguos.

## Temario y auditoría

La organización sigue la página 4 del PDF de **Prisma · Talento 2026-2** aportado
por el usuario: Números y Operaciones, Álgebra, Geometría, Estadística y
Trigonometría. Hay casos en las 55 unidades; no implica cobertura exhaustiva de
cada subhabilidad. PA/PG aparecen en Números y Operaciones, y Probabilidad y
Combinatoria dentro de Estadística. El temario oficial PUCP usa otra organización
por competencias; se explica esta distinción en la aplicación.

La auditoría corrigió alternativas duplicadas, condiciones de dominio y
enunciados en los originales 6, 24, 28, 51 y 54, además del extremo de intervalo
en la figura 33. Se preservan IDs, claves y el progreso previo.
Véase [auditoría y evidencia vigente](docs/temario-anzan-release.md).

## Ejecutar y construir

Abrir `index.html` directamente, incluso sin conexión, o servirlo localmente:

```powershell
python build.py
python -m http.server 8768 --bind 127.0.0.1
```

No requiere frameworks ni dependencias de frontend. `build.py` produce un único
HTML con estilos, datos y JavaScript incluidos. Las fuentes editables están en
`web/`; el banco nuevo, en `data/`; las figuras y resoluciones originales,
en `figs.py` y `data_p1.py` a `data_p4.py`.

## Validar

```powershell
python scripts/validate_bank.py
python scripts/validate_trigonometry.py
python scripts/validate_syllabus_additions.py
python scripts/audit-math-independent.py
python scripts/audit-syllabus-independent.py
node scripts/test-engine.cjs
node scripts/test-exam-coverage.cjs
node scripts/test-curriculum.cjs
node scripts/test-anzan.cjs
python build.py
node --check web/app.js
```

Los validadores comprueban resultados exactos, alternativas, dominios y
duplicados de parámetros matemáticos, además de enunciados. La prueba de navegador
`scripts/smoke-browser.cjs` necesita Playwright disponible en el entorno, el
servidor local y guarda capturas en `output/playwright/`.
`scripts/smoke-rose-anzan.cjs` verifica el Anzan, el examen con cinco áreas, la
identidad, el teclado, 320/375 px y la ejecución offline del HTML completo.

## Material local de academia

`Informacion/` y `output/` se excluyen de Git. Los PDFs, imágenes OCR y textos
extraídos **no se publican**. Solo se versiona metadata de procedencia.

Inventario: 74 archivos PDF, 43 documentos únicos, 31 copias idénticas. Índice:
875 fragmentos, con 287 páginas recuperadas por OCR local. Vectorización
**TF-IDF y similitud coseno**, sin API ni embeddings semánticos.

```powershell
python scripts/ingest_material.py
python scripts/search_material.py 'porcentajes sucesivos' --limit 8
```

La extracción usa PyMuPDF o pypdf. Para repetir OCR se requiere PyMuPDF y una
instalación local de Tesseract.js 7 en la carpeta de herramientas ignorada:

```powershell
npm install --prefix output/ocr-tooling --no-audit --no-fund tesseract.js@7
python scripts/render_ocr_pages.py
node scripts/ocr_material.cjs
python scripts/ingest_material.py
```

El OCR sirve para localizar temas; las fórmulas, claves y diagramas se revisan
visualmente antes de usarlos. Los ejercicios nuevos son elaboraciones originales
alineadas con el material, no transcripciones automáticas. Véanse
`docs/material-audit.md`, `docs/exercise-bank.md` y
`docs/production-checklist.md` para cobertura y evidencia.
