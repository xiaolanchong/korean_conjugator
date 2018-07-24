
import jamo
import stem2
import stem3


TENSE_NON_PAST = 1
TENSE_PAST = 2

STYLE_FORMAL = 1
STYLE_INFORMAL = 2

STYLE_POLITE = 1
STYLE_NON_POLITE = 2


final_ss = 'ᆻ'
word_ending = '다'
polite_ending = '요'
polite_formal_suffix = '습니'
polite_formal_question_ending = '까'


def get_seumni(word):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3 and letters[2] != stem2.final_l:
        return stem1 + polite_formal_suffix
    else:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_p) + '니'


def get_past(word, irregular):
    stem = stem2.get_stem2(word, irregular)
    letters = jamo.decompose(stem[-1])
    assert(len(letters) == 2)
    return stem[:-1] + jamo.compose(letters[0], letters[1], final_ss)


def get_informal_polite(word: str, adjective: bool):
    if adjective:
        return word
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 2 or letters[2] == stem2.final_l:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_n) + word_ending  # final l -> n
    else:
        return stem1 + '는' + word_ending


# TODO: 니 is a direct question, (느)냐 is indirect (quote)
def get_informal_polite_interrogative(word: str):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3 and letters[2] == stem2.final_l:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + '니'  # '냐'
    else:
        return stem1 + '니'  # '으' + '냐'


def get_informal_polite_past_interrogative(word: str, irregular):
    past = get_past(word, irregular)
    return past + '니'


class SentenceFinalForm:
    @staticmethod
    def interrogative(word, is_verb, is_irregular, tense, formal, polite):
        """
        해체        STYLE_INFORMAL, STYLE_NON_POLITE
        해라체      STYLE_FORMAL, STYLE_NON_POLITE
        해요체 	   STYLE_INFORMAL, STYLE_POLITE
        하십시오체   STYLE_FORMAL, STYLE_POLITE
        :param word:
        :param tense:
        :param formal:
        :param polite:
        :return:
        """
        conjugate_methods = {
            # non-past
            (TENSE_NON_PAST,
             STYLE_FORMAL, STYLE_POLITE):
            lambda x: get_seumni(word) + '까',

            (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
            lambda x: get_informal_polite_interrogative(word),

            (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
            lambda x: stem2.get_stem2(word, is_irregular) + polite_ending,

            (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
            lambda x: stem2.get_stem2(word, is_irregular),

            # past
            (TENSE_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_past(word, irregular=is_irregular) + polite_formal_suffix + polite_formal_question_ending,

            (TENSE_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_informal_polite_past_interrogative(word, irregular=is_irregular),

            (TENSE_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: get_past(word, is_irregular) + '어' + polite_ending,

            (TENSE_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: get_past(word, is_irregular) + '어',
        }

        method = conjugate_methods.get((tense, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'{tense}, {formal}, {polite} not implemented')

    @staticmethod
    def indicative(word, is_verb, is_irregular, tense, formal, polite):
        conjugate_methods = {
                # non-past
                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_seumni(word) + word_ending,

                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_informal_polite(word, adjective=not is_verb),

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem2(word, is_irregular) + polite_ending,

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                 lambda x: stem2.get_stem2(word, is_irregular),

                # past
                (TENSE_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_past(word, irregular=is_irregular) + polite_formal_suffix + word_ending,

                (TENSE_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_past(word, irregular=is_irregular) + word_ending,

                (TENSE_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: get_past(word, is_irregular) + '어' + polite_ending,

                (TENSE_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: get_past(word, is_irregular) + '어',
            }
        method = conjugate_methods.get((tense, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'{tense}, {formal}, {polite} not implemented')

    @staticmethod
    def assertive(word):
        pass
