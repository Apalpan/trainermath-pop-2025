# Aecodito · Supabase y Google Sheets

## Estado de la versión 4

- Proyecto Supabase: `ldcczlrarmmvreokpbdq`.
- Tablas aisladas: `tm_profiles`, `tm_user_state`, `tm_sessions`, `tm_attempts`,
  `tm_skill_states`, `tm_recommendations`, `tm_assistant_events` y `tm_sheet_outbox`.
- Las ocho tablas tienen RLS. Los intentos históricos no exponen `UPDATE` ni `DELETE`
  al cliente.
- Functions JWT: `trainer-math-sync`, `trainer-math-coach` y
  `trainer-math-sheet-sync`.
- Sheet operativo: `Entrenamiento PUCP`, pestaña `TrainerMath_v4`, columnas A:Q.
- La aplicación usa únicamente `sb_publishable_...`; ninguna clave secreta se
  publica en GitHub Pages.

## Activación de producción

1. En Supabase, abrir **Authentication → Sign In / Providers → User Signups** y
   habilitar **Allow anonymous sign-ins**. La sesión anónima da a Brenda un UUID
   privado sin pedir contraseña. Activar CAPTCHA antes de abrir el sitio a tráfico
   público amplio.
2. Elegir un proveedor para Aecodito en Edge Function secrets:
   - OpenAI: `OPENAI_API_KEY`, `AI_PROVIDER=openai` y opcional `OPENAI_MODEL`.
   - Gemini: `GEMINI_API_KEY`, `AI_PROVIDER=gemini` y opcional `GEMINI_MODEL`.
3. Para exportar sesiones, guardar `GOOGLE_SERVICE_ACCOUNT_JSON` como secreto y
   compartir el spreadsheet con el `client_email` de esa cuenta de servicio como
   editor. Opcionalmente fijar `TRAINERMATH_SHEET_ID` al ID del archivo.
4. Ejecutar `scripts/qa-cloud.cjs`. Debe mostrar `state: connected`, dejar la cola
   en cero y crear una fila de sesión sin duplicarla si se reintenta.

Las claves deben cargarse directamente en Supabase. No se pegan en el chat, el
repositorio, el HTML, Google Sheets ni `localStorage`.

## Contrato de datos

`session_finished` es el evento de cierre. Primero se guardan sesión e intentos en
Postgres; luego se recalcula el estado de las unidades tocadas y se crea una fila
idempotente en `tm_sheet_outbox`. Google recibe solo:

`event_id`, fecha, tipo, versión, código seudónimo, sesión, modo, área, unidad,
cantidad, correctas, precisión, mediana, porcentaje dentro de meta, estado de
dominio, siguiente acción y evidencia.

La IA no decide claves, selección, puntaje ni dominio. El catálogo local y el motor
adaptativo funcionan sin API; la Function remota se usa únicamente cuando Brenda
pide otra explicación después de responder. Durante el simulacro, Aecodito permanece
bloqueado hasta la entrega.
