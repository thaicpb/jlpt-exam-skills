import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


class FlashcardsTest(unittest.TestCase):
    def build(self, *args):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "cards.html"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "build_flashcards.py"),
                 "--level", "N2", *args, "--output", str(output)],
                capture_output=True, text=True)
            return result, output.read_text() if output.exists() else ""

    def test_preserves_source_without_exercise_fields(self):
        result, html = self.build("--lesson", "dai1", "--limit", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(re.search(r'id="fc-data">(.*?)</script>', html, re.S)[1])
        source = subprocess.check_output(
            [sys.executable, str(SCRIPTS / "load_vocabulary.py"),
             "--level", "N2", "--lesson", "dai1", "--limit", "3"], text=True)
        self.assertEqual(payload, json.loads(source))
        self.assertEqual(len(payload["items"]), 3)

    def test_exact_review_list_and_missing_word(self):
        result, html = self.build("--word", "価格")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(re.search(r'id="fc-data">(.*?)</script>', html, re.S)[1])
        self.assertTrue(data["items"])
        self.assertTrue(all(item["word"] == "価格" for item in data["items"]))
        result, html = self.build("--word", "NOT_IN_CORPUS")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(html, "")

    def test_missing_lesson(self):
        result, html = self.build("--lesson", "not_present")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(html, "")


if __name__ == "__main__":
    unittest.main()
