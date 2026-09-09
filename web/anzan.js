/* TrainerMath Anzan: entrenamiento mental aislado, sin persistencia ni historial. */
(function(root){
  'use strict';

  const COUNTS=[5,10,15,20];
  const BLANK_MS=80;

  function generateSequence(count,rng=Math.random){
    const safeCount=COUNTS.includes(Number(count))?Number(count):5;
    return Array.from({length:safeCount},()=>Math.min(9,Math.max(1,Math.floor(rng()*9)+1)));
  }

  function evaluateAnswer(sequence,value){
    const expected=sequence.reduce((sum,n)=>sum+n,0);
    const normalized=String(value??'').trim();
    const received=/^\d+$/.test(normalized)?Number(normalized):null;
    return {correct:received===expected,expected,received};
  }

  function parseSpeed(value){
    const normalized=String(value??'').trim().replace(',','.');
    if(!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(normalized))return {ok:false,error:'Escribe una velocidad numérica, por ejemplo 0,75.'};
    const speed=Number(normalized);
    if(speed<0.25||speed>5)return {ok:false,error:'La velocidad debe estar entre 0,25 y 5 segundos.'};
    if(Math.abs(speed*20-Math.round(speed*20))>1e-8)return {ok:false,error:'Usa incrementos de 0,05 segundos.'};
    return {ok:true,value:speed,error:''};
  }

  function timingPlan(value){
    const parsed=parseSpeed(value);
    if(!parsed.ok)return {...parsed,intervalMs:0,visibleMs:0,blankMs:BLANK_MS};
    const intervalMs=parsed.value*1000;
    return {...parsed,intervalMs,visibleMs:Math.max(0,intervalMs-BLANK_MS),blankMs:BLANK_MS};
  }

  function publicScreen(screen){return screen==='prep'?'preparing':screen;}

  function init(container,options={}){
    if(!container||typeof container.replaceChildren!=='function')throw new Error('TrainerAnzan necesita un contenedor válido.');

    let active=false,timer=0,screen='config',sequence=[],index=0,paused=false,pauseReason='',round=0,prepValue=3,launchToken=0,starting=false;
    let audioContext=null,soundStatus='',lastSoundToken='';
    const oscillators=new Set(),mascotSrc=typeof options.mascotSrc==='string'?options.mascotSrc:'',onState=typeof options.onState==='function'?options.onState:(typeof options.onstate==='function'?options.onstate:null);
    let settings={count:10,speed:1,mode:'auto',sound:false};
    const select=(s)=>container.querySelector(s);

    function clearTimer(){if(timer){clearTimeout(timer);timer=0;}}
    function focus(selector){requestAnimationFrame(()=>select(selector)?.focus({preventScroll:true}));}
    function setMarkup(html){container.innerHTML=html;}
    function escapeAttribute(value){return String(value).replace(/[&<>"]/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[char]));}
    function emitState(){if(!onState)return;try{onState(publicScreen(screen),{active,paused,immersive:['prep','running','answer'].includes(screen)});}catch(_){}}
    function stopSounds(){for(const node of oscillators){try{node.stop();}catch(_){}}oscillators.clear();}
    function showAudioStatus(message){soundStatus=message;let el=select('.anzan-audio-status');if(el){el.textContent=message;return;}const host=select('.anzan-stage,.anzan-prep');if(!host)return;el=document.createElement('p');el.className='anzan-audio-status';el.setAttribute('role','status');el.textContent=message;host.append(el);}

    async function unlockAudio(){
      soundStatus='';
      if(!settings.sound)return true;
      try{
        const Context=root.AudioContext||root.webkitAudioContext;
        if(!Context)throw new Error('unsupported');
        audioContext||=new Context();
        if(audioContext.state==='suspended')await audioContext.resume();
        if(audioContext.state!=='running')throw new Error('blocked');
        return true;
      }catch(_){settings.sound=false;soundStatus='El navegador bloqueó el sonido. La ronda continuará en silencio.';return false;}
    }

    function playDigitTone(){
      const token=`${round}:${index}`;
      if(!settings.sound||paused||screen!=='running'||lastSoundToken===token)return;
      if(!audioContext||audioContext.state!=='running'){settings.sound=false;showAudioStatus('El sonido dejó de estar disponible. La ronda continúa en silencio.');return;}
      lastSoundToken=token;
      try{
        const oscillator=audioContext.createOscillator(),gain=audioContext.createGain(),now=audioContext.currentTime;
        oscillator.type='sine';oscillator.frequency.setValueAtTime(520,now);gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(.045,now+.008);gain.gain.exponentialRampToValueAtTime(.0001,now+.065);
        oscillator.connect(gain);gain.connect(audioContext.destination);oscillators.add(oscillator);oscillator.onended=()=>oscillators.delete(oscillator);oscillator.start(now);oscillator.stop(now+.07);
      }catch(_){settings.sound=false;showAudioStatus('El sonido dejó de estar disponible. La ronda continúa en silencio.');}
    }

    function shell(content){
      return `<div class="anzan-shell anzan-screen-${screen}"><div class="anzan-head"><div><p class="anzan-kicker">Cálculo mental</p><h1>Anzan</h1></div><p>Suma cifras sin escribir operaciones. Precisión primero; velocidad después.</p></div>${content}</div>`;
    }

    function renderConfig(){
      clearTimer();stopSounds();launchToken+=1;starting=false;screen='config';paused=false;pauseReason='';emitState();
      setMarkup(shell(`<form class="anzan-config" id="anzanConfig">
        <div class="anzan-fields">
          <label>Cantidad de cifras<select name="count">${COUNTS.map(n=>`<option value="${n}" ${settings.count===n?'selected':''}>${n} cifras</option>`).join('')}</select></label>
          <div class="anzan-speed-field"><label for="anzanSpeed">Tiempo por cifra <small>(solo automática)</small></label><div class="anzan-speed-input"><input name="speed" id="anzanSpeed" type="text" inputmode="decimal" min="0.25" max="5" step="0.05" value="${settings.speed}" aria-describedby="anzanSpeedHelp anzanSpeedError" ${settings.mode==='manual'?'disabled':''}><span>s</span></div><p id="anzanSpeedHelp">Entre 0,25 y 5, en pasos de 0,05.</p><div class="anzan-speed-presets" aria-label="Velocidades rápidas">${[.75,1.25,1.5,1.75].map(n=>`<button type="button" data-speed="${n}" ${settings.mode==='manual'?'disabled':''}>${String(n).replace('.',',')}</button>`).join('')}</div><p class="anzan-error" id="anzanSpeedError" role="alert" hidden></p></div>
          <fieldset><legend>Presentación</legend><label class="anzan-radio"><input type="radio" name="mode" value="auto" ${settings.mode==='auto'?'checked':''}><span><strong>Automática</strong><small>Las cifras avanzan solas</small></span></label><label class="anzan-radio"><input type="radio" name="mode" value="manual" ${settings.mode==='manual'?'checked':''}><span><strong>Con flechas</strong><small>Tú marcas el ritmo, sin retroceder</small></span></label></fieldset>
        </div>
        <div class="anzan-note"><strong>Cómo entrenar</strong><p>Verás únicamente números del 1 al 9. Acumula cada cifra en tu mente; la suma solo se muestra después de responder.</p></div>
        <label class="anzan-sound"><input type="checkbox" name="sound" ${settings.sound?'checked':''}><span aria-hidden="true"></span><strong>Sonido suave por cifra</strong><small>Opcional y apagado por defecto</small></label>
        <button class="anzan-btn anzan-primary" type="submit">Comenzar ronda</button>
      </form>`));
      select('#anzanConfig').addEventListener('submit',async event=>{
        event.preventDefault();
        if(starting)return;
        const data=new FormData(event.currentTarget);
        const mode=data.get('mode')==='manual'?'manual':'auto',speedResult=mode==='auto'?parseSpeed(data.get('speed')):{ok:true,value:settings.speed};
        if(!speedResult.ok){const input=select('#anzanSpeed'),error=select('#anzanSpeedError');input.setAttribute('aria-invalid','true');error.textContent=speedResult.error;error.hidden=false;input.focus();return;}
        settings={count:Number(data.get('count')),speed:speedResult.value,mode,sound:data.get('sound')==='on'};
        starting=true;const token=++launchToken,submit=event.currentTarget.querySelector('[type="submit"]');submit.disabled=true;submit.textContent='Preparando…';
        await unlockAudio();
        if(!active||screen!=='config'||token!==launchToken){starting=false;return;}
        starting=false;startPreparation();
      });
      container.querySelectorAll('input[name="mode"]').forEach(input=>input.addEventListener('change',()=>{const manual=select('input[name="mode"]:checked').value==='manual';select('#anzanSpeed').disabled=manual;container.querySelectorAll('[data-speed]').forEach(button=>button.disabled=manual);}));
      container.querySelectorAll('[data-speed]').forEach(button=>button.addEventListener('click',()=>{const input=select('#anzanSpeed');input.value=button.dataset.speed;input.removeAttribute('aria-invalid');select('#anzanSpeedError').hidden=true;input.focus();}));
      select('#anzanSpeed').addEventListener('input',event=>{event.currentTarget.removeAttribute('aria-invalid');select('#anzanSpeedError').hidden=true;});
    }

    function startPreparation(){
      clearTimer();stopSounds();round+=1;sequence=generateSequence(settings.count);index=0;prepValue=3;paused=false;pauseReason='';lastSoundToken='';screen='prep';emitState();renderPreparation();schedulePreparation();container.scrollIntoView({block:'start',behavior:'instant'});
    }

    function schedulePreparation(){clearTimer();if(!active||screen!=='prep'||paused)return;timer=setTimeout(()=>{if(prepValue>1){prepValue-=1;updatePreparation();schedulePreparation();}else{screen='running';emitState();renderRunning();playDigitTone();}},700);}

    function renderPreparation(){
      setMarkup(shell(`<section class="anzan-prep" aria-labelledby="anzanPrepTitle">${mascotSrc?`<img class="anzan-mascot" width="872" height="872" src="${escapeAttribute(mascotSrc)}" alt="Aecodito te acompaña en la preparación">`:''}<p class="anzan-kicker">Prepárate</p><h2 id="anzanPrepTitle">${paused?'Preparación en pausa':'Respira, enfoca y suma.'}</h2><div class="anzan-countdown" id="anzanCountdown" role="status" aria-live="polite">${paused?'—':prepValue}</div><p id="anzanPrepNote">${paused?(pauseReason||'Reanuda cuando estés lista.'):'La ronda empieza después de la cuenta regresiva.'}</p>${soundStatus?`<p class="anzan-audio-status" role="status">${soundStatus}</p>`:''}<div class="anzan-actions"><button class="anzan-btn anzan-primary" type="button" id="anzanPrepPause">${paused?'Reanudar preparación':'Pausar preparación'}</button><button class="anzan-btn anzan-quiet" type="button" id="anzanPrepCancel">Cancelar</button></div></section>`));
      select('#anzanPrepPause').onclick=togglePreparation;select('#anzanPrepCancel').onclick=renderConfig;
    }

    function updatePreparation(){const el=select('#anzanCountdown');if(!el)return;el.textContent=String(prepValue);el.classList.remove('is-entering');void el.offsetWidth;el.classList.add('is-entering');}
    function togglePreparation(){if(screen!=='prep')return;clearTimer();paused=!paused;pauseReason='';renderPreparation();emitState();if(!paused)schedulePreparation();focus('#anzanPrepPause');}

    function schedule(){
      clearTimer();
      if(!active||screen!=='running'||paused||settings.mode!=='auto')return;
      const plan=timingPlan(settings.speed),interval=plan.intervalMs;
      timer=setTimeout(()=>{
        const digit=select('#anzanCurrent');
        if(digit){digit.textContent='';digit.classList.remove('is-entering');}
        timer=setTimeout(()=>advance(),BLANK_MS);
      },plan.visibleMs);
    }

    function renderRunning(){
      if(!active||screen!=='running')return;
      const current=sequence[index];
      setMarkup(shell(`<section class="anzan-stage" aria-labelledby="anzanRoundTitle">
        <div class="anzan-roundbar"><div><span>Ronda ${round}</span><strong id="anzanRoundTitle"><span id="anzanPosition">Cifra ${index+1} de ${sequence.length}</span></strong></div><div class="anzan-actions"><button class="anzan-btn anzan-quiet" type="button" id="anzanPause">${paused?'Reanudar':'Pausar'}</button><button class="anzan-btn anzan-quiet" type="button" id="anzanRestart">Reiniciar</button><button class="anzan-btn anzan-quiet" type="button" id="anzanExit">Salir</button></div></div>
        <div class="anzan-progress" aria-hidden="true"><span id="anzanProgress" style="width:${((index+1)/sequence.length)*100}%"></span></div>
        <div class="anzan-number-wrap ${paused?'is-paused':''}">
          ${paused?`<div class="anzan-paused"><strong>Ronda en pausa</strong><p>${pauseReason||'Reanuda cuando estés lista.'}</p></div>`:`<div class="anzan-number is-entering" id="anzanCurrent" role="status" aria-live="polite" aria-atomic="true">${current}</div>`}
        </div>
        ${settings.mode==='manual'?`<div class="anzan-manual"><p>Suma y avanza. Sin retroceder.</p><button class="anzan-btn anzan-primary" type="button" id="anzanAdvance" ${paused?'disabled':''}>${index===sequence.length-1?'Terminar cifras':'Siguiente cifra'} <span aria-hidden="true">→</span></button><small>Teclas: <kbd>→</kbd> o <kbd>Espacio</kbd></small></div>`:`<p class="anzan-auto-note">${paused?'El avance automático está detenido.':`Siguiente cifra en ${String(settings.speed).replace('.',',')} s`}</p>`}
      </section>`));
      bindRoundControls();
      if(settings.mode==='manual'&&!paused)focus('#anzanAdvance');
      schedule();
    }

    function bindRoundControls(){
      select('#anzanPause').addEventListener('click',()=>togglePause());
      select('#anzanRestart').addEventListener('click',startPreparation);
      select('#anzanExit').addEventListener('click',renderConfig);
      select('#anzanAdvance')?.addEventListener('click',advance);
    }

    function advance(){
      if(!active||screen!=='running'||paused)return;
      clearTimer();
      if(index>=sequence.length-1){renderAnswer();return;}
      index+=1;updateRunningDisplay();playDigitTone();schedule();
    }

    function updateRunningDisplay(){
      const digit=select('#anzanCurrent'),position=select('#anzanPosition'),progress=select('#anzanProgress'),next=select('#anzanAdvance');
      if(!digit||!position||!progress)return;
      digit.textContent=String(sequence[index]);digit.classList.remove('is-entering');void digit.offsetWidth;digit.classList.add('is-entering');
      position.textContent=`Cifra ${index+1} de ${sequence.length}`;progress.style.width=`${((index+1)/sequence.length)*100}%`;
      if(next)next.innerHTML=`${index===sequence.length-1?'Terminar cifras':'Siguiente cifra'} <span aria-hidden="true">→</span>`;
    }

    function togglePause(reason=''){
      if(screen!=='running')return;
      clearTimer();stopSounds();paused=!paused;pauseReason=paused?reason:'';renderRunning();emitState();
      focus('#anzanPause');
    }

    function pauseForHiddenTab(){
      if(!document.hidden||!active||paused)return;
      if(screen==='running'){paused=true;pauseReason='La pestaña se ocultó, así que detuvimos la ronda para que no pierdas cifras.';clearTimer();stopSounds();renderRunning();emitState();}
      else if(screen==='prep'){paused=true;pauseReason='La preparación se detuvo mientras la pestaña estuvo oculta.';clearTimer();renderPreparation();emitState();}
    }

    function renderAnswer(){
      clearTimer();stopSounds();screen='answer';paused=false;emitState();
      setMarkup(shell(`<section class="anzan-answer" aria-labelledby="anzanAnswerTitle">
        <p class="anzan-kicker">Cifras completadas</p><h3 id="anzanAnswerTitle" tabindex="-1">¿Cuál es la suma total?</h3>
        <p>Escribe el resultado que acumulaste mentalmente.</p>
        <form id="anzanAnswerForm"><label for="anzanTotal">Tu respuesta</label><input id="anzanTotal" name="total" inputmode="numeric" autocomplete="off" required aria-describedby="anzanAnswerError"><div class="anzan-keypad" aria-label="Teclado numérico">${[1,2,3,4,5,6,7,8,9].map(n=>`<button type="button" data-digit="${n}">${n}</button>`).join('')}<button type="button" data-action="clear">Limpiar</button><button type="button" data-digit="0">0</button><button type="button" data-action="backspace" aria-label="Borrar último dígito">⌫</button><button class="anzan-keypad-submit" type="submit">Confirmar respuesta</button></div><p class="anzan-error" id="anzanAnswerError" role="alert" hidden>Escribe la respuesta usando solo números.</p></form>
        <div class="anzan-actions anzan-answer-actions"><button class="anzan-btn anzan-quiet" type="button" id="anzanRestart">Reiniciar</button><button class="anzan-btn anzan-quiet" type="button" id="anzanExit">Salir</button></div>
      </section>`));
      select('#anzanAnswerForm').addEventListener('submit',event=>{event.preventDefault();const input=select('#anzanTotal'),result=evaluateAnswer(sequence,input.value);if(result.received===null){input.setAttribute('aria-invalid','true');select('#anzanAnswerError').hidden=false;input.focus();return;}renderFeedback(result);});
      container.querySelectorAll('[data-digit]').forEach(button=>button.addEventListener('click',()=>{const input=select('#anzanTotal');if(input.value.length<4)input.value+=button.dataset.digit;clearAnswerError();}));
      select('[data-action="clear"]').onclick=()=>{select('#anzanTotal').value='';clearAnswerError();};select('[data-action="backspace"]').onclick=()=>{const input=select('#anzanTotal');input.value=input.value.slice(0,-1);clearAnswerError();};select('#anzanTotal').addEventListener('input',clearAnswerError);
      select('#anzanRestart').addEventListener('click',startPreparation);select('#anzanExit').addEventListener('click',renderConfig);if(root.matchMedia?.('(pointer: coarse)').matches)focus('#anzanAnswerTitle');else focus('#anzanTotal');
    }

    function clearAnswerError(){const input=select('#anzanTotal'),error=select('#anzanAnswerError');input?.removeAttribute('aria-invalid');if(error)error.hidden=true;}

    function renderFeedback(result){
      screen='feedback';emitState();
      setMarkup(shell(`<section class="anzan-feedback" aria-live="polite" aria-labelledby="anzanFeedbackTitle">
        <div class="anzan-verdict ${result.correct?'is-correct':'is-wrong'}"><p class="anzan-kicker">Resultado</p><h3 id="anzanFeedbackTitle">${result.correct?'¡Suma correcta!':'Casi. Revisa dónde cambió tu acumulado.'}</h3><p>${result.received===null?'La respuesta debe contener solo números.':`Respondiste <strong>${result.received}</strong>.`} La suma era <strong>${result.expected}</strong>.</p></div>
        <div class="anzan-sequence"><span>Secuencia</span><ol>${sequence.map(n=>`<li>${n}</li>`).join('')}</ol></div>
        <div class="anzan-tip"><strong>Próxima ronda</strong><p>${result.correct?'Mantén la precisión y prueba una velocidad más corta cuando logres tres rondas seguidas.':'Haz grupos parciales de dos cifras y conserva el último subtotal antes de avanzar.'}</p></div>
        <div class="anzan-actions"><button class="anzan-btn anzan-primary" type="button" id="anzanNewRound">Nueva ronda</button><button class="anzan-btn anzan-quiet" type="button" id="anzanExit">Salir</button></div>
      </section>`));
      select('#anzanNewRound').addEventListener('click',startPreparation);select('#anzanExit').addEventListener('click',renderConfig);focus('#anzanNewRound');
    }

    function onKeydown(event){
      if(!active||screen!=='running'||settings.mode!=='manual'||paused||event.repeat||event.ctrlKey||event.metaKey||event.altKey)return;
      const tag=event.target.tagName;if(['INPUT','SELECT','TEXTAREA'].includes(tag)||event.target.isContentEditable)return;if(tag==='BUTTON'&&event.target.id!=='anzanAdvance'&&event.key!=='ArrowRight')return;
      if(event.key==='ArrowRight'||event.code==='Space'){event.preventDefault();advance();}
    }

    function activate(){
      if(active)return;active=true;container.hidden=false;document.addEventListener('visibilitychange',pauseForHiddenTab);document.addEventListener('keydown',onKeydown);renderConfig();
    }

    function deactivate(){
      if(!active)return;active=false;launchToken+=1;starting=false;clearTimer();stopSounds();screen='inactive';paused=false;emitState();document.removeEventListener('visibilitychange',pauseForHiddenTab);document.removeEventListener('keydown',onKeydown);container.replaceChildren();container.hidden=true;
    }

    return {activate,deactivate};
  }

  const api={init,generateSequence,evaluateAnswer,parseSpeed,timingPlan,publicScreen};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrainerAnzan=api;
})(typeof globalThis!=='undefined'?globalThis:this);
