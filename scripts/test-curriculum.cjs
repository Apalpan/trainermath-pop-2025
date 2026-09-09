'use strict';
const assert=require('node:assert/strict'),{execFileSync}=require('node:child_process'),path=require('node:path');
const E=require('../web/engine.js');
const bank=JSON.parse(execFileSync('python',['-c','import json; from build import load_bank; print(json.dumps(load_bank()))'],{cwd:path.resolve(__dirname,'..'),encoding:'utf8',maxBuffer:10*1024*1024}));
const map=require('../data/syllabus-map.json');
assert.equal(map.items.length,55);assert.equal(map.areas.length,5);
for(const p of bank){assert(map.items.some(i=>i.id===p.curriculum.item&&i.area===p.tema));assert(['directo','apoyo','complementario'].includes(p.curriculum.status));}
const pa=bank.filter(p=>['pa_termino','pa_suma','pg_termino','pg_suma'].includes(p.family));
assert.equal(pa.length,32);assert(pa.every(p=>p.tema==='Números y Operaciones'&&p.curriculum.item==='N17'));
assert(E.filtered(bank,{topic:'Álgebra'}).every(p=>!['N17','N18'].includes(p.curriculum.item)));
assert(bank.filter(p=>p.previousTopic==='Probabilidad').every(p=>p.tema==='Estadística'));
for(const item of map.items){const filtered=E.filtered(bank,{curriculumItem:item.id});assert(filtered.length>0,`Falta ${item.id}`);assert(filtered.every(p=>p.curriculum.item===item.id));}
const extras=bank.filter(p=>p.curriculum.status==='complementario');assert.equal(extras.length,10);
assert(extras.every(p=>p.practiceEligible===false));assert(E.selectProblems(bank,E.emptyState(),{count:10000}).every(p=>p.curriculum.status!=='complementario'));
const state=E.emptyState(),question=pa[0];state.attempts.push({key:'existing',qid:question.id,topic:'Álgebra',choice:question.ans,seconds:40,mode:'practice',at:Date.now()});
const migrated=E.normalize(state,bank);assert.equal(migrated.attempts[0].topic,'Números y Operaciones');assert.equal(migrated.attempts[0].choice,question.ans);assert.equal(migrated.attempts[0].seconds,40);
console.log('PASS curriculum: 55 units, five academy areas, PA/PG + probability classification, unit filters, 10 supplemental exclusions, preserved history');
