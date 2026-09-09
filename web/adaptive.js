/* TrainerMath adaptive learning and Aecodito's reviewed mental-math catalog. */
(function(root){
  'use strict';

  const DAY=86400000;
  const TIPS=[
    {id:'square_ending_5',title:'Cuadrados que terminan en 5',condition:'Úsalo cuando el número entero termina en 5.',rule:'Multiplica la parte anterior al 5 por su siguiente y agrega 25.',example:'25²: 2 × 3 = 6; agrega 25 → 625.',trap:'El 25 final siempre ocupa dos cifras.',areas:['Números y Operaciones','Álgebra'],keys:['cuadrado','potencia','exponente']},
    {id:'complete_ten',title:'Completa la decena',condition:'Úsalo en sumas cuando un sumando está cerca de la siguiente decena.',rule:'Parte el otro sumando: completa 10 y añade lo que queda.',example:'68 + 7 = 68 + 2 + 5 = 75.',trap:'Conserva la misma cantidad total al partir el sumando.',areas:['Números y Operaciones'],keys:['suma','adición','sumar']},
    {id:'addition_compensation',title:'Compensa una suma',condition:'Úsalo si un sumando está cerca de una centena o decena redonda.',rule:'Suma a un término y resta lo mismo al otro.',example:'398 + 267 = 400 + 265 = 665.',trap:'La compensación usa signos opuestos.',areas:['Números y Operaciones'],keys:['suma','adición']},
    {id:'subtraction_shift',title:'Desplaza la resta',condition:'Úsalo si el sustraendo está cerca de una cifra redonda.',rule:'Suma o resta la misma cantidad a ambos términos.',example:'752 − 298 = 754 − 300 = 454.',trap:'Ambos términos cambian en la misma dirección.',areas:['Números y Operaciones'],keys:['resta','diferencia','sustracción']},
    {id:'complement_power_10',title:'Busca el complemento',condition:'Úsalo al restar de 10, 100, 1000 o una potencia de diez.',rule:'Completa por posiciones, empezando desde la izquierda.',example:'1000 − 487: faltan 13 para 500 y 500 para 1000 → 513.',trap:'Comprueba sumando el complemento al número inicial.',areas:['Números y Operaciones'],keys:['complemento','resta']},
    {id:'multiply_5',title:'Multiplica por 5 con una mitad',condition:'Úsalo siempre que uno de los factores sea 5.',rule:'Multiplica por 10 y divide entre 2.',example:'86 × 5 = 860 ÷ 2 = 430.',trap:'Divide después de multiplicar por 10.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'divide_5',title:'Divide entre 5 doblando',condition:'Úsalo siempre que el divisor sea 5.',rule:'Duplica el dividendo y divide entre 10.',example:'735 ÷ 5 = 1470 ÷ 10 = 147.',trap:'El resultado puede conservar decimales.',areas:['Números y Operaciones'],keys:['división','cociente']},
    {id:'multiply_25',title:'Multiplica por 25',condition:'Úsalo siempre que uno de los factores sea 25.',rule:'Multiplica por 100 y divide entre 4.',example:'48 × 25 = 4800 ÷ 4 = 1200.',trap:'Primero revisa si dividir el otro factor entre 4 es más corto.',areas:['Números y Operaciones'],keys:['multiplicación','producto','porcentaje']},
    {id:'divide_25',title:'Divide entre 25',condition:'Úsalo siempre que el divisor sea 25.',rule:'Multiplica por 4 y divide entre 100.',example:'650 ÷ 25 = 2600 ÷ 100 = 26.',trap:'Mueve dos lugares la coma al dividir entre 100.',areas:['Números y Operaciones'],keys:['división','cociente']},
    {id:'multiply_125',title:'Multiplica por 125',condition:'Úsalo siempre que uno de los factores sea 125.',rule:'Multiplica por 1000 y divide entre 8.',example:'24 × 125 = 24000 ÷ 8 = 3000.',trap:'Si el otro factor es múltiplo de 8, divídelo primero.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'multiply_9',title:'Multiplica por 9',condition:'Úsalo siempre que uno de los factores sea 9.',rule:'Multiplica por 10 y resta una vez el número.',example:'47 × 9 = 470 − 47 = 423.',trap:'Resta exactamente un grupo, no nueve.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'multiply_11',title:'Multiplica dos cifras por 11',condition:'Úsalo directamente con números de dos cifras; controla el acarreo.',rule:'Coloca entre las cifras la suma de ambas.',example:'57 × 11: 5 | 5+7 | 7 = 5 | 12 | 7 → 627.',trap:'Si la suma supera 9, lleva una unidad a la primera cifra.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'multiply_99',title:'Multiplica por 99',condition:'Úsalo siempre que uno de los factores sea 99.',rule:'Multiplica por 100 y resta una vez el número.',example:'36 × 99 = 3600 − 36 = 3564.',trap:'Estima: el resultado debe ser apenas menor que 100 veces el número.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'multiply_101',title:'Multiplica por 101',condition:'Úsalo siempre que uno de los factores sea 101.',rule:'Multiplica por 100 y suma una vez el número.',example:'43 × 101 = 4300 + 43 = 4343.',trap:'No concatenes cifras si el número tiene más de dos dígitos.',areas:['Números y Operaciones'],keys:['multiplicación','producto']},
    {id:'double_half',title:'Dobla y divide a la mitad',condition:'Úsalo cuando un factor es par y el otro se vuelve más simple al doblarlo.',rule:'Duplica un factor y divide el otro entre 2; el producto no cambia.',example:'16 × 35 = 8 × 70 = 560.',trap:'Haz las dos transformaciones, no solo una.',areas:['Números y Operaciones','Álgebra'],keys:['multiplicación','producto']},
    {id:'distributive_split',title:'Parte un factor',condition:'Úsalo si un factor se separa en decenas y unidades fáciles.',rule:'Distribuye el otro factor sobre cada parte y suma.',example:'37 × 12 = 37 × 10 + 37 × 2 = 444.',trap:'Incluye todas las partes del factor.',areas:['Números y Operaciones','Álgebra'],keys:['distributiva','multiplicación','producto']},
    {id:'difference_squares',title:'Diferencia de cuadrados',condition:'Úsalo en factores equidistantes de un número central.',rule:'(a−b)(a+b) = a²−b².',example:'49 × 51 = 50² − 1² = 2499.',trap:'La distancia al centro debe ser la misma.',areas:['Álgebra','Números y Operaciones'],keys:['producto notable','factorización','cuadrado','multiplicación']},
    {id:'same_tens_units_10',title:'Misma decena, unidades suman 10',condition:'Úsalo si las decenas son iguales y las unidades suman 10.',rule:'Multiplica la decena por su siguiente; luego multiplica las unidades.',example:'43 × 47: 4×5 | 3×7 = 20 | 21 → 2021.',trap:'La parte de unidades debe ocupar dos cifras.',areas:['Números y Operaciones','Álgebra'],keys:['multiplicación','producto']},
    {id:'decimal_shift',title:'Mueve la coma con control',condition:'Úsalo al multiplicar o dividir por 10, 100, 1000 y sus potencias.',rule:'Mueve la coma tantos lugares como ceros tenga la potencia.',example:'3,75 × 100 = 375; 48 ÷ 100 = 0,48.',trap:'Mover la coma no elimina la unidad de medida.',areas:['Números y Operaciones'],keys:['decimal','potencia de diez']},
    {id:'fraction_cancel',title:'Simplifica antes de multiplicar',condition:'Úsalo en productos o cocientes de fracciones.',rule:'Cancela factores comunes antes de hacer productos grandes.',example:'18/35 × 14/27 → 2/5 × 2/3 = 4/15.',trap:'Solo se cancelan factores, no sumandos.',areas:['Números y Operaciones','Álgebra'],keys:['fracción','racional','proporción']},
    {id:'fraction_percent_map',title:'Automatiza fracciones frecuentes',condition:'Úsalo con medios, tercios, cuartos, quintos y octavos.',rule:'Reconoce 1/2=50%, 1/4=25%, 1/5=20%, 1/8=12,5%.',example:'3/4 de 240 = 75% de 240 = 180.',trap:'Un tercio es 33⅓%, no 33% exacto.',areas:['Números y Operaciones','Estadística y Probabilidad'],keys:['fracción','porcentaje','racional']},
    {id:'percent_blocks',title:'Construye el porcentaje',condition:'Úsalo cuando el porcentaje se compone con 10%, 5% o 1%.',rule:'Calcula bloques simples y súmalos.',example:'15% de 240 = 10% + 5% = 24 + 12 = 36.',trap:'El porcentaje siempre actúa sobre la misma base.',areas:['Números y Operaciones','Estadística y Probabilidad'],keys:['porcentaje','descuento','interés']},
    {id:'percent_symmetry',title:'Intercambia porcentaje y base',condition:'Úsalo en expresiones del tipo a% de b.',rule:'a% de b = b% de a; elige la versión más fácil.',example:'18% de 50 = 50% de 18 = 9.',trap:'Solo intercambias porcentaje y base dentro de esa expresión.',areas:['Números y Operaciones','Estadística y Probabilidad'],keys:['porcentaje']},
    {id:'successive_percentages',title:'Porcentajes sucesivos son factores',condition:'Úsalo cuando hay dos o más aumentos o descuentos consecutivos.',rule:'Convierte cada cambio en factor y multiplícalos.',example:'Sube 20% y 10%: 1,20 × 1,10 = 1,32; sube 32%.',trap:'No sumes porcentajes si cambia la base.',areas:['Números y Operaciones','Álgebra'],keys:['porcentaje','descuento','variación']},
    {id:'compare_fractions',title:'Compara con producto cruzado',condition:'Úsalo con dos fracciones y denominadores positivos.',rule:'Compara a×d con b×c para a/b y c/d.',example:'5/8 vs 7/12: 5×12=60 y 7×8=56; 5/8 es mayor.',trap:'Con denominadores negativos, normaliza primero los signos.',areas:['Números y Operaciones'],keys:['fracción','racional','comparar']},
    {id:'proportional_scale',title:'Reduce la razón primero',condition:'Úsalo en proporciones, escalas y regla de tres.',rule:'Simplifica la relación antes de multiplicar en cruz.',example:'6/15 = 2/5; si 2 corresponde a 14, 5 corresponde a 35.',trap:'Confirma qué magnitudes varían juntas y cuáles al revés.',areas:['Números y Operaciones','Álgebra'],keys:['proporción','razón','regla de tres','escala']},
    {id:'arithmetic_pairs',title:'Empareja extremos de una PA',condition:'Úsalo en una progresión aritmética finita.',rule:'Cada par de extremos suma lo mismo: S = n(a₁+aₙ)/2.',example:'4+7+10+13+16: 5(4+16)/2 = 50.',trap:'Verifica que la diferencia sea constante y cuenta bien los términos.',areas:['Números y Operaciones'],keys:['progresión aritmética','sucesión','serie']},
    {id:'equidistant_average',title:'Promedio de valores equidistantes',condition:'Úsalo cuando los datos o términos están igualmente espaciados.',rule:'El promedio es el valor central o el promedio de los dos centrales.',example:'12, 17, 22, 27, 32 tienen promedio 22.',trap:'La regla exige separaciones iguales.',areas:['Números y Operaciones','Estadística y Probabilidad'],keys:['promedio','media','progresión']},
    {id:'linear_isolate',title:'Aísla sin saltos de signo',condition:'Úsalo en ecuaciones lineales.',rule:'Haz la misma operación en ambos miembros y simplifica en cada paso.',example:'3x−7=20 → 3x=27 → x=9.',trap:'“Pasar” un término es abreviar una operación en ambos lados.',areas:['Álgebra'],keys:['ecuación','lineal','incógnita']},
    {id:'factor_before_formula',title:'Factoriza antes de usar fórmula',condition:'Úsalo si el polinomio tiene factor común o patrón notable.',rule:'Busca factor común, cuadrados y diferencia de cuadrados primero.',example:'x²−9 = (x−3)(x+3).',trap:'Comprueba multiplicando los factores.',areas:['Álgebra'],keys:['factorización','polinomio','raíz']},
    {id:'geometry_units',title:'Separa forma y unidades',condition:'Úsalo en perímetros, áreas y volúmenes.',rule:'Dibuja, escribe la fórmula y recién después reemplaza datos.',example:'Rectángulo 8×5: perímetro 26 u; área 40 u².',trap:'Perímetro, área y volumen usan unidades distintas.',areas:['Geometría'],keys:['área','perímetro','volumen','figura']},
    {id:'triangle_half',title:'Triángulo: mitad de un rectángulo',condition:'Úsalo cuando identificas base y altura perpendicular.',rule:'A = base × altura ÷ 2.',example:'Base 14 y altura 9: A = 14×9÷2 = 63.',trap:'La altura debe ser perpendicular a la base elegida.',areas:['Geometría'],keys:['triángulo','área','altura']},
    {id:'pythagorean_triples',title:'Reconoce ternas pitagóricas',condition:'Úsalo en triángulos rectángulos.',rule:'Busca múltiplos de 3-4-5, 5-12-13, 7-24-25 u 8-15-17.',example:'Catetos 9 y 12 → terna 3-4-5 por 3 → hipotenusa 15.',trap:'La hipotenusa siempre es el lado mayor.',areas:['Geometría','Trigonometría'],keys:['pitágoras','triángulo rectángulo','hipotenusa']},
    {id:'special_triangles',title:'Triángulos notables',condition:'Úsalo con ángulos 30°-60°-90° o 45°-45°-90°.',rule:'Recuerda razones 1:√3:2 y 1:1:√2.',example:'Si el cateto opuesto a 30° vale 6, la hipotenusa vale 12.',trap:'Ubica cada lado respecto del ángulo antes de usar la razón.',areas:['Trigonometría','Geometría'],keys:['seno','coseno','triángulo notable','30','45','60']},
    {id:'probability_complement',title:'Usa el complemento',condition:'Úsalo cuando piden “al menos uno”.',rule:'P(al menos uno) = 1 − P(ninguno).',example:'Dos intentos con fallo 1/4: 1 − (1/4)² = 15/16.',trap:'Multiplica probabilidades solo si los eventos son independientes.',areas:['Estadística y Probabilidad'],keys:['probabilidad','al menos','ninguno']},
    {id:'combinatorics_order',title:'Pregunta si el orden importa',condition:'Úsalo antes de contar arreglos o selecciones.',rule:'Orden importa: permutación/variación; no importa: combinación.',example:'Elegir presidenta y secretaria entre 6: 6×5=30.',trap:'Aclara también si se permite repetición.',areas:['Estadística y Probabilidad'],keys:['combinatoria','conteo','formas','maneras']},
    {id:'estimate_first',title:'Estima antes de operar',condition:'Úsalo en toda operación larga o con alternativas separadas.',rule:'Predice signo, rango y orden de magnitud; luego calcula.',example:'19% de 300 debe estar cerca de 60 y ser menor: 57.',trap:'La estimación controla la respuesta, no sustituye la exactitud pedida.',areas:['Números y Operaciones','Álgebra','Geometría','Estadística y Probabilidad','Trigonometría'],keys:['aproximación','estimación']},
    {id:'digit_filter',title:'Descarta por la última cifra',condition:'Úsalo cuando las alternativas difieren en paridad o cifra final.',rule:'Calcula solo la última cifra o aplica divisibilidad.',example:'27×34 termina en 8 porque 7×4 termina en 8.',trap:'Úsalo para descartar; puede no identificar una única opción.',areas:['Números y Operaciones','Álgebra'],keys:['divisibilidad','cifra','múltiplo']},
    {id:'backsolve_options',title:'Prueba las alternativas',condition:'Úsalo si sustituir opciones toma menos pasos que despejar.',rule:'Empieza por una opción central y descarta por tamaño.',example:'Si las opciones son raíces posibles, sustitúyelas en la ecuación.',trap:'No pruebes cuatro opciones si una propiedad las descarta antes.',areas:['Álgebra','Números y Operaciones'],keys:['alternativa','ecuación','valor']},
    {id:'exam_two_passes',title:'Haz dos vueltas',condition:'Úsalo durante el simulacro completo.',rule:'Primero asegura las directas; luego vuelve a las marcadas.',example:'Si en 40 s no aparece una ruta, marca, continúa y regresa.',trap:'Reservar tiempo no significa abandonar la pregunta.',areas:['Números y Operaciones','Álgebra','Geometría','Estadística y Probabilidad','Trigonometría'],keys:['examen','simulacro','tiempo']},
    {id:'sanity_check',title:'Control de 5 segundos',condition:'Úsalo antes de confirmar cualquier respuesta.',rule:'Revisa signo, unidad, rango y tamaño.',example:'Una probabilidad debe estar entre 0 y 1; un área no usa unidades lineales.',trap:'Comprueba la condición pedida, no todo el procedimiento.',areas:['Números y Operaciones','Álgebra','Geometría','Estadística y Probabilidad','Trigonometría'],keys:['verifica','respuesta']}
  ];

  const clean=value=>String(value??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const problemText=p=>clean([p?.tema,p?.sub,p?.family,p?.curriculum?.item,p?.curriculum?.label,String(p?.enun||'').replace(/<[^>]+>/g,' ')].join(' '));
  const median=values=>{const rows=values.filter(Number.isFinite).sort((a,b)=>a-b),m=Math.floor(rows.length/2);return rows.length?(rows.length%2?rows[m]:(rows[m-1]+rows[m])/2):null;};
  const unitKey=p=>p?.curriculum?.item||p?.family||String(p?.id??p?.n??'');

  function unitStates(state,bank,now=Date.now()){
    const byId=new Map(bank.map(p=>[String(p.id??p.n),p]));
    const rows=new Map();
    for(const p of bank.filter(x=>x.practiceEligible!==false)){
      const key=unitKey(p);if(!key)continue;
      if(!rows.has(key))rows.set(key,{id:key,label:p.curriculum?.label||p.sub||p.tema,area:p.tema,count:0,correct:0,assisted:0,within:0,seconds:[],latestAt:0,sessions:new Set(),attempts:[]});
    }
    for(const attempt of state?.attempts||[]){
      if(attempt.mode==='legacy')continue;const p=byId.get(String(attempt.qid));if(!p)continue;
      const row=rows.get(unitKey(p));if(!row)continue;
      row.count++;row.correct+=attempt.correct&&!attempt.hint?1:0;row.assisted+=attempt.hint?1:0;
      row.within+=attempt.correct&&!attempt.hint&&attempt.seconds>0&&attempt.seconds<=attempt.target?1:0;
      if(attempt.correct&&!attempt.hint&&attempt.seconds>0)row.seconds.push(Number(attempt.seconds));
      row.latestAt=Math.max(row.latestAt,Number(attempt.at)||0);row.sessions.add(String(attempt.key||'').split(':')[0]);row.attempts.push(attempt);
    }
    return [...rows.values()].map(row=>{
      const ordered=row.attempts.slice().sort((a,b)=>(a.at||0)-(b.at||0));
      const last5=ordered.slice(-5),speedEvidence=last5.filter(a=>a.correct&&!a.hint&&a.seconds>0&&a.seconds<=a.target).length;
      const accuracy=row.count?row.correct/row.count:0,slow=row.count?ordered.filter(a=>a.correct&&!a.hint&&a.seconds>a.target).length/row.count:0,assist=row.count?row.assisted/row.count:0;
      const mastered=row.count>=5&&last5.length===5&&speedEvidence>=4&&row.sessions.size>=2;
      const status=!row.count?'nuevo':mastered?'a velocidad':row.count<3?'señal inicial':accuracy>=.75?'estable':'en desarrollo';
      const age=row.latestAt?Math.max(0,(now-row.latestAt)/DAY):999;
      const weakness=row.count?(.55*(1-accuracy)+.25*slow+.15*assist+.05*Math.min(1,age/14)):0.42;
      return {...row,sessions:row.sessions.size,accuracy,median:median(row.seconds),weakness,status,mastered};
    });
  }

  function trickForProblem(problem,attempt,index=0){
    const haystack=problemText(problem),area=problem?.tema||'';
    const ranked=TIPS.map((tip,position)=>{
      let score=tip.areas.includes(area)?2:0;
      for(const key of tip.keys)if(haystack.includes(clean(key)))score+=3;
      if(attempt?.reason==='calculo'&&['complete_ten','addition_compensation','subtraction_shift','double_half','estimate_first'].includes(tip.id))score+=2;
      if(attempt?.reason==='tiempo'&&['estimate_first','digit_filter','backsolve_options','exam_two_passes'].includes(tip.id))score+=2;
      return {tip,score,position};
    }).sort((a,b)=>b.score-a.score||a.position-b.position);
    const strong=ranked.filter(x=>x.score>=3);const source=strong.length?strong:ranked.filter(x=>x.tip.areas.includes(area));
    return (source[index%Math.max(1,source.length)]||ranked[index%ranked.length]).tip;
  }

  function recommendation(state,bank,now=Date.now()){
    const units=unitStates(state,bank,now),attempted=units.filter(x=>x.count);
    if(!attempted.length){
      const first=units.find(x=>x.area==='Números y Operaciones')||units[0];
      return {kind:'baseline',title:'Construye tu línea base',evidence:'Completa 10 preguntas variadas para medir precisión y velocidad por unidad.',action:'Empieza con una práctica adaptativa corta.',unit:first,tip:TIPS.find(x=>x.id==='square_ending_5')};
    }
    const unit=attempted.slice().sort((a,b)=>b.weakness-a.weakness||a.count-b.count)[0];
    const confidence=unit.count>=8?'evidencia suficiente':unit.count>=3?'señal en desarrollo':'señal inicial';
    const acc=Math.round(unit.accuracy*100),within=unit.count?Math.round(unit.within/unit.count*100):0;
    const example=bank.find(p=>unitKey(p)===unit.id);
    return {kind:'adaptive',title:`Refuerza ${unit.label}`,evidence:`${confidence}: ${acc}% de precisión y ${within}% de respuestas a velocidad en ${unit.count} intento${unit.count===1?'':'s'}.`,action:'Haz 5 casos de esta unidad y busca 4 correctos sin pista dentro de la meta.',unit,tip:trickForProblem(example,unit.attempts.at(-1))};
  }

  function buildPriorityIndex(state,bank,now=Date.now()){
    const units=new Map(unitStates(state,bank,now).map(unit=>[unit.id,unit])),families=new Map();
    for(const attempt of state?.attempts||[]){const key=attempt.family||String(attempt.qid||'');if(!key)continue;if(!families.has(key))families.set(key,[]);families.get(key).push(attempt);}
    const bonuses=new Map();
    for(const [family,rows] of families){const sameFamily=rows.sort((a,b)=>(b.at||0)-(a.at||0)),latest=sameFamily[0],tail=sameFamily.slice(0,4);let streak=0,familyBonus=0;for(const a of tail){if(a.correct&&!a.hint&&a.seconds<=a.target)streak++;else break;}const interval=[0,1,3,7,14][Math.min(4,streak)]*DAY;if(!latest.correct||latest.hint||latest.seconds>latest.target)familyBonus=.35;if(now-(latest.at||0)>=interval)familyBonus+=.2;bonuses.set(family,familyBonus);}
    return problem=>(units.get(unitKey(problem))?.weakness||0)+(bonuses.get(problem.family||String(problem.id??problem.n))||0);
  }
  function priorityForProblem(problem,state,bank,now=Date.now()){return buildPriorityIndex(state,bank,now)(problem);}

  function catalogTip(index=0){return TIPS[((Number(index)||0)%TIPS.length+TIPS.length)%TIPS.length];}
  const api={VERSION:'trainer-adaptive-v1',TIPS,unitKey,unitStates,trickForProblem,recommendation,buildPriorityIndex,priorityForProblem,catalogTip};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrainerAdaptive=api;
})(typeof globalThis!=='undefined'?globalThis:this);
