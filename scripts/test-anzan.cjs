'use strict';
const assert=require('node:assert/strict');
const {generateSequence,evaluateAnswer,parseSpeed,timingPlan,publicScreen}=require('../web/anzan.js');

const low=generateSequence(5,()=>0);
const high=generateSequence(20,()=>0.999999);
assert.deepEqual(low,[1,1,1,1,1]);
assert.equal(high.length,20);
assert.ok(high.every(n=>n===9));
assert.ok(generateSequence(999,()=>0.5).every(n=>n>=1&&n<=9));

assert.deepEqual(evaluateAnswer([3,7,2],'12'),{correct:true,expected:12,received:12});
assert.deepEqual(evaluateAnswer([3,7,2],'11'),{correct:false,expected:12,received:11});
assert.deepEqual(evaluateAnswer([3,7,2],'12x'),{correct:false,expected:12,received:null});

assert.deepEqual(parseSpeed('0,75'),{ok:true,value:.75,error:''});
assert.deepEqual(parseSpeed('1.25'),{ok:true,value:1.25,error:''});
assert.equal(parseSpeed('.5').ok,true);
assert.equal(parseSpeed('0.30').ok,true);
assert.equal(parseSpeed('0.31').ok,false);
assert.equal(parseSpeed('5.05').ok,false);
assert.equal(timingPlan('.75').ok,true);
assert.deepEqual(timingPlan('0,75'),{ok:true,value:.75,error:'',intervalMs:750,visibleMs:670,blankMs:80});
assert.equal(publicScreen('prep'),'preparing');
assert.equal(publicScreen('running'),'running');

console.log('Anzan helpers: PASS');
