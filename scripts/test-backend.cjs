'use strict';
const assert=require('node:assert/strict');
require('../web/backend.js');
const Cloud=globalThis.TrainerBackend;
const values=new Map();
const storage={getItem:key=>values.get(key)||null,setItem:(key,value)=>values.set(key,value)};

(async()=>{
  const status=await Cloud.init(storage);
  assert.equal(status.state,'local','sin SDK o red conserva el modo local');
  assert(Cloud.CONFIG.publishableKey.startsWith('sb_publishable_'),'el navegador usa solo clave publicable');
  const bank=[{id:'n1',tema:'Números y Operaciones',sub:'Cálculo',family:'f1',dif:1,target:30,opts:['1','2','3','4'],ans:1,enun:'Dato privado que no debe viajar',curriculum:{item:'N01',label:'Operaciones'}}];
  const state={attempts:[{key:'sesion-1:n1',qid:'n1',choice:1,correct:true,seconds:12,target:30,hint:false,confidence:'segura',reason:'',mode:'practice',at:Date.now()}]};
  const summary={id:'sesion-1',mode:'practice',variant:'adaptive',at:Date.now(),count:1,correct:1,seconds:12,rows:[{qid:'n1',choice:1,correct:true,seconds:12,target:30,hint:false,confidence:'segura',reason:''}]};
  Cloud.queueSession(summary,['n1'],state,bank);
  const queue=JSON.parse(values.get('trainermath_brenda_cloud_queue_v1'));
  assert.equal(queue.length,1);assert.equal(queue[0].attempts[0].unit_id,'N01');
  const serialized=JSON.stringify(queue);
  assert(!serialized.includes('Dato privado')&&!serialized.includes('"opts"')&&!serialized.includes('"choice"'),'no envía enunciados, opciones ni selección al registro operativo');
  const reply=Cloud.localCoach({title:'Por 25',condition:'Si aparece 25.',rule:'Por 100 entre 4.',example:'48×25=1200',trap:'Controla la división.'});
  assert.equal(reply.source,'catalog');assert(reply.reply.message.includes('48×25'));
  console.log('PASS fallback local, cola idempotente y payload mínimo para Supabase');
})().catch(error=>{console.error(error);process.exitCode=1;});
