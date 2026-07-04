# TrainerMath · POP 2025

Entrenador interactivo del **examen Reconstruido PUCP — Primera Opción 2025** (23-nov-2025, Academia Prisma): los 62 problemas resueltos paso a paso. Tema light, single-file.

**Live:** https://apalpan.github.io/trainermath-pop-2025/

## Uso

Abrir `index.html` en cualquier navegador. Sin dependencias ni build de JS (single-file).

- **Estudio**: grid de 62 problemas filtrable por tema (Aritmética, Álgebra, Geometría, Probabilidad, Estadística) y estado (pendientes / correctos / fallados). Cada problema: responde primero → feedback → resolución paso a paso con revelado progresivo, respuesta final e idea clave.
- **Simulacro**: preguntas al azar por tema, cronómetro, resumen final con revisión.
- **Teclado**: `A–D`/`1–4` responder · `Espacio` siguiente paso · `←/→` navegar · `Esc` cerrar.
- Progreso en `localStorage` (`tm_pop2025_v1`).

## Regenerar

```
python build.py   →  index.html
```

- `data_p1..p4.py` — enunciados, opciones, respuesta y pasos de los 62 problemas.
- `figs.py` — figuras SVG (21) generadas con coordenadas calculadas.
- `mh.py` — helpers de notación matemática (fracciones, raíces) en HTML/CSS puro.

## Verificación

- Las 62 respuestas fueron validadas por fuerza bruta/cómputo directo en Python (55 checks automáticos + 7 triviales a mano).
- Erratas del PDF reconstruido documentadas en la app (campo `nota`): P6 (alternativas A y C repetidas), P14 (línea «calcular √A» cortada), P49 («lleno» → «llano»), P51 («m²» → «cm²»).
- Fuente: `Reconstruido-examen-Primera-Opcion-2025.pdf`.
