"""Mechanical batch invariants; fixture sentences are not a learning question bank."""
import copy
import unittest

from build_dai2_exams import load_items, prepare_groups
from build_n1_exam import validate


class Dai2ExamTests(unittest.TestCase):
    def setUp(self):
        self.items = load_items()
        self.questions = []
        for index, item in enumerate(self.items):
            kind = ('reading', 'context', 'paraphrase', 'usage')[index % 4]
            word = item['word']
            options = [f'{word}テスト{index}-{i}' for i in range(4)]
            prompt = word if kind == 'usage' else f'【{word}】'
            if kind == 'context':
                prompt = '（　）'
            if kind == 'reading':
                options = [item['reading'].split(' (')[0], 'あああ', 'いいい', 'ううう']
            self.questions.append(dict(id=f'q{index}', type=kind, word=word,
                source_file=item['source_file'], source_line=item['source_line'], origin='authored',
                prompt=prompt, options=options, answer=0, explanations=[f'explanation-{i}' for i in range(4)]))
        self.bank = {'level': 'N1', 'questions': self.questions}

    def test_coverage_shuffle_alignment_and_reproducibility(self):
        groups = prepare_groups(self.bank, self.items, 42)
        self.assertEqual(groups, prepare_groups(self.bank, self.items, 42))
        self.assertEqual(len(groups), 5)
        flattened = [q for group in groups for q in group]
        self.assertEqual([q['word'] for q in flattened], [x['word'] for x in self.items])
        for original, shuffled in zip(self.questions, flattened):
            self.assertEqual(shuffled['options'][shuffled['answer']], original['options'][0])
            self.assertEqual(dict(zip(shuffled['options'], shuffled['explanations'])),
                             dict(zip(original['options'], original['explanations'])))
        for group in groups:
            validate({'level': 'N1', 'questions': group})
        for kind in ('reading', 'context', 'paraphrase', 'usage'):
            self.assertGreater(len({q['answer'] for q in flattened if q['type'] == kind}), 1)
        self.assertNotEqual(groups, prepare_groups(self.bank, self.items, 43))

    def test_rejects_missing_or_reordered_rows(self):
        for questions in (self.questions[:-1], self.questions[::-1]):
            with self.assertRaisesRegex(ValueError, 'CSV order'):
                prepare_groups({'level': 'N1', 'questions': questions}, self.items, 42)

    def test_rejects_generic_distractor_templates(self):
        bank = copy.deepcopy(self.bank)
        for q in bank['questions']:
            if q['type'] == 'usage':
                q['options'][1:] = [f'天気予報が{q["word"]}を食べた。',
                                    f'鉛筆で{q["word"]}を眠った。', f'駅を{q["word"]}として飲んだ。']
        with self.assertRaisesRegex(ValueError, 'repeated distractor'):
            prepare_groups(bank, self.items, 42)

    def test_rejects_unbalanced_group(self):
        bank = copy.deepcopy(self.bank)
        bank['questions'][0].update(type='paraphrase')
        with self.assertRaisesRegex(ValueError, 'five questions'):
            prepare_groups(bank, self.items, 42)


if __name__ == '__main__':
    unittest.main()
