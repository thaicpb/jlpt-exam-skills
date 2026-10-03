"""Check corpus provenance and malformed question rejection."""
import copy
import json
import unittest
from collections import Counter
from build_n2_exam import ROOT, TYPES, validate, render


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


    def test_reading_answer_and_bracket_must_match_source(self):
        for change in (
            lambda q: q['options'].__setitem__(q['answer'], 'まちがい'),
            lambda q: q.update(prompt='これは【別の語】です。'),
            lambda q: q['options'].__setitem__((q['answer'] + 1) % 4, 'not kana'),
        ):
            bank = copy.deepcopy(self.bank)
            change(bank['questions'][0])
            with self.assertRaises(ValueError):
                validate(bank)

    def test_suru_annotation_and_multiple_readings(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        question = copy.deepcopy(self.bank['questions'][0])
        row = {'source_file': question['source_file'], 'source_line': question['source_line'],
               'word': question['word'], 'reading': 'あっか （する）'}
        question.update(options=['あっか', 'あくか', 'わるか', 'あつか'], answer=0)
        bank = {'level': self.bank['level'], 'questions': [question]}
        with patch('build_n2_exam.subprocess.run', return_value=SimpleNamespace(stdout=json.dumps({'items': [row]}))):
            validate(bank)
        row['reading'] = 'あっか／あくか'
        with patch('build_n2_exam.subprocess.run', return_value=SimpleNamespace(stdout=json.dumps({'items': [row]}))):
            with self.assertRaisesRegex(ValueError, 'uniquely'):
                validate(bank)

    def test_orthography_must_match_csv_word_and_reading(self):
        for field, value in [('options', ['価各', '誤字', '格価', '加格']),
                             ('prompt', '値段は【まちがい】です。')]:
            bank = copy.deepcopy(self.bank)
            bank['questions'][1][field] = value
            with self.assertRaisesRegex(ValueError, 'orthography'):
                validate(bank)

    def test_published_full_exams(self):
        for lesson in range(1, 15):
            with self.subTest(lesson=lesson):
                bank = json.loads((ROOT.parent.parent / f'resources/N2/exams/dai{lesson}.json').read_text(encoding='utf-8'))
                self.assertEqual(bank['id'], f'n2-dai{lesson}-30')
                self.assertEqual(len(bank['questions']), 30)
                self.assertEqual(len({q['word'] for q in bank['questions']}), 30)
                self.assertEqual(Counter(q['type'] for q in bank['questions']),
                                 {kind: count for kind, (_, count) in TYPES.items()})
                self.assertEqual({q['source_file'] for q in bank['questions']},
                                 {f'resources/N2/goi/dai{lesson}.csv'})
                html = render(bank, mode='exam', home_href='../../#/exams/N2', full=True)
                payload = json.loads(html.split('id="exam-data">', 1)[1].split('</script>', 1)[0])
                self.assertEqual(payload['home_href'], '../../#/exams/N2')
                self.assertEqual(payload['title'], f'N2 · Bài {lesson} · 30 câu')
                self.assertTrue(all(q['source']['word'] == q['word'] for q in payload['questions']))

    def test_published_reading_evidence_must_match_choices(self):
        bank = json.loads((ROOT.parent.parent / 'resources/N2/exams/dai1.json').read_text(encoding='utf-8'))
        q = bank['questions'][0]
        q['option_lexemes'][0]['word'] = '無関係'
        with self.assertRaisesRegex(ValueError, 'unattested reading lexeme'):
            validate(bank)


if __name__ == "__main__":
    unittest.main()
