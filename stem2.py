
import jamo


final_l = 'ᆯ'
final_t = 'ᆮ'
final_p = 'ᆸ'
final_s = 'ᆺ'
final_h = 'ᇂ'
final_n = 'ᆫ'


def is_jamo_letter(sym):
    return len(sym) == 0 and 0x1100 <= ord(sym[0]) <= 0x11FF


def is_bright_vowel(vowel):
    return vowel in {'ᅡ',  'ᅩ'}  # 'ᅢ', 'ᅣ', 'ᅤ',


def get_jamo_after_vowel(vowel):
    return '아' if is_bright_vowel(vowel) else '어'


def get_stem1(word):
    if word[-1] != '다' or len(word) < 2:
        raise RuntimeError(f'{word} is not a verb or adjective')
    return word[:-1]


def stem1_to_word(stem1):
    return stem1 + '다'


def get_leu_irregular_stem2(prefix):
    if len(prefix) == 0:
        raise RuntimeError('르다 is not a verb')
    letters = jamo.decompose(prefix[-1])
    if len(letters) == 3:
        raise RuntimeError(f'{prefix}르다 is not a 르 verb')
    return prefix[:-1] + jamo.compose(letters[0], letters[1], final_l) + ('라' if is_bright_vowel(letters[1]) else '러')


def get_t_irregular_stem2(prefix, initial, vowel):
    return prefix + jamo.compose(initial, vowel, final_l) + get_jamo_after_vowel(vowel)


def get_p_irregular_stem2(prefix, initial, vowel):
    return prefix + jamo.compose(initial, vowel, None) + \
           ('와' if is_bright_vowel(vowel) and len(prefix) == 0 else '워')


def get_s_irregular_stem2(prefix, initial, vowel):
    return prefix + jamo.compose(initial, vowel, None) + get_jamo_after_vowel(vowel)


def get_h_irregular_stem2(prefix, initial):
    return prefix + jamo.compose(initial, 'ᅢ', None)


def get_eu_stem2(stem1, initial):
    if stem1[-1] == '쓰':   # 쓰다 derivatives always conjugate as 쓰다
        return stem1[:-1] + '써'
    elif len(stem1) > 1:
        letters = jamo.decompose(stem1[-2])
        if letters[1] == 'ᅡ':
            return stem1[:-1] + jamo.compose(initial, 'ᅡ', None)
        else:
            return stem1[:-1] + jamo.compose(initial, 'ᅥ', None)


def get_irregular_stem2(stem1):
    letters = jamo.decompose(stem1[-1])
    if stem1[-1] == '르':
        return get_leu_irregular_stem2(stem1[:-1])
    elif len(letters) == 2 and letters[1] == 'ᅳ':
        return get_eu_stem2(stem1, letters[0])
    elif len(letters) == 3:
        if letters[2] == final_t:
            return get_t_irregular_stem2(stem1[:-1], letters[0], letters[1])
        elif letters[2] == final_l:
            return get_regular_stem2(stem1)
        elif letters[2] == final_p:
            return get_p_irregular_stem2(stem1[:-1], letters[0], letters[1])
        elif letters[2] == final_s:
            return get_s_irregular_stem2(stem1[:-1], letters[0], letters[1])
        elif letters[2] == final_h:
            return get_h_irregular_stem2(stem1[:-1], letters[0])
    else:
        raise RuntimeError(f'{stem1}다 cannot be irregular')


def get_regular_stem2(stem1):
    letters = jamo.decompose(stem1[-1])
    vowel = letters[1]
    if len(letters) == 3:
        # if vowel in ('ᅩ', 'ᅣ', 'ᅪ'):
        return stem1 + ('아' if is_bright_vowel(vowel) else '어')
    else:
        if letters[1] == 'ᅳ':  # consider not irregular
            return get_eu_stem2(stem1, letters[0])
        replace_to = {'ᅩ': 'ᅪ',
                      'ᅮ': 'ᅯ',
                      'ᅵ': 'ᅧ'}
        vowel_to = replace_to.get(vowel)
        if vowel_to:
            return stem1[:-1] + jamo.compose(letters[0], vowel_to, None)
        else:
            return stem1


def stem1_to_stem2(stem1, irregular=False):
    if stem1[-1] == '하':
        return '해'

    if irregular:
        return get_irregular_stem2(stem1)
    else:
        return get_regular_stem2(stem1)


def get_stem2(word, irregular=False):
    return stem1_to_stem2(get_stem1(word), irregular=irregular)
