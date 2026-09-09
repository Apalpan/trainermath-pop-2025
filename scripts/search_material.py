#!/usr/bin/env python3
"""Query Informacion/_index with the same local TF-IDF + cosine model."""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "Informacion" / "_index"


def query_tokens(text: str, stopwords: set[str]) -> list[str]:
    return [value.lower() for value in re.findall(r"[a-záéíóúüñ]+(?:\d+)?|\d+(?:[.,]\d+)?", text, re.I) if value.lower() not in stopwords]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    model = json.loads((INDEX / "tfidf.json").read_text(encoding="utf-8"))
    lookup = {term: index for index, term in enumerate(model["vocabulary"])}
    counts = collections.Counter(query_tokens(args.query, set(model["stopwords"])))
    weighted = {lookup[term]: count * model["idf"][lookup[term]] for term, count in counts.items() if term in lookup}
    norm = math.sqrt(sum(value * value for value in weighted.values()))
    if not norm:
        raise SystemExit("No indexed query terms. Use terms present in the source material.")
    weighted = {term: value / norm for term, value in weighted.items()}
    vectors = {row["chunk_id"]: dict(row["vector"]) for row in (json.loads(line) for line in (INDEX / "vectors.jsonl").read_text(encoding="utf-8").splitlines())}
    scored = []
    for row in (json.loads(line) for line in (INDEX / "chunks.jsonl").read_text(encoding="utf-8").splitlines()):
        score = sum(weight * vectors[row["chunk_id"]].get(term, 0.0) for term, weight in weighted.items())
        if score:
            scored.append((score, row))
    for score, row in sorted(scored, reverse=True, key=lambda pair: pair[0])[: args.limit]:
        preview = re.sub(r"\s+", " ", row["text"])[:260]
        print(f"{score:.3f}\t{row['path']} p.{row['page']}\t{', '.join(row['topics'])} [{row.get('extraction','native_text')}]\n  {preview}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
