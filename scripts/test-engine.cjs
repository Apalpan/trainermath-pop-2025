'use strict';
const assert = require('node:assert/strict');
const E = require('../web/engine.js');
let passed = 0;
function test(name, run) { run(); passed++; console.log('PASS ' + name); }
const bank = Array.from({length:400},(_,i)=>({id:String(i+1),n:i+1,family:'f'+Math.floor(i/8),tema:i<200?'Aritmética':'Álgebra',sub:'Subtema',dif:1+i%3,target:i%2?90:45,opts:['1','2','3','4'],ans:2}));
const deterministic = () => .5;
test('400 distinct questions across 40 fresh sessions before any exact repeat',()=>{
  const state=E.emptyState(),all=new Set();
  for(let n=0;n<40;n++) {
    const selected=E.selectProblems(bank,state,{count:10},deterministic);
    for(const p of selected) { assert(!all.has(p.id));all.add(p.id);state.seen[p.id]=n+1; }
  }
  assert.equal(all.size,400);
  assert.equal(E.selectProblems(bank,state,{count:10},deterministic).length,10);
});
test('family diversity spans entire session when at least 20 families available',()=>{
  const selected=E.selectProblems(bank,E.emptyState(),{count:20},deterministic);
  assert.equal(new Set(selected.map(p=>p.family)).size,20);
});
test('a narrow topic/level pool never duplicates IDs or changes filters',()=>{
  const selected=E.selectProblems(bank,E.emptyState(),{count:300,topic:'Álgebra',level:3,mode:'speed'},deterministic);
  assert(selected.every(p=>p.tema==='Álgebra'&&p.dif===3&&p.target<=60));
  assert.equal(new Set(selected.map(p=>p.id)).size,selected.length);
  assert.equal(E.selectProblems(bank,E.emptyState(),{topic:'Inexistente'}).length,0);
});
test('canonical legacy duplicates excluded from training selection',()=>{
  assert.equal(E.selectProblems([{...bank[0],practiceEligible:false}],E.emptyState()).length,0);
});
test('seen questions cannot displace unseen ones in adaptive mode',()=>{
  const state=E.emptyState();bank.slice(0,399).forEach(p=>state.seen[p.id]=1);
  assert.equal(E.selectProblems(bank,state,{count:1,mode:'adaptive'})[0].id,'400');
});
test('answer is immutable in practice and explanation time is excluded',()=>{
  const s=E.createSession([bank[0]],{mode:'practice'},1000);
  assert(E.answer(s,bank[0],2,{},11000));
  assert.equal(s.answers['1'].seconds,10);
  assert.equal(E.answer(s,bank[0],0,{},12000),false);
  E.checkpoint(s,90000);E.checkpoint(s,190000);
  assert.equal(s.times['1'],10);
});
test('pause and resume do not charge paused time',()=>{
  const s=E.createSession([bank[0]],{},1000);
  E.checkpoint(s,6000);s.paused=true;E.checkpoint(s,100000);
  s.paused=false;s.runningSince=100000;
  E.answer(s,bank[0],2,{},107000);
  assert.equal(s.answers['1'].seconds,12);
});
test('exam answers editable until deadline; deadline does not move on reload',()=>{
  const now=Date.now(),s=E.createSession([bank[0]],{mode:'exam',duration:60},now);
  E.answer(s,bank[0],0,{},now+1000);E.answer(s,bank[0],2,{},now+2000);
  assert.equal(s.answers['1'].choice,2);
  assert.equal(E.remaining(s,now+30000),30);
  assert.equal(E.answer(s,bank[0],1,{},now+60000),false);
  const state=E.emptyState();state.active=s;
  assert.equal(E.normalize(JSON.parse(JSON.stringify(state)),bank).active.deadline,s.deadline);
});
test('exam navigation charges time to its own question and caps expiry',()=>{
  const s=E.createSession(bank.slice(0,2),{mode:'exam',duration:60},1000);
  E.checkpoint(s,11000);s.index=1;s.runningSince=11000;
  E.checkpoint(s,101000);
  assert.equal(s.times['1'],10);assert.equal(s.times['2'],50);
});
test('submitting an exam scores omissions, final choices and only once',()=>{
  const state=E.emptyState(),s=E.createSession(bank.slice(0,3),{mode:'exam',duration:60},1000);state.active=s;
  E.answer(s,bank[0],0,{},2000);E.answer(s,bank[0],2,{},3000);
  const sum=E.finishSession(state,bank,61000);
  assert.equal(sum.count,3);assert.equal(sum.correct,1);assert.equal(state.attempts.length,3);
  assert.equal(sum.rows.filter(a=>a.choice===null).length,2);
  assert.equal(E.finishSession(state,bank,62000),null);
  assert.equal(state.attempts.length,3);
});
test('practice records cannot double count between answering and finishing',()=>{
  const state=E.emptyState(),s=E.createSession(bank.slice(0,2),{},1000);state.active=s;
  E.answer(s,bank[0],2,{},3000);
  E.recordAttempt(state,s,bank[0],s.answers['1'],3000);
  E.finishSession(state,bank,4000,true);
  assert.equal(state.attempts.length,1);assert.equal(Object.keys(state.seen).length,1);
});
test('review follows latest result: wrong, hinted or slow needs review; fast correct clears',()=>{
  const state=E.emptyState();
  function record(choice,seconds,hint) {const s=E.createSession([bank[0]]);E.recordAttempt(state,s,bank[0],{choice,seconds,hint});}
  record(0,10,false);assert.equal(E.selectProblems(bank,state,{mode:'review',count:10}).length,1);
  record(2,60,false);assert.equal(E.stats(state).review,1);
  record(2,10,true);assert.equal(E.stats(state).review,1);
  record(2,10,false);assert.equal(E.stats(state).review,0);
});
test('accuracy does not reward hints and median excludes wrong answers',()=>{
  const state=E.emptyState();
  [ [2,10,false], [0,90,false], [2,20,false], [2,1,true] ].forEach(([choice,seconds,hint])=>E.recordAttempt(state,E.createSession([bank[0]]),bank[0],{choice,seconds,hint}));
  const stats=E.stats(state);assert.equal(stats.accuracy,67);assert.equal(stats.median,15);assert.equal(stats.correct,2);assert.equal(stats.fast,2);
});
test('legacy migration preserves original answers without fabricating measured speed',()=>{
  const old=JSON.stringify({ans:{1:{pick:2,ok:true}},seen:{2:1}});
  const storage={getItem:key=>key==='tm_pop2025_v1'?old:null};
  const oldBank=bank.slice(0,2).map(p=>({...p,origin:'original'}));
  const {state}=E.load(storage,oldBank);
  assert.equal(state.attempts.length,1);assert.equal(state.attempts[0].correct,true);assert.equal(E.stats(state).median,null);assert(state.seen['2']);
});
test('corrupt saved data is preserved through a read-only fallback',()=>{
  const result=E.load({getItem:()=>'{bad'},bank);
  assert(result.warning);assert.equal(result.readOnly,true);
});
test('denied/full storage returns an actionable warning without throwing',()=>{
  const result=E.save({setItem:()=>{throw Error('quota');}},E.emptyState());assert.equal(result.ok,false);assert(result.error);
});
test('import rejects unrelated documents and strips HTML/foreign data',()=>{
  assert.throws(()=>E.normalize({hello:1},bank));
  const state=E.emptyState();state.attempts=[{qid:'1',key:'k',choice:2,seconds:10,profile:'<img>',reason:'<img>',topic:'fake'}, {qid:'foreign'}];
  const normal=E.normalize(state,bank);
  assert.equal(normal.attempts.length,1);assert.equal(normal.attempts[0].topic,'Aritmética');assert.equal(normal.attempts[0].reason,'');assert.equal(normal.profile,'Brenda Sofía');
});
console.log(`\n${passed} engine scenarios passed.`);
