import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.116.0";

const SHEET_ID="1FT7gKsw5UKavMafbbtJaRianQi-Lj529Nfecq9IbVcI";
const TAB="TrainerMath_v4";
const allowedOrigins=new Set(["https://apalpan.github.io","http://127.0.0.1:8768","http://127.0.0.1:8769","http://localhost:8768","http://localhost:8769"]);
const headers=(origin:string|null)=>({"Access-Control-Allow-Origin":origin&&allowedOrigins.has(origin)?origin:"https://apalpan.github.io","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS","Content-Type":"application/json; charset=utf-8","Vary":"Origin"});
const respond=(origin:string|null,status:number,body:Record<string,unknown>)=>new Response(JSON.stringify(body),{status,headers:headers(origin)});
const clip=(value:unknown,max:number)=>String(value??"").trim().slice(0,max);
const object=(value:unknown)=>value&&typeof value==="object"&&!Array.isArray(value)?value as Record<string,unknown>:{};
const base64url=(input:Uint8Array|string)=>{const bytes=typeof input==="string"?new TextEncoder().encode(input):input;let binary="";for(const byte of bytes)binary+=String.fromCharCode(byte);return btoa(binary).replace(/\+/g,"-").replace(/\//g,"_").replace(/=+$/g,"");};

async function serviceToken(raw:string){
  const credentials=JSON.parse(raw) as Record<string,unknown>,email=clip(credentials.client_email,240),pem=clip(credentials.private_key,12000);
  if(!email||!pem)throw new Error("invalid_google_credentials");
  const binary=atob(pem.replace(/-----BEGIN PRIVATE KEY-----|-----END PRIVATE KEY-----|\s/g,"")),keyBytes=Uint8Array.from(binary,char=>char.charCodeAt(0));
  const key=await crypto.subtle.importKey("pkcs8",keyBytes,{name:"RSASSA-PKCS1-v1_5",hash:"SHA-256"},false,["sign"]);
  const now=Math.floor(Date.now()/1000),head=base64url(JSON.stringify({alg:"RS256",typ:"JWT"})),claims=base64url(JSON.stringify({iss:email,scope:"https://www.googleapis.com/auth/spreadsheets",aud:"https://oauth2.googleapis.com/token",iat:now,exp:now+3500}));
  const unsigned=`${head}.${claims}`,signature=await crypto.subtle.sign("RSASSA-PKCS1-v1_5",key,new TextEncoder().encode(unsigned)),assertion=`${unsigned}.${base64url(new Uint8Array(signature))}`;
  const response=await fetch("https://oauth2.googleapis.com/token",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:new URLSearchParams({grant_type:"urn:ietf:params:oauth:grant-type:jwt-bearer",assertion}).toString(),signal:AbortSignal.timeout(12000)});
  if(!response.ok)throw new Error(`google_auth_${response.status}`);const payload=await response.json() as Record<string,unknown>;const token=clip(payload.access_token,4096);if(!token)throw new Error("google_token_missing");return token;
}
const rowFrom=(payload:Record<string,unknown>)=>[payload.event_id,payload.fecha,payload.tipo,payload.version,payload.learner_code,payload.sesion,payload.modo,payload.area,payload.unidad,payload.intentos,payload.correctas,payload.precision_pct,payload.mediana_s,payload.dentro_meta_pct,payload.cambio_dominio,payload.siguiente_accion,payload.evidencia];

async function appendGoogle(rows:Record<string,unknown>[],credentials:string){
  const token=await serviceToken(credentials),sheetId=Deno.env.get("TRAINERMATH_SHEET_ID")||SHEET_ID,encoded=encodeURIComponent(`'${TAB}'!A:Q`),auth={Authorization:`Bearer ${token}`};
  const current=await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${encodeURIComponent(`'${TAB}'!A:A`)}?majorDimension=COLUMNS`,{headers:auth,signal:AbortSignal.timeout(12000)});
  if(!current.ok)throw new Error(`google_read_${current.status}`);const data=await current.json() as Record<string,unknown>,values=Array.isArray(data.values)?data.values:[],existing=new Set((Array.isArray(values[0])?values[0]:[]).map(String));
  const unique=rows.filter(row=>!existing.has(clip(row.event_id,180)));if(!unique.length)return 0;
  const response=await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${encoded}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS`,{method:"POST",headers:{...auth,"Content-Type":"application/json"},body:JSON.stringify({majorDimension:"ROWS",values:unique.map(rowFrom)}),signal:AbortSignal.timeout(12000)});
  if(!response.ok)throw new Error(`google_append_${response.status}`);return unique.length;
}

Deno.serve(async(req:Request)=>{
  const origin=req.headers.get("origin");if(req.method==="OPTIONS")return new Response(null,{status:204,headers:headers(origin)});if(req.method!=="POST")return respond(origin,405,{ok:false,code:"method_not_allowed"});
  const authHeader=req.headers.get("authorization")||"",token=authHeader.replace(/^Bearer\s+/i,"");if(!token)return respond(origin,401,{ok:false,code:"authentication_required"});
  const supabaseUrl=Deno.env.get("SUPABASE_URL")||"",anonKey=Deno.env.get("SUPABASE_ANON_KEY")||"",serviceKey=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")||"";
  const userClient=createClient(supabaseUrl,anonKey,{global:{headers:{Authorization:authHeader}}}),admin=createClient(supabaseUrl,serviceKey,{auth:{persistSession:false,autoRefreshToken:false}});
  const {data:userData,error:userError}=await userClient.auth.getUser(token);if(userError||!userData.user)return respond(origin,401,{ok:false,code:"invalid_session"});
  const googleCredentials=Deno.env.get("GOOGLE_SERVICE_ACCOUNT_JSON")||"",webhook=Deno.env.get("TRAINERMATH_SHEETS_WEBHOOK_URL")||"";if(!googleCredentials&&!webhook)return respond(origin,503,{ok:false,code:"sheet_credentials_missing"});
  let body:Record<string,unknown>={};try{body=object(await req.json());}catch{}const limit=Math.max(1,Math.min(20,Number(body.limit)||10));
  const {data:pending,error:readError}=await admin.from("tm_sheet_outbox").select("id,event_key,payload,attempts").eq("owner_id",userData.user.id).in("status",["pending","failed"]).lte("next_attempt_at",new Date().toISOString()).order("created_at",{ascending:true}).limit(limit);
  if(readError)return respond(origin,500,{ok:false,code:"outbox_read_failed"});if(!pending?.length)return respond(origin,200,{ok:true,sent:0,pending:0});
  const ids=pending.map(row=>row.id);await admin.from("tm_sheet_outbox").update({status:"processing"}).in("id",ids).eq("owner_id",userData.user.id);
  try{
    let sent=0;
    if(googleCredentials)sent=await appendGoogle(pending.map(row=>object(row.payload)),googleCredentials);
    else{const response=await fetch(webhook,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({tab:TAB,events:pending.map(row=>({event_key:row.event_key,payload:row.payload}))}),signal:AbortSignal.timeout(12000)});if(!response.ok)throw new Error(`webhook_${response.status}`);sent=pending.length;}
    await admin.from("tm_sheet_outbox").update({status:"sent",sent_at:new Date().toISOString(),last_error:null}).in("id",ids).eq("owner_id",userData.user.id);
    return respond(origin,200,{ok:true,sent,processed:pending.length,pending:0});
  }catch(error){
    for(const row of pending){const attempts=Math.min(20,Number(row.attempts||0)+1),delay=Math.min(24*60,Math.pow(2,attempts)*5);await admin.from("tm_sheet_outbox").update({status:"failed",attempts,last_error:clip(error instanceof Error?error.message:"sheet_sync_failed",240),next_attempt_at:new Date(Date.now()+delay*60000).toISOString()}).eq("id",row.id).eq("owner_id",userData.user.id);}
    return respond(origin,502,{ok:false,code:"sheet_sync_failed"});
  }
});
