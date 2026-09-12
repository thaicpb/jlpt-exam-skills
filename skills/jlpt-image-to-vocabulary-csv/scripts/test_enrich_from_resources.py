#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("enrich_from_resources.py")
HEADERS = ["từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ"]


class EnrichFromResourcesTest(unittest.TestCase):
    def write_csv(self, path: Path, rows: list[dict[str, str]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(rows)

    def run_script(self, source: Path, resources: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(source),
                "--resources",
                str(resources),
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_enriches_kanji_only_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            resources = root / "resources"
            expected = dict(zip(HEADERS, ["穴", "あな", "lỗ; hang", "壁に穴がある。"]))
            self.write_csv(resources / "N2/goi/dai1.csv", [expected])
            source = root / "input.json"
            output = root / "output.json"
            source.write_text('["穴"]', encoding="utf-8")

            result = self.run_script(source, resources, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [expected])

    def test_preserves_values_from_image(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            resources = root / "resources"
            stored = dict(zip(HEADERS, ["穴", "あな", "nghĩa cũ", "壁に穴がある。"]))
            self.write_csv(resources / "N2/goi/dai1.csv", [stored])
            source = root / "input.json"
            output = root / "output.json"
            source.write_text(
                json.dumps([{"từ mới": "穴", "nghĩa tiếng việt": "nghĩa trên ảnh"}], ensure_ascii=False),
                encoding="utf-8",
            )

            result = self.run_script(source, resources, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(output.read_text(encoding="utf-8"))[0]
            self.assertEqual(row["nghĩa tiếng việt"], "nghĩa trên ảnh")
            self.assertEqual(row["cách đọc"], "あな")

    def test_leaves_conflicting_field_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            resources = root / "resources"
            first = dict(zip(HEADERS, ["生", "せい", "sự sống", "生命を守る。"]))
            second = dict(zip(HEADERS, ["生", "なま", "tươi; sống", "生の魚を食べる。"]))
            self.write_csv(resources / "N2/goi/dai1.csv", [first])
            self.write_csv(resources / "N3/goi/dai1.csv", [second])
            source = root / "input.json"
            output = root / "output.json"
            source.write_text('["生"]', encoding="utf-8")

            result = self.run_script(source, resources, output)

            self.assertEqual(result.returncode, 2)
            row = json.loads(output.read_text(encoding="utf-8"))[0]
            self.assertEqual(row["cách đọc"], "")
            self.assertIn("conflict", result.stderr)
            self.assertIn("dai1.csv:2", result.stderr)


if __name__ == "__main__":
    unittest.main()
