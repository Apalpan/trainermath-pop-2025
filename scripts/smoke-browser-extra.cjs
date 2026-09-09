'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const out=path.resolve(__dirname,'../output/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const ctx=await browser.newContext({viewport:{width:375,height:850}}),page=await ctx.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8768/#p/6');await page.locator('#enterApp').click();
 await page.locator('#studyDetail').waitFor({state:'visible'});assert(await page.locator('#studyDetail .question-text').isVisible());
 console.log('PASS legacy #p/6 link and original solution');
 const downloadEvent=page.waitForEvent('download');await page.locator('#exportProgress').click();const download=await downloadEvent;
 const raw=JSON.parse(fs.readFileSync(await download.path(),'utf8'));assert.equal(raw.version,3);
 page.on('dialog',d=>d.accept());await page.locator('#importProgress').setInputFiles({name:'progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(raw))});
 await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('importado'));
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('trainermath_brenda_v3')).version),3);
 await page.locator('#importProgress').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{bad')});
 await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('no es un respaldo'));
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('trainermath_brenda_v3')).version),3);
 console.log('PASS export, valid import, malformed import preserves progress');
 await page.locator('button[data-nav="exam"]:visible').first().click();await page.locator('#examSetup button[type="submit"]').click();
 assert(await page.locator('#palettePanel').isHidden());assert(await page.locator('#showPalette').isVisible());
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 const point=await page.locator('#showPalette').evaluate(el=>{const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;return {hit:el.contains(document.elementFromPoint(x,y)),x,y};});assert(point.hit,'Mobile palette reopen button must not be covered by navigation');
 await page.locator('#examSession .option').first().click();await page.screenshot({path:path.join(out,'examen-mobile.png'),fullPage:true});
 await page.locator('#showPalette').click();assert(await page.locator('#palettePanel').isVisible());
 const sizes=await page.locator('.palette button').evaluateAll(els=>els.map(el=>{const r=el.getBoundingClientRect();return[r.width,r.height];}));assert(sizes.every(([w,h])=>w>=44&&h>=44));
 await page.locator('#hidePalette').click();console.log('PASS mobile exam question, palette close/reopen, 44px targets');
 await page.locator('#showPalette').click();await page.locator('#finishExam').click();await page.locator('#confirmFinish').click();
 await page.locator('button[data-nav="practice"]:visible').first().click();await page.locator('#practiceSetup button[type="submit"]').click();
 await page.locator('#practiceSession .option').first().click();await page.screenshot({path:path.join(out,'practica-feedback-mobile.png'),fullPage:true});
 const colors=await page.evaluate(()=>{const css=getComputedStyle(document.documentElement);return Object.fromEntries(['--brand','--ink','--muted','--danger','--bg','--surface'].map(x=>[x,css.getPropertyValue(x).trim()]));});
 function L(h){const rgb=h.replace('#','').match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;}
 function ratio(a,b){const x=L(a),y=L(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
 const contrast={action:ratio(colors['--brand'],'#ffffff'),muted:ratio(colors['--muted'],colors['--bg']),ink:ratio(colors['--ink'],'#ffffff'),danger:ratio(colors['--danger'],'#ffffff')};assert(Object.values(contrast).every(x=>x>=4.5));
 fs.writeFileSync(path.join(out,'contrast.json'),JSON.stringify(contrast,null,2));console.log('PASS contrast real tokens '+JSON.stringify(contrast));
 assert.deepEqual(errors,[]);await browser.close();
 }catch(error){await browser.close();throw error;}
})().catch(e=>{console.error(e);process.exitCode=1;});
