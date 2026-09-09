/* Supabase adapter. TrainerMath remains usable when the network or provider is unavailable. */
(function(root){
  'use strict';
  const CONFIG={
    url:'https://ldcczlrarmmvreokpbdq.supabase.co',
    publishableKey:'sb_publishable_imRx3FAMaLJktRYqG92sPQ_P6_8xFKn',
    syncFunction:'trainer-math-sync',coachFunction:'trainer-math-coach',sheetFunction:'trainer-math-sheet-sync',
    appVersion:'4.0.0',contentVersion:'prisma-2026-2-v1'
  };
  const QUEUE_KEY='trainermath_brenda_cloud_queue_v1';
  let client=null,storage=null,flushPromise=null;
  let current={state:'local',label:'En este dispositivo',detail:'El respaldo en la nube se conectará al entrar.',ai:false,sheet:false,pending:0,userId:''};
  const listeners=new Set();
  const emit=patch=>{current={...current,...patch};for(const listener of listeners)try{listener({...current});}catch(_){}};
  const clip=(value,max)=>String(value??'').trim().slice(0,max);
  const safeJson=value=>{try{return JSON.parse(value);}catch(_){return null;}};
  function getQueue(){try{const value=safeJson(storage?.getItem(QUEUE_KEY));return Array.isArray(value)?value.slice(-40):[];}catch(_){return [];}}
  function setQueue(queue){try{storage?.setItem(QUEUE_KEY,JSON.stringify(queue.slice(-40)));}catch(_){}emit({pending:queue.length});}
  function onStatus(listener){listeners.add(listener);listener({...current});return()=>listeners.delete(listener);}
  function status(){return {...current};}
  function loadSdk(){
    if(root.supabase?.createClient)return Promise.resolve(true);
    if(!root.document)return Promise.resolve(false);
    const existing=root.document.getElementById('trainerSupabaseSdk');
    if(existing)return new Promise(resolve=>{existing.addEventListener('load',()=>resolve(Boolean(root.supabase?.createClient)),{once:true});existing.addEventListener('error',()=>resolve(false),{once:true});});
    return new Promise(resolve=>{const script=root.document.createElement('script');script.id='trainerSupabaseSdk';script.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0/dist/umd/supabase.min.js';script.crossOrigin='anonymous';script.onload=()=>resolve(Boolean(root.supabase?.createClient));script.onerror=()=>resolve(false);root.document.head.append(script);});
  }
  function stripHtml(value){const div=root.document?.createElement('div');if(!div)return clip(value,900);div.innerHTML=String(value??'');return clip(div.textContent,900);}

  async function invoke(name,body){
    if(!client)throw new Error('cloud_unavailable');
    const {data,error}=await client.functions.invoke(name,{body});
    if(error)throw error;if(!data?.ok)throw new Error(data?.code||'remote_error');return data;
  }

  async function init(preferredStorage){
    storage=preferredStorage||root.localStorage;
    emit({state:'connecting',label:'Conectando…',detail:'Protegiendo el progreso de Brenda en Supabase.'});
    if(!await loadSdk()){emit({state:'local',label:'Modo local',detail:'No se pudo cargar la conexión; el entrenamiento sigue disponible.'});return status();}
    try{
      client=root.supabase.createClient(CONFIG.url,CONFIG.publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:false,storageKey:'trainermath_brenda_auth_v1'}});
      let {data:{session}}=await client.auth.getSession();
      if(!session){const result=await client.auth.signInAnonymously({options:{data:{display_name:'Brenda Sofía',application:'TrainerMath'}}});if(result.error)throw result.error;session=result.data.session;}
      if(!session?.user?.id)throw new Error('anonymous_session_missing');
      const bootstrap=await invoke(CONFIG.syncFunction,{action:'bootstrap',profile:{display_name:'Brenda Sofía',timezone:'America/Lima'},app_version:CONFIG.appVersion});
      emit({state:'connected',label:'Progreso protegido',detail:'Sincronización privada activa con Supabase.',ai:Boolean(bootstrap.ai_available),sheet:Boolean(bootstrap.sheet_available),userId:session.user.id,pending:getQueue().length});
      void flush();
    }catch(error){const code=clip(error?.message||error?.code||'cloud_unavailable',120);client=null;emit({state:'local',label:'Modo local',detail:'La nube no respondió; el progreso continúa seguro en este navegador.',errorCode:code,ai:false,sheet:false});}
    return status();
  }

  function sessionPayload(summary,ids,state,bank){
    const byId=new Map(bank.map(p=>[String(p.id??p.n),p]));
    const rows=(summary?.rows||[]).map(row=>{const p=byId.get(String(row.qid))||{};const saved=(state?.attempts||[]).find(a=>a.key===`${summary.id}:${row.qid}`)||row;return {
      client_attempt_key:clip(saved.key||`${summary.id}:${row.qid}`,140),question_id:clip(row.qid,80),area:clip(p.tema,90),unit_id:clip(p.curriculum?.item,40),unit_label:clip(p.curriculum?.label||p.sub,140),family:clip(p.family||row.qid,100),difficulty:Number(p.dif)||1,
      correct:Boolean(row.correct),seconds:Math.max(0,Number(row.seconds)||0),target_seconds:Math.max(1,Number(row.target||p.target)||90),assisted:Boolean(row.hint),confidence:clip(row.confidence,20),error_reason:clip(row.reason,20),skipped:row.choice==null,attempted_at:new Date(Number(summary.at)||Date.now()).toISOString()
    };});
    return {action:'complete_session',app_version:CONFIG.appVersion,content_version:CONFIG.contentVersion,session:{client_session_id:clip(summary.id,80),mode:summary.mode==='exam'?'exam':'practice',variant:clip(summary.variant||'variety',30),finished_at:new Date(Number(summary.at)||Date.now()).toISOString(),question_count:Number(summary.count)||rows.length,correct_count:Number(summary.correct)||0,seconds:Math.max(0,Number(summary.seconds)||0),question_ids:(ids||[]).map(x=>clip(x,80)).slice(0,50)},attempts:rows};
  }

  function queueSession(summary,ids,state,bank){
    if(!summary?.id)return;
    const queue=getQueue(),payload=sessionPayload(summary,ids,state,bank);
    if(!queue.some(item=>item?.session?.client_session_id===payload.session.client_session_id))queue.push(payload);
    setQueue(queue);void flush();
  }

  async function flush(){
    if(flushPromise)return flushPromise;
    flushPromise=(async()=>{
      if(!client||current.state!=='connected')return status();
      const queue=getQueue(),pending=[];
      for(const payload of queue){
        try{
          const result=await invoke(CONFIG.syncFunction,payload);
          emit({state:'connected',label:'Progreso protegido',detail:result.sheet_queued?'Sesión guardada; resumen preparado para Google Sheets.':'Sesión guardada en Supabase.',ai:Boolean(result.ai_available),sheet:Boolean(result.sheet_available)});
          if(result.sheet_available){try{await invoke(CONFIG.sheetFunction,{limit:10});emit({sheet:true,detail:'Sesión guardada en Supabase y reflejada en Google Sheets.'});}catch(_){emit({detail:'Sesión guardada; Google Sheets queda en reintento seguro.'});}}
        }catch(_){pending.push(payload);}
      }
      setQueue(pending);
      if(pending.length)emit({state:'queued',label:`${pending.length} pendiente${pending.length===1?'':'s'}`,detail:'Se enviará automáticamente cuando vuelva la conexión.'});
      return status();
    })().finally(()=>{flushPromise=null;});
    return flushPromise;
  }

  function localCoach(tip){return {ok:true,source:'catalog',ai_available:false,reply:{title:tip?.title||'Encuentra el camino corto',message:[tip?.condition,tip?.rule,tip?.example].filter(Boolean).join(' '),action:tip?.trap?`Control: ${tip.trap}`:'Aplica el método en el siguiente caso y verifica el resultado.',confidence:'rule_based'},next_drill:null};}
  async function askCoach(input){
    const tip=input?.tip||root.TrainerAdaptive?.catalogTip(0),fallback=localCoach(tip);
    if(!client||current.state!=='connected')return fallback;
    const p=input?.problem||{},a=input?.attempt||{};
    const body={intent:['explain','strategy','summary'].includes(input?.intent)?input.intent:'strategy',session_id:clip(input?.sessionId,80),user_question:clip(input?.userQuestion,240),exercise:{id:clip(p.id??p.n??'general',80),area:clip(p.tema,90),unit_id:clip(p.curriculum?.item,40),unit:clip(p.curriculum?.label||p.sub,140),question:stripHtml(p.enun||input?.userQuestion||'Consejo general de cálculo rápido'),correct_answer:a.answered?clip(p.opts?.[p.ans],200):'',method:a.answered?clip(p.idea,700):'',trap:a.answered?clip(p.trap,400):''},attempt:{answered:Boolean(a.answered),correct:Boolean(a.correct),within_target:Boolean(a.withinTarget),seconds:Number(a.seconds)||0,target_seconds:Number(a.target||p.target)||0,error_reason:clip(a.reason,20),confidence:clip(a.confidence,20)},curated_tip:tip?{id:tip.id,title:tip.title,condition:tip.condition,rule:tip.rule,example:tip.example,trap:tip.trap}:null,app_version:CONFIG.appVersion};
    try{const result=await invoke(CONFIG.coachFunction,body);emit({ai:Boolean(result.ai_available)});return result;}catch(_){return fallback;}
  }

  root.TrainerBackend={CONFIG,init,onStatus,status,queueSession,flush,askCoach,localCoach};
})(typeof globalThis!=='undefined'?globalThis:this);
