"""Check N1 type boundaries, corpus provenance and malformed question rejection."""
import copy
import json
import unittest
from build_n1_exam import ROOT, validate


class N1ExamValidationTests(unittest.TestCase):
    def setUp(self):
        self.bank = json.loads((ROOT / "assets/n1-sample.json").read_text())

    def test_exactly_four_n1_types_have_csv_provenance(self):
        bank = validate(self.bank)
        self.assertEqual({q["type"] for q in bank["questions"]}, {"reading", "context", "paraphrase", "usage"})
        for q in bank["questions"]:
            self.assertEqual(q["source"]["word"], q["word"])
            self.assertTrue(q["source_file"].startswith("resources/N1/goi/"))

    def test_n2_only_types_are_rejected(self):
        for n2_type in ("orthography", "formation"):
            bank = copy.deepcopy(self.bank)
            bank["questions"][0]["type"] = n2_type
            with self.subTest(n2_type=n2_type), self.assertRaises(ValueError):
                validate(bank)

    def test_non_n1_bank_is_rejected(self):
        bank = copy.deepcopy(self.bank)
        bank["level"] = "N2"
        with self.assertRaises(ValueError):
            validate(bank)

    def test_malformed_questions_are_rejected(self):
        mutations = [
            lambda b: b["questions"][0].update(word="NOT_IN_CSV"),
            lambda b: b["questions"][0].update(source_line=999999),
            lambda b: b["questions"][0].update(options=["a"] * 4),
            lambda b: b["questions"][0].update(answer=4),
            lambda b: b["questions"][0].update(explanations=["missing"]),
            lambda b: b["questions"][1].update(prompt="No blank"),
            lambda b: b["questions"][-1].update(options=["no target", "a", "b", "c"]),
        ]
        for change in mutations:
            bank = copy.deepcopy(self.bank)
            change(bank)
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate(bank)


if __name__ == "__main__":
    unittest.main()
