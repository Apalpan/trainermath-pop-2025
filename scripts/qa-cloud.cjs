'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const URL=process.env.TRAINER_URL||'http://127.0.0.1:8768/';

(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    const context=await browser.newContext({viewport:{width:1200,height:900}}),page=await context.newPage(),consoleErrors=[];
    page.on('console',message=>{if(message.type()==='error')consoleErrors.push(message.text());});
    await page.goto(URL,{waitUntil:'domcontentloaded'});await page.locator('#enterApp').click();
    await page.waitForFunction(()=>window.TrainerBackend?.status().state!=='connecting',null,{timeout:20000});
    const connected=await page.evaluate(()=>window.TrainerBackend.status());assert.equal(connected.state,'connected',JSON.stringify(connected));assert(connected.userId);
    await page.locator('button[data-nav="practice"]:visible').click();await page.locator('#practiceCount [data-value="5"]').click();await page.locator('#practiceSetup button[type="submit"]').click();
    for(let index=0;index<5;index++){
      const active=await page.evaluate(()=>JSON.parse(localStorage.getItem('trainermath_brenda_v3')).active),id=active.ids[active.index];
      const correct=await page.evaluate(qid=>window.TRAINER_DATA.find(p=>String(p.id)===qid).ans,id);await page.keyboard.press(String(correct+1));
      if(index===0){await page.locator('#askCurrentCoach').click();await page.locator('#coachQuestion').fill('¿Cuál es el camino más corto y cómo lo verifico?');await page.locator('#coachForm button').click();await page.locator('.coach-reply').waitFor({state:'visible',timeout:20000});await page.locator('#closeCoach').click();}
      await page.locator('#nextPractice').click();
    }
    await page.locator('#practiceResult').waitFor({state:'visible'});await page.waitForFunction(()=>window.TrainerBackend.status().pending===0,null,{timeout:20000});
    const finalStatus=await page.evaluate(()=>window.TrainerBackend.status()),replyLabel=await page.locator('.coach-reply>span').count()?await page.locator('.coach-reply>span').innerText():'';
    console.log(JSON.stringify({userId:connected.userId,initial:connected,final:finalStatus,replyLabel,consoleErrors},null,2));
    await context.close();
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
