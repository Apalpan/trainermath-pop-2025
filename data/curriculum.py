"""Taxonomía de la ruta Prisma y trazabilidad por unidad, sin cambiar IDs."""
import json
from pathlib import Path

MAP = json.loads((Path(__file__).parent / 'syllabus-map.json').read_text(encoding='utf-8'))
ITEMS = {item['id']: item for item in MAP['items']}


def apply_curriculum(bank):
    for p in bank:
        mapping = MAP['originals'].get(str(p['n'])) if p['origin'] == 'original' else MAP['families'].get(p['family'])
        if not mapping:
            raise ValueError(f"Ejercicio sin auditoría de temario: {p['id']} / {p['family']}")
        item_id, status = mapping.split(':', 1)
        item = ITEMS[item_id]
        p['previousTopic'] = p['tema']
        p['tema'] = item['area']
        competency = 'Cantidad' if item_id.startswith('N') else 'Regularidad, equivalencia y cambio' if item_id.startswith('A') else 'Forma, movimiento y localización' if item_id.startswith(('G', 'T')) else 'Gestión de datos e incertidumbre'
        if item_id in ('N17','N18'): competency = 'Regularidad, equivalencia y cambio'
        if item_id == 'N14': competency = 'Gestión de datos e incertidumbre'
        p['curriculum'] = {'item':item_id, 'label':item['label'], 'status':status,
                           'source':'Prisma · Talento 2026-2', 'page':4, 'competencyReference':competency}
        if status == 'complementario':
            p['practiceEligible'] = False
    return bank


def public_syllabus():
    return {key:MAP[key] for key in ('source','officialReference','areas','items')}
