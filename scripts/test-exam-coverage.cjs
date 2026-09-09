'use strict';

const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const path = require('node:path');
const E = require('../web/engine.js');

const ROOT = path.resolve(__dirname, '..');
let passed = 0;
function test(name, run) { run(); passed++; console.log('PASS ' + name); }

function loadRealBank() {
  const code = [
    'import json,sys',
    'sys.stdout.reconfigure(encoding="utf-8")',
    'import build',
    'print(json.dumps(build.load_bank(), ensure_ascii=False, separators=(",",":")))',
  ].join('; ');
  const result = spawnSync(process.env.PYTHON || 'python', ['-c', code], {
    cwd: ROOT,
    encoding: 'utf8',
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.equal(result.status, 0, result.stderr || 'No se pudo cargar el banco real.');
  return JSON.parse(result.stdout);
}

function rng(seed) {
  let value = seed >>> 0;
  return () => {
    value = (value * 1664525 + 1013904223) >>> 0;
    return value / 0x100000000;
  };
}

function countsByTopic(items) {
  return Object.fromEntries([...new Map(items.map(p => [p.tema, 0])).keys()].map(topic => [
    topic,
    items.filter(p => p.tema === topic).length,
  ]));
}

function topicOrder(bank) {
  return [...new Set(bank.filter(p => p.practiceEligible !== false).map(p => p.tema))];
}

const bank = loadRealBank();
const topics = topicOrder(bank);

test('el banco real contiene las seis áreas matemáticas del simulacro', () => {
  assert.equal(bank.length, 510);
  assert.deepEqual(new Set(topics), new Set(['Aritmética', 'Álgebra', 'Geometría', 'Trigonometría', 'Estadística', 'Probabilidad']));
});

test('20, 30 y 40 preguntas cubren todas las áreas para cada nivel en 100 semillas', () => {
  for (const level of [0, 1, 2, 3]) {
    for (const count of [20, 30, 40]) {
      for (let seed = 1; seed <= 100; seed++) {
        const state = E.emptyState();
        const plan = E.examPlan(bank, {level, count}, state);
        assert.equal(plan.error, '', `plan vacío para nivel ${level}, cantidad ${count}, semilla ${seed}`);
        const selected = E.selectExamProblems(bank, state, {level, count}, rng(seed));
        assert.equal(selected.length, count, `cantidad incorrecta: nivel ${level}, cantidad ${count}, semilla ${seed}`);
        assert.equal(new Set(selected.map(E.qid)).size, count, `ID repetido: nivel ${level}, cantidad ${count}, semilla ${seed}`);
        assert.deepEqual(new Set(selected.map(p => p.tema)), new Set(topics), `área ausente: nivel ${level}, cantidad ${count}, semilla ${seed}`);
        assert(selected.every(p => !level || p.dif === level), `nivel filtrado incorrectamente: ${level}`);
        assert.deepEqual(countsByTopic(selected), Object.fromEntries(plan.areas.map(a => [a.topic, a.count])));
      }
    }
  }
});

test('los restos de cuota rotan entre exámenes y 30 se reparte exactamente', () => {
  for (const count of [20, 40]) {
    const first = E.examPlan(bank, {count}, E.emptyState());
    const state = E.emptyState();
    state.sessions.push({mode: 'exam'});
    const second = E.examPlan(bank, {count}, state);
    const base = Math.floor(count / topics.length);
    const firstBonus = first.areas.filter(a => a.count === base + 1).map(a => a.topic);
    const secondBonus = second.areas.filter(a => a.count === base + 1).map(a => a.topic);
    const remainder = count % topics.length;
    assert.equal(firstBonus.length, remainder);
    assert.equal(secondBonus.length, remainder);
    assert.deepEqual(firstBonus, topics.slice(0, remainder));
    assert.deepEqual(secondBonus, [...topics.slice(1), topics[0]].slice(0, remainder));
  }
  const even = E.examPlan(bank, {count: 30}, E.emptyState());
  assert(even.areas.every(area => area.count === 5));
});

test('no repite una pregunta por área en tres simulacros mientras queda banco nuevo suficiente', () => {
  const state = E.emptyState();
  const usedByTopic = new Map(topics.map(topic => [topic, new Set()]));
  for (let exam = 0; exam < 3; exam++) {
    const selected = E.selectExamProblems(bank, state, {count: 40}, rng(900 + exam));
    for (const p of selected) {
      assert(!usedByTopic.get(p.tema).has(E.qid(p)), `repite ${p.tema}/${E.qid(p)} en examen ${exam + 1}`);
      usedByTopic.get(p.tema).add(E.qid(p));
      state.seen[E.qid(p)] = exam + 1;
    }
    state.sessions.push({mode: 'exam'});
  }
});

test('un área vacía en el nivel elegido devuelve error explícito', () => {
  const missingLevel = bank.map(p => p.tema === 'Trigonometría' ? {...p, dif: 2} : p);
  const plan = E.examPlan(missingLevel, {level: 3, count: 20}, E.emptyState());
  assert(plan.error);
  assert.match(plan.error, /todas las áreas/i);
  assert.throws(() => E.selectExamProblems(missingLevel, E.emptyState(), {level: 3, count: 20}, rng(1)), /todas las áreas/i);
});

test('un pool pequeño conserva las seis áreas, limita la cuota escasa y reparte el resto', () => {
  const tinyTopic = 'Aritmética';
  const synthetic = topics.flatMap((topic, topicIndex) => Array.from({length: topic === tinyTopic ? 1 : 10}, (_, index) => ({
    id: `small-${topicIndex}-${index}`,
    tema: topic,
    family: `family-${topicIndex}-${index}`,
    dif: 1,
    target: 60,
    opts: ['1', '2', '3', '4'],
    ans: 0,
  })));
  const plan = E.examPlan(synthetic, {count: 20, level: 1}, E.emptyState());
  assert.equal(plan.error, '');
  assert.equal(plan.count, 20);
  assert.equal(plan.areas.find(area => area.topic === tinyTopic).count, 1);
  assert.equal(plan.areas.reduce((sum, area) => sum + area.count, 0), 20);
  const selected = E.selectExamProblems(synthetic, E.emptyState(), {count: 20, level: 1}, rng(77));
  assert.equal(selected.length, 20);
  assert.equal(new Set(selected.map(E.qid)).size, 20);
  assert.deepEqual(new Set(selected.map(p => p.tema)), new Set(topics));
});

console.log(`\n${passed} exam-coverage scenarios passed.`);
