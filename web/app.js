(function(){
  'use strict';
  const E=window.TrainerEngine, bank=Array.isArray(window.TRAINER_DATA)?window.TRAINER_DATA:[];
  const byId=new Map(bank.map(p=>[E.qid(p),p]));
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const letters=['A','B','C','D'];
  const topics=[...new Set(bank.map(p=>p.tema).filter(Boolean))];
  const modes={
    variety:['Variedad','Mezcla familias y prioriza preguntas nuevas'],
    adaptive:['Adaptativo','Da prioridad a temas donde necesitas refuerzo'],
    speed:['Velocidad','Solo preguntas con meta de hasta 60 segundos'],
    review:['Repaso','Errores, pistas y respuestas fuera de meta']
  };
  let storage;try{storage=window.localStorage;}catch(_){storage={getItem(){return null;},setItem(){throw new Error('storage unavailable');}};}
  let loaded=E.load(storage,bank), state=loaded.state, readOnly=!!loaded.readOnly;
  let currentView='home', tickHandle=0, toastHandle=0, lastResult=null, paletteOpen=!window.matchMedia('(max-width:900px)').matches, practicePanelOpen=true, reviewDetailOpen=true, selectedReviewId='';
  const revealedSteps={};
  let anzan;
  const prefs={practice:{topic:'Todos',level:0,count:10,mode:'variety'},exam:{topic:'Todos',level:0,count:20,minutes:40}};

  function esc(v){return String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
  function fmtTime(value){const s=Math.max(0,Math.round(Number(value)||0));return `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`;}
  function stars(n){return `<span aria-label="Nivel ${n} de 3">${'★'.repeat(n)}${'☆'.repeat(3-n)}</span>`;}
  function notify(message){const el=$('#toast');el.textContent=message;el.classList.add('on');clearTimeout(toastHandle);toastHandle=setTimeout(()=>el.classList.remove('on'),3200);}
  function save(){if(readOnly)return false;const r=E.save(storage,state);if(!r.ok){readOnly=true;showStorage(r.error);return false;}return true;}
  function showStorage(message){const el=$('#storageAlert');el.hidden=false;el.textContent=message;}
  function markSeen(p){const id=E.qid(p);state.seen[id]=Date.now();save();}
  function setChoice(root,value){$$('button',root).forEach(b=>b.setAttribute('aria-pressed',String(String(b.dataset.value)===String(value))));}
  function fillSelect(el,values){el.innerHTML=values.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('');}
  function makeStars(root,key){root.innerHTML=[0,1,2,3].map(n=>`<button type="button" data-value="${n}" aria-pressed="${prefs[key].level===n}">${n?`${'★'.repeat(n)}<span class="sr-only">Nivel ${n}</span>`:'Todos'}</button>`).join('');root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;prefs[key].level=+b.dataset.value;setChoice(root,prefs[key].level);updateConfig(key);});}
  function makeCounts(root,key,values){root.innerHTML=values.map(n=>`<button type="button" data-value="${n}" aria-pressed="${prefs[key].count===n}">${n}</button>`).join('');root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;prefs[key].count=+b.dataset.value;setChoice(root,prefs[key].count);updateConfig(key);});}

  function stats(){return E.stats(state);}
  function renderHome(){
    const s=stats(), eligible=bank.filter(p=>p.practiceEligible!==false), generatedItems=eligible.filter(p=>p.origin==='generated'), total=eligible.length, generated=generatedItems.length, families=new Set(generatedItems.map(p=>p.family).filter(Boolean)).size;
    $('#homeMetrics').innerHTML=[
      ['Banco disponible',total,`${generated} nuevos · ${families} familias nuevas`],
      ['Preguntas resueltas',s.count,'intentos cronometrados'],
      ['Precisión',s.accuracy==null?'—':`${s.accuracy}%`,s.accuracy==null?'Empieza para crear tu línea base':'sin contar respuestas con pista'],
      ['Mediana',s.median==null?'—':fmtTime(s.median),s.median==null?'Aún sin respuestas correctas':'tiempo en respuestas correctas']
    ].map(x=>`<div class="metric"><span>${x[0]}</span><strong>${x[1]}</strong><small>${x[2]}</small></div>`).join('');
    const rows=topics.map(t=>{const v=s.topics[t];const acc=v?v.accuracy:0;return `<div class="topic-row"><strong>${esc(t)}</strong><div class="track" aria-label="${esc(t)}: ${acc}% de precisión"><span style="width:${acc}%"></span></div><small>${v?`${v.correct}/${v.count}`:'Sin intentos'}</small></div>`;});
    $('#topicProgress').innerHTML=rows.length?rows.join(''):`<div class="empty-state"><strong>Banco en preparación</strong>No hay temas disponibles.</div>`;
    $('#reviewActionLabel').textContent=s.review?`${s.review} pregunta${s.review===1?'':'s'} para reforzar`:'No tienes pendientes todavía';
    const quick=$('#quickStart');
    if(state.active){quick.textContent=state.active.mode==='exam'?'Continuar examen en curso':'Continuar práctica en curso';}
    else quick.textContent='Practicar 10 preguntas';
    quick.disabled=!total;
  }

  function showView(name,focus=true){
    if(!['home','practice','exam','review','anzan'].includes(name))name='home';
    if(state.active?.mode==='practice'&&currentView==='practice'&&name!=='practice'&&!state.active.paused){E.checkpoint(state.active);state.active.paused=true;state.active.runningSince=0;save();}
    if(currentView==='anzan'&&name!=='anzan')anzan?.deactivate();
    currentView=name;
    $$('.view').forEach(v=>v.hidden=v.dataset.view!==name);
    $$('[data-nav]').forEach(b=>{if(b.tagName==='BUTTON')b.setAttribute('aria-current',b.dataset.nav===name?'page':'false');});
    location.hash=name==='home'?'inicio':name;
    if(name==='home')renderHome();
    if(name==='practice')renderPracticeSurface();
    if(name==='exam')renderExamSurface();
    if(name==='review')renderReview();
    if(name==='anzan')anzan?.activate();
    window.scrollTo({top:0,behavior:'auto'});
    if(focus)$('#mainContent').focus({preventScroll:true});
  }

  function filteredCount(kind){
    const p=prefs[kind], mode=kind==='practice'?p.mode:'variety';
    return E.filtered(bank,{topic:p.topic,level:p.level,mode}).filter(q=>mode!=='review'||E.needsReview(E.latestAttempts(state).get(E.qid(q)))).length;
  }
  function updateConfig(kind){
    const p=prefs[kind], count=filteredCount(kind), take=Math.min(p.count,count);
    $(`#${kind}Pool`).textContent=`${count} disponible${count===1?'':'s'}`;
    if(kind==='practice'){
      const secs=E.filtered(bank,{topic:p.topic,level:p.level,mode:p.mode}).slice(0,take).reduce((n,q)=>n+(q.target||90),0);
      const sourcePool=E.filtered(bank,{topic:p.topic,level:p.level,mode:p.mode}), generatedItems=sourcePool.filter(q=>q.origin==='generated'), generated=generatedItems.length, families=new Set(generatedItems.map(q=>q.family).filter(Boolean)).size;
      $('#practiceEstimate').textContent=count?`${take} pregunta${take===1?'':'s'} · meta aprox. ${Math.max(1,Math.ceil(secs/60))} min · ${generated} ejercicios nuevos en ${families} familias nuevas con este filtro.`:'No hay preguntas con esta combinación. Cambia un filtro.';
      $('#practiceSetup button[type="submit"]').disabled=!count;
    }else{
      const plan=E.examPlan(bank,p,state);
      $('#examCoverage').innerHTML=plan.areas.map(a=>`<div class="coverage-item"><span>${esc(a.topic)}</span><strong>${a.count}<small> preguntas</small></strong></div>`).join('');
      $('#examEstimate').textContent=plan.error||`${plan.count} preguntas · ${p.minutes} min totales · ${Math.round(p.minutes*60/plan.count)} s promedio por pregunta · todas las áreas incluidas.`;
      $('#examSetup button[type="submit"]').disabled=!!plan.error;
    }
  }

  function setupConfigs(){
    fillSelect($('#practiceTopic'),['Todos',...topics]);
    $('#practiceTopic').addEventListener('change',e=>{prefs.practice.topic=e.target.value;updateConfig('practice');});
    makeStars($('#practiceLevel'),'practice');makeStars($('#examLevel'),'exam');
    makeCounts($('#practiceCount'),'practice',[5,10,20]);makeCounts($('#examCount'),'exam',[20,30,40]);
    $('#practiceModes').innerHTML=Object.entries(modes).map(([id,v])=>`<label class="mode-option"><input type="radio" name="practiceMode" value="${id}" ${id==='variety'?'checked':''}><span><strong>${v[0]}</strong><small>${v[1]}</small></span></label>`).join('');
    $('#practiceModes').addEventListener('change',e=>{prefs.practice.mode=e.target.value;updateConfig('practice');});
    $('#examMinutes').addEventListener('change',e=>{prefs.exam.minutes=+e.target.value;updateConfig('exam');});
    updateConfig('practice');updateConfig('exam');
  }

  function selectAndStart(kind,overrides={}){
    if(state.active){showView(state.active.mode==='exam'?'exam':'practice');return;}
    const p={...prefs[kind],...overrides};
    const selectionMode=kind==='practice'?p.mode:'variety';
    let selected;
    try{selected=kind==='exam'?E.selectExamProblems(bank,state,p):E.selectProblems(bank,state,{topic:p.topic,level:p.level,count:p.count,mode:selectionMode});}
    catch(error){notify(error.message);return;}
    if(!selected.length){notify('No hay preguntas disponibles con esos filtros.');return;}
    state.active=E.createSession(selected,kind==='exam'?{mode:'exam',variant:'variety',duration:p.minutes*60}:{mode:'practice',variant:selectionMode});
    save();lastResult=null;showView(kind==='exam'?'exam':'practice');
  }

  function currentProblem(){return state.active?byId.get(state.active.ids[state.active.index]):null;}
  function elapsedPractice(){const s=state.active,p=currentProblem();if(!s||!p)return 0;let value=s.times[E.qid(p)]||0;if(s.runningSince&&!s.paused&&!s.answers[E.qid(p)])value+=(Date.now()-s.runningSince)/1000;return value;}
  function startTicker(){clearInterval(tickHandle);tickHandle=setInterval(()=>{
    if(!state.active)return;
    if(state.active.mode==='exam'){
      const rem=E.remaining(state.active),el=$('#examClock');if(el)el.textContent=fmtTime(rem);if(rem<=0)finishExam(true);
    }else{
      const p=currentProblem(),el=$('#practiceClock');if(el&&p&&!state.active.answers[E.qid(p)]){const t=elapsedPractice();el.textContent=fmtTime(t);el.classList.toggle('over',t>(p.target||90));}
    }
  },500);}

  function problemBody(p,answer,mode){
    const id=E.qid(p), answered=!!answer, solutionAllowed=mode==='study'||mode==='result'||(mode==='practice'&&answered);
    const options=p.opts.map((o,i)=>{
      let cls='option';if(answer?.choice===i)cls+=' selected';if(solutionAllowed&&i===p.ans)cls+=' correct reveal';if(solutionAllowed&&answer&&answer.choice===i&&i!==p.ans)cls+=' wrong';
      return `<button type="button" class="${cls}" data-choice="${i}" aria-pressed="${answer?.choice===i}" ${mode==='study'||mode==='result'||answered?'disabled':''}><span class="option-key">${letters[i]}</span><span>${o}</span></button>`;
    }).join('');
    return `<div class="question-meta"><span class="tag">${esc(p.tema)}</span><span class="tag">${esc(p.sub||'Práctica')}</span><span class="tag level">${stars(Number(p.dif)||1)}</span><span class="tag">Meta ${fmtTime(p.target||90)}</span></div><div class="question-text">${p.enun}</div>${p.fig?`<div class="question-figure">${p.fig}</div>`:''}<div class="options" aria-label="Alternativas">${options}</div>`;
  }
  function solutionHtml(p){return `<div class="steps">${(p.steps||[]).map((s,i)=>`<article class="step"><h3><span class="step-index">${i+1}.</span>${esc(s.t)}</h3><div>${s.d}</div></article>`).join('')}</div><div class="answer-box"><strong>Respuesta ${letters[p.ans]}:</strong> ${p.opts[p.ans]}</div>${p.idea?`<div class="tip-card"><strong>Idea clave</strong><div>${p.idea}</div></div>`:''}${p.nota?`<div class="trap-card"><strong>Nota del material original:</strong> ${p.nota}</div>`:''}`;}
  function progressiveSolution(p){const key=`${state.active.id}:${E.qid(p)}`,shown=revealedSteps[key]||0,steps=p.steps||[];return `<details class="solution" ${shown?'open':''}><summary>Solución paso a paso</summary><div class="steps">${steps.slice(0,shown).map((s,i)=>`<article class="step"><h3><span class="step-index">${i+1}.</span>${esc(s.t)}</h3><div>${s.d}</div></article>`).join('')}</div>${shown>=steps.length&&steps.length?`<div class="answer-box"><strong>Respuesta ${letters[p.ans]}:</strong> ${p.opts[p.ans]}</div>`:''}<div class="question-actions">${shown<steps.length?`<button class="button primary small" type="button" id="nextSolutionStep">${shown?'Ver siguiente paso':'Ver primer paso'}</button><button class="button secondary small" type="button" id="allSolutionSteps">Mostrar todo</button>`:''}</div></details>`;}

  function renderPracticeSurface(){
    const active=state.active?.mode==='practice';
    $('#practiceSetup').hidden=active||lastResult?.mode==='practice';$('#practiceSession').hidden=!active;$('#practiceResult').hidden=!(lastResult?.mode==='practice');$('#studyArea').hidden=true;
    $('#practiceTab').setAttribute('aria-selected','true');$('#studyTab').setAttribute('aria-selected','false');
    if(active){renderPracticeQuestion();startTicker();}else if(lastResult?.mode==='practice')renderPracticeResult();else updateConfig('practice');
  }
  function renderPracticeQuestion(){
    const s=state.active,p=currentProblem();if(!s||!p)return;markSeen(p);
    const id=E.qid(p),a=s.answers[id], elapsed=a?.seconds??elapsedPractice(), pct=Math.round((s.index+1)/s.ids.length*100);
    $('#practiceSession').innerHTML=`<div class="session-shell ${practicePanelOpen?'':'no-panel'}"><div class="session-main"><div class="session-top"><span class="session-position">Pregunta ${s.index+1} de ${s.ids.length}</span><span class="spacer"></span>${practicePanelOpen?'':`<button type="button" class="button small secondary" id="showPracticePanel">Mostrar resumen</button>`}<span class="timer-pill ${elapsed>(p.target||90)?'over':''}" id="practiceClock">${fmtTime(elapsed)}</span><button type="button" class="button small secondary" id="pausePractice">${s.paused?'Reanudar':'Pausar'}</button></div><article class="question-card">${problemBody(p,a,'practice')}<div class="question-actions" id="practiceActions">${a?'':`<button class="button secondary" type="button" id="hintButton">Ver pista</button><button class="button secondary" type="button" id="skipButton">No sé todavía</button><span class="assist-note">Usar una pista marca el intento como asistido, pero te ayuda a aprender el camino.</span>`}</div>${a?practiceFeedback(p,a):''}</article><div class="session-nav"><button class="button secondary" type="button" id="exitPractice">Terminar sesión</button>${a?`<button class="button primary" type="button" id="nextPractice">${s.index===s.ids.length-1?'Ver resultado':'Siguiente pregunta'} →</button>`:''}</div></div>${practicePanelOpen?`<aside class="surface side-panel"><button type="button" class="button secondary small" id="hidePracticePanel">Ocultar resumen</button><p class="eyebrow">Sesión activa</p><h2>${esc(modes[s.variant]?.[0]||'Práctica')}</h2><div class="goal-meter"><p><span>Avance</span><strong>${pct}%</strong></p><div class="track"><span style="width:${pct}%"></span></div></div><p class="session-note"><strong>${esc(p.tema)}</strong><br>${esc(p.sub||'')}</p><p class="session-note">Meta de esta pregunta: ${fmtTime(p.target||90)}</p><p class="session-note">La explicación no suma a tu tiempo.</p></aside>`:''}</div>`;
    $$('.option',$('#practiceSession')).forEach(b=>b.addEventListener('click',()=>answerPractice(+b.dataset.choice)));
    $('#hintButton')?.addEventListener('click',()=>showHint(p));$('#skipButton')?.addEventListener('click',()=>answerPractice(null));
    $('#pausePractice').addEventListener('click',togglePause);$('#nextPractice')?.addEventListener('click',nextPractice);$('#exitPractice').addEventListener('click',()=>finishPractice(true));
    $('#hidePracticePanel')?.addEventListener('click',()=>{practicePanelOpen=false;renderPracticeQuestion();});$('#showPracticePanel')?.addEventListener('click',()=>{practicePanelOpen=true;renderPracticeQuestion();});
    $('#nextSolutionStep')?.addEventListener('click',()=>revealPracticeStep(p,1));$('#allSolutionSteps')?.addEventListener('click',()=>revealPracticeStep(p,(p.steps||[]).length));bindReflection();
  }
  function showHint(p){const s=state.active,id=E.qid(p);if(!s.hintIds.includes(id))s.hintIds.push(id);save();const hint=p.hint||p.idea||'Identifica primero la condición que reduce más alternativas y estima antes de operar.';const actions=$('#practiceActions');let old=$('.tip-card',actions);if(!old){old=document.createElement('div');old.className='tip-card';old.innerHTML=`<strong>Pista orientativa</strong><div>${hint}</div>`;actions.prepend(old);}notify('Pista abierta: este intento quedará marcado como asistido.');}
  function answerPractice(choice){const s=state.active,p=currentProblem();if(!s||s.paused){notify('Reanuda la sesión para responder.');return;}if(!E.answer(s,p,choice))return;save();renderPracticeQuestion();}
  function practiceFeedback(p,a){const good=a.choice===p.ans, timeText=a.seconds<=(p.target||90)?`Dentro de la meta de ${fmtTime(p.target||90)}`:`${fmtTime(a.seconds-(p.target||90))} sobre la meta`;
    const trap=p.trap||(!good?'Revisa la condición que cambia el modelo antes de volver a calcular.':'No te detengas en operaciones que una condición ya permite descartar.');
    return `<section class="feedback" aria-live="polite"><div class="feedback-head"><div><p class="eyebrow">Feedback inmediato</p><h2 class="${good?'':'bad'}">${good?'Correcto':'Aún no'}${a.hint?' · con pista':''}</h2></div><span class="feedback-time">${fmtTime(a.seconds)} · ${timeText}</span></div><div class="tip-card"><strong>Atajo práctico</strong><div>${p.idea||'Resume el método en una condición, una operación y una verificación.'}</div></div><div class="trap-card"><strong>Evita esta trampa:</strong> ${trap}</div>${progressiveSolution(p)}<div class="reflection"><fieldset><legend>¿Con qué confianza respondiste?</legend><div class="choice-row reflect-confidence"><button type="button" data-value="segura" aria-pressed="${a.confidence==='segura'}">Segura</button><button type="button" data-value="duda" aria-pressed="${a.confidence==='duda'}">Con duda</button><button type="button" data-value="azar" aria-pressed="${a.confidence==='azar'}">Al azar</button></div></fieldset>${good?'':`<fieldset><legend>¿Qué te frenó?</legend><div class="choice-row reflect-reason"><button type="button" data-value="concepto" aria-pressed="${a.reason==='concepto'}">Concepto</button><button type="button" data-value="calculo" aria-pressed="${a.reason==='calculo'}">Cálculo</button><button type="button" data-value="lectura" aria-pressed="${a.reason==='lectura'}">Lectura</button><button type="button" data-value="tiempo" aria-pressed="${a.reason==='tiempo'}">Tiempo</button></div></fieldset>`}</div></section>`;}
  function revealPracticeStep(p,amount){const key=`${state.active.id}:${E.qid(p)}`,max=(p.steps||[]).length;revealedSteps[key]=amount===max?max:Math.min(max,(revealedSteps[key]||0)+amount);renderPracticeQuestion();}
  function bindReflection(){const a=state.active?.answers[E.qid(currentProblem()||{})];if(!a)return;$$('.reflect-confidence button').forEach(b=>b.addEventListener('click',()=>{a.confidence=b.dataset.value;setChoice(b.parentElement,a.confidence);save();}));$$('.reflect-reason button').forEach(b=>b.addEventListener('click',()=>{a.reason=b.dataset.value;setChoice(b.parentElement,a.reason);save();}));}
  function togglePause(){const s=state.active;if(!s||s.mode!=='practice')return;if(s.paused){s.paused=false;s.runningSince=Date.now();}else{E.checkpoint(s);s.paused=true;s.runningSince=0;}save();renderPracticeQuestion();}
  function nextPractice(){const s=state.active;if(!s)return;if(s.index>=s.ids.length-1){finishPractice(false);return;}s.index++;s.paused=false;s.runningSince=Date.now();save();renderPracticeQuestion();window.scrollTo({top:0,behavior:'smooth'});}
  function finishPractice(aborted){const ids=[...(state.active?.ids||[])],summary=E.finishSession(state,bank,Date.now(),aborted);if(!summary)return;lastResult={...summary,mode:'practice',ids};save();renderPracticeSurface();renderHome();}
  function renderPracticeResult(){const r=lastResult,attempted=r.rows.length,correct=r.correct,assisted=r.rows.filter(x=>x.hint).length;$('#practiceResult').innerHTML=`<section class="surface result-hero"><p class="eyebrow">Sesión completada</p><div class="result-score">${correct}/${attempted}</div><h2>${correct===attempted&&attempted?'Ritmo y precisión':'Ya sabes qué reforzar después'}</h2><div class="result-grid"><div><span>Correctas</span><strong>${correct}</strong></div><div><span>Por revisar</span><strong>${attempted-correct}</strong></div><div><span>Con pista</span><strong>${assisted}</strong></div><div><span>Tiempo resolviendo</span><strong>${fmtTime(r.seconds)}</strong></div></div><div class="result-actions"><button class="button primary" id="newPractice">Nueva práctica</button><button class="button secondary" data-nav="review">Revisar pendientes</button></div></section>`;$('#newPractice').onclick=()=>{lastResult=null;renderPracticeSurface();};$('[data-nav="review"]',$('#practiceResult')).onclick=()=>showView('review');}

  function showStudy(){
    if(state.active?.mode==='practice'&&!state.active.paused){E.checkpoint(state.active);state.active.paused=true;state.active.runningSince=0;save();}
    $('#practiceSetup').hidden=true;$('#practiceSession').hidden=true;$('#practiceResult').hidden=true;$('#studyArea').hidden=false;$('#practiceTab').setAttribute('aria-selected','false');$('#studyTab').setAttribute('aria-selected','true');
    const originals=bank.filter(p=>p.origin==='original');
    $('#studyArea').innerHTML=`<div class="study-toolbar"><label class="sr-only" for="studyTopic">Filtrar tema</label><select id="studyTopic"><option>Todos</option>${topics.map(t=>`<option>${esc(t)}</option>`).join('')}</select><p class="session-note">Abrir una solución aquí no registra intento ni tiempo.</p></div><div class="study-grid" id="studyGrid"></div><div id="studyDetail"></div>`;
    const paint=()=>{const t=$('#studyTopic').value,list=originals.filter(p=>t==='Todos'||p.tema===t);$('#studyGrid').innerHTML=list.map(p=>`<button class="study-card" type="button" data-id="${esc(E.qid(p))}"><span class="tag">Original ${esc(p.n||p.id)}</span><strong>${esc(p.sub||p.tema)}</strong><small>${esc(p.tema)} · ${'★'.repeat(p.dif||1)}</small></button>`).join('')||`<div class="empty-state"><strong>Sin problemas</strong>No hay originales con este filtro.</div>`;$$('.study-card').forEach(b=>b.onclick=()=>openStudy(b.dataset.id));};
    $('#studyTopic').onchange=paint;paint();
  }
  function openStudy(id){const p=byId.get(String(id));if(!p)return;$('#studyGrid').hidden=true;const root=$('#studyDetail');root.innerHTML=`<button class="button secondary small" type="button" id="closeStudy">← Volver al listado</button><article class="surface study-solution" style="margin-top:14px">${problemBody(p,{choice:p.ans},'study')}<details class="solution" open><summary>Resolución original</summary>${solutionHtml(p)}</details></article>`;$('#closeStudy').onclick=()=>{$('#studyGrid').hidden=false;root.innerHTML='';};}

  function renderExamSurface(){const active=state.active?.mode==='exam';$('#examSetup').hidden=active||lastResult?.mode==='exam';$('#examSession').hidden=!active;$('#examResult').hidden=!(lastResult?.mode==='exam');if(active){renderExamQuestion();startTicker();}else if(lastResult?.mode==='exam')renderExamResult();else updateConfig('exam');}
  function renderExamQuestion(){const s=state.active,p=currentProblem();if(!s||!p)return;markSeen(p);const id=E.qid(p),a=s.answers[id],answered=Object.hasOwn(s.answers,id),flagged=s.flags.includes(id),ansCount=Object.keys(s.answers).length;
    $('#examSession').innerHTML=`<div class="session-shell ${paletteOpen?'':'no-panel'}"><div class="session-main"><div class="session-top"><span class="session-position">Pregunta ${s.index+1} de ${s.ids.length}</span><span class="spacer"></span><span class="exam-clock" id="examClock">${fmtTime(E.remaining(s))}</span></div><article class="question-card">${problemBody(p,a,'exam')}<div class="question-actions"><button type="button" class="button secondary flag-toggle" id="flagQuestion" aria-pressed="${flagged}">${flagged?'★ Marcada':'☆ Marcar para volver'}</button><button type="button" class="button ghost" id="omitQuestion">Omitir por ahora</button></div></article><div class="session-nav"><button class="button secondary" id="examPrev" ${s.index===0?'disabled':''}>← Anterior</button><button class="button primary" id="examNext">${s.index===s.ids.length-1?'Ir al inicio':'Siguiente'} →</button></div></div><aside class="surface side-panel palette-panel" id="palettePanel" ${paletteOpen?'':'hidden'}><button class="button secondary small" id="hidePalette">Ocultar panel</button><p class="eyebrow">Mapa del examen</p><h2>${ansCount}/${s.ids.length} respondidas</h2><div class="palette">${s.ids.map((qid,i)=>`<button type="button" data-index="${i}" class="${s.answers[qid]?'answered ':''}${s.flags.includes(qid)?'flagged ':''}${i===s.index?'current':''}" aria-label="Pregunta ${i+1}${s.answers[qid]?', respondida':''}${s.flags.includes(qid)?', marcada':''}">${i+1}</button>`).join('')}</div><p class="session-note">Rosa: respondida · línea ámbar: marcada</p><button class="button danger" id="finishExam">Terminar y entregar</button></aside></div>${paletteOpen?'':`<button class="button primary palette-reopen" id="showPalette">Mostrar preguntas</button>`}`;
    $$('.option',$('#examSession')).forEach(b=>{b.disabled=false;b.onclick=()=>answerExam(+b.dataset.choice);});
    $('#flagQuestion').onclick=toggleFlag;$('#omitQuestion').onclick=()=>goExam(1);$('#examPrev').onclick=()=>goExam(-1);$('#examNext').onclick=()=>goExam(s.index===s.ids.length-1?-s.index:1);
    $$('.palette button').forEach(b=>b.onclick=()=>goExamTo(+b.dataset.index));$('#hidePalette')?.addEventListener('click',()=>{paletteOpen=false;renderExamQuestion();});$('#showPalette')?.addEventListener('click',()=>{paletteOpen=true;renderExamQuestion();});$('#finishExam')?.addEventListener('click',askFinish);
  }
  function answerExam(choice){const s=state.active,p=currentProblem();if(!s||!E.answer(s,p,choice))return;save();renderExamQuestion();}
  function goExam(delta){goExamTo(Math.max(0,Math.min(state.active.ids.length-1,state.active.index+delta)));}
  function goExamTo(index){const s=state.active;if(!s)return;E.checkpoint(s);s.index=index;s.runningSince=Date.now();save();renderExamQuestion();window.scrollTo({top:0,behavior:'smooth'});}
  function toggleFlag(){const s=state.active,id=E.qid(currentProblem()),i=s.flags.indexOf(id);if(i>=0)s.flags.splice(i,1);else s.flags.push(id);save();renderExamQuestion();}
  function askFinish(){const s=state.active,answered=Object.keys(s.answers).length,omitted=s.ids.length-answered;$('#finishDialogText').textContent=omitted?`Quedan ${omitted} pregunta${omitted===1?'':'s'} sin responder. Podrás revisar las soluciones después de entregar.`:'Respondiste todas las preguntas. Podrás revisar las soluciones después de entregar.';$('#finishDialog').showModal();}
  function finishExam(auto=false){if(!state.active||state.active.mode!=='exam')return;const dialog=$('#finishDialog');if(dialog.open)dialog.close('cancel');const ids=[...state.active.ids],summary=E.finishSession(state,bank);lastResult={...summary,mode:'exam',ids};save();renderExamSurface();renderHome();if(auto)notify('Tiempo terminado. El examen se entregó automáticamente.');}
  function renderExamResult(){const r=lastResult,wrong=r.rows.filter(x=>x.choice!==null&&!x.correct).length,omitted=r.rows.filter(x=>x.choice===null).length,answered=r.count-omitted,accuracy=answered?Math.round(r.correct/answered*100):0;
    $('#examResult').innerHTML=`<section class="surface result-hero"><p class="eyebrow">Examen entregado</p><div class="result-score">${r.correct}/${r.count}</div><h2>Resultado de entrenamiento</h2><div class="result-grid"><div><span>Correctas</span><strong>${r.correct}</strong></div><div><span>Errores</span><strong>${wrong}</strong></div><div><span>Omitidas</span><strong>${omitted}</strong></div><div><span>Precisión respondidas</span><strong>${accuracy}%</strong></div></div><p class="session-note">Tiempo total: ${fmtTime(r.seconds)}. Este simulacro es configurable y no representa una escala oficial.</p><section class="exam-area-results"><h3>Tu resultado por área</h3><div class="exam-coverage">${topics.map(topic=>{const rows=r.rows.filter(a=>byId.get(a.qid)?.tema===topic);if(!rows.length)return "";const correct=rows.filter(a=>a.correct).length;return `<div class="coverage-item"><span>${esc(topic)}</span><strong>${correct}/${rows.length}<small>correctas · ${fmtTime(rows.reduce((sum,a)=>sum+a.seconds,0))}</small></strong></div>`;}).join("")}</div></section><div class="result-actions"><button class="button primary" id="newExam">Nuevo examen</button><button class="button secondary" id="toggleExamReview">Revisar soluciones</button></div></section><div class="result-review" id="examReview" hidden>${r.ids.map((id,i)=>{const p=byId.get(id),a=r.rows.find(x=>x.qid===id);return `<details class="result-item"><summary><strong>Pregunta ${i+1} · ${a?.correct?'Correcta':a?.choice==null?'Omitida':'Incorrecta'}</strong> <span>${a?fmtTime(a.seconds):'—'}</span></summary><div class="study-solution">${problemBody(p,a,'result')}<div class="solution">${solutionHtml(p)}</div></div></details>`;}).join('')}</div>`;
    $('#newExam').onclick=()=>{lastResult=null;renderExamSurface();};$('#toggleExamReview').onclick=()=>{const el=$('#examReview');el.hidden=!el.hidden;$('#toggleExamReview').textContent=el.hidden?'Revisar soluciones':'Ocultar soluciones';};}

  function reviewItems(){const latest=E.latestAttempts(state);return [...latest.values()].filter(E.needsReview).sort((a,b)=>b.at-a.at);}
  function renderReview(){const list=reviewItems();if(!selectedReviewId||!list.some(a=>a.qid===selectedReviewId))selectedReviewId=list[0]?.qid||'';
    $('.review-layout').classList.toggle('no-detail',!reviewDetailOpen);$('#reviewDetail').hidden=!reviewDetailOpen;
    $('#reviewList').innerHTML=`<div class="review-list-head"><p class="eyebrow">Cola de refuerzo</p><h2>${list.length} pendiente${list.length===1?'':'s'}</h2>${!reviewDetailOpen&&list.length?`<button type="button" class="button secondary small" id="showReviewDetail">Mostrar solución seleccionada</button>`:''}</div>${list.map(a=>{const p=byId.get(a.qid),reason=!a.correct?'Error':a.hint?'Con pista':'Fuera de meta';return `<button type="button" class="review-row" data-id="${esc(a.qid)}" aria-current="${a.qid===selectedReviewId}"><span><strong>${esc(p?.sub||p?.tema||'Pregunta')}</strong><small>${esc(p?.tema||'')} · ${fmtTime(a.seconds)} / meta ${fmtTime(a.target)}</small></span><span>${reason}</span></button>`;}).join('')||`<div class="empty-state"><strong>Sin pendientes</strong>Cuando falles, uses pista o superes la meta, aparecerá aquí.</div>`}`;
    $$('.review-row').forEach(b=>b.onclick=()=>{selectedReviewId=b.dataset.id;reviewDetailOpen=true;renderReview();});$('#showReviewDetail')?.addEventListener('click',()=>{reviewDetailOpen=true;renderReview();});renderReviewDetail();$('#startReview').disabled=!list.length;
  }
  function renderReviewDetail(){if(!reviewDetailOpen)return;const root=$('#reviewDetail'),p=byId.get(selectedReviewId),a=reviewItems().find(x=>x.qid===selectedReviewId);if(!p||!a){root.innerHTML=`<div class="empty-state"><strong>Tu revisión está limpia</strong>Haz una práctica para detectar qué reforzar.</div>`;return;}root.innerHTML=`<button type="button" class="button secondary small" id="hideReviewDetail">Ocultar solución</button><article class="study-solution" style="margin-top:14px"><div class="question-meta"><span class="tag">${esc(p.tema)}</span><span class="tag">${stars(p.dif||1)}</span><span class="tag">${a.correct?'Correcta asistida o lenta':'Respuesta incorrecta'}</span></div>${problemBody(p,a,'study')}<details class="solution" open><summary>Cómo resolverlo</summary>${solutionHtml(p)}</details></article>`;$('#hideReviewDetail').onclick=()=>{reviewDetailOpen=false;renderReview();};}

  function exportProgress(){if(state.active)E.checkpoint(state.active);save();const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`trainermath-brenda-${new Date().toISOString().slice(0,10)}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('Respaldo exportado.');}
  async function importProgress(file){if(!file)return;try{const raw=JSON.parse(await file.text()),normalized=E.normalize(raw,bank);if(!confirm('Este respaldo reemplazará el progreso local actual, incluida cualquier sesión activa. ¿Continuar?'))return;if(normalized.active?.mode==='practice'){normalized.active.paused=true;normalized.active.runningSince=0;}state=normalized;readOnly=false;const saved=E.save(storage,state);if(!saved.ok){readOnly=true;showStorage(saved.error);}else{$('#storageAlert').hidden=true;$('#storageAlert').textContent='';}lastResult=null;selectedReviewId='';notify('Progreso importado correctamente.');showView(state.active?(state.active.mode==='exam'?'exam':'practice'):'home');}catch(err){showStorage('Archivo no válido. Elige un respaldo exportado por TrainerMath. Tu progreso se conserva.');notify('El archivo no es un respaldo válido.');}finally{$('#importProgress').value='';}}

  function bind(){
    const tips=[
      ['Encuentra el camino corto.','Antes de operar, identifica qué dato elimina alternativas. La velocidad empieza en el criterio.'],
      ['Completa la decena.','Para sumar 8 + 7, piensa 8 + 2 + 5 = 15. En Anzan, guarda el subtotal y sigue.'],
      ['Estima antes de calcular.','Si piden 19% de 300, el resultado estará cerca de 60 y será menor. Luego calcula 20% menos 1%: 57.'],
      ['Cambia de pregunta a tiempo.','Si te atoras en el simulacro, marca la pregunta y continúa. Regresa cuando hayas asegurado los casos que reconoces.'],
      ['Reconoce una diferencia de cuadrados.','Para 49 × 51, usa (50 − 1)(50 + 1) = 2500 − 1. Reconocer la forma ahorra operaciones.']
    ];
    let tipIndex=0;
    const nextTip=()=>{tipIndex=(tipIndex+1)%tips.length;$('#dailyTitle').textContent=tips[tipIndex][0];$('#dailyTip').textContent=tips[tipIndex][1];const mascot=$('#mascotTip');mascot.classList.remove('tip-bounce');requestAnimationFrame(()=>mascot.classList.add('tip-bounce'));};
    $('#mascotTip').addEventListener('click',nextTip);$('#nextTip').addEventListener('click',nextTip);
    $$('[data-nav]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();showView(b.dataset.nav);}));
    $$('[data-preset]').forEach(b=>b.onclick=()=>{prefs.practice.mode=b.dataset.preset;showView('practice');$$('input[name="practiceMode"]').forEach(i=>i.checked=i.value===prefs.practice.mode);updateConfig('practice');});
    $('#quickStart').onclick=()=>state.active?showView(state.active.mode==='exam'?'exam':'practice'):selectAndStart('practice',{count:10,mode:'variety'});
    $('#practiceSetup').addEventListener('submit',e=>{e.preventDefault();selectAndStart('practice');});$('#examSetup').addEventListener('submit',e=>{e.preventDefault();selectAndStart('exam');});
    $('#practiceTab').onclick=()=>renderPracticeSurface();$('#studyTab').onclick=showStudy;
    $('#startReview').onclick=()=>{prefs.practice.mode='review';selectAndStart('practice',{mode:'review',count:10});};
    $('#finishDialog').addEventListener('close',()=>{if($('#finishDialog').returnValue==='confirm')finishExam(false);});
    $('#exportProgress').onclick=exportProgress;$('#importProgressButton').onclick=()=>$('#importProgress').click();$('#importProgress').onchange=e=>importProgress(e.target.files?.[0]);
    document.addEventListener('keydown',e=>{
      if(e.defaultPrevented||e.ctrlKey||e.metaKey||e.altKey)return;const tag=e.target.tagName;if(['INPUT','SELECT','TEXTAREA'].includes(tag)||e.target.isContentEditable)return;
      if(e.key==='Escape'&&$('#finishDialog').open){$('#finishDialog').close('cancel');return;}
      if(!state.active||$('#finishDialog').open)return;const modeView=state.active.mode==='exam'?'exam':'practice',sessionEl=state.active.mode==='exam'?$('#examSession'):$('#practiceSession');if(currentView!==modeView||sessionEl.hidden)return;const idx=/^[1-4]$/.test(e.key)?+e.key-1:letters.indexOf(e.key.toUpperCase());
      if(idx>=0&&idx<4){e.preventDefault();state.active.mode==='exam'?answerExam(idx):answerPractice(idx);}
      if(state.active?.mode==='exam'&&e.key==='ArrowLeft'){e.preventDefault();goExam(-1);}else if(state.active?.mode==='exam'&&e.key==='ArrowRight'){e.preventDefault();goExam(1);}
    });
    document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.active?.mode==='practice'&&!state.active.paused&&!state.active.answers[E.qid(currentProblem())]){E.checkpoint(state.active);state.active.paused=true;state.active.runningSince=0;save();}else if(!document.hidden&&state.active?.mode==='practice'&&currentView==='practice')renderPracticeQuestion();});
    window.addEventListener('beforeunload',()=>{if(state.active?.mode==='practice'&&!state.active.paused)E.checkpoint(state.active);else if(state.active?.mode==='exam')E.checkpoint(state.active);save();});
  }

  function init(){
    if(!E){document.body.innerHTML='<p style="padding:24px">No se pudo iniciar TrainerMath.</p>';return;}
    anzan=window.TrainerAnzan?.init($('#view-anzan'));
    setupConfigs();bind();
    if(loaded.warning)showStorage(loaded.warning);
    if(!bank.length)showStorage('El banco de preguntas no está disponible. Vuelve a generar la aplicación.');
    if(state.active?.mode==='practice'&&!state.active.paused){state.active.paused=true;state.active.runningSince=0;save();}
    let entered=false;try{entered=storage.getItem('trainermath_brenda_entered')==='1';}catch(_){}
    const legacyHash=location.hash.match(/^#p\/(.+)$/);
    $('#enterApp').onclick=()=>{try{storage.setItem('trainermath_brenda_entered','1');}catch(_){}$('#accessGate').hidden=true;$('#appShell').hidden=false;const target=state.active?(state.active.mode==='exam'?'exam':'practice'):(legacyHash?'practice':'home');showView(target,false);if(legacyHash&&!state.active){showStudy();openStudy(legacyHash[1]);}};
    if(entered){$('#accessGate').hidden=true;$('#appShell').hidden=false;const hash=location.hash.replace('#','');const mapped={inicio:'home',home:'home',practice:'practice',exam:'exam',review:'review',anzan:'anzan'}[hash];showView(state.active?(state.active.mode==='exam'?'exam':'practice'):(legacyHash?'practice':(mapped||'home')),false);if(legacyHash&&!state.active){showStudy();openStudy(legacyHash[1]);}}
    renderHome();
  }
  init();
})();
