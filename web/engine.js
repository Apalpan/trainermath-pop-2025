/* TrainerMath: selection, scoring and browser-local progress. No network calls. */
(function (root) {
  'use strict';
  const KEY = 'trainermath_brenda_v3';
  const VERSION = 3;
  const emptyState = () => ({version: VERSION, profile: 'Brenda Sofía', attempts: [], seen: {}, sessions: [], active: null});
  const qid = p => String(p.id ?? p.n);
  const isObj = x => x && typeof x === 'object' && !Array.isArray(x);
  const numeric = (x, fallback = 0) => Number.isFinite(Number(x)) ? Number(x) : fallback;
  const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, numeric(x)));
  const randomId = () => Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  function normalize(raw, bank) {
    if (!isObj(raw) || raw.version !== VERSION || !Array.isArray(raw.attempts) || !isObj(raw.seen) || !Array.isArray(raw.sessions)) throw new Error('El archivo no es un respaldo válido de TrainerMath.');
    const byId = new Map(bank.map(p => [qid(p), p]));
    const state = emptyState();
    const keys = new Set();
    state.attempts = raw.attempts.filter(isObj).filter(a => byId.has(String(a.qid))).slice(-30000).map(a => {
      const p = byId.get(String(a.qid));
      const choice = Number.isInteger(a.choice) && a.choice >= 0 && a.choice < p.opts.length ? a.choice : null;
      return {key: String(a.key || randomId()).slice(0, 140), qid: qid(p), topic: p.tema, family: p.family || qid(p), choice,
        correct: choice === p.ans, seconds: clamp(a.seconds, 0, 86400), target: p.target || 90,
        hint: a.hint === true, mode: ['practice', 'exam', 'legacy'].includes(a.mode) ? a.mode : 'practice',
        at: clamp(a.at, 0, Date.now()), confidence: ['segura', 'duda', 'azar'].includes(a.confidence) ? a.confidence : '',
        reason: ['concepto', 'calculo', 'lectura', 'tiempo'].includes(a.reason) ? a.reason : '', skipped: choice === null};
    }).filter(a => !keys.has(a.key) && keys.add(a.key));
    for (const [id, value] of Object.entries(raw.seen)) if (byId.has(id)) state.seen[id] = clamp(value, 0, Date.now());
    state.sessions = raw.sessions.filter(isObj).slice(-200).map(s => ({id: String(s.id).slice(0, 80), mode: s.mode === 'exam' ? 'exam' : 'practice', at: clamp(s.at, 0, Date.now()), count: clamp(s.count, 0, bank.length), correct: clamp(s.correct, 0, bank.length), seconds: clamp(s.seconds, 0, 86400)}));
    if (isObj(raw.active) && Array.isArray(raw.active.ids) && raw.active.ids.length && raw.active.ids.every(id => byId.has(String(id)))) {
      const a = raw.active;
      const ids = [...new Set(a.ids.map(String))];
      const answers = {};
      for (const id of ids) {
        const ans = isObj(a.answers) ? a.answers[id] : null;
        if (!isObj(ans)) continue;
        const p = byId.get(id);
        answers[id] = {choice: Number.isInteger(ans.choice) && ans.choice >= 0 && ans.choice < p.opts.length ? ans.choice : null, seconds: clamp(ans.seconds, 0, 86400), hint: ans.hint === true, confidence: ['segura','duda','azar'].includes(ans.confidence) ? ans.confidence : '', reason: ['concepto','calculo','lectura','tiempo'].includes(ans.reason) ? ans.reason : ''};
      }
      const times = {};
      for (const id of ids) times[id] = clamp(a.times?.[id], 0, 86400);
      state.active = {id: String(a.id).slice(0,80), mode: a.mode === 'exam' ? 'exam' : 'practice', variant: ['variety','speed','review','adaptive','study'].includes(a.variant) ? a.variant : 'variety', ids, index: clamp(Math.trunc(a.index),0,ids.length-1), answers, times,
        flags: Array.isArray(a.flags) ? a.flags.map(String).filter(id => ids.includes(id)) : [], startedAt: clamp(a.startedAt,0,Date.now()), deadline: clamp(a.deadline,0,Date.now()+86400000), duration: clamp(a.duration,60,86400), paused: a.paused === true,
        runningSince: clamp(a.runningSince,0,Date.now()), hintIds: Array.isArray(a.hintIds) ? a.hintIds.map(String).filter(id => ids.includes(id)) : []};
    }
    return state;
  }
  function load(storage, bank) {
    try {
      const raw = storage.getItem(KEY);
      if (raw) return {state: normalize(JSON.parse(raw), bank), warning: ''};
      const state = emptyState();
      const legacyRaw = storage.getItem('tm_pop2025_v1');
      if (legacyRaw) {
        const old = JSON.parse(legacyRaw);
        for (const p of bank.filter(p => p.origin === 'original')) {
          if (old?.seen?.[p.n]) state.seen[qid(p)] = Date.now();
          const a = old?.ans?.[p.n];
          if (!a) continue;
          state.seen[qid(p)] = Date.now();
          const choice = Number.isInteger(a.pick) ? a.pick : Number.isInteger(a.i) ? a.i : (a.ok ? p.ans : null);
          state.attempts.push({key: 'legacy-'+qid(p), qid: qid(p), topic:p.tema, family:p.family, choice, correct:choice===p.ans, seconds:0, target:p.target, hint:true, mode:'legacy', at:Date.now(), confidence:'', reason:'', skipped:choice===null});
        }
      }
      return {state, warning: ''};
    } catch (error) { return {state: emptyState(), warning: 'No se pudo leer el progreso guardado. Esta sesión funcionará en memoria; el respaldo anterior no se sobrescribe.', readOnly: true}; }
  }
  function save(storage, state) {
    try { storage.setItem(KEY, JSON.stringify(state)); return {ok:true}; }
    catch (error) { return {ok:false, error:'No se pudo guardar en este navegador. Exporta tu progreso antes de cerrar.'}; }
  }
  function latestAttempts(state) {
    const map = new Map();
    for (const a of state.attempts) map.set(a.qid, a);
    return map;
  }
  function needsReview(a) { return !!a && (!a.correct || a.hint || (a.seconds > a.target && a.mode !== 'legacy')); }
  function filtered(bank, options = {}) {
    return bank.filter(p => p.practiceEligible !== false && (!options.topic || options.topic === 'Todos' || p.tema === options.topic) && (!Number(options.level) || p.dif === Number(options.level)) && (!options.subtopic || options.subtopic === 'Todos' || p.sub === options.subtopic) && (!options.curriculumItem || options.curriculumItem === 'Todos' || p.curriculum?.item === options.curriculumItem) && (options.mode !== 'speed' || p.target <= 60));
  }
  function selectProblems(bank, state, options = {}, rng = Math.random) {
    let pool = filtered(bank, options);
    const latest = latestAttempts(state);
    if (options.mode === 'review') pool = pool.filter(p => needsReview(latest.get(qid(p))));
    const topicStats = stats(state).topics;
    const ranked = pool.map(p => {
      const seen = Object.hasOwn(state.seen, qid(p));
      const weakness = topicStats[p.tema] ? 1 - topicStats[p.tema].accuracy / 100 : 0.4;
      // Unseen questions always precede recycled questions. Within those, mix families and weak topics.
      return {p, priority: seen ? 1 : 0, age: seen ? state.seen[qid(p)] : 0, score: rng() + (options.mode === 'adaptive' ? weakness * .8 : 0)};
    }).sort((a,b) => a.priority-b.priority || (a.priority ? a.age-b.age : b.score-a.score));
    const result = [];
    const count = Math.min(Math.max(0, Math.trunc(numeric(options.count,10))), ranked.length);
    while (result.length < count) {
      const recent = result.slice(-3).map(p => p.family || qid(p));
      // Never jump from unseen to seen solely to vary the family.
      const priority = ranked[0].priority;
      const used = result.map(p => p.family || qid(p));
      let i = ranked.findIndex(r => r.priority === priority && !used.includes(r.p.family || qid(r.p)));
      if (i < 0) i = ranked.findIndex(r => r.priority === priority && !recent.includes(r.p.family || qid(r.p)));
      if (i < 0) i = 0;
      result.push(ranked.splice(i,1)[0].p);
    }
    return result;
  }
  function examPlan(bank, options = {}, state = emptyState()) {
    const topics = [...new Set(filtered(bank).map(p => p.tema))];
    const pool = filtered(bank, {level: options.level});
    const areas = topics.map(topic => ({topic, available: pool.filter(p => p.tema === topic).length, count: 0}));
    const count = Math.min(Math.max(0, Math.trunc(numeric(options.count, 20))), pool.length);
    if (!areas.length || areas.some(a => !a.available) || count < areas.length) return {areas, count: 0, available: pool.length, error: 'Este nivel no permite incluir todas las áreas. Elige Todos los niveles.'};
    // Rotate the remainder between exams, so no area always receives more questions.
    const offset = state.sessions.filter(s => s.mode === 'exam').length % areas.length;
    let assigned = 0;
    while (assigned < count) {
      for (let i = 0; i < areas.length && assigned < count; i++) {
        const area = areas[(i + offset) % areas.length];
        if (area.count < area.available) { area.count++; assigned++; }
      }
    }
    return {areas, count, available: pool.length, error: ''};
  }
  function selectExamProblems(bank, state, options = {}, rng = Math.random) {
    const plan = examPlan(bank, options, state);
    if (plan.error) throw new Error(plan.error);
    const selected = plan.areas.flatMap(area => selectProblems(bank, state, {topic: area.topic, level: options.level, count: area.count, mode: 'variety'}, rng));
    for (let i = selected.length - 1; i > 0; i--) {
      const j = Math.min(i, Math.max(0, Math.floor(rng() * (i + 1))));
      [selected[i], selected[j]] = [selected[j], selected[i]];
    }
    return selected;
  }
  function createSession(problems, options = {}, now = Date.now()) {
    const ids = problems.map(qid);
    if (!ids.length || new Set(ids).size !== ids.length) throw new Error('No hay preguntas nuevas disponibles con estos filtros.');
    const mode = options.mode === 'exam' ? 'exam' : 'practice';
    const duration = clamp(options.duration || 1800, 60, 86400);
    return {id:randomId(), mode, variant:options.variant || 'variety', ids, index:0, answers:{}, times:{}, flags:[], startedAt:now, deadline:mode === 'exam' ? now + duration*1000 : 0, duration, paused:false, runningSince:now, hintIds:[]};
  }
  function remaining(session, now = Date.now()) { return session.mode === 'exam' ? Math.max(0, Math.ceil((session.deadline-now)/1000)) : null; }
  function checkpoint(session, now = Date.now()) {
    const id = session.ids[session.index];
    if (session.mode === 'practice' && session.answers[id]) {
      session.runningSince = 0;
      return session.times[id] || session.answers[id].seconds || 0;
    }
    if (session.runningSince && !session.paused) {
      const until = session.mode === 'exam' ? Math.min(now, session.deadline) : now;
      session.times[id] = (session.times[id] || 0) + Math.max(0, (until-session.runningSince)/1000);
    }
    session.runningSince = session.paused ? 0 : now;
    return session.times[id] || 0;
  }
  function answer(session, p, choice, extra = {}, now = Date.now()) {
    const id = qid(p);
    if (!session.ids.includes(id) || (session.mode === 'exam' && remaining(session,now) === 0)) return false;
    if (session.mode === 'practice' && session.answers[id]) return false;
    if (choice !== null && (!Number.isInteger(choice) || choice < 0 || choice >= p.opts.length)) return false;
    checkpoint(session, now);
    session.answers[id] = {choice, seconds:session.times[id] || 0, hint:session.hintIds.includes(id), confidence:extra.confidence || '', reason:extra.reason || ''};
    if (session.mode === 'practice') session.runningSince = 0;
    return true;
  }
  function recordAttempt(state, session, p, value, now = Date.now()) {
    const id = qid(p), key = session.id+':'+id;
    state.seen[id] = now;
    if (state.attempts.some(a => a.key === key)) return false;
    state.attempts.push({key, qid:id, topic:p.tema, family:p.family || id, choice:value.choice, correct:value.choice===p.ans,
      seconds:numeric(value.seconds), target:p.target || 90, hint:!!value.hint, mode:session.mode, at:now,
      confidence:value.confidence || '', reason:value.reason || '', skipped:value.choice===null});
    return true;
  }
  function finishSession(state, bank, now = Date.now(), aborted = false) {
    const session = state.active;
    if (!session) return null;
    checkpoint(session,now);
    const byId = new Map(bank.map(p=>[qid(p),p]));
    const rows = [];
    for (const id of session.ids) {
      if (aborted && session.mode === 'practice' && !session.answers[id]) continue;
      const p = byId.get(id);
      if (!p) continue;
      const a = session.answers[id] || {choice:null, seconds:session.times[id] || 0, hint:session.hintIds.includes(id)};
      if (session.mode === 'exam') a.seconds = session.times[id] || 0;
      recordAttempt(state,session,p,a,now);
      rows.push({...a,qid:id,correct:a.choice===p.ans,target:p.target});
    }
    const seconds = session.mode === 'exam' ? Math.min(session.duration, Math.max(0,(now-session.startedAt)/1000)) : rows.reduce((n,a)=>n+a.seconds,0);
    const summary = {id:session.id,mode:session.mode,at:now,count:rows.length,correct:rows.filter(a=>a.correct).length,seconds};
    state.sessions.push(summary);
    state.sessions = state.sessions.slice(-200);
    state.active = null;
    return {...summary,rows};
  }
  function stats(state) {
    const attempts = state.attempts.filter(a=>a.mode !== 'legacy');
    const unassisted = attempts.filter(a=>!a.hint);
    const correct = unassisted.filter(a=>a.correct);
    const totalSeconds = unassisted.reduce((n,a)=>n+a.seconds,0);
    const topics = {};
    for (const a of attempts) {
      const t = topics[a.topic] ||= {count:0,correct:0,fast:0,seconds:0,accuracy:0};
      t.count++; t.correct += a.correct && !a.hint ? 1 : 0; t.fast += a.correct && !a.hint && a.seconds <= a.target ? 1 : 0; t.seconds += a.seconds;
      t.accuracy = Math.round(t.correct/t.count*100);
    }
    const times = correct.filter(a=>a.seconds>0).map(a=>a.seconds).sort((a,b)=>a-b);
    const mid = Math.floor(times.length/2);
    const median = times.length ? (times.length%2 ? times[mid] : (times[mid-1]+times[mid])/2) : null;
    return {count:attempts.length, correct:correct.length, accuracy:unassisted.length ? Math.round(correct.length/unassisted.length*100) : null,
      median, correctPerMinute:totalSeconds ? correct.length/(totalSeconds/60) : null, fast:correct.filter(a=>a.seconds>0 && a.seconds<=a.target).length,
      seen:Object.keys(state.seen).length, review:[...latestAttempts(state).values()].filter(needsReview).length, topics};
  }
  const api = {KEY,VERSION,qid,emptyState,normalize,load,save,filtered,latestAttempts,needsReview,selectProblems,examPlan,selectExamProblems,createSession,remaining,checkpoint,answer,recordAttempt,finishSession,stats};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.TrainerEngine = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
