/* Real browser checks. Requires Playwright in NODE_PATH or the current environment. */
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const URL=process.env.TRAINER_URL || 'http://127.0.0.1:8768/';
const out=path.resolve(__dirname,'../output/playwright');fs.mkdirSync(out,{recursive:true});
const checks=[];
function pass(name){checks.push(name);console.log('PASS '+name);}
const snap=async(page,name)=>page.screenshot({path:path.join(out,name+'.png'),fullPage:true});
const state=page=>page.evaluate(()=>JSON.parse(localStorage.getItem('trainermath_brenda_v3')));
const nav=async(page,name)=>page.locator(`button[data-nav="${name}"]:visible`).first().click();
(async()=>{
  const browser=await chromium.launch({headless:true});
  try {
    const context=await browser.newContext({viewport:{width:1440,height:1000}});
    const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(URL);await page.locator('#enterApp').click();
    await page.locator('#view-home').waitFor({state:'visible'});
    assert((await page.evaluate(()=>window.TRAINER_DATA.length))>=600);
    await snap(page,'inicio-desktop');pass('local access, Inicio and expanded question bank');
    await nav(page,'practice');await page.locator('#practiceCount [data-value="5"]').click();
    await page.locator('#practiceSetup button[type="submit"]').click();
    let s=await state(page);assert.equal(new Set(s.active.ids).size,5);
    await page.locator('#pausePractice').click();const paused=await state(page);
    await page.reload();s=await state(page);assert(s.active.paused);assert.equal(s.active.times[s.active.ids[s.active.index]],paused.active.times[paused.active.ids[paused.active.index]]);
    await page.locator('#pausePractice').click();
    const w1=(await page.locator('#practiceSession .session-main').boundingBox()).width;
    await page.locator('#hidePracticePanel').click();const w2=(await page.locator('#practiceSession .session-main').boundingBox()).width;
    assert(w2>w1+100);await page.locator('#showPracticePanel').click();pass('practice pause/reload and summary close/reopen frees space');
    const ids=[];
    for(let i=0;i<5;i++){
      s=await state(page);const id=s.active.ids[s.active.index];ids.push(id);
      const correct=await page.evaluate(id=>window.TRAINER_DATA.find(p=>String(p.id)===id).ans,id);
      if(i===0)await page.locator('#hintButton').click();
      await page.keyboard.press(String((i===1?(correct+1)%4:correct)+1));
      assert.equal(await page.locator('#practiceSession .feedback').count(),1);
      if(i===0){
        await page.locator('#practiceSession .solution summary').click();await page.locator('#nextSolutionStep').click();
        assert.equal(await page.locator('#practiceSession .step').count(),1);
        await page.locator('#allSolutionSteps').click();
        assert((await page.locator('#practiceSession .step').count())>=2);
        const after=await state(page);assert(after.active.answers[id].hint);assert.equal(after.active.runningSince,0);
      }
      await page.locator('#nextPractice').click();
    }
    s=await state(page);assert.equal(s.attempts.length,5);assert.equal(new Set(ids).size,5);assert.equal(s.active,null);
    await snap(page,'practica-resultado');pass('five questions, keyboard answers, hints, progressive solutions and final scoring');
    await nav(page,'review');assert((await page.locator('.review-row').count())>=2);
    await nav(page,'exam');await page.locator('#examSetup button[type="submit"]').click();
    s=await state(page);const deadline=s.active.deadline;const first=s.active.ids[0];
    await page.keyboard.press('1');await page.keyboard.press('2');s=await state(page);assert.equal(s.active.answers[first].choice,1);
    assert.equal(await page.locator('#examSession .correct').count(),0);assert.equal(await page.locator('#examSession .solution').count(),0);
    await page.locator('#flagQuestion').click();await page.locator('#examNext').click();await page.locator('#examPrev').click();
    s=await state(page);assert(s.active.flags.includes(first));assert.equal(s.active.answers[first].choice,1);
    await page.reload();s=await state(page);assert.equal(s.active.deadline,deadline);
    const ew1=(await page.locator('#examSession .session-main').boundingBox()).width;
    await page.locator('#hidePalette').click();const ew2=(await page.locator('#examSession .session-main').boundingBox()).width;
    assert(ew2>ew1+100);await page.locator('#showPalette').click();
    await page.locator('#finishExam').click();s=await state(page);await page.keyboard.press('3');assert.deepEqual((await state(page)).active.answers,s.active.answers);
    await page.keyboard.press('Escape');assert.equal(await page.locator('#finishDialog').evaluate(x=>x.open),false);
    await nav(page,'home');s=await state(page);await page.keyboard.press('4');assert.deepEqual((await state(page)).active.answers,s.active.answers);
    await nav(page,'exam');await snap(page,'examen-desktop');
    await page.locator('#finishExam').click();await page.locator('#confirmFinish').click();await page.locator('#examResult .result-score').waitFor({state:'visible'});
    s=await state(page);assert.equal(s.attempts.length,25);assert.equal(s.active,null);
    await page.locator('#toggleExamReview').click();await page.locator('#examReview details').first().locator('summary').click();
    assert((await page.locator('#examReview .step').count())>0);pass('exam change/flag/navigate, no early answers, persistent deadline, modal keyboard and submission');
    await page.locator('#newExam').click();await page.locator('#examSetup button[type="submit"]').click();
    // Model elapsed real time by importing a past deadline, then reloading the actual application.
    await page.addInitScript(()=>{const key='trainermath_brenda_v3',s=JSON.parse(localStorage.getItem(key));if(s?.active){s.active.deadline=Date.now()-1;s.active.startedAt=Date.now()-s.active.duration*1000;s.active.runningSince=Date.now()-3000;localStorage.setItem(key,JSON.stringify(s));}});
    await page.reload();await page.locator('#examResult .result-score').waitFor({state:'visible',timeout:6000});assert.equal((await state(page)).active,null);pass('expired exam automatically submits after reload');
    for(const width of [375,320]){
      await page.setViewportSize({width,height:900});await nav(page,'practice');if(await page.locator('#newPractice').isVisible())await page.locator('#newPractice').click();
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await snap(page,`practica-${width}`);
      await nav(page,'review');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    }
    await page.emulateMedia({reducedMotion:'reduce'});await nav(page,'home');await page.keyboard.press('Tab');
    assert(await page.evaluate(()=>document.activeElement!==document.body));pass('375/320px layouts, no horizontal overflow, reduced motion and keyboard focus');
    assert.deepEqual(errors,[]);pass('no browser runtime errors');
    const blocked=await browser.newContext({viewport:{width:375,height:900}});
    await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('denied','SecurityError');}});});
    const b=await blocked.newPage();const blockedErrors=[];b.on('pageerror',e=>blockedErrors.push(e.message));await b.goto(URL);await b.locator('#enterApp').click();await b.locator('#quickStart').click();assert.equal(await b.locator('.question-text').count(),1);assert.deepEqual(blockedErrors,[]);pass('storage-denied browser remains usable');
    await browser.close();
    fs.writeFileSync(path.join(out,'smoke-results.json'),JSON.stringify({url:URL,at:new Date().toISOString(),checks},null,2));
  }catch(e){await browser.close();throw e;}
})().catch(e=>{console.error(e);process.exitCode=1;});
