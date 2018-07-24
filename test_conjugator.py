# -*- coding: utf-8 -*-

import os.path
import unittest
import sys
import itertools

from stem2 import stem1_to_stem2, get_stem1
from stem3 import stem1_to_stem3
import conjugator
from conjugator import get_informal_polite, SentenceFinalForm

sys.path.append(os.path.abspath('..'))


def get_form_params():
    forms_params_no_time = [(conjugator.STYLE_POLITE, conjugator.STYLE_INFORMAL),
                            (conjugator.STYLE_NON_POLITE, conjugator.STYLE_INFORMAL),
                            (conjugator.STYLE_NON_POLITE, conjugator.STYLE_FORMAL),
                            (conjugator.STYLE_POLITE, conjugator.STYLE_FORMAL)]
    forms_params = list(itertools.product([conjugator.TENSE_NON_PAST, conjugator.TENSE_PAST], forms_params_no_time))
    for param in forms_params:
        yield param[0], param[1][0], param[1][1]


class TestStem1(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testStem1(self):
        self.assertEqual('가', get_stem1('가다'))


class TestStem2(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testStem2Regular(self):
        self.assertEqual('가', stem1_to_stem2('가'))
        self.assertEqual('서', stem1_to_stem2('서'))

        self.assertEqual('뵙어', stem1_to_stem2('뵙'))
        self.assertEqual('먹어', stem1_to_stem2('먹'))
        self.assertEqual('가다듬어', stem1_to_stem2('가다듬'))

        self.assertEqual('가둬', stem1_to_stem2('가두'))    # diphtong
        self.assertEqual('봐',   stem1_to_stem2('보'))

        self.assertEqual('개',    stem1_to_stem2('개'))
        self.assertEqual('기다려', stem1_to_stem2('기다리'))

        self.assertEqual('곪아', stem1_to_stem2('곪'))
        self.assertEqual('얇어', stem1_to_stem2('얇'))

    def testStem2_eu(self):
        self.assertEqual('침담가', stem1_to_stem2('침담그'))
        self.assertEqual('써', stem1_to_stem2('쓰'))
        self.assertEqual('악써', stem1_to_stem2('악쓰'))

    def testStem2_t(self):
        self.assertEqual('걸어',   stem1_to_stem2('걷', irregular=True))
        self.assertEqual('깨달아', stem1_to_stem2('깨닫', irregular=True))
        self.assertEqual('실어',   stem1_to_stem2('실', irregular=True))

        self.assertEqual('받아',   stem1_to_stem2('받', irregular=False))
        self.assertEqual('얻어', stem1_to_stem2('얻', irregular=False))
        self.assertEqual('묻어',   stem1_to_stem2('묻', irregular=False))

    def testStem2_l(self):
        self.assertEqual('길어', stem1_to_stem2('길', irregular=True))
        self.assertEqual('길어', stem1_to_stem2('길', irregular=False))
        self.assertEqual('열어', stem1_to_stem2('열', irregular=False))

    def testStem2_leu(self):
        self.assertEqual('따라', stem1_to_stem2('따르', irregular=False))
        self.assertEqual('골라', stem1_to_stem2('고르', irregular=True))
        self.assertEqual('일러', stem1_to_stem2('이르', irregular=True))

    def testStem2_p(self):
        self.assertEqual('고마워', stem1_to_stem2('고맙', irregular=True))
        self.assertEqual('도와', stem1_to_stem2('돕', irregular=True))
        self.assertEqual('어려워', stem1_to_stem2('어렵', irregular=True))
        self.assertEqual('아름다워', stem1_to_stem2('아름답',irregular=True))

        self.assertEqual('잡아', stem1_to_stem2('잡'))

    def testStem2_s(self):
        self.assertEqual('나아', stem1_to_stem2('낫', irregular=True))
        self.assertEqual('벗어', stem1_to_stem2('벗', irregular=False))

    def testStem2_h(self):
        self.assertEqual('노래', stem1_to_stem2('노랗', irregular=True))
        self.assertEqual('좋아', stem1_to_stem2('좋', irregular=False))


class TestStem3(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testStem3_regular(self):
        self.assertEqual('먹으', stem1_to_stem3('먹', irregular=False))
        self.assertEqual('가', stem1_to_stem3('가', irregular=False))

    def testStem3_irregular(self):
        self.assertEqual('지으', stem1_to_stem3('짓', irregular=True))
        self.assertEqual('걸으', stem1_to_stem3('걷', irregular=True))
        self.assertEqual('누우', stem1_to_stem3('눕', irregular=True))
        self.assertEqual('여', stem1_to_stem3('열', irregular=True))


class TestFinalForms(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testInformalPolite_regular(self):
        self.assertEqual('간다', get_informal_polite('가다', adjective=False))
        self.assertEqual('먹는다', get_informal_polite('먹다', adjective=False))
        self.assertEqual('논다', get_informal_polite('놀다', adjective=False))

        self.assertEqual('길다', get_informal_polite('길다', adjective=True))
        self.assertEqual('짜다', get_informal_polite('짜다', adjective=True))

    def runFormTest(self, word, is_verb, is_irregular, results, indicative=True):
        forms_params = list(get_form_params())
        assert(len(results) == len(forms_params))
        for params, expected in zip(forms_params, results):
            func = SentenceFinalForm.indicative if indicative else SentenceFinalForm.interrogative
            result = func(word, is_verb=is_verb, is_irregular=is_irregular,
                          tense=params[0], formal=params[1], polite=params[2])
            self.assertEqual(expected, result)

    def testIndicativeVowelEnding(self):
        verb = '가다'
        forms = ['간다', '가', '가요', '갑니다',
                 '갔다', '갔어', '갔어요', '갔습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms)

    def testIndicativeConsonantEnding(self):
        verb = '먹다'
        forms = ['먹는다', '먹어', '먹어요', '먹습니다',
                 '먹었다', '먹었어', '먹었어요', '먹었습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms)

    def testIndicativeLIrregular(self):
        verb = '열다'
        forms = ['연다', '열어', '열어요', '엽니다',
                 '열었다', '열었어', '열었어요', '열었습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=True, results=forms)

    def testIndicativeAdjective(self):
        adj = '많다'
        forms = ['많다', '많아', '많아요', '많습니다',
                 '많았다', '많았어', '많았어요', '많았습니다']
        self.runFormTest(adj, is_verb=False, is_irregular=False, results=forms)

    def testInterrogativeVerb(self):
        verb = '가다'
        forms = ['가니', '가', '가요', '갑니까',
                 '갔니', '갔어', '갔어요', '갔습니까']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms, indicative=False)

    def testInterrogativeAdjective(self):
        adj = '많다'
        forms = ['많니', '많아', '많아요', '많습니까',
                 '많았니', '많았어', '많았어요', '많았습니까']
        self.runFormTest(adj, is_verb=False, is_irregular=False, results=forms, indicative=False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem1)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem3)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFinalForms)
    unittest.TextTestRunner(verbosity=2).run(suite)