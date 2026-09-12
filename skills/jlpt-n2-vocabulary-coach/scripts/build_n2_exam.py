#!/usr/bin/env python3
"""Validate authored exercises against the local corpus and render a quiz."""
import argparse
import json
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
        if q["type"] == "usage" and not all(row["word"] in x for x in options):
            raise ValueError(f"{identity}: all usage sentences must contain target")
        q["source"] = row
    return bank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=ROOT / "assets/n2-sample.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["practice", "exam"], default="practice")
    parser.add_argument("--type", choices=list(TYPES))
    parser.add_argument("--full", action="store_true", help="Require 5/5/3/7/5/5 questions")
    args = parser.parse_args()
    try:
        bank = validate(json.loads(args.bank.read_text(encoding="utf-8")))
        if args.type:
            bank["questions"] = [q for q in bank["questions"] if q["type"] == args.type]
        counts = {kind: sum(q["type"] == kind for q in bank["questions"]) for kind in TYPES}
        if not bank["questions"]:
            raise ValueError("No questions for selected type")
        if args.full and any(counts[k] != TYPES[k][1] for k in TYPES):
            raise ValueError(f"Full exam requires 5/5/3/7/5/5; available: {counts}")
        bank["mode"] = args.mode
        bank["types"] = {k: v[0] for k, v in TYPES.items()}
        bank["full"] = args.full
        data = json.dumps(bank, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
        template = (ROOT / "assets/n2-exam.html").read_text(encoding="utf-8")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(template.replace("__EXAM_DATA__", data), encoding="utf-8")
        print(json.dumps({"output": str(args.output.resolve()), "counts": counts}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Cannot build exam: {error}\n")


if __name__ == "__main__":
    main()
