# -*- coding: utf-8 -*-
"""Build the offline-capable TrainerMath app. Run from any working directory."""
import json
import re
import html
import base64
from pathlib import Path
from data_p1 import PROBLEMS_1
from data_p2 import PROBLEMS_2
from data_p3 import PROBLEMS_3
from data_p4 import PROBLEMS_4
from figs import FIGS
from data.editorial_fixes import apply_editorial_fixes
from data.curriculum import apply_curriculum, public_syllabus

ROOT = Path(__file__).resolve().parent


def load_bank():
    from data.generated_bank import PROBLEMS_GENERATED
    from data.trigonometry_bank import PROBLEMS_TRIGONOMETRY
    from data.syllabus_additions import PROBLEMS_SYLLABUS
    original = apply_editorial_fixes(PROBLEMS_1 + PROBLEMS_2 + PROBLEMS_3 + PROBLEMS_4)
    assert [p['n'] for p in original] == list(range(1, 63))
    for p in original:
        p.update(id=str(p['n']), family='pop-' + str(p.get('dup') or p['n']),
                 origin='original', target={1:60, 2:90, 3:150}[p['dif']],
                 source={'file':'Reconstruido-examen-Primera-Opcion-2025.pdf', 'page':None, 'concept':p['sub']},
                 practiceEligible=not bool(p.get('dup')))
        p['fig'] = FIGS.get(p.get('fig'), '')
        p.setdefault('hint', 'Identifica qué cantidad se pide, sus unidades y la condición que limita la respuesta. Elige una estrategia antes de operar.')
        p.setdefault('trap', 'Comprueba la condición final del enunciado antes de marcar una alternativa.')
        p.setdefault('nota', '')
    generated = [dict(p) for p in PROBLEMS_GENERATED + PROBLEMS_TRIGONOMETRY + PROBLEMS_SYLLABUS]
    assert len(generated) >= 300, 'Se requieren al menos 300 ejercicios nuevos'
    fingerprints = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', p['enun']))).strip().casefold() for p in generated]
    assert len(set(fingerprints)) == len(fingerprints), 'Enunciados nuevos repetidos'
    assert {p['dif'] for p in generated} == {1,2,3}, 'Falta cobertura de un nivel'
    assert all(len(set(p['opts'])) == 4 for p in generated), 'Alternativas duplicadas'
    bank = original + generated
    assert len({str(p['id']) for p in bank}) == len(bank), 'IDs duplicados'
    for p in bank:
        assert 0 <= p['ans'] < len(p['opts']), p['id']
        assert 1 <= p['dif'] <= 3 and p['target'] > 0, p['id']
        assert p['steps'] and p['idea'], p['id']
        for field in ('params', 'check', 'validation', 'validator'):
            p.pop(field, None)
    return apply_curriculum(bank)


def main():
    bank = load_bank()
    template = (ROOT / 'web/template.html').read_text(encoding='utf-8')
    css = '\n'.join((ROOT / 'web' / file).read_text(encoding='utf-8-sig') for file in ('legacy-math.css','app.css','brand.css','anzan.css'))
    replacements = {
        '__CSS__':css,
        '__DATA__':json.dumps(bank,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'),
        '__SYLLABUS__':json.dumps(public_syllabus(),ensure_ascii=False,separators=(',',':')).replace('</','<\\/'),
        '__ENGINE__':(ROOT/'web/engine.js').read_text(encoding='utf-8'),
        '__ADAPTIVE__':(ROOT/'web/adaptive.js').read_text(encoding='utf-8'),
        '__ANZAN__':(ROOT/'web/anzan.js').read_text(encoding='utf-8'),
        '__BACKEND__':(ROOT/'web/backend.js').read_text(encoding='utf-8'),
        '__APP__':(ROOT/'web/app.js').read_text(encoding='utf-8'),
        '__LOGO__':'data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/trainermath-mark.svg').read_bytes()).decode('ascii'),
        '__MASCOT__':'data:image/png;base64,'+base64.b64encode((ROOT/'assets/aecodito.png').read_bytes()).decode('ascii'),
    }
    for token, content in replacements.items():
        assert token in template, f'Missing template token {token}'
        template = template.replace(token, content)
    (ROOT / 'index.html').write_text(template, encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Built index.html: {len(bank)} problems, {len(template.encode("utf-8")) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
