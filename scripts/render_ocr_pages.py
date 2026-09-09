"""Render all pages requiring OCR, locally. Never uploads academy PDFs."""
import hashlib
import json
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'Informacion' / '_ocr'
DEST.mkdir(exist_ok=True)
documents = json.loads((ROOT/'Informacion/_index/documents.json').read_text(encoding='utf-8'))
planned = [{'path':d['path'], 'sha256':d['sha256'], 'page':n,
            'image':str(DEST / d['sha256'][:16] / f'{n:03}.png'),
            'output':str(DEST / d['sha256'][:16] / f'{n:03}.json')}
           for d in documents if d['extraction_quality'] != 'usable_text' or d.get('ocr_pages',0)
           for n in range(1,d['page_count']+1)]
(DEST/'queue.json').write_text(json.dumps(planned,ensure_ascii=False,indent=2),encoding='utf-8')
if '--queue-only' in sys.argv:
    print(f'Queued {len(planned)} pages')
    raise SystemExit(0)
queue = []
for item in documents:
    if item['extraction_quality'] == 'usable_text' and not item.get('ocr_pages',0):
        continue
    file = ROOT / item['path']
    folder = DEST / item['sha256'][:16]
    folder.mkdir(exist_ok=True)
    with fitz.open(file) as pdf:
        for number, page in enumerate(pdf, 1):
            image = folder / f'{number:03}.png'
            output = folder / f'{number:03}.json'
            if not output.exists() and not image.exists():
                page.get_pixmap(matrix=fitz.Matrix(1.65,1.65), alpha=False).save(image)
            queue.append({'path':item['path'], 'sha256':item['sha256'], 'page':number, 'image':str(image), 'output':str(output)})
    print(f'Rendered {item["page_count"]} pages: {file.name}', flush=True)
(DEST/'queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'OCR queue: {len(queue)} pages')
