import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import load_vocabulary

SCRIPTS = Path(__file__).resolve().parent


class FlashcardsTest(unittest.TestCase):
    def test_entire_corpus_has_complete_annotations(self):
        for level in ('N1', 'N2'):
            source = subprocess.check_output(
                [sys.executable, str(SCRIPTS / 'load_vocabulary.py'), '--level', level], text=True)
            items = json.loads(source)['items']
            self.assertTrue(items)
            for item in items:
                with self.subTest(source=item['source_file'], word=item['word']):
                    self.assertTrue(item.get('example_vi', '').strip())
                    self.assertTrue(item.get('example_segments'))
                    self.assertTrue(item.get('example_notes_source'))

    def test_target_inflections(self):
        for segment, valid in (({'text': '飽きた', 'target': True}, True),
                               ({'text': '飽きた', 'target': True, 'reading': 'あきた'}, False),
                               ({'text': '食べた', 'target': True}, False)):
            with self.subTest(segment=segment), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'dai1.csv'
                entry = {'word': '飽きる', 'example': segment['text'] + '。',
                         'example_vi': 'Đã chán.', 'example_segments': [segment, {'text': '。'}]}
                path.with_suffix('.examples.json').write_text(json.dumps({'version': 1, 'items': [entry]}))
                with patch.object(load_vocabulary, 'RESOURCE_ROOT', Path(folder) / 'resources'):
                    if valid:
                        notes, _ = load_vocabulary.load_examples(path)
                        self.assertEqual(notes[('飽きる', '飽きた。')], entry)
                    else:
                        with self.assertRaises(SystemExit):
                            load_vocabulary.load_examples(path)

    def test_n1_annotations_preserve_all_sentences(self):
        source = subprocess.check_output(
            [sys.executable, str(SCRIPTS / 'load_vocabulary.py'),
             '--level', 'N1', '--lesson', 'dai1'], text=True)
        items = json.loads(source)['items']
        self.assertEqual(len(items), 100)
        for item in items:
            self.assertTrue(item['example_vi'].strip())
            self.assertEqual(''.join(s['text'] for s in item['example_segments']), item['example'])
            for segment in item['example_segments']:
                if 'reading' in segment:
                    self.assertNotIn(item['word'], segment['text'])
                else:
                    self.assertIsNone(re.search('[一-龯々]', segment['text'].replace(item['word'], '')))

    def test_invalid_annotations_rejected(self):
        for segments in ([{'text': '別の文'}],
                         [{'text': '無理が悪化する。'}],
                         [{'text': '無理', 'reading': 'むり'}, {'text': 'が'},
                          {'text': '悪化', 'reading': 'あっか'}, {'text': 'する。'}]):
            with self.subTest(segments=segments), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'dai1.csv'
                path.with_suffix('.examples.json').write_text(json.dumps({
                    'version': 1, 'items': [{'word': '悪化', 'example': '無理が悪化する。',
                    'example_vi': 'Bản dịch', 'example_segments': segments}]}))
                with self.assertRaises(SystemExit):
                    load_vocabulary.load_examples(path)

    def test_missing_sidecar_compatible(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(load_vocabulary.load_examples(Path(folder) / 'dai1.csv'), ({}, None))

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

    def test_no_javascript_fallback_contains_every_selected_card(self):
        result, html = self.build("--lesson", "dai1", "--limit", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
        fallback = no_scripts.split('<section id="fc-interactive"', 1)[0]
        self.assertIn('<section id="fc-static"', fallback)
        self.assertEqual(fallback.count('class="fc-static-card"'), 3)
        source = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "load_vocabulary.py"),
             "--level", "N2", "--lesson", "dai1", "--limit", "3"], text=True))
        for item in source["items"]:
            with self.subTest(word=item["word"]):
                self.assertIn(item["word"], fallback)
                self.assertIn(item["reading"], fallback)
                self.assertIn(item["meaning_vi"], fallback)
                self.assertIn(item["example_vi"], fallback)
                self.assertIn(f'{item["source_file"]}:{item["source_line"]}', fallback)

    def test_offset_selects_a_contiguous_card_set(self):
        result, html = self.build("--lesson", "dai1", "--offset", "2", "--limit", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(re.search(r'id="fc-data">(.*?)</script>', html, re.S)[1])
        source = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "load_vocabulary.py"),
             "--level", "N2", "--lesson", "dai1"], text=True))
        self.assertEqual(payload["items"], source["items"][2:5])
        self.assertEqual(payload["count"], 3)

    def test_interactive_ui_activates_only_after_render(self):
        result, html = self.build("--lesson", "dai1", "--limit", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('<section id="fc-interactive" hidden', html)
        render_at = html.rindex("render();")
        reveal_at = html.rindex("get('fc-interactive').hidden=false;")
        hide_fallback_at = html.rindex("get('fc-static').hidden=true;")
        self.assertLess(render_at, reveal_at)
        self.assertLess(reveal_at, hide_fallback_at)

    def test_exact_review_list_and_missing_word(self):
        result, html = self.build("--word", "価格")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(re.search(r'id="fc-data">(.*?)</script>', html, re.S)[1])
        self.assertTrue(data["items"])
        self.assertTrue(all(item["word"] == "価格" for item in data["items"]))
        result, html = self.build("--word", "NOT_IN_CORPUS")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(html, "")

    def test_word_cannot_be_combined_with_offset(self):
        result, html = self.build("--word", "価格", "--offset", "1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--word cannot be combined", result.stderr)
        self.assertEqual(html, "")

    def test_missing_lesson(self):
        result, html = self.build("--lesson", "not_present")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(html, "")


if __name__ == "__main__":
    unittest.main()
