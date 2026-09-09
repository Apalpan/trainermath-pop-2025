'use strict';

const assert=require('node:assert/strict');
const {chromium}=require('playwright');

const URL=process.env.ANZAN_URL||'http://127.0.0.1:8768';

async function installAudioProbe(page,{pending=false,rejectResume=false}={}){
  await page.addInitScript(({pendingResume,shouldReject})=>{
    const probe=window.__anzanAudio={starts:0,scheduledStops:0,immediateStops:0,resumeCalls:0,pendingResume,shouldReject,resolvers:[]};
    class FakeParam{setValueAtTime(){} exponentialRampToValueAtTime(){}}
    class FakeOscillator{
      constructor(){this.frequency=new FakeParam();this.onended=null;this.ended=false;}
      connect(){}
      start(){probe.starts+=1;}
      stop(when){
        if(when==null){probe.immediateStops+=1;this.finish();return;}
        probe.scheduledStops+=1;
      }
      finish(){if(this.ended)return;this.ended=true;this.onended?.();}
    }
    class FakeGain{constructor(){this.gain=new FakeParam();}connect(){}}
    class FakeAudioContext{
      constructor(){this.state='suspended';this.currentTime=0;probe.context=this;}
      resume(){probe.resumeCalls+=1;if(probe.shouldReject)return Promise.reject(new Error('resume blocked'));if(!probe.pendingResume){this.state='running';return Promise.resolve();}return new Promise(resolve=>probe.resolvers.push(()=>{this.state='running';resolve();}));}
      createOscillator(){return new FakeOscillator();}
      createGain(){return new FakeGain();}
      get destination(){return {};}
    }
    window.AudioContext=FakeAudioContext;window.webkitAudioContext=undefined;
  },{pendingResume:pending,shouldReject:rejectResume});
}

async function installNativeAudioCounter(page){
  await page.addInitScript(()=>{
    const NativeContext=window.AudioContext||window.webkitAudioContext;
    const probe=window.__anzanNativeAudio={available:!!NativeContext,creates:0,starts:0,context:null};
    if(!NativeContext)return;
    const nativeCreate=NativeContext.prototype.createOscillator;
    NativeContext.prototype.createOscillator=function(...args){
      probe.creates+=1;const oscillator=nativeCreate.apply(this,args),nativeStart=oscillator.start.bind(oscillator);
      oscillator.start=(...startArgs)=>{probe.starts+=1;return nativeStart(...startArgs);};
      return oscillator;
    };
    const Wrapped=new Proxy(NativeContext,{construct(target,args,newTarget){const context=Reflect.construct(target,args,newTarget===Wrapped?target:newTarget);probe.context=context;return context;}});
    window.AudioContext=Wrapped;if(window.webkitAudioContext===NativeContext)window.webkitAudioContext=Wrapped;
  });
}

async function enterAnzan(page){
  await page.goto(URL,{waitUntil:'domcontentloaded'});
  const enter=page.locator('#enterApp');
  if(await enter.isVisible())await enter.click();
  await page.locator('.main-nav [data-nav="anzan"]').click();
  await page.locator('#anzanConfig').waitFor();
}

async function configure(page,{mode='manual',sound=false,speed='1',count='5'}={}){
  await page.selectOption('#anzanConfig select[name="count"]',count);
  const modeInput=page.locator(`#anzanConfig input[name="mode"][value="${mode}"]`);
  if(!await modeInput.isChecked())await modeInput.locator('..').click();
  if(mode==='auto')await page.locator('#anzanSpeed').fill(speed);
  const soundToggle=page.locator('#anzanConfig input[name="sound"]');
  if(await soundToggle.isChecked()!==sound)await page.locator('.anzan-sound').click();
}

async function probe(page){return page.evaluate(()=>({...window.__anzanAudio,resolvers:undefined,context:undefined}));}

async function testSoundOff(browser){
  const page=await browser.newPage();await installAudioProbe(page);await enterAnzan(page);await configure(page,{sound:false});
  await page.locator('#anzanConfig [type="submit"]').click();await page.locator('#anzanCurrent').waitFor({timeout:4000});
  assert.equal((await probe(page)).starts,0,'sound off must create zero tones');
  await page.locator('#anzanExit').click();await page.close();
}

async function testSoundAndPause(browser){
  const page=await browser.newPage();await installAudioProbe(page);await enterAnzan(page);await configure(page,{sound:true,mode:'manual'});
  await page.locator('#anzanConfig [type="submit"]').click();await page.locator('#anzanCurrent').waitFor({timeout:4000});
  assert.equal((await probe(page)).starts,1,'first visible digit must sound once');
  await page.locator('#anzanPause').click();const paused=await probe(page);assert.ok(paused.immediateStops>=1,'pause must stop a live tone');
  await page.locator('#anzanPause').click();assert.equal((await probe(page)).starts,1,'resume must not replay the same digit');
  await page.keyboard.press('ArrowRight');assert.equal((await probe(page)).starts,2,'ArrowRight must advance even while Pause keeps focus');
  for(let i=0;i<3;i++)await page.locator('#anzanAdvance').click();
  assert.equal((await probe(page)).starts,5,'five appearances must create exactly five tones');
  await page.locator('#anzanAdvance').click();await page.locator('#anzanAnswerForm').waitFor();assert.equal((await probe(page)).starts,5,'answer screen must not create a tone');
  await page.close();
}

async function testCancelAndExit(browser){
  const page=await browser.newPage();await installAudioProbe(page);await enterAnzan(page);await configure(page,{sound:true,mode:'auto',speed:'0.25'});
  await page.locator('#anzanConfig [type="submit"]').click();await page.locator('#anzanPrepCancel').click();await page.waitForTimeout(2300);
  assert.equal((await probe(page)).starts,0,'cancelled preparation must never start tones');
  await configure(page,{sound:true,mode:'auto',speed:'0.25'});await page.locator('#anzanConfig [type="submit"]').click();await page.locator('.anzan-stage').waitFor({timeout:4000});await page.waitForFunction(()=>window.__anzanAudio.starts>=1);
  await page.locator('#anzanExit').click();const afterExit=(await probe(page)).starts;await page.waitForTimeout(500);assert.equal((await probe(page)).starts,afterExit,'exit must cancel all later tones');
  await page.close();
}

async function testPendingResumeRace(browser){
  const page=await browser.newPage();await installAudioProbe(page,{pending:true});await enterAnzan(page);await configure(page,{sound:true,mode:'manual'});
  await page.evaluate(()=>{const form=document.querySelector('#anzanConfig');form.requestSubmit();form.requestSubmit();});await page.waitForTimeout(30);
  assert.equal((await probe(page)).resumeCalls,1,'double submit must share one pending launch');
  await page.locator('.main-nav [data-nav="home"]').click();
  await page.evaluate(()=>{const p=window.__anzanAudio;p.pendingResume=false;p.resolvers.splice(0).forEach(resolve=>resolve());});await page.waitForTimeout(80);
  assert.equal(await page.locator('#view-anzan').evaluate(el=>el.childElementCount),0,'late resume must not revive deactivated Anzan');
  assert.equal(await page.locator('body').evaluate(el=>el.classList.contains('anzan-focus')),false,'late resume must not restore immersive state');
  assert.equal((await probe(page)).starts,0,'late resume must not create tones');
  await page.close();
}

async function testRejectedResumeFallback(browser){
  const page=await browser.newPage();await installAudioProbe(page,{rejectResume:true});await enterAnzan(page);await configure(page,{sound:true,mode:'manual'});
  await page.locator('#anzanConfig [type="submit"]').click();
  const notice=page.locator('.anzan-audio-status');await notice.waitFor({timeout:1500});assert.match(await notice.textContent(),/bloqueó el sonido|silencio/i,'rejected resume must show a visible fallback');
  assert.equal((await probe(page)).starts,0,'rejected resume must not synthesize tones');await page.locator('#anzanPrepCancel').click();await page.close();
}

async function testNativeAudioContext(browser){
  const page=await browser.newPage();await installNativeAudioCounter(page);await enterAnzan(page);
  assert.equal(await page.evaluate(()=>window.__anzanNativeAudio.available),true,'Chromium must expose a native AudioContext');
  await configure(page,{sound:true,mode:'manual'});await page.locator('#anzanConfig [type="submit"]').click();await page.locator('#anzanCurrent').waitFor({timeout:4000});
  const result=await page.evaluate(()=>({state:window.__anzanNativeAudio.context?.state,creates:window.__anzanNativeAudio.creates,starts:window.__anzanNativeAudio.starts,error:document.querySelector('.anzan-audio-status')?.textContent||''}));
  assert.equal(result.state,'running','native AudioContext must be running after the user gesture');assert.ok(result.creates>=1,'native createOscillator must be called');assert.ok(result.starts>=1,'native oscillator.start must be called');assert.equal(result.error,'','native path must not show an audio error');
  await page.evaluate(()=>window.__anzanNativeAudio.context?.close());await page.close();
}

(async()=>{
  const browser=await chromium.launch({headless:true});
  try{
    await testSoundOff(browser);
    await testSoundAndPause(browser);
    await testCancelAndExit(browser);
    await testPendingResumeRace(browser);
    await testRejectedResumeFallback(browser);
    await testNativeAudioContext(browser);
    console.log('Anzan Web Audio browser logic: PASS');
    console.log('Native Chromium AudioContext: running; createOscillator/start observed.');
    console.log('Hardware audio output: not verified.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
