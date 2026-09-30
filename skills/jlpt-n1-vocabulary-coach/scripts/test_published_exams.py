"""Check published selections and reject broken answer/evidence pairings."""
import copy
import json
import unittest
from collections import Counter

from build_n1_exam import ROOT, validate, render


class PublishedExamsTests(unittest.TestCase):
    def setUp(self):
        self.banks = [json.loads((ROOT.parent.parent / f"resources/N1/exams/dai{n}.json").read_text())
                      for n in range(1, 31)]

    def test_all_thirty_random_banks_and_balanced_answer_positions(self):
        for n, bank in enumerate(self.banks, 1):
            with self.subTest(lesson=n):
                validate(bank)
                qs = bank["questions"]
                self.assertEqual(len(qs), 30)
                self.assertEqual(len({q["word"] for q in qs}), 30)
                self.assertEqual({q["source_file"] for q in qs}, {f"resources/N1/goi/dai{n}.csv"})
                self.assertEqual(sorted(Counter(q["answer"] for q in qs).values()), [7, 7, 8, 8])
                readings = [q for q in qs if q["type"] == "reading"]
                self.assertEqual(len(readings), 7 if n == 7 else 8)
                self.assertTrue(all(len(q["option_lexemes"]) == 4 for q in readings))

    def test_fake_reading_even_with_correct_answer_is_rejected(self):
        bank = self.banks[0]
        q = bank["questions"][0]
        slot = (q["answer"] + 1) % 4
        q["options"][slot] = "あいうえお"
        q["option_lexemes"][slot]["reading"] = "あいうえお"
        with self.assertRaisesRegex(ValueError, "unattested"):
            validate(bank)

    def test_missing_or_misaligned_reading_evidence_is_rejected(self):
        for mutate in (lambda q: q.pop("option_lexemes"),
                       lambda q: q["option_lexemes"].reverse()):
            bank = copy.deepcopy(self.banks[0])
            mutate(bank["questions"][0])
            with self.assertRaises(ValueError):
                validate(bank)

    def test_selection_cannot_be_changed_or_repeat_a_word(self):
        for mutate in (lambda b: b["selection"].update(seed=1),
                       lambda b: b["questions"].__setitem__(1, dict(b["questions"][0], id="duplicate-target"))):
            bank = copy.deepcopy(self.banks[0])
            mutate(bank)
            with self.assertRaisesRegex(ValueError, "random lesson selection"):
                validate(bank)

    def test_wrong_reading_answer_is_rejected(self):
        bank = self.banks[0]
        q = bank["questions"][0]
        q["answer"] = (q["answer"] + 1) % 4
        with self.assertRaisesRegex(ValueError, "uniquely"):
            validate(bank)

    def test_render_retains_title_exam_mode_and_home_link(self):
        html = render(self.banks[0], mode="exam", home_href="../../#/exams/N1")
        payload = json.loads(html.split('id="exam-data">', 1)[1].split('</script>', 1)[0])
        self.assertEqual(payload["title"], "N1 · Bài 1 · 30 câu")
        self.assertEqual(payload["mode"], "exam")
        self.assertEqual(payload["home_href"], "../../#/exams/N1")
        self.assertEqual(len(payload["questions"]), 30)
        self.assertNotIn("__EXAM_DATA__", html)


if __name__ == "__main__":
    unittest.main()
