'use strict';
const assert=require('node:assert/strict');
const A=require('../web/adaptive.js');

assert.equal(A.TIPS.length,41,'el catálogo debe conservar 41 trucos revisados');
assert.equal(new Set(A.TIPS.map(x=>x.id)).size,A.TIPS.length,'IDs de trucos únicos');
for(const tip of A.TIPS){assert(tip.title&&tip.condition&&tip.rule&&tip.example&&tip.trap,`contrato completo: ${tip.id}`);}
const square=A.TIPS.find(x=>x.id==='square_ending_5');
assert(square.example.includes('2 × 3')&&square.example.includes('625'),'incluye la regla solicitada para 25²');

const bank=[
  {id:'1',tema:'Números y Operaciones',sub:'Adición',family:'sumas',target:30,practiceEligible:true,curriculum:{item:'N01',label:'Operaciones'}},
  {id:'2',tema:'Álgebra',sub:'Ecuaciones',family:'lineales',target:60,practiceEligible:true,curriculum:{item:'A01',label:'Ecuaciones lineales'}},
  {id:'3',tema:'Números y Operaciones',sub:'Progresión aritmética',family:'pa',target:60,practiceEligible:true,curriculum:{item:'N17',label:'Progresiones aritméticas'}}
];
const attempt=(key,qid,correct,seconds,target=60,hint=false)=>({key,qid,family:qid==='2'?'lineales':'sumas',topic:qid==='2'?'Álgebra':'Números y Operaciones',correct,seconds,target,hint,mode:'practice',at:Date.now()});
const state={attempts:[attempt('s1:1','1',true,20,30),attempt('s1:2','2',false,70),attempt('s2:2','2',false,80),attempt('s3:2','2',true,90)],seen:{},sessions:[]};
const recommendation=A.recommendation(state,bank);
assert.equal(recommendation.unit.id,'A01','prioriza la unidad con evidencia de error y demora');
assert(recommendation.evidence.includes('3 intentos'),'explica la evidencia sin fingir certeza');
assert(A.priorityForProblem(bank[1],state,bank)>A.priorityForProblem(bank[0],state,bank),'la debilidad pesa más que la unidad estable');
assert.equal(A.trickForProblem(bank[2],null).id,'arithmetic_pairs','la PA recibe el truco curricular correcto');

const mastered={attempts:[
  attempt('a:1','1',true,20,30),attempt('a:1b','1',true,19,30),attempt('b:1','1',true,22,30),attempt('b:1b','1',true,21,30),attempt('b:1c','1',true,24,30)
]};
assert.equal(A.unitStates(mastered,bank).find(x=>x.id==='N01').status,'a velocidad','dominio exige cinco evidencias y dos sesiones');
console.log('PASS 41 trucos, recomendación por unidad, mapeo curricular y dominio a velocidad');
