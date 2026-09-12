"""Check corpus provenance and malformed question rejection."""
import copy
import json
import unittest
from build_n2_exam import ROOT, validate


class ExamValidationTests(unittest.TestCase):
    def setUp(self):
        self.bank = json.loads((ROOT / "assets/n2-sample.json").read_text())

    def test_all_types_have_csv_provenance(self):
        bank = validate(self.bank)
        self.assertEqual(len({q["type"] for q in bank["questions"]}), 6)
        for q in bank["questions"]:
            self.assertEqual(q["source"]["word"], q["word"])

    def test_invalid_questions_rejected(self):
        mutations = [
            lambda b: b["questions"][0].update(word="NOT_IN_CSV"),
            lambda b: b["questions"][0].update(source_line=999999),
            lambda b: b["questions"][0].update(options=["a"]*4),
            lambda b: b["questions"][0].update(answer=4),
            lambda b: b["questions"][0].update(explanations=["missing"]),
            lambda b: b["questions"][2].update(formation={"prefix":"", "suffix":""}),
            lambda b: b["questions"][-1].update(options=["no target", "a", "b", "c"]),
        ]
        for change in mutations:
            with self.subTest(change=change):
                bank = copy.deepcopy(self.bank)
                change(bank)
                with self.assertRaises(ValueError):
                    validate(bank)


if __name__ == "__main__":
    unittest.main()
