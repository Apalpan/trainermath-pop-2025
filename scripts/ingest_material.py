#!/usr/bin/env python3
"""Create a local, reproducible TF-IDF index for the academy PDF corpus.

The index stays below Informacion/_index (gitignored).  It is intended for
retrieval and curriculum coverage checks, not for publishing academy material.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

try:  # PyMuPDF is preferred when the runtime provides it.
    import fitz  # type: ignore
except ImportError:  # Keep the index reproducible in the bundled fallback runtime.
    fitz = None
    from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "Informacion"
TOKEN_RE = re.compile(r"[a-záéíóúüñ]+(?:\d+)?|\d+(?:[.,]\d+)?", re.I)
SPACE_RE = re.compile(r"\s+")
STOPWORDS = {
    "a", "al", "ante", "bajo", "con", "contra", "de", "del", "desde", "el", "en",
    "entre", "es", "esta", "este", "la", "las", "lo", "los", "o", "para", "por", "que",
    "se", "sin", "su", "sus", "un", "una", "uno", "y", "ya", "como", "cuál", "cuanto",
}
TOPICS = {
    "Aritmética": ("aritmética", "divisibilidad", "fracción", "porcentaje", "razón", "proporción", "interés", "mezcla", "promedio"),
    "Álgebra": ("álgebra", "ecuación", "inecuación", "polinomio", "factorización", "logaritmo", "sucesión", "función"),
    "Geometría": ("geometría", "triángulo", "circunferencia", "ángulo", "área", "perímetro", "volumen", "recta", "polígono"),
    "Trigonometría": ("trigonometría", "seno", "coseno", "tangente", "identidad", "radian", "triángulo rectángulo"),
    "Probabilidad y estadística": ("probabilidad", "estadística", "combinatoria", "permutación", "varianza", "media", "mediana", "azar"),
    "Ciencias prácticas": ("ciencias practicas", "crp", "paideia", "seminario", "practiquemos", "simulacro"),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalize(text: str) -> str:
    return SPACE_RE.sub(" ", text.replace("\x00", " ")).strip()


def read_pages(path: Path) -> list[str]:
    if fitz is not None:
        document = fitz.open(path)
        try:
            return [normalize(page.get_text("text")) for page in document]
        finally:
            document.close()
    reader = PdfReader(str(path))
    return [normalize(page.extract_text() or "") for page in reader.pages]


def tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS]


def chunk_page(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    if len(words) <= size:
        return [text]
    stride = max(1, size - overlap)
    return [" ".join(words[start : start + size]) for start in range(0, len(words), stride) if words[start : start + size]]


def quality(pages: list[str]) -> str:
    chars = sum(len(page) for page in pages)
    populated = sum(bool(page) for page in pages)
    if populated == 0:
        return "scanned_or_no_extractable_text"
    if chars / max(1, len(pages)) < 80:
        return "low_text_needs_visual_or_ocr_review"
    return "usable_text"


def topic_hits(label: str, text: str) -> list[str]:
    haystack = (label + " " + text[:3000]).lower()
    return [name for name, clues in TOPICS.items() if any(clue in haystack for clue in clues)] or ["Por clasificar"]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_SOURCE / "_index")
    parser.add_argument("--chunk-words", type=int, default=220)
    parser.add_argument("--overlap-words", type=int, default=40)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    pdfs = sorted(path for path in source.rglob("*.pdf") if output not in path.parents)
    if not pdfs:
        raise SystemExit(f"No PDFs found under {source}")
    if source not in output.parents:
        raise SystemExit('The index output must stay inside the named material directory.')
    output.mkdir(parents=True, exist_ok=True)

    canonical: dict[str, dict] = {}
    aliases: dict[str, list[str]] = collections.defaultdict(list)
    failures: list[dict] = []
    for path in pdfs:
        sha = digest(path)
        aliases[sha].append(rel(path))
        if sha in canonical:
            continue
        try:
            pages = read_pages(path)
        except Exception as error:  # Keep the complete inventory even for corrupt PDFs.
            failures.append({"path": rel(path), "sha256": sha, "error": str(error)})
            canonical[sha] = {"path": rel(path), "sha256": sha, "pages": [], "error": str(error)}
            continue
        ocr = {}
        for number, native in enumerate(pages, 1):
            ocr_file = source / '_ocr' / sha[:16] / f'{number:03}.json'
            if len(native) < 80 and ocr_file.exists():
                result = json.loads(ocr_file.read_text(encoding='utf-8'))
                recovered = normalize(result.get('text', ''))
                if len(recovered) > len(native):
                    pages[number-1] = recovered
                    ocr[number] = result.get('confidence', 0)
        canonical[sha] = {"path": rel(path), "sha256": sha, "pages": pages, 'ocr':ocr}

    documents, chunks = [], []
    for doc_number, item in enumerate(canonical.values(), 1):
        pages = item["pages"]
        ocr = item.get('ocr', {})
        full_text = " ".join(pages)
        doc = {
            "document_id": f"doc-{doc_number:03d}", "path": item["path"], "sha256": item["sha256"],
            "aliases": aliases[item["sha256"]], "page_count": len(pages), "text_characters": len(full_text),
            "populated_pages": sum(bool(page) for page in pages), "extraction_quality": quality(pages),
            "topics": topic_hits(item["path"], full_text),
            'ocr_pages':len(ocr),
            'ocr_mean_confidence':round(sum(ocr.values())/len(ocr),1) if ocr else None,
        }
        if "error" in item:
            doc["error"] = item["error"]
        documents.append(doc)
        for page_number, page in enumerate(pages, 1):
            for part, text in enumerate(chunk_page(page, args.chunk_words, args.overlap_words), 1):
                chunks.append({"chunk_id": f"{doc['document_id']}-p{page_number:03d}-c{part:02d}", "document_id": doc["document_id"], "path": doc["path"], "page": page_number, "topics": topic_hits(doc["path"], text), "text": text, 'extraction':'ocr_needs_formula_review' if page_number in ocr else 'native_text', 'ocr_confidence':ocr.get(page_number)})

    # Transparent sparse TF-IDF: vocabulary, IDF and non-zero (term_id, weight) pairs.
    dfs: collections.Counter[str] = collections.Counter()
    chunk_terms: list[collections.Counter[str]] = []
    for chunk in chunks:
        counts = collections.Counter(tokens(chunk["text"]))
        chunk_terms.append(counts)
        dfs.update(counts.keys())
    vocabulary = sorted(term for term, count in dfs.items() if count >= 2)
    term_ids = {term: index for index, term in enumerate(vocabulary)}
    total = len(chunks)
    idf = [round(math.log((1 + total) / (1 + dfs[term])) + 1, 8) for term in vocabulary]
    with (output / "vectors.jsonl").open("w", encoding="utf-8") as handle:
        for chunk, counts in zip(chunks, chunk_terms):
            weights = {term_ids[term]: count * idf[term_ids[term]] for term, count in counts.items() if term in term_ids}
            norm = math.sqrt(sum(weight * weight for weight in weights.values())) or 1.0
            vector = [[term_id, round(weight / norm, 8)] for term_id, weight in sorted(weights.items())]
            handle.write(json.dumps({"chunk_id": chunk["chunk_id"], "vector": vector}, ensure_ascii=False) + "\n")
    with (output / "chunks.jsonl").open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    write_json(output / "documents.json", documents)
    write_json(output / "tfidf.json", {"method": "token TF-IDF with cosine similarity; no semantic embeddings", "token_pattern": TOKEN_RE.pattern, "stopwords": sorted(STOPWORDS), "vocabulary": vocabulary, "idf": idf})
    manifest = {"created_at": datetime.now(timezone.utc).isoformat(), "extractor": "PyMuPDF" if fitz else "pypdf fallback (PyMuPDF unavailable in this runtime)", "source": rel(source), "files_discovered": len(pdfs), "unique_documents": len(documents), "duplicate_file_copies": len(pdfs) - len(documents), "chunks": len(chunks), "failed_documents": len(failures), "chunk_words": args.chunk_words, "overlap_words": args.overlap_words}
    manifest['ocr_pages'] = sum(d['ocr_pages'] for d in documents)
    manifest['ocr_note'] = 'Local Spanish OCR; equations and diagrams require visual verification.'
    write_json(output / "manifest.json", manifest)
    write_json(output / "failures.json", failures)
    # This is deliberately publication-safe: it contains no extracted text,
    # questions, answers, chunks, hashes, or private absolute paths.
    public_data = ROOT / "data"
    public_data.mkdir(exist_ok=True)
    write_json(public_data / "source-map.json", {
        "schema_version": 1,
        "generated_from": "Informacion PDFs; metadata only",
        "corpus": {key: manifest[key] for key in ("files_discovered", "unique_documents", "duplicate_file_copies", "failed_documents")},
        "sources": [{key: doc[key] for key in ("path", "page_count", "extraction_quality", "topics", 'ocr_pages','ocr_mean_confidence')} for doc in documents],
    })
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
