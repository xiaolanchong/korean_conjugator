
import jamo
import stem2
import stem3


TENSE_NON_PAST = 1
TENSE_PAST = 2

STYLE_FORMAL = 3
STYLE_INFORMAL = 4

STYLE_POLITE = 5
STYLE_NON_POLITE = 6


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


def get_eupsi(word):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3 and letters[2] != stem2.final_l:
        return stem1 + '읍시'
    else:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_p) + '시'


def get_past(word, irregular):
    stem = stem2.get_stem2(word, irregular)
    letters = jamo.decompose(stem[-1])
    assert(len(letters) == 2)
    return stem[:-1] + jamo.compose(letters[0], letters[1], final_ss)


def get_plain(word: str, adjective: bool):
    if adjective:
        return word
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 2 or letters[2] == stem2.final_l:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_n) + word_ending  # final l -> n
    else:
        return stem1 + '는' + word_ending


# TODO: 니 is a direct question, (느)냐 is indirect (quote)
def get_plain_interrogative(word: str):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3 and letters[2] == stem2.final_l:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + '니'  # '냐'
    else:
        return stem1 + '니'  # '으' + '냐'


def get_plan_past_interrogative(word: str, irregular):
    past = get_past(word, irregular)
    return past + '니'


class SentenceFinalForm:
    @staticmethod
    def indicative(word, is_verb, is_irregular, tense, formal, polite):
        conjugate_methods = {
                # non-past
                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_seumni(word) + word_ending,

                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_plain(word, adjective=not is_verb),

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
                lambda x: get_past(word, irregular=is_irregular) + '어' + polite_ending,

                (TENSE_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: get_past(word, irregular=is_irregular) + '어',
            }
        method = conjugate_methods.get((tense, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'{tense}, {formal}, {polite} not implemented')

    @staticmethod
    def interrogative(word: str, is_irregular: bool, tense, formal, polite):
        """
        해체        STYLE_INFORMAL, STYLE_NON_POLITE
        해라체      STYLE_FORMAL, STYLE_NON_POLITE
        해요체 	   STYLE_INFORMAL, STYLE_POLITE
        하십시오체   STYLE_FORMAL, STYLE_POLITE
        :param word:
        :param is_irregular:
        :param tense:
        :param formal:
        :param polite:
        :return:
        """
        conjugate_methods = {
            # non-past
            (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
            lambda x: get_seumni(word) + '까',

            (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_plain_interrogative(word),


            (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem2(word, is_irregular) + polite_ending,

            (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
            lambda x: stem2.get_stem2(word, is_irregular),

            # past
            (TENSE_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_past(word, irregular=is_irregular) + polite_formal_suffix + polite_formal_question_ending,

            (TENSE_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: get_plan_past_interrogative(word, irregular=is_irregular),

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
    def assertive(word, formal, polite):
        assertive_suffix = '겠'
        conjugate_methods = {
                # non-past
                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem1(word) + assertive_suffix + polite_formal_suffix + word_ending,

                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem1(word) + assertive_suffix + word_ending,

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem1(word) + assertive_suffix + '어' + polite_ending,

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem1(word) + assertive_suffix + '어'
        }
        method = conjugate_methods.get((TENSE_NON_PAST, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'Assertive form of {formal}, {polite} not implemented')

    @staticmethod
    def imperative(word, formal, polite):
        conjugate_methods = {
                # non-past
                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_eupsi(word) + '오',

                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem1(word) + '라',

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem2(word) + polite_ending,

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem2(word)
        }
        method = conjugate_methods.get((TENSE_NON_PAST, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'Assertive form of {formal}, {polite} not implemented')

    @staticmethod
    def hortative(word, formal, polite):
        conjugate_methods = {
                # non-past
                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_POLITE):
                lambda x: get_eupsi(word) + '다',

                (TENSE_NON_PAST, STYLE_FORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem2(word) + '자',

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_POLITE):
                lambda x: stem2.get_stem2(word) + polite_ending,

                (TENSE_NON_PAST, STYLE_INFORMAL, STYLE_NON_POLITE):
                lambda x: stem2.get_stem1(word)
        }
        method = conjugate_methods.get((TENSE_NON_PAST, formal, polite))
        if method:
            return method(word)
        else:
            raise RuntimeError(f'Assertive form of {formal}, {polite} not implemented')


class ConnectiveForm:
    @staticmethod
    def reason(word: str, irregular: bool):
        st2 = stem2.get_stem2(word, irregular=irregular)
        st3 = stem3.get_stem3(word, irregular=irregular)
        return [st2, st2 + '서', st3 + '니', st3 + '니까']

    @staticmethod
    def contrast(word):
        st1 = stem2.get_stem1(word)
        return [st1 + '지만', st1 + '는데', st1 + '더니']

    @staticmethod
    def conjunction(word):
        st1 = stem2.get_stem1(word)
        return [st1 + '고']

    @staticmethod
    def condition(word, irregular: bool):
        return [stem3.get_stem3(word, irregular=irregular) + '면',
                stem2.get_stem2(word, irregular=irregular) + '야']

    @staticmethod
    def motive(word, irregular: bool):
        return [stem3.get_stem3(word, irregular=irregular) + '려고']


def get_past_determiner(word, irregular):
    return get_past_and_future_determiner(word, irregular, '은', '운', stem2.final_n)


def get_future_determiner(word, irregular):
    return get_past_and_future_determiner(word, irregular, '을', '울', stem2.final_l)


def get_past_and_future_determiner(word, irregular, regular_ending, p_irregular_ending, ending_final):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if irregular and len(letters) == 3:
        if letters[2] == stem2.final_s:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + regular_ending  # s removed
        elif letters[2] == stem2.final_t:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_l) + regular_ending  # t -> l
        elif letters[2] == stem2.final_p:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + p_irregular_ending  # p -> un/ul

    if len(letters) == 2 or letters[2] == stem2.final_l or letters[2] == stem2.final_h:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], ending_final)
    else:
        return stem1 + regular_ending


def get_present_determiner(word):
    stem1 = stem2.get_stem1(word)
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3 and letters[2] == stem2.final_l:
        return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + '는'
    else:
        return stem1 + '는'


class DeterminerForm:
    PAST = 1
    PRESENT = 2
    FUTURE = 3

    @staticmethod
    def get(word, tense: int, irregular: bool):
        if tense == DeterminerForm.PAST:
            return get_past_determiner(word, irregular=irregular)
        elif tense == DeterminerForm.PRESENT:
            return get_present_determiner(word)
        elif tense == DeterminerForm.FUTURE:
            return get_future_determiner(word, irregular=irregular)


class NounForm:
    PAST = 1
    PRESENT = 2

    @staticmethod
    def get(word, tense: int, irregular: bool):
        if tense == NounForm.PRESENT:
            st1 = stem2.get_stem1(word)
            letters = jamo.decompose(st1[-1])
            if len(letters) == 3 and letters[2] == stem2.final_l:
                nominalization = (st1[:-1] + jamo.compose(letters[0], letters[1], 'ᆱ'))
            else:
                nominalization = stem2.get_stem1(word) + '음'
            return [nominalization, stem2.get_stem1(word) + '기']
        elif tense == NounForm.PAST:
            past = get_past(word, irregular)
            return [past + '음', past + '기']
