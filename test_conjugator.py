﻿# -*- coding: utf-8 -*-

import os.path
import unittest
import sys
import itertools
import functools

from stem2 import stem1_to_stem2, get_stem1
from stem3 import stem1_to_stem3
import conjugator
from conjugator import get_plain, SentenceFinalForm, DeterminerForm, ConnectiveForm

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
        self.assertEqual('간다', get_plain('가다', adjective=False))
        self.assertEqual('먹는다', get_plain('먹다', adjective=False))
        self.assertEqual('논다', get_plain('놀다', adjective=False))

        self.assertEqual('길다', get_plain('길다', adjective=True))
        self.assertEqual('짜다', get_plain('짜다', adjective=True))

    def runFormTest(self, word, is_verb, is_irregular, results, indicative=True):
        forms_params = list(get_form_params())
        assert(len(results) == len(forms_params))
        for params, expected in zip(forms_params, results):
            func = functools.partial(SentenceFinalForm.indicative, is_verb=is_verb) if indicative \
                   else SentenceFinalForm.interrogative
            result = func(word, is_irregular=is_irregular,
                          tense=params[0], formal=params[2], polite=params[1])
            self.assertEqual(expected, result)

    def testIndicativeVowelEnding(self):
        verb = '가다'
        forms = ['가요', '가', '간다', '갑니다',
                 '갔어요', '갔어', '갔다', '갔습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms)

    def testIndicativeConsonantEnding(self):
        verb = '먹다'
        forms = ['먹어요', '먹어', '먹는다', '먹습니다',
                 '먹었어요', '먹었어', '먹었다', '먹었습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms)

    def testIndicativeLIrregular(self):
        verb = '열다'
        forms = ['열어요', '열어', '연다', '엽니다',
                 '열었어요', '열었어', '열었다', '열었습니다']
        self.runFormTest(verb, is_verb=True, is_irregular=True, results=forms)

    def testIndicativeAdjective(self):
        adj = '많다'
        forms = ['많아요', '많아', '많다', '많습니다',
                 '많았어요', '많았어', '많았다', '많았습니다']
        self.runFormTest(adj, is_verb=False, is_irregular=False, results=forms)

    # interrogative
    def testInterrogativeVerb(self):
        verb = '가다'
        forms = ['가요', '가', '가니', '갑니까',
                 '갔어요', '갔어', '갔니', '갔습니까']
        self.runFormTest(verb, is_verb=True, is_irregular=False, results=forms, indicative=False)

    def testInterrogativeAdjective(self):
        adj = '많다'
        forms = ['많아요', '많아', '많니', '많습니까',
                 '많았어요', '많았어', '많았니', '많았습니까']
        self.runFormTest(adj, is_verb=False, is_irregular=False, results=forms, indicative=False)

    def testHortative(self):
        self.assertEqual('갑시다', SentenceFinalForm.hortative('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가자', SentenceFinalForm.hortative('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_NON_POLITE))
        self.assertEqual('가요', SentenceFinalForm.hortative('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가', SentenceFinalForm.hortative('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_NON_POLITE))

    def testImperative(self):
        self.assertEqual('갑시오', SentenceFinalForm.imperative('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가라', SentenceFinalForm.imperative('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_NON_POLITE))
        self.assertEqual('가요', SentenceFinalForm.imperative('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가', SentenceFinalForm.imperative('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_NON_POLITE))

    def testAssertive(self):
        self.assertEqual('가겠습니다', SentenceFinalForm.assertive('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가겠다', SentenceFinalForm.assertive('가다', conjugator.STYLE_FORMAL, conjugator.STYLE_NON_POLITE))
        self.assertEqual('가겠어요', SentenceFinalForm.assertive('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_POLITE))
        self.assertEqual('가겠어', SentenceFinalForm.assertive('가다', conjugator.STYLE_INFORMAL, conjugator.STYLE_NON_POLITE))


class TestConnectiveForm(unittest.TestCase):
    def testCause(self):
        result = ConnectiveForm.reason('가다', irregular=False)
        self.assertEqual(['가', '가서', '가니', '가니까'], result)
        result = ConnectiveForm.reason('먹다', irregular=False)
        self.assertEqual(['먹어', '먹어서', '먹으니', '먹으니까'], result)

    def testContrast(self):
        result = ConnectiveForm.contrast('가다')
        self.assertEqual(['가지만', '가는데', '가더니'], result)
        result = ConnectiveForm.contrast('먹다')
        self.assertEqual(['먹지만', '먹는데', '먹더니'], result)

    def testConjunction(self):
        result = ConnectiveForm.conjunction('가다')
        self.assertEqual(['가고'], result)
        result = ConnectiveForm.conjunction('먹다')
        self.assertEqual(['먹고'], result)

    def testCondition(self):
        result = ConnectiveForm.condition('가다', irregular=False)
        self.assertEqual(['가면', '가야'], result)
        result = ConnectiveForm.condition('먹다', irregular=False)
        self.assertEqual(['먹으면', '먹어야'], result)

    def testMotive(self):
        result = ConnectiveForm.motive('가다', irregular=False)
        self.assertEqual(['가려고'], result)
        result = ConnectiveForm.motive('먹다', irregular=False)
        self.assertEqual(['먹으려고'], result)


class TestDeterminerForm(unittest.TestCase):
    def testPast(self):
        self.assertEqual('간', DeterminerForm.get('가다', tense=DeterminerForm.PAST, irregular=False))
        self.assertEqual('먹은', DeterminerForm.get('먹다', tense=DeterminerForm.PAST, irregular=False))

        self.assertEqual('자은', DeterminerForm.get('잣다', tense=DeterminerForm.PAST, irregular=True))
        self.assertEqual('연', DeterminerForm.get('열다', tense=DeterminerForm.PAST, irregular=True))
        self.assertEqual('마른', DeterminerForm.get('마르다', tense=DeterminerForm.PAST, irregular=True))
        self.assertEqual('걸은', DeterminerForm.get('걷다', tense=DeterminerForm.PAST, irregular=True))
        self.assertEqual('어떤', DeterminerForm.get('어떻다', tense=DeterminerForm.PAST, irregular=True))

    def testPresent(self):
        self.assertEqual('가는', DeterminerForm.get('가다', tense=DeterminerForm.PRESENT, irregular=False))
        self.assertEqual('먹는', DeterminerForm.get('먹다', tense=DeterminerForm.PRESENT, irregular=False))

        self.assertEqual('잣는', DeterminerForm.get('잣다', tense=DeterminerForm.PRESENT, irregular=True))
        self.assertEqual('여는', DeterminerForm.get('열다', tense=DeterminerForm.PRESENT, irregular=True))
        self.assertEqual('모르는', DeterminerForm.get('모르다', tense=DeterminerForm.PRESENT, irregular=True))
        self.assertEqual('걷는', DeterminerForm.get('걷다', tense=DeterminerForm.PRESENT, irregular=True))

    def testFuture(self):
        self.assertEqual('갈', DeterminerForm.get('가다', tense=DeterminerForm.FUTURE, irregular=False))
        self.assertEqual('먹을', DeterminerForm.get('먹다', tense=DeterminerForm.FUTURE, irregular=False))

        self.assertEqual('자을', DeterminerForm.get('잣다', tense=DeterminerForm.FUTURE, irregular=True))
        self.assertEqual('열', DeterminerForm.get('열다', tense=DeterminerForm.FUTURE, irregular=True))
        self.assertEqual('마를', DeterminerForm.get('마르다', tense=DeterminerForm.FUTURE, irregular=True))
        self.assertEqual('걸을', DeterminerForm.get('걷다', tense=DeterminerForm.FUTURE, irregular=True))
        self.assertEqual('어떨', DeterminerForm.get('어떻다', tense=DeterminerForm.FUTURE, irregular=True))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem1)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStem3)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFinalForms)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDeterminerForm)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConnectiveForm)
    unittest.TextTestRunner(verbosity=2).run(suite)
