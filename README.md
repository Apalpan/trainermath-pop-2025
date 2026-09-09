# TrainerMath · Brenda Sofía

Entrenamiento de precisión, velocidad y criterio para admisión. **510 ejercicios**:
448 nuevos en 56 familias matemáticas y los 62 originales POP 2025, con sus
soluciones y figuras. Las cinco copias declaradas del examen original se conservan
para estudio y se excluyen del sorteo de entrenamiento: **505 preguntas elegibles**.

**Aplicación:** [Abrir TrainerMath](https://apalpan.github.io/trainermath-pop-2025/)

## Uso

- **Inicio:** identidad rosa pastel para Brenda Sofía, logo matemático Σ y Aecodito
  oficial con consejos interactivos. Animaciones breves con respeto a movimiento reducido.
- **Práctica:** tema, estrellas, cantidad y enfoque (variedad, adaptativo, velocidad
  o repaso). Prioriza preguntas no vistas y distintas familias; recicla las más
  antiguas solo al agotar el filtro. El repaso recupera errores de forma deliberada.
- **Aprendizaje:** pista opcional, atajo, trampa habitual y solución con revelado
  progresivo. La explicación no aumenta el tiempo de resolución.
- **Anzan:** solo cifras del 1 al 9, cantidad 5/10/15/20, aparición automática a
  0.5/1/1.5/2 segundos o avance con flecha derecha/Espacio. Sumar mentalmente y
  comprobar al final. Pausa, reinicio y salida; se detiene al ocultar la pestaña.
  Este calentamiento no modifica las métricas de ejercicios CEPRE.
- **Examen CEPRE:** elegir estrellas, preguntas y minutos. Siempre incluye las seis
  áreas matemáticas; muestra las cuotas antes y los resultados por área después.
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
node scripts/test-engine.cjs
node scripts/test-exam-coverage.cjs
node scripts/test-anzan.cjs
python build.py
node --check web/app.js
```

Los validadores comprueban resultados exactos, alternativas, dominios y
duplicados de parámetros matemáticos, además de enunciados. La prueba de navegador
`scripts/smoke-browser.cjs` necesita Playwright disponible en el entorno, el
servidor local y guarda capturas en `output/playwright/`.
`scripts/smoke-rose-anzan.cjs` verifica el Anzan, el examen con seis áreas, la
identidad, el teclado, 320/375 px y la ejecución offline del HTML completo.

## Material local de academia

`Informacion/` y `output/` se excluyen de Git. Los PDFs, imágenes OCR y textos
extraídos **no se publican**. Solo se versiona metadata de procedencia.

Inventario: 73 archivos PDF, 42 documentos únicos, 31 copias idénticas. Índice:
868 fragmentos, con 287 páginas recuperadas por OCR local. Vectorización
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
