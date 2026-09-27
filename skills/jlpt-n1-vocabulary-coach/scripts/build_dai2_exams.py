#!/usr/bin/env python3
"""Validate an authored dai2 bank, shuffle options and render five matched exams."""
import argparse
import copy
import json
import random
import subprocess
import sys
from pathlib import Path

from build_n1_exam import ROOT, TYPES, validate

PROJECT = ROOT.parent.parent
OUTPUT_DIR = PROJECT / "outputs" / "n1-dai2-tests"


def load_items():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/load_vocabulary.py"), "--level", "N1", "--lesson", "dai2"],
        capture_output=True, text=True, check=True,
    )
    items = json.loads(result.stdout)["items"]
    if len(items) != 100:
        raise ValueError(f"Expected 100 words in dai2.csv, found {len(items)}")
    return items


def prepare_groups(bank, items, seed):
    bank = validate(copy.deepcopy(bank))
    questions = bank["questions"]
    key = lambda row: (row["source_file"], row["source_line"], row["word"])
    if len(questions) != 100 or [key(q) for q in questions] != [key(x) for x in items]:
        raise ValueError("Bank must cover all 100 dai2 rows exactly once in CSV order")
    seen_distractors = set()
    for q in questions:
        if q["type"] in ("paraphrase", "usage"):
            signature = (q["type"], tuple(sorted(
                option.replace(q["word"], "<target>").strip()
                for index, option in enumerate(q["options"]) if index != q["answer"]
            )))
            if signature in seen_distractors:
                raise ValueError(f"{q['id']}: repeated distractor template; author context-specific options")
            seen_distractors.add(signature)
    rng = random.Random(seed)
    groups = []
    for start in range(0, 100, 20):
        group = questions[start:start + 20]
        if any(sum(q["type"] == kind for q in group) != 5 for kind in TYPES):
            raise ValueError(f"Group {start // 20 + 1} must contain five questions of each N1 type")
        for q in group:
            order = list(range(4))
            rng.shuffle(order)
            q["options"] = [q["options"][i] for i in order]
            q["explanations"] = [q["explanations"][i] for i in order]
            q["answer"] = order.index(q["answer"])
            q.pop("source", None)
        groups.append(group)
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", required=True, type=Path, help="Semantically reviewed authored 100-question dai2 bank")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    try:
        groups = prepare_groups(json.loads(args.bank.read_text(encoding="utf-8")), load_items(), args.seed)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        manifest = []
        for index, questions in enumerate(groups, 1):
            bank_path = args.output_dir / f"n1-dai2-test-{index}.json"
            html_path = args.output_dir / f"n1-dai2-test-{index}.html"
            bank_path.write_text(json.dumps({"level": "N1", "questions": questions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            subprocess.run([sys.executable, str(ROOT / "scripts/build_n1_exam.py"), "--bank", str(bank_path),
                            "--mode", "exam", "--output", str(html_path)], check=True)
            manifest.append({"test": index, "range": [(index - 1) * 20 + 1, index * 20],
                             "words": [q["word"] for q in questions], "html": html_path.name,
                             "bank": bank_path.name, "seed": args.seed})
        (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output_dir": str(args.output_dir.resolve()), "tests": 5, "questions": 100}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Cannot build dai2 exams: {error}\n")


if __name__ == "__main__":
    main()
