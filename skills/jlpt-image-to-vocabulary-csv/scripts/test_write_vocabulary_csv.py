#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("write_vocabulary_csv.py")
HEADERS = ["từ mới", "cách đọc", "nghĩa tiếng việt", "ví dụ sử dụng minh hoạ"]


class WriteVocabularyCsvTest(unittest.TestCase):
    def run_script(self, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_writes_bom_exact_header_and_normalized_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "rows.json"
            output = root / "lesson.csv"
            source.write_text(
                json.dumps(
                    [{
                        "từ mới": "  穴  ",
                        "cách đọc": "あな",
                        "nghĩa tiếng việt": "lỗ;  hang",
                        "ví dụ sử dụng minh hoạ": "壁に小さな穴が\n開いている。",
                    }],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = self.run_script("--input", source, "--output", output)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.read_bytes().startswith(b"\xef\xbb\xbf"))
            with output.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(list(rows[0]), HEADERS)
            self.assertEqual(rows[0]["từ mới"], "穴")
            self.assertEqual(rows[0]["nghĩa tiếng việt"], "lỗ; hang")
            self.assertEqual(rows[0]["ví dụ sử dụng minh hoạ"], "壁に小さな穴が 開いている。")

    def test_rejects_empty_cell_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "rows.json"
            source.write_text(
                json.dumps([dict.fromkeys(HEADERS, "")], ensure_ascii=False),
                encoding="utf-8",
            )
            result = self.run_script("--input", source, "--output", root / "lesson.csv")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("empty columns", result.stderr)

    def test_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "rows.json"
            output = root / "lesson.csv"
            source.write_text(
                json.dumps([dict.fromkeys(HEADERS, "x")], ensure_ascii=False),
                encoding="utf-8",
            )
            output.write_text("keep", encoding="utf-8")
            result = self.run_script("--input", source, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
