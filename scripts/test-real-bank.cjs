'use strict';
const assert=require('node:assert/strict');
const E=require('../web/engine.js');
const bank=JSON.parse(require('node:child_process').execFileSync(process.env.PYTHON || 'python',['-c','import json; from build import load_bank; print(json.dumps(load_bank()))'],{cwd:require('node:path').resolve(__dirname,'..'),encoding:'utf8',maxBuffer:8*1024*1024}));
const actual=E.filtered(bank), state=E.emptyState(), seen=new Set();
let batches=0;
while(seen.size<actual.length) {
  const size=Math.min(20,actual.length-seen.size);
  const selected=E.selectProblems(bank,state,{count:size,mode:'adaptive'});
  assert.equal(selected.length,size);
  for(const p of selected) {assert(!seen.has(p.id),`Repeated ${p.id}`);seen.add(p.id);state.seen[p.id]=Date.now();}
  batches++;
}
for(const topic of new Set(actual.map(p=>p.tema))) for(const level of [1,2,3]) {
  const pool=actual.filter(p=>p.tema===topic&&p.dif===level);
  const selected=E.selectProblems(bank,E.emptyState(),{count:20,topic,level});
  assert.equal(selected.length,Math.min(20,pool.length));
  assert(selected.every(p=>p.tema===topic&&p.dif===level));
}
const exam=E.createSession(E.selectProblems(bank,E.emptyState(),{count:40}),{mode:'exam',duration:2400});
assert.equal(exam.ids.length,40);assert.equal(new Set(exam.ids).size,40);
console.log(`PASS real bank: ${actual.length} eligible questions, ${batches} successive sessions without repetition; all topic/level filters; 40-question exam.`);
