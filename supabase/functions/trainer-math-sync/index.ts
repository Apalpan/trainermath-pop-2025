import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.116.0";

const allowedOrigins = new Set([
  "https://apalpan.github.io",
  "http://127.0.0.1:8768",
  "http://127.0.0.1:8769",
  "http://localhost:8768",
  "http://localhost:8769",
]);
const headers = (origin: string | null) => ({
  "Access-Control-Allow-Origin": origin && allowedOrigins.has(origin) ? origin : "https://apalpan.github.io",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Content-Type": "application/json; charset=utf-8",
  "Vary": "Origin",
});
const respond = (origin: string | null, status: number, body: Record<string, unknown>) => new Response(JSON.stringify(body), { status, headers: headers(origin) });
const clip = (value: unknown, max: number) => String(value ?? "").trim().slice(0, max);
const numberIn = (value: unknown, min: number, max: number) => Math.max(min, Math.min(max, Number(value) || 0));
const median = (values: number[]) => { const rows = values.filter(Number.isFinite).sort((a, b) => a - b); const mid = Math.floor(rows.length / 2); return rows.length ? (rows.length % 2 ? rows[mid] : (rows[mid - 1] + rows[mid]) / 2) : 0; };
const configured = () => ({
  ai: Boolean(Deno.env.get("OPENAI_API_KEY") || Deno.env.get("GEMINI_API_KEY")),
  sheet: Boolean(Deno.env.get("GOOGLE_SERVICE_ACCOUNT_JSON") || Deno.env.get("TRAINERMATH_SHEETS_WEBHOOK_URL")),
});

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: headers(origin) });
  if (req.method !== "POST") return respond(origin, 405, { ok: false, code: "method_not_allowed" });
  const authHeader = req.headers.get("authorization") || "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) return respond(origin, 401, { ok: false, code: "authentication_required" });

  const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
  const anonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";
  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  const userClient = createClient(supabaseUrl, anonKey, { global: { headers: { Authorization: authHeader } } });
  const admin = createClient(supabaseUrl, serviceKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const { data: userData, error: userError } = await userClient.auth.getUser(token);
  if (userError || !userData.user) return respond(origin, 401, { ok: false, code: "invalid_session" });
  const ownerId = userData.user.id;

  const raw = await req.text();
  if (raw.length > 180_000) return respond(origin, 413, { ok: false, code: "payload_too_large" });
  let body: Record<string, unknown>;
  try { body = JSON.parse(raw); } catch { return respond(origin, 400, { ok: false, code: "invalid_json" }); }
  const action = clip(body.action, 30);
  const services = configured();

  if (action === "bootstrap") {
    const profile = body.profile && typeof body.profile === "object" ? body.profile as Record<string, unknown> : {};
    const { error } = await admin.from("tm_profiles").upsert({
      owner_id: ownerId,
      display_name: clip(profile.display_name, 80) || "Brenda Sofía",
      timezone: clip(profile.timezone, 80) || "America/Lima",
      app_version: clip(body.app_version, 30) || "4.0.0",
    }, { onConflict: "owner_id" });
    if (error) return respond(origin, 500, { ok: false, code: "profile_write_failed" });
    return respond(origin, 200, { ok: true, ai_available: services.ai, sheet_available: services.sheet });
  }

  if (action !== "complete_session") return respond(origin, 400, { ok: false, code: "invalid_action" });
  const sessionInput = body.session && typeof body.session === "object" ? body.session as Record<string, unknown> : {};
  const attemptsInput = Array.isArray(body.attempts) ? body.attempts.slice(0, 50) as Record<string, unknown>[] : [];
  const sessionId = clip(sessionInput.client_session_id, 80);
  const mode = clip(sessionInput.mode, 20);
  if (!/^[a-z0-9-]{4,80}$/i.test(sessionId) || !["practice", "exam"].includes(mode)) return respond(origin, 400, { ok: false, code: "invalid_session" });
  const questionIds = Array.isArray(sessionInput.question_ids) ? sessionInput.question_ids.map(id => clip(id, 80)).filter(Boolean).slice(0, 50) : [];
  const questionCount = Math.round(numberIn(sessionInput.question_count, 0, 50));
  const correctCount = Math.round(numberIn(sessionInput.correct_count, 0, questionCount));
  const finishedAt = new Date(clip(sessionInput.finished_at, 40));
  if (!Number.isFinite(finishedAt.getTime()) || attemptsInput.length !== questionCount) return respond(origin, 400, { ok: false, code: "session_rows_mismatch" });

  const sessionRow = {
    owner_id: ownerId, client_session_id: sessionId, mode,
    variant: clip(sessionInput.variant, 30) || "variety", question_count: questionCount,
    correct_count: correctCount, seconds: numberIn(sessionInput.seconds, 0, 86400), question_ids: questionIds,
    content_version: clip(body.content_version, 80) || "unknown", app_version: clip(body.app_version, 30) || "unknown",
    finished_at: finishedAt.toISOString(),
  };
  const { error: sessionError } = await admin.from("tm_sessions").upsert(sessionRow, { onConflict: "owner_id,client_session_id", ignoreDuplicates: true });
  if (sessionError) return respond(origin, 500, { ok: false, code: "session_write_failed" });

  const attemptRows = attemptsInput.map(item => ({
    owner_id: ownerId, client_attempt_key: clip(item.client_attempt_key, 140), client_session_id: sessionId,
    question_id: clip(item.question_id, 80), area: clip(item.area, 90), unit_id: clip(item.unit_id, 40),
    unit_label: clip(item.unit_label, 140), family: clip(item.family, 100), difficulty: Math.round(numberIn(item.difficulty, 1, 3)),
    correct: Boolean(item.correct), seconds: numberIn(item.seconds, 0, 86400), target_seconds: numberIn(item.target_seconds, 1, 86400),
    assisted: Boolean(item.assisted), confidence: ["segura", "duda", "azar"].includes(clip(item.confidence, 20)) ? clip(item.confidence, 20) : "",
    error_reason: ["concepto", "calculo", "lectura", "tiempo"].includes(clip(item.error_reason, 20)) ? clip(item.error_reason, 20) : "",
    skipped: Boolean(item.skipped), attempted_at: Number.isFinite(new Date(clip(item.attempted_at, 40)).getTime()) ? new Date(clip(item.attempted_at, 40)).toISOString() : finishedAt.toISOString(),
  }));
  if (attemptRows.some(row => !row.client_attempt_key || !row.question_id || !row.area || !row.unit_id || !row.unit_label || !row.family)) return respond(origin, 400, { ok: false, code: "invalid_attempt" });
  if (attemptRows.length) {
    const { error: attemptsError } = await admin.from("tm_attempts").upsert(attemptRows, { onConflict: "owner_id,client_attempt_key", ignoreDuplicates: true });
    if (attemptsError) return respond(origin, 500, { ok: false, code: "attempt_write_failed" });
  }

  const touchedUnits = [...new Set(attemptRows.map(row => row.unit_id))];
  const skillResults: Array<Record<string, unknown>> = [];
  for (const unitId of touchedUnits) {
    const { data: history } = await admin.from("tm_attempts")
      .select("unit_id,unit_label,area,correct,assisted,seconds,target_seconds,attempted_at,client_session_id")
      .eq("owner_id", ownerId).eq("unit_id", unitId).order("attempted_at", { ascending: true }).limit(500);
    const rows = history || [], count = rows.length;
    const correct = rows.filter(row => row.correct && !row.assisted).length;
    const within = rows.filter(row => row.correct && !row.assisted && Number(row.seconds) <= Number(row.target_seconds)).length;
    const assisted = rows.filter(row => row.assisted).length;
    const last5 = rows.slice(-5), speedEvidence = last5.filter(row => row.correct && !row.assisted && Number(row.seconds) <= Number(row.target_seconds)).length;
    const sessions = new Set(rows.map(row => row.client_session_id)).size;
    const mastered = count >= 5 && last5.length === 5 && speedEvidence >= 4 && sessions >= 2;
    const accuracy = count ? correct / count : 0, speedRate = count ? within / count : 0;
    const status = !count ? "nuevo" : mastered ? "a velocidad" : count < 3 ? "señal inicial" : accuracy >= .75 ? "estable" : "en desarrollo";
    const latest = rows.at(-1), latestStrong = latest?.correct && !latest?.assisted && Number(latest?.seconds) <= Number(latest?.target_seconds);
    const reviewDays = latestStrong ? (mastered ? 14 : accuracy >= .75 ? 7 : 3) : 1;
    const nextReview = new Date((latest ? new Date(latest.attempted_at).getTime() : Date.now()) + reviewDays * 86400000).toISOString();
    const skill = { owner_id: ownerId, unit_id: unitId, unit_label: clip(rows[0]?.unit_label, 140), area: clip(rows[0]?.area, 90), attempts: count, correct_unassisted: correct, within_target: within, assisted, accuracy, speed_rate: speedRate, status, next_review_at: nextReview, algorithm_version: "adaptive-v1" };
    await admin.from("tm_skill_states").upsert(skill, { onConflict: "owner_id,unit_id" });
    skillResults.push(skill);
  }

  const weakest = skillResults.slice().sort((a, b) => Number(a.accuracy) - Number(b.accuracy) || Number(a.speed_rate) - Number(b.speed_rate))[0];
  if (weakest) await admin.from("tm_recommendations").insert({ owner_id: ownerId, unit_id: weakest.unit_id, area: weakest.area, reason: `Refuerza ${weakest.unit_label}: ${Math.round(Number(weakest.accuracy) * 100)}% de precisión y ${Math.round(Number(weakest.speed_rate) * 100)}% a velocidad.`, payload: { next_count: 5, mode: "adaptive", status: weakest.status }, algorithm_version: "adaptive-v1" });

  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(ownerId));
  const learnerCode = Array.from(new Uint8Array(digest)).map(byte => byte.toString(16).padStart(2, "0")).join("").slice(0, 10);
  const times = attemptRows.map(row => Number(row.seconds)).filter(value => value > 0);
  const withinCount = attemptRows.filter(row => row.correct && !row.assisted && Number(row.seconds) <= Number(row.target_seconds)).length;
  const areas = [...new Set(attemptRows.map(row => row.area))];
  const units = [...new Set(attemptRows.map(row => row.unit_label))];
  const sheetPayload = {
    event_id: sessionId, fecha: finishedAt.toISOString(), tipo: "session", version: clip(body.app_version, 30) || "4.0.0",
    learner_code: `brenda-${learnerCode}`, sesion: sessionId, modo: mode,
    area: areas.length === 5 ? "5 áreas" : areas.join(" · ").slice(0, 160), unidad: units.slice(0, 3).join(" · ").slice(0, 240),
    intentos: questionCount, correctas: correctCount, precision_pct: questionCount ? Math.round(correctCount / questionCount * 100) : 0,
    mediana_s: Number(median(times).toFixed(1)), dentro_meta_pct: questionCount ? Math.round(withinCount / questionCount * 100) : 0,
    cambio_dominio: weakest ? weakest.status : "sin evidencia", siguiente_accion: weakest ? `5 casos · ${weakest.unit_label}` : "Completar diagnóstico", evidencia: "Supabase tm_sessions/tm_attempts",
  };
  const { error: outboxError } = await admin.from("tm_sheet_outbox").upsert({ owner_id: ownerId, event_key: `${ownerId}:${sessionId}`, event_type: "session", payload: sheetPayload, status: "pending", next_attempt_at: new Date().toISOString() }, { onConflict: "event_key", ignoreDuplicates: true });
  if (outboxError) return respond(origin, 500, { ok: false, code: "outbox_write_failed" });

  return respond(origin, 200, { ok: true, ai_available: services.ai, sheet_available: services.sheet, sheet_queued: true, skill_states_updated: skillResults.length });
});
