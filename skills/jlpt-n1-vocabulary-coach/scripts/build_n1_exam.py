#!/usr/bin/env python3
"""Validate N1 exercises against the local corpus and render a quiz."""
import argparse
import csv
import json
import random
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = {
    "reading": ("漢字読み · Đọc kanji", 6),
    "context": ("文脈規定 · Ngữ cảnh", 7),
    "paraphrase": ("言い換え類義 · Gần nghĩa", 6),
    "usage": ("用法 · Cách dùng", 6),
}


def normalized_readings(value):
    value = unicodedata.normalize("NFKC", value).strip()
    value = re.sub(r"\s*\((?:する|な)\)$", "", value)
    return {part.strip() for part in re.split(r"[/／]", value)}


def load_sources(bank):
    """Read only lessons referenced by targets or attested reading options."""
    refs = list(bank.get("questions", []))
    refs += [entry for q in bank.get("questions", []) for entry in q.get("option_lexemes", [])]
    files = {ref.get("source_file", "") for ref in refs}
    source = {}
    headers = ["từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ"]
    for name in sorted(files):
        if not re.fullmatch(r"resources/N1/goi/dai[0-9]+\.csv", name):
            raise ValueError(f"Invalid N1 CSV source: {name}")
        with (ROOT.parent.parent / name).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != headers:
                raise ValueError(f"Unexpected columns in {name}")
            for line, row in enumerate(reader, 2):
                source[(name, line)] = dict(zip(
                    ["word", "reading", "meaning_vi", "example"],
                    [row[h] for h in headers],
                ), source_file=name, source_line=line)
    return source


def validate(bank):
    if bank.get("level") != "N1":
        raise ValueError("This exercise format is for N1")
    questions = bank.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions must be a nonempty list")
    source = load_sources(bank)
    seen = set()
    for q in questions:
        identity = q.get("id")
        if not isinstance(identity, str) or not identity.strip() or identity in seen:
            raise ValueError("Each question needs a unique nonempty id")
        seen.add(identity)
        if q.get("type") not in TYPES or q.get("origin") != "authored":
            raise ValueError(f"{identity}: invalid N1 type/origin")
        row = source.get((q.get("source_file"), q.get("source_line")))
        if row is None or row["word"] != q.get("word"):
            raise ValueError(f"{identity}: target does not match N1 CSV source")
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
        if q["type"] in ("reading", "paraphrase"):
            if prompt.count("【") != 1 or prompt.count("】") != 1 or prompt.index("【") >= prompt.index("】") - 1:
                raise ValueError(f"{identity}: mark exactly one target with brackets")
        if q["type"] == "context" and prompt.count("（　）") != 1:
            raise ValueError(f"{identity}: exactly one blank required")
        if q["type"] == "reading":
            if not re.search(r"[一-龯々]", row["word"]):
                raise ValueError(f"{identity}: reading target must contain kanji")
            marked = prompt.split("【", 1)[1].split("】", 1)[0]
            # Strip only known grammar notes; the marked target stays uninflected.
            readings = normalized_readings(row["reading"])
            normalized_options = [unicodedata.normalize("NFKC", x).strip() for x in options]
            if marked != row["word"]:
                raise ValueError(f"{identity}: reading brackets must contain the exact CSV target")
            if not all(re.fullmatch(r"[ぁ-ゖァ-ヺー・]+", x) for x in normalized_options):
                raise ValueError(f"{identity}: reading options must be kana")
            matches = [i for i, option in enumerate(normalized_options) if option in readings]
            if matches != [q["answer"]]:
                raise ValueError(f"{identity}: reading answer must uniquely match the CSV reading")
            if bank.get("reading_policy") == "attested-csv":
                lexemes = q.get("option_lexemes")
                if not isinstance(lexemes, list) or len(lexemes) != 4:
                    raise ValueError(f"{identity}: four attested reading options required")
                for option, entry in zip(normalized_options, lexemes):
                    witness = source.get((entry.get("source_file"), entry.get("source_line")))
                    if (witness is None or witness["word"] != entry.get("word")
                            or entry.get("reading") != option
                            or option not in normalized_readings(witness["reading"])):
                        raise ValueError(f"{identity}: unattested reading option {option}")
        if q["type"] == "usage" and not all(row["word"] in x for x in options):
            raise ValueError(f"{identity}: all usage sentences must contain target")
        q["source"] = row
    selection = bank.get("selection")
    if selection is not None:
        count, seed = selection.get("count"), selection.get("seed")
        name = selection.get("source_file")
        if (selection.get("method") != "random.sample" or type(seed) is not int
                or type(count) is not int or count < 1 or count != len(questions)
                or name != f"resources/N1/goi/{bank.get('lesson')}.csv"):
            raise ValueError("Invalid random selection metadata")
        population = [row for (filename, _), row in source.items() if filename == name]
        expected = {row["source_line"] for row in random.Random(seed).sample(population, count)}
        if (any(q["source_file"] != name for q in questions)
                or {q["source_line"] for q in questions} != expected
                or len({q["word"] for q in questions}) != count):
            raise ValueError("Questions must match the unique random lesson selection")
        counts = [sum(q["type"] == kind for q in questions) for kind in TYPES]
        if max(counts) - min(counts) > 1:
            # Do not turn kana-only entries into questions that display their answer.
            # Scarcity is derived from the actual selected CSV rows, not bank claims.
            kanji_count = sum(bool(re.search(r"[一-龯々]", q["word"])) for q in questions)
            remaining = counts[1:]
            if not (kanji_count < count // 4 and counts[0] == kanji_count
                    and max(remaining) - min(remaining) <= 1):
                raise ValueError("Random lesson exams must balance N1 types, allowing only source-based kanji scarcity")
    return bank


def render(bank, mode="exam", home_href=None, full=False):
    bank = validate(bank)
    bank["mode"] = mode
    bank["types"] = {k: v[0] for k, v in TYPES.items()}
    bank["full"] = full
    if home_href:
        bank["home_href"] = home_href
    data = json.dumps(bank, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")
    template = (ROOT / "assets/n1-exam.html").read_text(encoding="utf-8")
    return template.replace("__EXAM_DATA__", data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=ROOT / "assets/n1-sample.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["practice", "exam"], default="practice")
    parser.add_argument("--type", choices=list(TYPES))
    parser.add_argument("--full", action="store_true", help="Require 6/7/6/6 questions")
    args = parser.parse_args()
    try:
        bank = validate(json.loads(args.bank.read_text(encoding="utf-8")))
        if args.type:
            bank["questions"] = [q for q in bank["questions"] if q["type"] == args.type]
            bank.pop("selection", None)
        counts = {kind: sum(q["type"] == kind for q in bank["questions"]) for kind in TYPES}
        if not bank["questions"]:
            raise ValueError("No questions for selected type")
        if args.full and any(counts[k] != TYPES[k][1] for k in TYPES):
            raise ValueError(f"Full N1 exam requires 6/7/6/6; available: {counts}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render(bank, args.mode, full=args.full), encoding="utf-8")
        print(json.dumps({"output": str(args.output.resolve()), "counts": counts}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f"Cannot build N1 exam: {error}\n")


if __name__ == "__main__":
    main()
