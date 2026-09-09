/* Local Spanish OCR. Install tooling under ignored output/ocr-tooling. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {createWorker} = require('../output/ocr-tooling/node_modules/tesseract.js');
const root = path.resolve(__dirname,'..');
const dir = path.join(root,'Informacion','_ocr');
const all = JSON.parse(fs.readFileSync(path.join(dir,'queue.json'),'utf8'));
const from = Math.max(0,Number(process.argv[2]) || 0);
const to = Math.min(all.length,Number(process.argv[3]) || all.length);
const queue = all.slice(from,to);
let cursor = 0, done = 0, failures = 0;
async function run() {
  const worker = await createWorker('spa', 1, {cachePath:dir});
  try {
    while (cursor < queue.length) {
      const item = queue[cursor++];
      if (fs.existsSync(item.output)) {done++; continue;}
      try {
        let waits = 0;
        while (!fs.existsSync(item.image) && waits++ < 600) await new Promise(resolve=>setTimeout(resolve,1000));
        if (!fs.existsSync(item.image)) throw Error('Rendered page was not available after 10 minutes');
        const {data} = await worker.recognize(item.image);
        fs.writeFileSync(item.output,JSON.stringify({path:item.path,sha256:item.sha256,page:item.page,method:'Tesseract.js 7 local Spanish OCR',confidence:data.confidence,text:data.text},null,2));
        done++;
        if (done % 10 === 0 || done === queue.length) console.log(`OCR ${done}/${queue.length}; last confidence ${data.confidence}`);
      } catch(error) {failures++; console.error(`${item.path} p${item.page}: ${error.message}`);}
    }
  } finally {await worker.terminate();}
}
Promise.all([run(),run()]).then(()=>{console.log(`Finished: ${done}/${queue.length}, failures: ${failures}`);process.exitCode=failures?1:0;}).catch(error=>{console.error(error);process.exitCode=1;});
