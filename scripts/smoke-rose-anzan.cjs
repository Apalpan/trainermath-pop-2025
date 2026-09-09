'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out=path.resolve(__dirname,'../output/playwright');
const url=process.env.TRAINER_URL||'http://127.0.0.1:8768/';
const nav=(p,name)=>p.locator(`nav [data-nav="${name}"]`).click();
const enter=async p=>{await p.goto(url);await p.locator('#enterApp').click();};
const start=async p=>{await p.locator('#anzanConfig button[type="submit"]').click();await p.locator('#anzanCountdown').waitFor();};
const manual=async p=>{await p.locator('#anzanConfig select[name="count"]').selectOption('5');await p.locator('.anzan-radio').filter({has:p.locator('[value="manual"]')}).click();};
const snap=(p,name)=>p.screenshot({animations:'disabled',path:path.join(out,name+'.png'),fullPage:false});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  fs.mkdirSync(out,{recursive:true});
  const ctx=await browser.newContext({viewport:{width:1440,height:1000}}),page=await ctx.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await enter(page);
  assert(await page.locator('#mascotTip img').evaluate(el=>el.complete&&el.naturalWidth===872));
  const oldTip=await page.locator('#dailyTip').innerText();await page.locator('#mascotTip').click();assert.notEqual(await page.locator('#dailyTip').innerText(),oldTip);
  await nav(page,'practice');await page.locator('#curriculumPanel summary').first().click();assert((await page.locator('#curriculumCoverage').innerText()).includes('55'));
  await page.locator('#practiceTopic').selectOption('Álgebra');assert(!/Progresiones aritméticas/.test(await page.locator('#practiceUnit').innerText()));
  await page.locator('#practiceTopic').selectOption('Números y Operaciones');await page.locator('#practiceUnit').selectOption('N17');
  await page.locator('#practiceCount [data-value="5"]').click();await page.locator('#practiceSetup button[type="submit"]').click();
  assert(await page.evaluate(()=>{const s=JSON.parse(localStorage.getItem('trainermath_brenda_v3'));return s.active.ids.every(id=>TRAINER_DATA.find(p=>String(p.id)===id).curriculum.item==='N17');}));
  console.log('PASS syllabus coverage and real progression session under Números');
  const examCtx=await browser.newContext(),exam=await examCtx.newPage();await enter(exam);await nav(exam,'exam');await exam.locator('#examCount [data-value="30"]').click();
  assert.equal(await exam.locator('#examCoverage .coverage-item').count(),5);assert((await exam.locator('#examCoverage .coverage-item strong').allTextContents()).every(x=>x.trim().startsWith('6')));
  await snap(exam,'temario-examen-distribucion');await exam.locator('#examSetup button[type="submit"]').click();
  const areas=await exam.evaluate(()=>{const s=JSON.parse(localStorage.getItem('trainermath_brenda_v3'));return s.active.ids.map(id=>TRAINER_DATA.find(p=>String(p.id)===id).tema);});assert.equal(new Set(areas).size,5);assert.equal(areas.length,30);
  await exam.locator('#finishExam').click();await exam.locator('#confirmFinish').click();await exam.locator('.exam-area-results').waitFor({state:'visible'});assert.equal(await exam.locator('.exam-area-results .coverage-item').count(),5);await examCtx.close();console.log('PASS five-area exam preview, session and results');
  await nav(page,'anzan');const before=await page.evaluate(()=>localStorage.getItem('trainermath_brenda_v3'));
  await page.locator('#anzanSpeed').fill('0.1');await page.locator('#anzanConfig button[type="submit"]').click();assert(await page.locator('#anzanSpeedError').isVisible());
  for(const speed of ['0.75','1.25','1.5','1.75']){await page.locator(`[data-speed="${speed}"]`).click();assert.equal(await page.locator('#anzanSpeed').inputValue(),speed);}
  await page.locator('#anzanSpeed').fill('0,75');await start(page);assert(await page.locator('.anzan-mascot').evaluate(el=>el.complete&&el.naturalWidth===872));assert(!(await page.locator('.topbar').isVisible()));
  await page.locator('#anzanPrepPause').click();assert.equal(await page.locator('#anzanCountdown').innerText(),'—');await snap(page,'anzan-preparacion');await page.locator('#anzanPrepCancel').click();
  await manual(page);assert(await page.locator('#anzanSpeed').isDisabled());await start(page);await page.locator('#anzanCurrent').waitFor();let sum=0;
  for(let i=0;i<5;i++){
   const digit=+(await page.locator('#anzanCurrent').innerText());assert(digit>=1&&digit<=9);sum+=digit;
   if(i===0){await page.locator('#anzanPause').click();await page.locator('#anzanPause').click();await page.waitForTimeout(50);await page.locator('#anzanPause').dispatchEvent('keydown',{key:'ArrowRight',repeat:true});assert((await page.locator('#anzanPosition').innerText()).includes('1 de 5'));}
   await page.keyboard.press('ArrowRight');
  }
  assert(await page.locator('#anzanTotal').isVisible());assert.equal(await page.locator('.anzan-sequence').count(),0);
  await page.locator('#anzanTotal').fill('abc');await page.keyboard.press('Enter');assert(await page.locator('#anzanAnswerError').isVisible());
  await page.locator('[data-action="clear"]').click();await page.locator('[data-digit="9"]').click();await page.locator('[data-action="backspace"]').click();assert.equal(await page.locator('#anzanTotal').inputValue(),'');
  for(const n of String(sum))await page.locator(`[data-digit="${n}"]`).click();await page.locator('.anzan-keypad-submit').click();assert(await page.locator('.anzan-verdict.is-correct').isVisible());assert.equal(await page.locator('.anzan-sequence li').count(),5);
  assert.equal(await page.evaluate(()=>localStorage.getItem('trainermath_brenda_v3')),before);console.log('PASS decimals, preparation, arrows after pause, keypad and isolated progress');
  await page.locator('#anzanExit').click();await page.locator('.anzan-radio').filter({has:page.locator('[value="auto"]')}).click();await page.locator('#anzanSpeed').fill('0,75');await page.evaluate(()=>{Math.random=()=>0.5;});
  await start(page);await page.locator('#anzanCurrent').waitFor();await page.locator('#anzanPause').focus();
  await page.evaluate(()=>{window.appearances=[];new MutationObserver(()=>{const el=document.querySelector('#anzanCurrent');if(el)window.appearances.push({value:el.textContent,at:performance.now()});}).observe(document.querySelector('#anzanCurrent'),{childList:true,subtree:true,characterData:true});});
  await page.waitForFunction(()=>document.querySelector('#anzanPosition')?.textContent.includes('3 de 5'));assert.equal(await page.evaluate(()=>document.activeElement.id),'anzanPause');
  await page.locator('#anzanPause').click();const position=await page.locator('#anzanPosition').innerText();await page.waitForTimeout(850);assert.equal(await page.locator('#anzanPosition').innerText(),position);
  const flashes=await page.evaluate(()=>window.appearances);assert(flashes.some(x=>x.value===''));const timings=flashes.filter(x=>x.value==='5');assert(timings.length>=2);assert(Math.abs(timings[1].at-timings[0].at-750)<150);
  await page.locator('#anzanPause').click();await page.locator('#anzanTotal').waitFor();await page.locator('#anzanTotal').fill('25');await page.keyboard.press('Enter');assert(await page.locator('.anzan-verdict.is-correct').isVisible());
  await page.locator('#anzanNewRound').click();await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));});assert((await page.locator('#anzanPrepNote').innerText()).includes('oculta'));
  await page.evaluate(()=>{delete document.hidden;});await page.locator('#anzanPrepCancel').click();await nav(page,'home');await nav(page,'anzan');console.log('PASS 0.75s cadence, repeated-number gap, stable focus, hidden-tab pause and teardown');
  const mobileCtx=await browser.newContext({viewport:{width:320,height:812},isMobile:true,hasTouch:true}),mobile=await mobileCtx.newPage();await enter(mobile);await nav(mobile,'anzan');
  assert(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await snap(mobile,'anzan-config-320');
  await manual(mobile);await start(mobile);await mobile.locator('#anzanCurrent').waitFor();
  assert(await mobile.locator('#anzanAdvance').evaluate(el=>{const r=el.getBoundingClientRect();return r.bottom<=innerHeight&&r.height>=44;}));assert(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await snap(mobile,'anzan-ronda-320');
  for(let i=0;i<5;i++)await mobile.locator('#anzanAdvance').click();await mobile.locator('#anzanTotal').waitFor();await mobile.waitForTimeout(100);assert.notEqual(await mobile.evaluate(()=>document.activeElement.id),'anzanTotal');
  assert(await mobile.locator('.anzan-keypad-submit').evaluate(el=>el.getBoundingClientRect().bottom<=innerHeight));assert(await mobile.locator('.anzan-keypad button').evaluateAll(els=>els.every(el=>el.getBoundingClientRect().height>=44)));await snap(mobile,'anzan-calculadora-320');
  await mobile.locator('#anzanExit').click();await mobile.emulateMedia({reducedMotion:'reduce'});await nav(mobile,'home');assert.equal(await mobile.locator('#mascotTip img').evaluate(el=>getComputedStyle(el).animationName),'none');assert.deepEqual(errors,[]);console.log('PASS 320/375px, immersive touch keypad, reduced motion, no runtime errors');
  const offline=await browser.newContext(),local=await offline.newPage();await offline.setOffline(true);await local.goto('file:///'+path.resolve(__dirname,'../index.html').replaceAll('\\','/'));await local.locator('#enterApp').click();await nav(local,'anzan');assert(await local.locator('#anzanConfig').isVisible());console.log('PASS offline self-contained HTML');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
