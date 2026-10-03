#!/usr/bin/env python3
"""Validate authored exercises against the local corpus and render a quiz."""
import argparse
import json
import re
import unicodedata
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = {
    "reading": ("漢字読み · Đọc kanji", 5),
    "orthography": ("表記 · Cách viết", 5),
    "formation": ("語形成 · Cấu tạo từ", 3),
    "context": ("文脈規定 · Ngữ cảnh", 7),
    "paraphrase": ("言い換え類義 · Gần nghĩa", 5),
    "usage": ("用法 · Cách dùng", 5),
}


def validate(bank):
    if bank.get("level") != "N2":
        raise ValueError("This exercise format is for N2")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/load_vocabulary.py"),
                             "--level", "N2"], capture_output=True, text=True, check=True)
    corpus = json.loads(result.stdout)["items"]
    source = {(x["source_file"], x["source_line"]): x for x in corpus}
    evidence_source = None
    questions = bank.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions must be a nonempty list")
    seen = set()
    for q in questions:
        identity = q.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            raise ValueError("Each question needs a unique nonempty id")
        seen.add(identity)
        if q.get("type") not in TYPES or q.get("origin") != "authored":
            raise ValueError(f"{identity}: invalid type/origin")
        row = source.get((q.get("source_file"), q.get("source_line")))
        if row is None or row["word"] != q.get("word"):
            raise ValueError(f"{identity}: target does not match CSV source")
        options, explanations = q.get("options"), q.get("explanations")
        for name, values in [("options", options), ("explanations", explanations)]:
            if not isinstance(values, list) or len(values) != 4 or not all(isinstance(x, str) and x.strip() for x in values):
                raise ValueError(f"{identity}: {name} must contain four nonempty strings")
        if len(set(x.strip() for x in options)) != 4:
            raise ValueError(f"{identity}: duplicate options")
        if type(q.get("answer")) is not int or not 0 <= q["answer"] < 4:
            raise ValueError(f"{identity}: answer must be index 0..3")
        prompt = q.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError(f"{identity}: missing prompt")
        if q["type"] in ("reading", "orthography", "paraphrase"):
            if prompt.count("【") != 1 or prompt.count("】") != 1 or prompt.index("【") >= prompt.index("】") - 1:
                raise ValueError(f"{identity}: mark exactly one target with brackets")
        if q["type"] in ("formation", "context") and prompt.count("（　）") != 1:
            raise ValueError(f"{identity}: exactly one blank required")
        if q["type"] == "formation":
            form = q.get("formation", {})
            if not all(isinstance(form.get(k), str) for k in ("prefix", "suffix")):
                raise ValueError(f"{identity}: formation needs prefix/suffix")
            if not form["prefix"] and not form["suffix"]:
                raise ValueError(f"{identity}: formation must leave part of the word visible")
            if form["prefix"] + options[q["answer"]] + form["suffix"] != row["word"]:
                raise ValueError(f"{identity}: formation must reconstruct the CSV target")
        if q["type"] in ("reading", "orthography"):
            marked = prompt.split("【", 1)[1].split("】", 1)[0]
            # Remove only the corpus's grammatical annotations, not arbitrary text.
            reading = unicodedata.normalize("NFKC", row["reading"]).strip()
            reading = re.sub(r"\s*\((?:する|な)\)$", "", reading)
            readings = {part.strip() for part in re.split(r"[/／]", reading)}
            kana = lambda value: unicodedata.normalize("NFKC", value).strip()
            if q["type"] == "reading":
                if marked != row["word"]:
                    raise ValueError(f"{identity}: reading brackets must contain the exact CSV target")
                if not all(re.fullmatch(r"[ぁ-ゖァ-ヺー・]+", kana(x)) for x in options):
                    raise ValueError(f"{identity}: reading options must be kana")
                matches = [i for i, option in enumerate(options) if kana(option) in readings]
                if matches != [q["answer"]]:
                    raise ValueError(f"{identity}: reading answer must uniquely match the CSV reading")
                if "option_lexemes" in q:
                    if evidence_source is None:
                        n1_result = subprocess.run([sys.executable, str(ROOT / "scripts/load_vocabulary.py"),
                                                    "--level", "N1"], capture_output=True, text=True, check=True)
                        evidence_source = {**source, **{
                            (x["source_file"], x["source_line"]): x
                            for x in json.loads(n1_result.stdout)["items"]}}
                    lexemes = q["option_lexemes"]
                    if not isinstance(lexemes, list) or len(lexemes) != 4:
                        raise ValueError(f"{identity}: four reading lexemes required")
                    for option, lexeme in zip(options, lexemes):
                        if not isinstance(lexeme, dict):
                            raise ValueError(f"{identity}: invalid reading lexeme")
                        evidence = evidence_source.get((lexeme.get("source_file"), lexeme.get("source_line")))
                        if evidence is None or evidence["word"] != lexeme.get("word"):
                            raise ValueError(f"{identity}: unattested reading lexeme")
                        evidence_reading = re.sub(r"\s*\((?:する|な)\)$", "", kana(evidence["reading"]))
                        if kana(lexeme.get("reading", "")) != kana(option) or kana(option) not in {
                                part.strip() for part in re.split(r"[/／]", evidence_reading)}:
                            raise ValueError(f"{identity}: reading lexeme does not match its option")
            elif options[q["answer"]] != row["word"] or kana(marked) not in readings:
                raise ValueError(f"{identity}: orthography answer/marked reading must match CSV")
        if q["type"] == "usage" and not all(row["word"] in x for x in options):
            raise ValueError(f"{identity}: all usage sentences must contain target")
        q["source"] = row
    return bank


def render(bank, mode="exam", home_href=None, full=False):
    """Render a validated N2 bank for a standalone file or the web app."""
    bank = validate(bank)
    counts = {kind: sum(q["type"] == kind for q in bank["questions"]) for kind in TYPES}
    if full and any(counts[k] != TYPES[k][1] for k in TYPES):
        raise ValueError(f"Full exam requires 5/5/3/7/5/5; available: {counts}")
    bank["mode"] = mode
    bank["types"] = {k: v[0] for k, v in TYPES.items()}
    bank["full"] = full
    if home_href is not None:
        bank["home_href"] = home_href
    data = json.dumps(bank, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    template = (ROOT / "assets/n2-exam.html").read_text(encoding="utf-8")
    return template.replace("__EXAM_DATA__", data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=ROOT / "assets/n2-sample.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["practice", "exam"], default="practice")
    parser.add_argument("--type", choices=list(TYPES))
    parser.add_argument("--full", action="store_true", help="Require 5/5/3/7/5/5 questions")
    args = parser.parse_args()
    try:
        bank = json.loads(args.bank.read_text(encoding="utf-8"))
        if args.type:
            bank["questions"] = [q for q in bank["questions"] if q["type"] == args.type]
        if not bank["questions"]:
            raise ValueError("No questions for selected type")
        html = render(bank, mode=args.mode, full=args.full)
        counts = {kind: sum(q["type"] == kind for q in bank["questions"]) for kind in TYPES}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
        print(json.dumps({"output": str(args.output.resolve()), "counts": counts}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Cannot build exam: {error}\n")


if __name__ == "__main__":
    main()
