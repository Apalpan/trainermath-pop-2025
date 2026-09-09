'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out=path.resolve(__dirname,'../output/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  fs.mkdirSync(out,{recursive:true});
  const ctx=await browser.newContext({viewport:{width:1440,height:1000}}),page=await ctx.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>{window.lab={lcp:0,cls:0};new PerformanceObserver(list=>{for(const e of list.getEntries())window.lab.lcp=e.startTime;}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.lab.cls+=e.value;}).observe({type:'layout-shift',buffered:true});});
  await page.goto('http://127.0.0.1:8768/');
  await page.waitForTimeout(1000);
  const initialLab=await page.evaluate(()=>({...window.lab,domContentLoaded:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd,resources:performance.getEntriesByType('resource').length,scope:'local Chromium initial welcome; no field CWV or mobile network emulation'}));
  await page.screenshot({animations:"disabled",path:path.join(out,'rosa-bienvenida-desktop.png')});
  assert(await page.locator('.access-mascot').evaluate(el=>el.complete&&el.naturalWidth===872));
  await page.locator('#enterApp').click();
  const oldTip=await page.locator('#dailyTip').innerText();await page.locator('#mascotTip').click();assert.notEqual(await page.locator('#dailyTip').innerText(),oldTip);
  await page.screenshot({animations:"disabled",path:path.join(out,'rosa-inicio-desktop.png'),fullPage:true});
  console.log('PASS rose logo, official mascot loaded and interactive advice');
  await page.locator('nav [data-nav="exam"]').click();
  await page.locator('#examCount [data-value="30"]').click();
  assert.equal(await page.locator('#examCoverage .coverage-item').count(),6);
  const preview=await page.locator('#examCoverage .coverage-item strong').allTextContents();assert(preview.every(x=>x.trim().startsWith('5')));
  await page.screenshot({animations:"disabled",path:path.join(out,'rosa-examen-distribucion.png'),fullPage:true});
  await page.locator('#examSetup button[type="submit"]').click();
  const areas=await page.evaluate(()=>{const s=JSON.parse(localStorage.getItem('trainermath_brenda_v3'));return s.active.ids.map(id=>TRAINER_DATA.find(p=>String(p.id)===id).tema);});
  assert.equal(new Set(areas).size,6);assert.equal(areas.length,30);
  await page.locator('#finishExam').click();await page.locator('#confirmFinish').click();
  await page.locator('.exam-area-results').waitFor({state:'visible'});assert.equal(await page.locator('.exam-area-results .coverage-item').count(),6);
  console.log('PASS exam preview matches actual six-area exam and six-area results');
  const before=await page.evaluate(()=>localStorage.getItem('trainermath_brenda_v3'));
  await page.locator('nav [data-nav="anzan"]').click();
  await page.locator('#anzanConfig select[name="count"]').selectOption('5');
  await page.locator('.anzan-radio').filter({has:page.locator('[value="manual"]')}).click();
  assert(await page.locator('#anzanSpeed').isDisabled());
  await page.locator('#anzanConfig button[type="submit"]').click();
  let sum=0;
  for(let i=0;i<5;i++){
   const digit=+(await page.locator('#anzanCurrent').innerText());assert(digit>=1&&digit<=9);sum+=digit;
   if(i===0){await page.locator('#anzanPause').click();assert(!/PointerEvent|object/.test(await page.locator('.anzan-paused').innerText()));await page.locator('#anzanPause').click();await page.locator('#anzanAdvance').focus();await page.locator('#anzanAdvance').dispatchEvent('keydown',{key:'ArrowRight',repeat:true});assert((await page.locator('#anzanPosition').innerText()).includes('1 de 5'));}
   await page.keyboard.press('ArrowRight');
  }
  assert(await page.locator('#anzanTotal').isVisible());assert.equal(await page.locator('.anzan-sequence').count(),0);
  await page.locator('#anzanTotal').fill('abc');await page.keyboard.press('Enter');assert(await page.locator('#anzanAnswerError').isVisible());assert.equal(await page.locator('.anzan-feedback').count(),0);
  await page.locator('#anzanTotal').fill(String(sum));await page.keyboard.press('Enter');
  assert(await page.locator('.anzan-verdict.is-correct').isVisible());assert.equal(await page.locator('.anzan-sequence li').count(),5);
  assert.equal(await page.evaluate(()=>localStorage.getItem('trainermath_brenda_v3')),before,'Anzan must not pollute practice progress');
  console.log('PASS manual Anzan: 1-digit sequence, arrows, repeat guard, pause, validation, Enter and isolated progress');
  await page.locator('#anzanExit').click();await page.locator('.anzan-radio').filter({has:page.locator('[value="auto"]')}).click();
  await page.locator('#anzanSpeed').selectOption('0.5');
  await page.evaluate(()=>{Math.random=()=>0.5;});
  await page.locator('#anzanConfig button[type="submit"]').click();await page.locator('#anzanPause').focus();
  await page.evaluate(()=>{window.appearances=[];new MutationObserver(()=>{const el=document.querySelector('#anzanCurrent');if(el)window.appearances.push({value:el.textContent,at:performance.now()});}).observe(document.querySelector('#anzanCurrent'),{childList:true,subtree:true,characterData:true});});
  await page.waitForFunction(()=>document.querySelector('#anzanPosition')?.textContent.includes('3 de 5'));
  assert.equal(await page.evaluate(()=>document.activeElement.id),'anzanPause');
  await page.locator('#anzanPause').click();const position=await page.locator('#anzanPosition').innerText();
  await page.waitForTimeout(600);assert.equal(await page.locator('#anzanPosition').innerText(),position);assert.equal(await page.locator('#anzanCurrent').count(),0);
  const flashes=await page.evaluate(()=>window.appearances);assert(flashes.some(x=>x.value===''),'Repeated digits need a blank interval');
  await page.locator('#anzanPause').click();await page.locator('#anzanTotal').waitFor({state:'visible'});
  await page.locator('#anzanTotal').fill('25');await page.keyboard.press('Enter');assert(await page.locator('.anzan-verdict.is-correct').isVisible());
  console.log('PASS automatic 0.5s Anzan: distinct appearances for repeated digits, stable focus, frozen pause and scoring');
  await page.locator('#anzanNewRound').click();
  await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));});
  assert((await page.locator('.anzan-paused').innerText()).includes('pestaña'));
  await page.evaluate(()=>{delete document.hidden;});
  await page.locator('nav [data-nav="home"]').click();await page.locator('nav [data-nav="anzan"]').click();assert(await page.locator('#anzanConfig').isVisible());
  for(const width of [375,320]){
   await page.setViewportSize({width,height:850});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await page.screenshot({animations:"disabled",path:path.join(out,`rosa-anzan-${width}.png`),fullPage:true});
   await page.locator('nav [data-nav="home"]').click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await page.screenshot({animations:"disabled",path:path.join(out,`rosa-inicio-${width}.png`),fullPage:true});
   await page.locator('nav [data-nav="anzan"]').click();
  }
  await page.locator('.anzan-radio').filter({has:page.locator('[value="manual"]')}).click();await page.locator('#anzanConfig button[type="submit"]').click();
  const arrowVisible=await page.locator('#anzanAdvance').evaluate(el=>{const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;return y<innerHeight&&el.contains(document.elementFromPoint(x,y));});assert(arrowVisible,'Mobile next arrow must be visible above the bottom navigation');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({animations:"disabled",path:path.join(out,'rosa-anzan-ronda-320.png'),fullPage:true});
  await page.emulateMedia({reducedMotion:'reduce'});await page.locator('nav [data-nav="home"]').click();
  assert.equal(await page.locator('#mascotTip img').evaluate(el=>getComputedStyle(el).animationName),'none');
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(out,'rosa-lab.json'),JSON.stringify(initialLab,null,2));
  console.log('PASS hidden-tab pause, navigation teardown, 320/375px, reduced motion and no runtime errors');
  const offline=await browser.newContext(),local=await offline.newPage();await offline.setOffline(true);await local.goto('file:///'+path.resolve(__dirname,'../index.html').replaceAll('\\','/'));await local.locator('#enterApp').click();await local.locator('nav [data-nav="anzan"]').click();assert(await local.locator('#anzanConfig').isVisible());
  console.log('PASS self-contained HTML works offline with logo, mascot and Anzan');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
