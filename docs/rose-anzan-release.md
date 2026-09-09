# Actualización rosa y Anzan · 2026-09-09

## Cambios entregables

- Simulacros con Aritmética, Álgebra, Geometría, Trigonometría, Estadística y
  Probabilidad en cada sesión. Cuotas visibles antes de empezar y resultados por
  área al entregar. Se rota el reparto sobrante entre simulacros; una cuota se
  redistribuye si el nivel elegido tiene pocos casos en un área.
- Prioridad de casos nuevos dentro de cada área. Se conservan las garantías de
  práctica; el examen debe reciclar preguntas de un área cuando esa área se agota,
  aunque queden preguntas nuevas en otras áreas.
- Anzan independiente: números 1–9, 5/10/15/20 cifras, 0.5/1/1.5/2 segundos y
  presentación automática o con flechas. Pausa, reinicio, salida, respuesta final
  y comprobación de secuencia. El modo manual permite flecha derecha y Espacio,
  sin retroceder. La velocidad solo se usa en modo automático.
- El Anzan separa cifras idénticas con 80 ms en blanco dentro del intervalo,
  conserva foco durante el avance, pausa al ocultar la pestaña y no revela la suma
  al ingresar un formato inválido. Las rondas no alteran los intentos CEPRE.
- Logo sigma en SVG, paleta rosa pastel y Aecodito oficial. Entrada animada,
  respuesta de la mascota al tocarla y consejos de cálculo. Se respeta movimiento
  reducido. Las animaciones decorativas se limitan a bienvenida e Inicio.

## Validación local

| Comprobación | Resultado |
| --- | --- |
| 20/30/40 preguntas, niveles 0–3, 100 semillas por combinación | Pass: 1,200 simulacros incluyen las seis áreas, sin IDs duplicados |
| Rotación de cuotas, agotamiento y pools pequeños | Pass: `test-exam-coverage.cjs` |
| Motor anterior, migración y tiempos | Pass: 17 escenarios de `test-engine.cjs` |
| Cifras y suma Anzan | Pass: `test-anzan.cjs` |
| Práctica, examen, recarga, diálogos, respaldo y almacenamiento denegado | Pass: `smoke-browser.cjs` y `smoke-browser-extra.cjs` |
| Anzan manual/automático, teclado, pausa, foco, error y resultado | Pass: `smoke-rose-anzan.cjs` |
| Pantallas 320/375 px, flecha libre de la barra inferior | Pass: comprobación de overflow y `elementFromPoint` |
| Mascota oficial, consejos interactivos y movimiento reducido | Pass: navegador y revisión visual |
| HTML autónomo con navegador sin red | Pass: Anzan, logo y mascota desde archivo local |
| Errores de JavaScript | 0 en las rutas verificadas |
| Contraste real | Acción 6.66:1; texto secundario 6.08:1; texto principal 14.55:1 |

Fuentes: `web/engine.js`, `web/anzan.js`, `web/anzan.css`, `web/app.js`,
`web/brand.css`, `web/template.html`, `assets/` y `build.py`.
Capturas y métricas locales: `output/playwright/rosa-*` (ignoradas en Git).

El HTML pesa aproximadamente 1.3 MB sin compresión, con todas sus imágenes,
preguntas y código incluidos. La prueba local no realiza solicitudes adicionales.
El LCP no fue reportado por el observador usado y queda sin medición; no hay
validación de Core Web Vitals de campo ni pruebas en un teléfono físico.

Este es un simulacro de matemática para entrenamiento, sin pesos ni calificación
oficial de una convocatoria CEPRE. La mejora de Brenda requiere medir su uso real.
