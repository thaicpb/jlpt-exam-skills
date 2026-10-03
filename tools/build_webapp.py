#!/usr/bin/env python3
"""Build the flashcard web app (PWA) from resources/ into dist/.

Usage: python3 tools/build_webapp.py [--output dist]

Data is loaded through the flashcard skill's loader, so the web app uses the
same validation as the skills (CSV schema, furigana annotations, stale notes).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RESOURCES = PROJECT / "resources"
WEBAPP = PROJECT / "webapp"
LOADER = PROJECT / "skills/jlpt-vocabulary-flashcards/scripts/load_vocabulary.py"
EXAM_BUILDERS = {
    "N1": PROJECT / "skills/jlpt-n1-vocabulary-coach/scripts/build_n1_exam.py",
    "N2": PROJECT / "skills/jlpt-n2-vocabulary-coach/scripts/build_n2_exam.py",
}


def build_exams(level: str, lessons: list[str], out: Path, digest) -> list[dict]:
    banks = sorted((RESOURCES / level / "exams").glob("*.json"), key=lambda p: lesson_number(p.stem))
    if not banks:
        return []
    if level not in EXAM_BUILDERS:
        raise ValueError(f"No exam builder configured for {level}")
    spec = importlib.util.spec_from_file_location(f"{level.lower()}_exam_builder", EXAM_BUILDERS[level])
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    exams = []
    for path in banks:
        bank = json.loads(path.read_text(encoding="utf-8"))
        if (bank.get("lesson") != path.stem or path.stem not in lessons
                or bank.get("id") != f"{level.lower()}-{path.stem}-30"
                or not isinstance(bank.get("title"), str) or not bank["title"].strip()
                or (level == "N1" and (bank.get("reading_policy") != "attested-csv"
                    or bank.get("selection", {}).get("count") != 30))
                or (level == "N2" and (len(bank.get("questions", [])) != 30
                    or len({q.get("source_line") for q in bank["questions"]}) != 30
                    or {q.get("source_file") for q in bank["questions"]}
                    != {f"resources/N2/goi/{path.stem}.csv"}))):
            raise ValueError(f"Invalid published exam metadata: {path}")
        rel = f"exams/{level}/{path.stem}.html"
        html = builder.render(bank, mode="exam", home_href=f"../../#/exams/{level}",
                              **({"full": True} if level == "N2" else {}))
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        digest.update(rel.encode() + html.encode())
        exams.append({"id": bank["id"], "lesson": path.stem, "title": bank["title"],
                      "count": len(bank["questions"]), "file": rel,
                      "type_count": len({q["type"] for q in bank["questions"]})})
    return exams


def lesson_number(stem: str) -> int:
    match = re.search(r"\d+", stem)
    return int(match.group()) if match else 10**6


def load_lesson(level: str, lesson: str) -> list[dict]:
    result = subprocess.run(
        [sys.executable, str(LOADER), "--level", level, "--lesson", lesson],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"Loader failed for {level}/{lesson}: {result.stderr.strip() or result.stdout.strip()}")
    items = json.loads(result.stdout)["items"]
    cards = []
    for item in items:
        card = {"w": item["word"], "r": item["reading"], "m": item["meaning_vi"], "e": item["example"]}
        if item.get("example_vi"):
            card["t"] = item["example_vi"]
        segments = item.get("example_segments")
        if segments:
            card["s"] = [
                [s["text"], 1] if s.get("target") is True
                else [s["text"], s["reading"]] if s.get("reading")
                else [s["text"]]
                for s in segments
            ]
        cards.append(card)
    return cards


def dump(path: Path, data) -> bytes:
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PROJECT / "dist")
    args = parser.parse_args()
    out: Path = args.output.resolve()
    if out == PROJECT or PROJECT.is_relative_to(out):
        raise SystemExit("Refusing to write into the project root")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    digest = hashlib.sha256()
    catalog = {"levels": []}
    data_files = []
    for level_dir in sorted(RESOURCES.glob("N[1-5]")):
        goi = level_dir / "goi"
        stems = sorted((p.stem for p in goi.glob("*.csv")), key=lesson_number)
        if not stems:
            continue
        lessons = []
        for stem in stems:
            cards = load_lesson(level_dir.name, stem)
            rel = f"data/{level_dir.name}/{stem}.json"
            digest.update(dump(out / rel, cards))
            data_files.append(rel)
            lessons.append({"id": stem, "title": f"Bài {lesson_number(stem)}", "count": len(cards), "file": rel})
        exams = build_exams(level_dir.name, stems, out, digest)
        data_files.extend(exam["file"] for exam in exams)
        catalog["levels"].append({"id": level_dir.name, "lessons": lessons, "exams": exams})

    static_files = []
    for src in sorted(WEBAPP.rglob("*")):
        if src.is_file() and src.name != ".DS_Store" and src.name != "sw.js":
            rel = src.relative_to(WEBAPP).as_posix()
            dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            digest.update(rel.encode() + src.read_bytes())
            static_files.append(rel)

    # Navigation/cache changes must also invalidate an already-installed PWA.
    digest.update((WEBAPP / "sw.js").read_bytes())
    version = digest.hexdigest()[:12]
    catalog["version"] = version
    dump(out / "data/catalog.json", catalog)

    precache = ["./"] + [f for f in static_files if f != "index.html"] + ["data/catalog.json"] + data_files
    sw = (WEBAPP / "sw.js").read_text(encoding="utf-8")
    sw = sw.replace("__VERSION__", version).replace("__PRECACHE__", json.dumps(precache, ensure_ascii=False))
    (out / "sw.js").write_text(sw, encoding="utf-8")
    (out / ".nojekyll").write_text("")

    total = sum(len(l["lessons"]) for l in catalog["levels"])
    words = sum(x["count"] for l in catalog["levels"] for x in l["lessons"])
    exams = sum(len(level["exams"]) for level in catalog["levels"])
    print(f"Built {out} · version {version} · {total} lessons · {words} cards · {exams} exams")


if __name__ == "__main__":
    main()
