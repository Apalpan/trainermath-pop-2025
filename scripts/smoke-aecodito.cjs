'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const URL=process.env.TRAINER_URL||'http://127.0.0.1:8768/';
const out=path.resolve(__dirname,'../output/playwright');fs.mkdirSync(out,{recursive:true});

(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
    await page.goto(URL);await page.locator('#enterApp').click();await page.locator('#adaptiveBrief').waitFor({state:'visible'});
    assert((await page.locator('#adaptiveBrief').innerText()).includes('línea base'));
    await page.locator('#coachLauncher').click();await page.locator('#coachDrawer').waitFor({state:'visible'});
    const coachText=await page.locator('#coachDrawer').innerText();assert(coachText.includes('Cuadrados que terminan en 5')&&coachText.includes('2 × 3')&&coachText.includes('625'));
    await page.locator('#coachDrawer').evaluate(async element=>Promise.all(element.getAnimations().map(animation=>animation.finished)));
    await page.screenshot({path:path.join(out,'aecodito-desktop.png')});
    await page.locator('#closeCoach').click();assert(await page.locator('#coachDrawer').isHidden());assert.equal(await page.evaluate(()=>document.activeElement.id),'coachLauncher');
    await page.locator('#coachLauncher').click();await page.keyboard.press('Escape');assert(await page.locator('#coachDrawer').isHidden());assert.equal(await page.evaluate(()=>document.activeElement.id),'coachLauncher');

    await page.locator('button[data-nav="practice"]:visible').click();await page.locator('#practiceCount [data-value="5"]').click();await page.locator('#practiceSetup button[type="submit"]').click();
    const active=await page.evaluate(()=>JSON.parse(localStorage.getItem('trainermath_brenda_v3')).active),id=active.ids[0];
    const correct=await page.evaluate(qid=>window.TRAINER_DATA.find(p=>String(p.id)===qid).ans,id);await page.keyboard.press(String(correct+1));
    await page.locator('.aecodito-inline').waitFor({state:'visible'});await page.locator('#askCurrentCoach').click();assert(await page.locator('#coachQuestion').isEnabled());
    await page.locator('#coachQuestion').fill('Explícame el camino corto');await page.locator('#coachForm button').click();
    try{await page.locator('.coach-reply').waitFor({state:'visible',timeout:8000});}catch(error){console.error(JSON.stringify({status:await page.evaluate(()=>window.TrainerBackend.status()),coach:await page.locator('#coachContent').innerText(),errors},null,2));throw error;}
    assert((await page.locator('.coach-reply').innerText()).length>40);
    await page.setViewportSize({width:320,height:780});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.equal(await page.locator('#coachQuestion').evaluate(el=>getComputedStyle(el).fontSize),'16px');const aria=await page.locator('#coachDrawer').ariaSnapshot();assert(aria.includes('Cerrar Aecodito')&&aria.includes('Pregúntale por un método rápido'));await page.screenshot({path:path.join(out,'aecodito-mobile.png')});
    await context.close();

    const examContext=await browser.newContext({viewport:{width:1280,height:900}}),exam=await examContext.newPage();await exam.goto(URL);await exam.locator('#enterApp').click();await exam.locator('button[data-nav="exam"]:visible').click();await exam.locator('#examSetup button[type="submit"]').click();assert(await exam.locator('#coachLauncher').isHidden());
    await exam.locator('#finishExam').click();await exam.locator('#confirmFinish').click();await exam.locator('#openExamCoach').click();assert(await exam.locator('#coachDrawer').isVisible());
    await examContext.close();assert.deepEqual(errors,[]);console.log('PASS Aecodito catalog, close/reopen, post-answer tutor, exam lock and 320px drawer');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
