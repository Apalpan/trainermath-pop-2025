# TrainerMath: validación de entrega

Actualización vigente: [rosa pastel, seis áreas y Anzan](rose-anzan-release.md).
La evidencia siguiente corresponde a la entrega anterior, antes de esa actualización.

Usuario: Brenda Sofía. Producto: TrainerMath; se mantiene la identidad clara con
acento verde del entrenador original.

Objetivo funcional: practicar casos diferentes, medir precisión y velocidad,
entender los errores y entrenar un examen configurable con tiempo total.

## Comprobaciones

| Comprobación | Estado | Evidencia |
| --- | --- | --- |
| Selección sin repetición exacta hasta recorrer el banco | Pass | Banco real: 505 preguntas a través de 26 sesiones en `scripts/test-real-bank.cjs`; además 17 escenarios del motor |
| Diversidad de familias durante una sesión | Pass | 20 familias distintas cuando hay suficientes disponibles |
| Filtros de tema, nivel, velocidad y banco vacío | Pass | Pruebas del motor |
| Temporizador examen persiste y expira | Pass | Pruebas de reloj absoluto, recarga, navegación y autoentrega del motor |
| Tiempo de explicación separado de resolución | Pass | Práctica: reloj detenido al responder |
| Revisión y métricas sin premiar pistas | Pass | Último intento, precisión sin asistencia, mediana de aciertos |
| Migración y respaldo de progreso | Pass | Pruebas de migración, validación y almacenamiento denegado |
| Verificación matemática banco nuevo | Pass | 400 + 48 respuestas exactas; 448 parámetros únicos y 56 familias; validadores y auditoría matemática |
| Flujo navegador escritorio y móvil | Pass | `scripts/smoke-browser.cjs`, 8 grupos; escritorio 1440, móvil 375 y 320 px, recarga, pausa, entrega, almacenamiento denegado |
| Exportación, importación y enlaces anteriores | Pass | `scripts/smoke-browser-extra.cjs`: #p/6, exportación, importación válida/inválida sin pérdida de progreso |
| Teclado, foco, diálogos, contraste | Pass | Teclas 1-4, modal Escape, bloqueo fuera de sesión; contraste acción 4.95:1, texto secundario 5.87:1, texto principal 16.07:1; controles táctiles verificados |
| Rendimiento de laboratorio local | Pass | Chromium 1440 px: LCP 156 ms, CLS 0, DOMContentLoaded 119 ms, 0 solicitudes adicionales; HTML 559459 bytes |
| Publicación real GitHub Pages | Pass | Feature commit `0f66aa2`, workflow `34311039011` exitoso, Pages `built`, HTTP 200 y HTML idéntico al blob Git publicado |

URL verificada: https://apalpan.github.io/trainermath-pop-2025/
Prueba en producción: 510 preguntas cargadas, filtro Trigonometría, inicio de
práctica y respuesta con feedback. Hash SHA-256 del HTML publicado:
`492322eb9b45f6ccf71b91be7a862e1ef850c14cfd6127abf2a7875c0ed4b16d`.
La copia local Windows solo difiere en finales de línea CRLF/LF.

Capturas locales: `output/playwright/`. En móvil, el mapa del examen comienza
cerrado y se abre por un botón situado sobre la navegación inferior. No hay
scroll horizontal en 320/375 px. El perfil puede usarse incluso si el navegador
bloquea almacenamiento; en ese caso se informa y se ofrece exportar.

Índice local verificado: 868 fragmentos TF-IDF; 299 páginas procesadas con OCR y
287 incorporadas por aportar texto frente a la extracción original. El OCR no
certifica ecuaciones ni diagramas. Se conserva evidencia visual de temas y se
generan ejercicios originales con cálculo verificado.

Las métricas de tiempo son metas de entrenamiento. El simulacro no certifica
formato, distribución o calificación oficial CEPRE. Los datos permanecen en el
navegador y los respaldos se exportan manualmente.

No hay medición de mejora real de Brenda todavía. Recomendación de validación:
comparar cinco sesiones de igual tema y nivel; buscar menos tiempo manteniendo
precisión. No deducir aprendizaje solo de un menor cronómetro.
Las cifras de rendimiento son una medición local, sin emulación de una red móvil;
no representan Core Web Vitals de usuarios reales ni una medición de INP en campo.
