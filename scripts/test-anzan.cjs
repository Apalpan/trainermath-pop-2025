'use strict';
const assert=require('node:assert/strict');
const {generateSequence,evaluateAnswer}=require('../web/anzan.js');

const low=generateSequence(5,()=>0);
const high=generateSequence(20,()=>0.999999);
assert.deepEqual(low,[1,1,1,1,1]);
assert.equal(high.length,20);
assert.ok(high.every(n=>n===9));
assert.ok(generateSequence(999,()=>0.5).every(n=>n>=1&&n<=9));

assert.deepEqual(evaluateAnswer([3,7,2],'12'),{correct:true,expected:12,received:12});
assert.deepEqual(evaluateAnswer([3,7,2],'11'),{correct:false,expected:12,received:11});
assert.deepEqual(evaluateAnswer([3,7,2],'12x'),{correct:false,expected:12,received:null});

console.log('Anzan helpers: PASS');
