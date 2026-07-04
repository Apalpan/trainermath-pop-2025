# -*- coding: utf-8 -*-
"""TrainerMath · POP 2025 — generador del single-file index.html"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from data_p1 import PROBLEMS_1
from data_p2 import PROBLEMS_2
from data_p3 import PROBLEMS_3
from data_p4 import PROBLEMS_4
from figs import FIGS

PROBLEMS = PROBLEMS_1 + PROBLEMS_2 + PROBLEMS_3 + PROBLEMS_4
assert [p["n"] for p in PROBLEMS] == list(range(1, 63)), "faltan o sobran problemas"

for p in PROBLEMS:
    p["fig"] = FIGS.get(p.get("fig"), "") if p.get("fig") else ""
    p.setdefault("nota", "")
    p.setdefault("dup", 0)

TEMAS = ["Aritmética", "Álgebra", "Geometría", "Probabilidad", "Estadística"]
DATA = json.dumps(PROBLEMS, ensure_ascii=False).replace("</", "<\\/")

CSS = r"""
:root{
  --bg:#f5f6fb; --s1:#ffffff; --s2:#eef0f8; --s3:#e3e7f4;
  --line:rgba(28,36,80,.10); --line2:rgba(28,36,80,.18);
  --ink:#171c33; --ink2:#454d70; --ink3:#7c83a6;
  --acc:#00805d; --accL:#00a876; --acc2:rgba(0,150,110,.10); --acc3:rgba(0,150,110,.30);
  --bad:#cf3453; --bad2:rgba(207,52,83,.10);
  --ease:cubic-bezier(.32,.72,0,1); --fast:150ms; --med:240ms;
  --r:14px; --rs:10px;
  --sh:0 1px 2px rgba(23,28,51,.05), 0 8px 24px -12px rgba(23,28,51,.12);
}
@supports (color:oklch(0% 0 0)){
  :root{ --bg:oklch(.972 .008 275); --s2:oklch(.945 .012 275); --s3:oklch(.915 .016 275);
         --acc:oklch(.55 .12 165); }
}
*{box-sizing:border-box; margin:0}
html{scrollbar-gutter:stable; color-scheme:light}
body{
  background:var(--bg); color:var(--ink);
  font:400 16px/1.62 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  -webkit-font-smoothing:antialiased; min-height:100dvh;
  background-image:radial-gradient(1100px 500px at 85% -10%, rgba(0,160,120,.07), transparent 60%),
                   radial-gradient(900px 420px at -10% 0%, rgba(90,110,240,.06), transparent 55%);
  background-attachment:fixed;
}
::selection{background:var(--acc3)}
h1,h2,h3,.dsp{font-family:"Space Grotesk",Inter,system-ui,sans-serif; letter-spacing:-.015em; text-wrap:balance}
button{font:inherit; color:inherit; background:none; border:0; cursor:pointer}
:focus-visible{outline:none; box-shadow:0 0 0 2px var(--bg),0 0 0 4px var(--acc); border-radius:8px}
.num{font-variant-numeric:tabular-nums}

/* ── header ─────────────────────────────────────── */
.top{position:sticky; top:0; z-index:40; backdrop-filter:blur(14px);
  background:color-mix(in srgb, var(--bg) 82%, transparent);
  border-bottom:1px solid var(--line)}
.top-in{max-width:1180px; margin:0 auto; padding:14px 22px; display:flex; align-items:center; gap:18px}
.brand{display:flex; flex-direction:column; gap:2px; min-width:0}
.brand b{font-family:"Space Grotesk"; font-size:1.06rem; letter-spacing:-.01em; white-space:nowrap}
.brand b i{color:var(--acc); font-style:normal}
.brand small{color:var(--ink3); font-size:.74rem; letter-spacing:.06em; text-transform:uppercase; white-space:nowrap}
.tstats{margin-left:auto; display:flex; align-items:center; gap:20px}
.tstat{display:flex; flex-direction:column; align-items:flex-end; line-height:1.25}
.tstat b{font-size:1.02rem; font-variant-numeric:tabular-nums}
.tstat span{font-size:.7rem; color:var(--ink3); text-transform:uppercase; letter-spacing:.08em}
.ring{width:46px; height:46px; flex:none}
.ring circle{fill:none; stroke-width:4}
.ring .bgc{stroke:var(--s3)}
.ring .fgc{stroke:var(--acc); stroke-linecap:round; transform:rotate(-90deg); transform-origin:center;
  transition:stroke-dashoffset .6s var(--ease)}
.ring text{fill:var(--ink); font-size:12.5px; font-weight:600; font-variant-numeric:tabular-nums}

/* ── hero + filtros ─────────────────────────────── */
.wrap{max-width:1180px; margin:0 auto; padding:30px 22px 90px}
.hero{display:flex; align-items:flex-end; justify-content:space-between; gap:24px; margin:14px 0 26px; flex-wrap:wrap}
.hero h1{font-size:clamp(1.5rem,3.4vw,2.2rem); line-height:1.14}
.hero p{color:var(--ink2); max-width:56ch; margin-top:8px; text-wrap:pretty}
.hero .cta{display:flex; gap:12px; flex-wrap:wrap}
.btn{display:inline-flex; align-items:center; gap:9px; padding:11px 20px; border-radius:12px;
  background:var(--s1); border:1px solid var(--line2); font-weight:600; font-size:.95rem;
  box-shadow:var(--sh); transition:transform var(--fast) var(--ease), background var(--fast) linear}
.btn:hover{background:var(--s2); transform:translateY(-1px)}
.btn:active{transform:scale(.97)}
.btn.pri{background:var(--acc); color:#fff; border-color:transparent}
.btn.pri:hover{background:var(--accL)}
.chips{display:flex; gap:8px; flex-wrap:wrap; margin:0 0 12px}
.chip{padding:7px 15px; border-radius:99px; border:1px solid var(--line2); color:var(--ink2);
  font-size:.86rem; font-weight:500; background:var(--s1); transition:all var(--fast) linear}
.chip:hover{color:var(--ink); border-color:var(--ink3)}
.chip[aria-pressed="true"]{background:var(--acc); border-color:var(--acc); color:#fff; font-weight:600}
.chip .ct{opacity:.65; font-size:.78em; margin-left:5px; font-variant-numeric:tabular-nums}
.subchips .chip{padding:5px 12px; font-size:.8rem}

/* ── grid de problemas ──────────────────────────── */
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(158px,1fr)); gap:12px; margin-top:18px}
.card{position:relative; text-align:left; background:var(--s1); border:1px solid var(--line);
  border-radius:var(--r); padding:15px 15px 13px; display:flex; flex-direction:column; gap:7px;
  box-shadow:var(--sh);
  transition:transform var(--fast) var(--ease), border-color var(--fast) linear, background var(--fast) linear}
.card:hover{transform:translateY(-2px); border-color:var(--acc3)}
.card:active{transform:scale(.98)}
.card .cn{font-family:"Space Grotesk"; font-size:1.5rem; font-weight:600; line-height:1;
  font-variant-numeric:tabular-nums}
.card .cs{font-size:.78rem; color:var(--ink2); line-height:1.35; min-height:2.1em}
.card .cf{display:flex; align-items:center; gap:7px; margin-top:auto}
.card .tag{font-size:.68rem; letter-spacing:.05em; text-transform:uppercase; color:var(--ink3)}
.card .st{margin-left:auto; width:20px; height:20px; border-radius:99px; display:grid; place-items:center;
  font-size:.72rem; font-weight:800; color:#fff}
.card .st.ok{background:var(--acc)} .card .st.bad{background:var(--bad)}
.card .st.pend{background:none; border:1.5px dashed var(--line2)}
.difd{display:inline-flex; gap:3px}
.difd i{width:5px; height:5px; border-radius:99px; background:var(--s3)}
.difd i.on{background:var(--ink3)}
.empty{grid-column:1/-1; text-align:center; color:var(--ink3); padding:70px 0; border:1px dashed var(--line2); border-radius:var(--r)}

/* ── overlay de problema ────────────────────────── */
.ov{position:fixed; inset:0; z-index:60; display:none; overflow-y:auto; overscroll-behavior:contain;
  background:color-mix(in srgb, var(--bg) 55%, white)}
.ov.on{display:block}
.ov-in{max-width:880px; margin:0 auto; padding:26px 22px 120px}
@media (prefers-reduced-motion:no-preference){
  .ov.on .panel{animation:up var(--med) var(--ease)}
  @keyframes up{from{opacity:0; transform:translateY(14px)}}
}
.ovbar{display:flex; align-items:center; gap:10px; margin-bottom:16px; position:sticky; top:0;
  padding:10px 0; background:color-mix(in srgb, var(--bg) 75%, white); z-index:5}
.ovbar .pos{color:var(--ink3); font-size:.86rem; font-variant-numeric:tabular-nums}
.icob{width:38px; height:38px; border-radius:11px; display:grid; place-items:center;
  background:var(--s1); border:1px solid var(--line2); font-size:1rem;
  transition:transform var(--fast) var(--ease), background var(--fast) linear}
.icob:hover{background:var(--s2)} .icob:active{transform:scale(.94)}
.ovbar .sp{flex:1}
.timer{font-variant-numeric:tabular-nums; color:var(--acc); font-weight:600; font-size:.95rem;
  padding:6px 13px; border:1px solid var(--acc3); border-radius:99px; background:var(--acc2)}
.panel{background:var(--s1); border:1px solid var(--line); border-radius:20px;
  padding:clamp(20px,4vw,34px); box-shadow:var(--sh)}
.phead{display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:14px}
.pnum{font-family:"Space Grotesk"; font-weight:700; font-size:1.05rem; color:var(--acc);
  background:var(--acc2); border:1px solid var(--acc3); padding:4px 13px; border-radius:99px;
  font-variant-numeric:tabular-nums}
.ptag{font-size:.8rem; color:var(--ink2); border:1px solid var(--line2); padding:4px 12px; border-radius:99px}
.psub{font-size:.8rem; color:var(--ink3)}
.dupn{font-size:.8rem; color:var(--ink3); font-style:italic}
.enun{font-size:1.06rem; line-height:1.75; text-wrap:pretty}
.fig{margin:20px auto 6px; max-width:560px}
.fig svg{width:100%; height:auto; display:block}
.fig text{font-family:Inter,system-ui,sans-serif; font-size:13.5px}

/* figuras */
.ln{stroke:var(--ink2); stroke-width:1.6; fill:none; stroke-linecap:round; stroke-linejoin:round}
.lnB{stroke:var(--ink3); stroke-width:1.5; fill:none; stroke-linecap:round}
.lnA{stroke:var(--acc); stroke-width:1.7; fill:none; stroke-linecap:round}
.lngrid{stroke:var(--line); stroke-width:.8}
.lndash{stroke:var(--ink3); stroke-width:1.3; stroke-dasharray:4 5; fill:none}
.lndashA{stroke:var(--acc); stroke-width:1.3; stroke-dasharray:4 5; fill:none; opacity:.8}
.ar{stroke:var(--ink3); stroke-width:1.4; fill:none}
.arA{stroke:var(--acc); stroke-width:1.6; fill:none}
.arX{stroke:var(--acc); stroke-width:2.2; fill:none}
.lb{fill:var(--ink); font-weight:500}
.lbdim{fill:var(--ink3); font-size:12.5px}
.lbB{fill:var(--ink2)}
.lbA{fill:var(--acc); font-weight:600}
.lbX{fill:var(--acc); font-weight:700}
.fillA{fill:var(--acc2); stroke:none}
.fillB{fill:rgba(23,28,51,.06); stroke:none}
.fillCut{fill:var(--s1); stroke:none}
.cellA{fill:var(--acc3)}
.ra{fill:none; stroke:var(--ink3); stroke-width:1.2}
.dotO{fill:var(--s1)} .dotC{fill:currentColor}
.bar{fill:var(--acc); opacity:.55}
.bar:hover{opacity:.8}
.dtab{margin:18px auto 4px; border-collapse:collapse; font-size:.95rem; min-width:260px}
.dtab caption{color:var(--ink3); font-size:.8rem; padding-bottom:8px}
.dtab th,.dtab td{border:1px solid var(--line2); padding:7px 18px; text-align:left}
.dtab td{text-align:right; font-variant-numeric:tabular-nums}
.dtab .tot th,.dtab .tot td{color:var(--acc); font-weight:600}

/* opciones */
.opts{display:grid; grid-template-columns:1fr 1fr; gap:11px; margin:24px 0 8px}
@media (max-width:640px){.opts{grid-template-columns:1fr}}
.opt{display:flex; align-items:center; gap:13px; text-align:left; padding:13px 16px;
  background:var(--s2); border:1px solid var(--line2); border-radius:var(--r); font-size:1rem;
  transition:transform var(--fast) var(--ease), border-color var(--fast) linear, background var(--fast) linear}
.opt:hover{border-color:var(--ink3); transform:translateY(-1px)}
.opt:active{transform:scale(.98)}
.opt .L{flex:none; width:30px; height:30px; border-radius:9px; display:grid; place-items:center;
  background:var(--s3); font-weight:700; font-size:.86rem; transition:background var(--fast) linear}
.opt.sel-ok{border-color:var(--acc); background:var(--acc2)}
.opt.sel-ok .L{background:var(--acc); color:#fff}
.opt.sel-bad{border-color:var(--bad); background:var(--bad2)}
.opt.sel-bad .L{background:var(--bad); color:#fff}
.opt.reveal{border-color:var(--acc3)}
.opt.reveal .L{box-shadow:inset 0 0 0 2px var(--acc)}
.opt:disabled{cursor:default}
.opt:disabled:hover{transform:none}
.verdict{display:none; align-items:center; gap:10px; margin:14px 2px 0; font-weight:600}
.verdict.on{display:flex}
.verdict.good{color:var(--acc)} .verdict.bad{color:var(--bad)}
.verdict small{color:var(--ink3); font-weight:400}

/* resolución */
.sol{margin-top:30px; border-top:1px solid var(--line); padding-top:24px}
.sol>h3{font-size:1.02rem; margin-bottom:4px; display:flex; align-items:center; gap:10px}
.sol>h3 .sdots{display:inline-flex; gap:4px; margin-left:auto}
.sdots i{width:7px; height:7px; border-radius:99px; background:var(--s3); transition:background var(--fast) linear}
.sdots i.on{background:var(--acc)}
.lock{color:var(--ink3); font-size:.9rem; padding:14px 0}
.steps{display:flex; flex-direction:column; gap:14px; margin-top:14px}
.step{display:none; background:var(--s2); border:1px solid var(--line); border-radius:var(--r);
  padding:16px 19px}
.step.on{display:block}
@media (prefers-reduced-motion:no-preference){
  .step.on{transition:opacity var(--med) var(--ease), transform var(--med) var(--ease)}
  @starting-style{.step.on{opacity:0; transform:translateY(10px)}}
}
.step h4{font-size:.94rem; display:flex; gap:11px; align-items:baseline; margin-bottom:7px}
.step h4 .k{flex:none; color:var(--acc); font-family:"Space Grotesk"; font-variant-numeric:tabular-nums;
  font-size:.82rem; letter-spacing:.04em}
.step p{color:var(--ink2); font-size:.95rem; text-wrap:pretty}
.step p+p{margin-top:7px}
.step b{color:var(--ink)}
.sbtns{display:flex; gap:11px; margin-top:18px; flex-wrap:wrap}
.answer{display:none; margin-top:16px; padding:15px 19px; border-radius:var(--r);
  background:var(--acc2); border:1px solid var(--acc3); font-size:1.02rem}
.answer.on{display:block}
.answer b{color:var(--acc)}
.idea{display:none; margin-top:12px; padding:14px 19px; border-radius:var(--r);
  background:var(--s2); border:1px dashed var(--acc3); font-size:.92rem; color:var(--ink2)}
.idea.on{display:block}
.idea b{color:var(--acc); font-size:.78rem; letter-spacing:.09em; text-transform:uppercase; display:block; margin-bottom:4px}
.notare{display:none; margin-top:12px; font-size:.83rem; color:var(--ink3); padding:0 4px}
.notare.on{display:block}
.pnav{display:flex; gap:11px; margin-top:26px}
.pnav .btn{flex:1; justify-content:center}

/* matemática */
.mv{font-style:italic; padding:0 .04em}
.fr{display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center;
  margin:0 .16em; line-height:1.2; font-size:.94em}
.fr .fn{border-bottom:1.4px solid currentColor; padding:0 .3em .06em}
.fr .fd{padding:.06em .3em 0}
.fr .fr{font-size:.9em; margin:.1em .1em}
.sqrt{display:inline-flex; align-items:stretch; margin:0 .1em}
.sqrt .rad{font-size:1.12em; line-height:1.25; align-self:flex-end}
.sqrt .vin{border-top:1.5px solid currentColor; padding:.1em .3em 0 .12em}
.sqrt .ridx{font-size:.6em; align-self:flex-start; margin:-.2em -.3em 0 0; z-index:1}
.disp{margin:.8rem 0 .2rem; padding:.78rem 1.05rem; background:color-mix(in srgb, var(--bg) 55%, var(--s1));
  border-left:2px solid var(--acc3); border-radius:11px; font-size:1.05rem; line-height:2;
  overflow-x:auto; font-variant-numeric:tabular-nums}
.disp+.disp{margin-top:.5rem}
.enun .disp{background:color-mix(in srgb, var(--bg) 45%, var(--s1))}
.hlm{color:var(--acc); font-weight:650}
.mrow{white-space:nowrap}
sup,sub{line-height:0}

/* ── simulacro ──────────────────────────────────── */
dialog{border:0; border-radius:20px; background:var(--s1); color:var(--ink); padding:0;
  max-width:430px; width:calc(100vw - 40px); box-shadow:0 30px 80px rgba(23,28,51,.25)}
dialog::backdrop{background:rgba(23,28,51,.35); backdrop-filter:blur(4px)}
.dlg{padding:28px}
.dlg h3{margin-bottom:6px}
.dlg p{color:var(--ink2); font-size:.92rem; margin-bottom:18px}
.dlg .row{display:flex; gap:8px; flex-wrap:wrap; margin:8px 0 18px}
.dlg label{display:block; font-size:.78rem; color:var(--ink3); text-transform:uppercase; letter-spacing:.07em; margin-bottom:7px}
.sumline{display:flex; align-items:center; gap:12px; padding:9px 4px; border-bottom:1px solid var(--line); font-size:.94rem}
.sumline:last-child{border:0}
.sumline .sn{width:34px; color:var(--ink3); font-variant-numeric:tabular-nums}
.sumline .si{margin-left:auto; font-weight:700}
.sumline .si.ok{color:var(--acc)} .sumline .si.bad{color:var(--bad)}
.bigscore{font-family:"Space Grotesk"; font-size:2.6rem; font-weight:700; line-height:1;
  color:var(--acc); margin:10px 0 2px; font-variant-numeric:tabular-nums}
.sumlist{max-height:300px; overflow-y:auto; margin-top:14px}

footer{margin-top:60px; text-align:center; color:var(--ink3); font-size:.82rem}
footer b{color:var(--ink2)}
@media (max-width:720px){
  .tstats{gap:12px} .tstat span{display:none}
  .top-in{padding:12px 16px} .wrap{padding:22px 16px 80px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(128px,1fr)); gap:9px}
  .enun{font-size:1rem}
}
@media (prefers-reduced-motion:reduce){
  *{transition:none !important; animation:none !important}
}
"""

JS = r"""
const P = __DATA__;
const TEMAS = __TEMAS__;
const LS = 'tm_pop2025_v1';
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
let st = {ans:{}, seen:{}};
try{ st = Object.assign(st, JSON.parse(localStorage.getItem(LS)||'{}')); }catch(e){}
if(!st.ans || typeof st.ans!=='object') st.ans={};
if(!st.seen || typeof st.seen!=='object') st.seen={};
const save = () => localStorage.setItem(LS, JSON.stringify(st));

let fTema='Todos', fEstado='Todos';
let order = P.map(p=>p.n);
let cur = null;               // problema abierto
let stepIdx = 0;
let simu = null;              // {list, i, t0, res:[], timerId}

/* ── stats ── */
function stats(){
  const ns = Object.keys(st.ans);
  const ok = ns.filter(n=>st.ans[n].ok).length;
  return {tot:P.length, done:ns.length, ok, acc: ns.length? Math.round(ok/ns.length*100):0};
}
function paintStats(){
  const s = stats();
  $('#stDone').textContent = s.done+'/'+s.tot;
  $('#stOk').textContent = s.ok;
  $('#stAcc').textContent = s.acc+'%';
  const C = 2*Math.PI*19;
  $('#ringFg').style.strokeDasharray = C;
  $('#ringFg').style.strokeDashoffset = C*(1 - s.done/s.tot);
  $('#ringTx').textContent = Math.round(s.done/s.tot*100)+'%';
  $('#ctaGo').textContent = s.done ? 'Continuar' : 'Empezar por el problema 1';
}

/* ── filtros + grid ── */
function match(p){
  if(fTema!=='Todos' && p.tema!==fTema) return false;
  const a = st.ans[p.n];
  if(fEstado==='Pendientes') return !a;
  if(fEstado==='Correctos') return a && a.ok;
  if(fEstado==='Fallados') return a && !a.ok;
  return true;
}
function paintChips(){
  const cnt = t => P.filter(p=>t==='Todos'||p.tema===t).length;
  $('#chips').innerHTML = ['Todos',...TEMAS].map(t=>
    `<button class="chip" aria-pressed="${t===fTema}" data-t="${t}">${t}<span class="ct">${cnt(t)}</span></button>`).join('');
  $$('#chips .chip').forEach(c=>c.onclick=()=>{fTema=c.dataset.t; paintChips(); paintGrid();});
  const est=['Todos','Pendientes','Correctos','Fallados'];
  $('#subchips').innerHTML = est.map(e=>
    `<button class="chip" aria-pressed="${e===fEstado}" data-e="${e}">${e}</button>`).join('');
  $$('#subchips .chip').forEach(c=>c.onclick=()=>{fEstado=c.dataset.e; paintChips(); paintGrid();});
}
function paintGrid(){
  const list = P.filter(match);
  order = list.map(p=>p.n);
  $('#grid').innerHTML = list.length ? list.map(p=>{
    const a = st.ans[p.n];
    const stc = a ? (a.ok?'ok':'bad') : 'pend';
    const sts = a ? (a.ok?'&#10003;':'&#10007;') : '';
    const dots = [1,2,3].map(i=>`<i class="${i<=p.dif?'on':''}"></i>`).join('');
    return `<button class="card" data-n="${p.n}" aria-label="Problema ${p.n}: ${p.sub}">
      <span class="cn num">${String(p.n).padStart(2,'0')}</span>
      <span class="cs">${p.sub}</span>
      <span class="cf"><span class="tag">${p.tema.slice(0,4)}</span><span class="difd">${dots}</span>
      <span class="st ${stc}">${sts}</span></span></button>`;
  }).join('') : `<div class="empty">No hay problemas con este filtro. Cambia el tema o el estado.</div>`;
  $$('#grid .card').forEach(c=>c.onclick=()=>open(+c.dataset.n));
}

/* ── overlay de problema ── */
function open(n, fromHash){
  cur = P.find(p=>p.n===n); stepIdx = 0;
  if(!fromHash && !simu) history.replaceState(null,'','#p/'+n);
  const inSim = !!simu;
  const a = st.ans[n];
  const oi = order.indexOf(n);
  const pos = inSim ? `Pregunta ${simu.i+1} / ${simu.list.length}`
                    : (oi>=0 ? `${oi+1} / ${order.length} en este filtro` : `P${n} · fuera del filtro actual`);
  $('#ovPos').textContent = pos;
  $('#ovTimer').style.display = inSim ? '' : 'none';
  $('#pHead').innerHTML = `<span class="pnum">P${n}</span>
    <span class="ptag">${cur.tema}</span><span class="psub">${cur.sub}</span>
    ${cur.dup?`<span class="dupn">&#8646; repetido del P${cur.dup}</span>`:''}`;
  $('#pEnun').innerHTML = cur.enun;
  $('#pFig').innerHTML = cur.fig || '';
  $('#pFig').style.display = cur.fig ? '' : 'none';
  const L = 'ABCD';
  $('#pOpts').innerHTML = cur.opts.map((o,i)=>
    `<button class="opt" data-i="${i}"><span class="L">${L[i]}</span><span>${o}</span></button>`).join('');
  $$('#pOpts .opt').forEach(b=>b.onclick=()=>pick(+b.dataset.i));
  $('#pVerdict').className = 'verdict';
  // resolución
  $('#pSteps').innerHTML = cur.steps.map((s,i)=>
    `<div class="step" data-i="${i}"><h4><span class="k">PASO ${i+1}</span><span>${s.t}</span></h4>${s.d}</div>`).join('');
  $('#sdots').innerHTML = cur.steps.map((_,i)=>`<i data-i="${i}"></i>`).join('');
  $('#pAnswer').innerHTML = `Respuesta: <b>${L[cur.ans]}</b> &nbsp;&mdash;&nbsp; <span>${cur.opts[cur.ans]}</span>`;
  $('#pAnswer').className = 'answer';
  $('#pIdea').innerHTML = `<b>Idea clave</b>${cur.idea}`;
  $('#pIdea').className = 'idea';
  $('#pNota').innerHTML = cur.nota ? '&#9998; '+cur.nota : '';
  $('#pNota').className = 'notare'+(cur.nota?' on':'');
  $('#solZone').style.display = inSim ? 'none' : '';
  $('#solLock').style.display = 'none';
  $('#btnStep').textContent = 'Resolver paso a paso';
  $('#btnAll').style.display = '';
  if(a && !inSim && Number.isInteger(a.pick)) showPick(a.pick, false);
  const noNav = inSim || oi<0;
  $('#ovPrev').style.display = noNav?'none':'';
  $('#ovNext').style.display = noNav?'none':'';
  $('#pnavRow').style.display = noNav?'none':'';
  $('#ov').classList.add('on');
  document.body.style.overflow='hidden';
  $('#ov').scrollTop = 0;
}
function close(){
  $('#ov').classList.remove('on');
  document.body.style.overflow='';
  if(!simu) history.replaceState(null,'','#');
  cur=null; paintGrid(); paintStats();
}
function showPick(i, animate){
  const bs = $$('#pOpts .opt');
  if(!bs[i]) return;
  bs.forEach(b=>{b.disabled=true;});
  const good = i===cur.ans;
  bs[i].classList.add(good?'sel-ok':'sel-bad');
  if(!good) bs[cur.ans].classList.add('reveal');
  const v = $('#pVerdict');
  v.className = 'verdict on '+(good?'good':'bad');
  v.innerHTML = good ? '&#10003; ¡Correcto! <small>Revisa igual la resolución para fijar el método.</small>'
    : `&#10007; La correcta es ${'ABCD'[cur.ans]}. <small>Mira la resolución paso a paso y entiende dónde estuvo el error.</small>`;
}
function pick(i){
  if(!cur) return;
  if(!st.ans[cur.n]){ st.ans[cur.n] = {pick:i, ok: i===cur.ans}; save(); paintStats(); }
  if(simu){
    simu.res.push({n:cur.n, ok:i===cur.ans, pick:i});
    showPick(i,true);
    setTimeout(nextSim, i===cur.ans? 650: 1400);
  } else showPick(i,true);
}

/* pasos */
function reveal(k){
  const steps = $$('#pSteps .step');
  steps.forEach((s,i)=>s.classList.toggle('on', i<k));
  $$('#sdots i').forEach((d,i)=>d.classList.toggle('on', i<k));
  const done = k>=steps.length;
  $('#btnStep').textContent = k===0?'Resolver paso a paso':(done?'Resolución completa':'Siguiente paso');
  $('#btnStep').style.display = done?'none':'';
  $('#btnAll').style.display = done?'none':'';
  $('#pAnswer').classList.toggle('on', done);
  $('#pIdea').classList.toggle('on', done);
  if(done){ st.seen[cur.n]=1; save(); }
  if(k>0 && !done){
    const el = steps[k-1];
    requestAnimationFrame(()=>el.scrollIntoView({block:'nearest', behavior:'smooth'}));
  }
}
function nextStep(){ if(!cur) return; stepIdx=Math.min(stepIdx+1, cur.steps.length); reveal(stepIdx); }
function allSteps(){ if(!cur) return; stepIdx=cur.steps.length; reveal(stepIdx); }

/* navegación */
function nav(d){
  if(!cur||simu) return;
  const i = order.indexOf(cur.n);
  if(i<0) return;
  const j = i+d;
  if(j<0||j>=order.length) return;
  open(order[j]);
}

/* ── simulacro ── */
function startSim(tema, cant){
  let pool = P.filter(p=>tema==='Todos'||p.tema===tema).map(p=>p.n);
  for(let i=pool.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1)); [pool[i],pool[j]]=[pool[j],pool[i]];}
  pool = pool.slice(0, Math.min(cant, pool.length));
  simu = {list:pool, i:0, t0:Date.now(), res:[]};
  $('#dlgSim').close();
  tick(); simu.timerId = setInterval(tick, 1000);
  open(pool[0]);
}
function tick(){
  if(!simu) return;
  const s = Math.floor((Date.now()-simu.t0)/1000);
  $('#ovTimer').textContent = String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
}
function nextSim(){
  if(!simu) return;
  simu.i++;
  if(simu.i < simu.list.length){ open(simu.list[simu.i]); return; }
  clearInterval(simu.timerId);
  const secs = Math.floor((Date.now()-simu.t0)/1000);
  const ok = simu.res.filter(r=>r.ok).length;
  $('#sumScore').textContent = ok+' / '+simu.res.length;
  $('#sumTime').textContent = 'Tiempo: '+String(Math.floor(secs/60)).padStart(2,'0')+':'+String(secs%60).padStart(2,'0')
      +' · '+(simu.res.length?Math.round(secs/simu.res.length):0)+' s por pregunta';
  $('#sumList').innerHTML = simu.res.map(r=>{
    const p=P.find(x=>x.n===r.n);
    return `<div class="sumline"><span class="sn num">P${r.n}</span><span>${p.sub}</span>
      <button class="chip" data-n="${r.n}" style="padding:3px 10px;font-size:.75rem">revisar</button>
      <span class="si ${r.ok?'ok':'bad'}">${r.ok?'&#10003;':'&#10007;'}</span></div>`;
  }).join('');
  const done = simu; simu=null;
  close();
  $('#dlgSum').showModal();
  $$('#sumList .chip').forEach(b=>b.onclick=()=>{ $('#dlgSum').close(); open(+b.dataset.n); });
}

/* ── eventos globales ── */
document.addEventListener('keydown', e=>{
  if($('#dlgSim').open || $('#dlgSum').open) return;
  if(!cur){ return; }
  if(e.ctrlKey || e.metaKey || e.altKey) return;
  if(e.key==='Escape'){ if(!simu) close(); return; }
  if(e.key==='ArrowRight'){ nav(1); return; }
  if(e.key==='ArrowLeft'){ nav(-1); return; }
  if(e.key===' '||e.key==='Enter'){
    if(document.activeElement && document.activeElement.closest('button')) return;
    if(!simu && $('#pOpts .opt:disabled')){ e.preventDefault(); nextStep(); } return;
  }
  const k = e.key.toUpperCase();
  const idx = 'ABCD'.indexOf(k)>=0 ? 'ABCD'.indexOf(k) : ('1234'.indexOf(e.key)>=0?'1234'.indexOf(e.key):-1);
  if(idx>=0 && !$('#pOpts .opt:disabled')) pick(idx);
});
$('#ovClose').onclick = ()=>{ if(simu){ if(confirm('¿Abandonar el simulacro?')){clearInterval(simu.timerId); simu=null; close();} } else close(); };
$('#ovPrev').onclick = ()=>nav(-1);
$('#ovNext').onclick = ()=>nav(1);
$('#btnStep').onclick = nextStep;
$('#btnAll').onclick = allSteps;
$('#ctaGo').onclick = ()=>{
  const pend = P.find(p=>!st.ans[p.n]);
  open(pend?pend.n:1);
};
$('#ctaSim').onclick = ()=>{ paintSimDlg(); $('#dlgSim').showModal(); };
$('#stReset').onclick = ()=>{ if(confirm('¿Borrar todo tu progreso?')){ st={ans:{},seen:{}}; save(); paintStats(); paintGrid(); } };

function paintSimDlg(){
  $('#simTemas').innerHTML = ['Todos',...TEMAS].map((t,i)=>
    `<button class="chip" aria-pressed="${i===0}" data-t="${t}">${t}</button>`).join('');
  $$('#simTemas .chip').forEach(c=>c.onclick=()=>{
    $$('#simTemas .chip').forEach(x=>x.setAttribute('aria-pressed','false'));
    c.setAttribute('aria-pressed','true');});
  $('#simCants').innerHTML = [10,20,62].map((c,i)=>
    `<button class="chip" aria-pressed="${i===0}" data-c="${c}">${c===62?'Todos (62)':c}</button>`).join('');
  $$('#simCants .chip').forEach(c=>c.onclick=()=>{
    $$('#simCants .chip').forEach(x=>x.setAttribute('aria-pressed','false'));
    c.setAttribute('aria-pressed','true');});
}
$('#simGo').onclick = ()=>{
  const t = $('#simTemas .chip[aria-pressed="true"]').dataset.t;
  const c = +$('#simCants .chip[aria-pressed="true"]').dataset.c;
  startSim(t, c);
};
$('#simCancel').onclick = ()=>$('#dlgSim').close();
$('#sumClose').onclick = ()=>$('#dlgSum').close();

/* init */
paintChips(); paintGrid(); paintStats();
const m = location.hash.match(/^#p\/(\d+)$/);
if(m){ const n=+m[1]; if(n>=1&&n<=62) open(n,true); }
"""

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TrainerMath · POP 2025 — Reconstruido PUCP resuelto</title>
<meta name="description" content="Los 62 problemas del examen reconstruido Primera Opción PUCP 2025 resueltos paso a paso: entrena, responde y aprende el método.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400..750;1,400..600&family=Space+Grotesk:wght@500..700&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128221;</text></svg>">
<style>__CSS__</style>
</head>
<body>

<header class="top">
  <div class="top-in">
    <div class="brand">
      <b>Trainer<i>Math</i> · POP 2025</b>
      <small>Reconstruido PUCP · Primera Opción · 23-nov-2025</small>
    </div>
    <div class="tstats">
      <div class="tstat"><b id="stDone" class="num">0/62</b><span>respondidos</span></div>
      <div class="tstat"><b id="stOk" class="num">0</b><span>aciertos</span></div>
      <div class="tstat"><b id="stAcc" class="num">0%</b><span>precisión</span></div>
      <svg class="ring" viewBox="0 0 46 46" aria-label="progreso">
        <circle class="bgc" cx="23" cy="23" r="19"/>
        <circle class="fgc" id="ringFg" cx="23" cy="23" r="19"/>
        <text id="ringTx" x="23" y="27.5" text-anchor="middle">0%</text>
      </svg>
      <button class="icob" id="stReset" title="Reiniciar progreso" aria-label="Reiniciar progreso">&#8635;</button>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div>
      <h1>El examen completo,<br>resuelto como lo resolverías tú.</h1>
      <p>62 problemas de Aritmética, Álgebra, Geometría, Probabilidad y Estadística.
      Responde primero, equivócate sin miedo y luego abre la resolución paso a paso
      con la idea clave de cada método.</p>
    </div>
    <div class="cta">
      <button class="btn pri" id="ctaGo">Empezar</button>
      <button class="btn" id="ctaSim">&#9201; Simulacro</button>
    </div>
  </section>

  <div class="chips" id="chips"></div>
  <div class="chips subchips" id="subchips"></div>
  <div class="grid" id="grid"></div>

  <footer>
    <b>TrainerMath</b> · examen reconstruido por Academia Prisma · resoluciones y app: AP — uso educativo
  </footer>
</main>

<!-- overlay problema -->
<div class="ov" id="ov" role="dialog" aria-modal="true" aria-label="Problema">
  <div class="ov-in">
    <div class="ovbar">
      <button class="icob" id="ovClose" aria-label="Cerrar">&#10005;</button>
      <span class="pos" id="ovPos"></span>
      <span class="sp"></span>
      <span class="timer" id="ovTimer" style="display:none">00:00</span>
      <button class="icob" id="ovPrev" aria-label="Anterior">&#8592;</button>
      <button class="icob" id="ovNext" aria-label="Siguiente">&#8594;</button>
    </div>
    <div class="panel">
      <div class="phead" id="pHead"></div>
      <div class="enun" id="pEnun"></div>
      <div class="fig" id="pFig"></div>
      <div class="opts" id="pOpts"></div>
      <div class="verdict" id="pVerdict"></div>
      <div class="sol" id="solZone">
        <h3>Resolución <span class="sdots" id="sdots"></span></h3>
        <div class="lock" id="solLock" style="display:none"></div>
        <div class="steps" id="pSteps"></div>
        <div class="sbtns">
          <button class="btn pri" id="btnStep">Resolver paso a paso</button>
          <button class="btn" id="btnAll">Mostrar todo</button>
        </div>
        <div class="answer" id="pAnswer"></div>
        <div class="idea" id="pIdea"></div>
        <div class="notare" id="pNota"></div>
      </div>
      <div class="pnav" id="pnavRow">
        <button class="btn" onclick="nav(-1)">&#8592; Anterior</button>
        <button class="btn" onclick="nav(1)">Siguiente &#8594;</button>
      </div>
    </div>
  </div>
</div>

<!-- diálogo simulacro -->
<dialog id="dlgSim">
  <div class="dlg">
    <h3>&#9201; Simulacro</h3>
    <p>Preguntas al azar, con cronómetro y sin ver las resoluciones hasta el final.</p>
    <label>Tema</label><div class="row" id="simTemas"></div>
    <label>Cantidad</label><div class="row" id="simCants"></div>
    <div class="row" style="margin-top:6px">
      <button class="btn pri" id="simGo">Comenzar</button>
      <button class="btn" id="simCancel">Cancelar</button>
    </div>
  </div>
</dialog>

<!-- diálogo resumen -->
<dialog id="dlgSum">
  <div class="dlg">
    <h3>Resultado del simulacro</h3>
    <div class="bigscore num" id="sumScore">0/0</div>
    <p id="sumTime"></p>
    <div class="sumlist" id="sumList"></div>
    <div class="row" style="margin-top:16px"><button class="btn pri" id="sumClose">Cerrar</button></div>
  </div>
</dialog>

<script>__JS__</script>
</body>
</html>
"""

html = (HTML.replace("__CSS__", CSS)
            .replace("__JS__", JS.replace("__DATA__", DATA).replace("__TEMAS__", json.dumps(TEMAS, ensure_ascii=False))))

out = r"d:\AP\trainermath-pop-2025\index.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"OK -> {out}  ({len(html)/1024:.0f} KB, {len(PROBLEMS)} problemas)")
