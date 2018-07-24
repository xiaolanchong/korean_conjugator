
import jamo
import stem2


stem3_final = '으'


def get_regular_stem3(stem1):
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3:
        return stem1 + stem3_final
    else:
        return stem1


def get_irregular_stem3(stem1):
    letters = jamo.decompose(stem1[-1])
    if len(letters) == 3:
        if letters[2] == stem2.final_s:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + stem3_final
        elif letters[2] == stem2.final_t:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], stem2.final_l) + stem3_final
        elif letters[2] == stem2.final_p:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], None) + '우'
        elif letters[2] == stem2.final_l:
            return stem1[:-1] + jamo.compose(letters[0], letters[1], None)
    raise RuntimeError(f'{stem2.stem1_to_word(stem1)} cannot be irregular verb')


def stem1_to_stem3(stem1, irregular):
    return get_irregular_stem3(stem1) if irregular else get_regular_stem3(stem1)


def get_stem3(word, irregular):
    return stem1_to_stem3(stem2.get_stem1(word), irregular)
