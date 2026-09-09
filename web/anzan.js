/* TrainerMath Anzan: entrenamiento mental aislado, sin persistencia ni historial. */
(function(root){
  'use strict';

  const COUNTS=[5,10,15,20];
  const SPEEDS=[0.5,1,1.5,2];
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

  function init(container){
    if(!container||typeof container.replaceChildren!=='function')throw new Error('TrainerAnzan necesita un contenedor válido.');

    let active=false,timer=0,screen='config',sequence=[],index=0,paused=false,pauseReason='',round=0;
    let settings={count:10,speed:1,mode:'auto'};
    const select=(s)=>container.querySelector(s);

    function clearTimer(){if(timer){clearTimeout(timer);timer=0;}}
    function focus(selector){requestAnimationFrame(()=>select(selector)?.focus({preventScroll:true}));}
    function setMarkup(html){container.innerHTML=html;}

    function shell(content){
      return `<div class="anzan-shell"><div class="anzan-head"><div><p class="anzan-kicker">Cálculo mental</p><h1>Anzan</h1></div><p>Suma cifras sin escribir operaciones. Precisión primero; velocidad después.</p></div>${content}</div>`;
    }

    function renderConfig(){
      clearTimer();screen='config';paused=false;pauseReason='';
      setMarkup(shell(`<form class="anzan-config" id="anzanConfig">
        <div class="anzan-fields">
          <label>Cantidad de cifras<select name="count">${COUNTS.map(n=>`<option value="${n}" ${settings.count===n?'selected':''}>${n} cifras</option>`).join('')}</select></label>
          <label>Tiempo por cifra <small>(solo automática)</small><select name="speed" id="anzanSpeed" ${settings.mode==='manual'?'disabled':''}>${SPEEDS.map(n=>`<option value="${n}" ${settings.speed===n?'selected':''}>${String(n).replace('.',',')} s</option>`).join('')}</select></label>
          <fieldset><legend>Presentación</legend><label class="anzan-radio"><input type="radio" name="mode" value="auto" ${settings.mode==='auto'?'checked':''}><span><strong>Automática</strong><small>Las cifras avanzan solas</small></span></label><label class="anzan-radio"><input type="radio" name="mode" value="manual" ${settings.mode==='manual'?'checked':''}><span><strong>Con flechas</strong><small>Tú marcas el ritmo, sin retroceder</small></span></label></fieldset>
        </div>
        <div class="anzan-note"><strong>Cómo entrenar</strong><p>Verás únicamente números del 1 al 9. Acumula cada cifra en tu mente; la suma solo se muestra después de responder.</p></div>
        <button class="anzan-btn anzan-primary" type="submit">Comenzar ronda</button>
      </form>`));
      select('#anzanConfig').addEventListener('submit',event=>{
        event.preventDefault();
        const data=new FormData(event.currentTarget);
        settings={count:Number(data.get('count')),speed:Number(data.get('speed')||settings.speed),mode:data.get('mode')==='manual'?'manual':'auto'};
        startRound();
      });
      container.querySelectorAll('input[name="mode"]').forEach(input=>input.addEventListener('change',()=>{select('#anzanSpeed').disabled=input.value==='manual'&&input.checked;}));
    }

    function startRound(){
      clearTimer();round+=1;sequence=generateSequence(settings.count);index=0;paused=false;pauseReason='';screen='running';renderRunning();
      container.scrollIntoView({block:'start',behavior:'instant'});
    }

    function schedule(){
      clearTimer();
      if(!active||screen!=='running'||paused||settings.mode!=='auto')return;
      const interval=settings.speed*1000;
      timer=setTimeout(()=>{
        const digit=select('#anzanCurrent');
        if(digit){digit.textContent='';digit.classList.remove('is-entering');}
        timer=setTimeout(()=>advance(),BLANK_MS);
      },Math.max(0,interval-BLANK_MS));
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
      select('#anzanRestart').addEventListener('click',startRound);
      select('#anzanExit').addEventListener('click',renderConfig);
      select('#anzanAdvance')?.addEventListener('click',advance);
    }

    function advance(){
      if(!active||screen!=='running'||paused)return;
      clearTimer();
      if(index>=sequence.length-1){renderAnswer();return;}
      index+=1;updateRunningDisplay();schedule();
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
      clearTimer();paused=!paused;pauseReason=paused?reason:'';renderRunning();
      focus('#anzanPause');
    }

    function pauseForHiddenTab(){
      if(document.hidden&&active&&screen==='running'&&!paused){paused=true;pauseReason='La pestaña se ocultó, así que detuvimos la ronda para que no pierdas cifras.';clearTimer();renderRunning();}
    }

    function renderAnswer(){
      clearTimer();screen='answer';paused=false;
      setMarkup(shell(`<section class="anzan-answer" aria-labelledby="anzanAnswerTitle">
        <p class="anzan-kicker">Cifras completadas</p><h3 id="anzanAnswerTitle">¿Cuál es la suma total?</h3>
        <p>Escribe el resultado que acumulaste mentalmente.</p>
        <form id="anzanAnswerForm"><label for="anzanTotal">Tu respuesta</label><input id="anzanTotal" name="total" inputmode="numeric" autocomplete="off" required aria-describedby="anzanAnswerError"><button class="anzan-btn anzan-primary" type="submit">Comprobar suma</button><p class="anzan-error" id="anzanAnswerError" role="alert" hidden>Escribe la respuesta usando solo números.</p></form>
        <div class="anzan-actions anzan-answer-actions"><button class="anzan-btn anzan-quiet" type="button" id="anzanRestart">Reiniciar</button><button class="anzan-btn anzan-quiet" type="button" id="anzanExit">Salir</button></div>
      </section>`));
      select('#anzanAnswerForm').addEventListener('submit',event=>{event.preventDefault();const input=select('#anzanTotal'),result=evaluateAnswer(sequence,input.value);if(result.received===null){input.setAttribute('aria-invalid','true');select('#anzanAnswerError').hidden=false;input.focus();return;}renderFeedback(result);});
      select('#anzanRestart').addEventListener('click',startRound);select('#anzanExit').addEventListener('click',renderConfig);focus('#anzanTotal');
    }

    function renderFeedback(result){
      screen='feedback';
      setMarkup(shell(`<section class="anzan-feedback" aria-live="polite" aria-labelledby="anzanFeedbackTitle">
        <div class="anzan-verdict ${result.correct?'is-correct':'is-wrong'}"><p class="anzan-kicker">Resultado</p><h3 id="anzanFeedbackTitle">${result.correct?'¡Suma correcta!':'Casi. Revisa dónde cambió tu acumulado.'}</h3><p>${result.received===null?'La respuesta debe contener solo números.':`Respondiste <strong>${result.received}</strong>.`} La suma era <strong>${result.expected}</strong>.</p></div>
        <div class="anzan-sequence"><span>Secuencia</span><ol>${sequence.map(n=>`<li>${n}</li>`).join('')}</ol></div>
        <div class="anzan-tip"><strong>Próxima ronda</strong><p>${result.correct?'Mantén la precisión y prueba una velocidad más corta cuando logres tres rondas seguidas.':'Haz grupos parciales de dos cifras y conserva el último subtotal antes de avanzar.'}</p></div>
        <div class="anzan-actions"><button class="anzan-btn anzan-primary" type="button" id="anzanNewRound">Nueva ronda</button><button class="anzan-btn anzan-quiet" type="button" id="anzanExit">Salir</button></div>
      </section>`));
      select('#anzanNewRound').addEventListener('click',startRound);select('#anzanExit').addEventListener('click',renderConfig);focus('#anzanNewRound');
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
      if(!active)return;active=false;clearTimer();document.removeEventListener('visibilitychange',pauseForHiddenTab);document.removeEventListener('keydown',onKeydown);container.replaceChildren();container.hidden=true;
    }

    return {activate,deactivate};
  }

  const api={init,generateSequence,evaluateAnswer};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrainerAnzan=api;
})(typeof globalThis!=='undefined'?globalThis:this);
