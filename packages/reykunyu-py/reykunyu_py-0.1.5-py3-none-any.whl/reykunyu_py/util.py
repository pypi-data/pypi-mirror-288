"""The support module for reykunyu-py. Most users should not need to access this module.
"""
from reykunyu_py.errors import *


class Translation:
    """Na'vi text with multiple translations.

    Attributes
    ----------
    languages

    Parameters
    ----------
    navi : str
        The Na'vi text that the translations are for.
    translations : dict [str, str]
        The translations available for the text. Formatted as a dict where K = ISO 639-1 language code OR ``"x-navi"``, V = translation.
    """
    def __init__(self, navi: str, translations: dict[str, str]):
        self._navi = navi
        self._translations = translations
        self._languages = []
        for translation in translations:
            self._languages.append(translation)

    def translate(self, lang_code: str) -> str:
        """Return the translation of the text into the given language.

        Parameters
        ----------
        lang_code : str
            The ISO 639-1 language code of the target language. This may also be ``"x-navi"``, for Na'vi dictionary definitions.

        Returns
        -------
        str
            The translation of the text into the target language.

        Raises
        ------
        LanguageNotSupportedError
            Raised if the text does not have a translation for the target language.
        """
        if lang_code in self._translations:
            return self._translations.get(lang_code)
        else:
            raise LanguageNotSupportedError(self._navi, lang_code)

    @property
    def languages(self) -> list[str]:
        """The list of valid ISO 639-1 language codes for this text. (list[str], read-only)
        """
        return self._languages


class Pronunciation:
    """The pronunciation information for a Na'vi word.

    Attributes
    ----------
    raw

    Parameters
    ----------
    data : dict
        The raw data from Reykunyu.
    """
    def __init__(self, data: dict):
        self._syllables = data.get("syllables").split('-')
        self._stressed_index = data.get("stressed") - 1
        self._forest_ipa = data.get("ipa").get("FN")
        self._reef_ipa = data.get("ipa").get("RN")

    @property
    def raw(self) -> tuple[list[str], int]:
        """The list of syllables and the index of the stressed syllable. (tuple[list[str], int], read-only)
        """
        return self._syllables, self._stressed_index

    def get(self, deliminator="-", prefix="", suffix="", capitalized=True):
        """Return the pronunciation as a string, with a variety of options for stress marking.

        Parameters
        ----------
        deliminator : str
            The string used to separate the syllables. Default is ``"-"``.
        prefix : str
            A string that will be added immediately before the stressed syllable. Default is ``""``.
        suffix : str
            A string that will be added immediately after the stressed syllable. Default is ``""``.
        capitalized : bool
            If ``True``, the stressed syllable will be capitalized. Default is ``True``.

        Returns
        -------
        str
            The pronunciation, with the stressed syllable marked in the manner configured.
        """
        syllables = self._syllables.copy()
        if capitalized:
            syllables[self._stressed_index] = syllables[self._stressed_index].upper()
        syllables[self._stressed_index] = prefix + syllables[self._stressed_index] + suffix
        return deliminator.join(syllables)

    def ipa(self, dialect: str):
        """Return the IPA transcription of the pronunciation for the given dialect.

        Parameters
        ----------
        dialect : str
            The dialect of Na'vi. Must be one of ``['forest', 'reef']``

        Returns
        -------
        str
            The IPA transcription.

        Raises
        ------
        ValueError
            Raised if `dialect` is not one of ``['forest', 'reef']``.
        """
        valid_dialects = ['forest', 'reef']
        if dialect not in valid_dialects:
            raise ValueError("dialect must be one of %r" % valid_dialects)

        if dialect == 'forest':
            return self._forest_ipa
        elif dialect == 'reef':
            return self._reef_ipa


class Answer:
    """A possible meaning and its info for an `Entry` in a Reykunyu API Response.

    Attributes
    ----------
    raw
    root
    translations
    part_of_speech
    pronunciations
    best_pronunciation

    Parameters
    ----------
    data : dict
        The raw data from Reykunyu.

    Notes
    -----
    If an `Entry` may have multiple meanings it will have more than one `Answer`.
    """
    def __init__(self, data: dict):
        self._data = data
        self._translations = []
        for entry in data.get("translations"):
            self._translations.append(Translation(self.root, entry))
        self._pronunciations = []
        if data.get("pronunciation"):
            for pronunciation in data.get("pronunciation"):
                self._pronunciations.append(Pronunciation(pronunciation))

    @property
    def raw(self) -> dict:
        """The raw data of the `Answer`. (dict, read-only)
        """
        return self._data

    @property
    def root(self) -> str:
        """The root word of the answer in Na'vi. (str, read-only)
        """
        return self._data.get("na'vi")

    @property
    def translations(self) -> list[Translation]:
        """The list of translations for this word. (list[Translation], read-only)
        """
        return self._translations

    def translate(self, lang_code) -> list[str]:
        """Return all translations of a particular language.
        """
        translations = []
        for entry in self._translations:
            translations.append(entry.translate(lang_code))

        return translations

    @property
    def part_of_speech(self) -> str:
        """The part of speech of the word. (str, read-only)
        """
        return self._data.get("type")

    @property
    def pronunciations(self) -> list[Pronunciation]:
        """The list of pronunciations of the word. (list[Pronunciation], read-only)
        """
        return self._pronunciations

    @property
    def best_pronunciation(self):
        """The first pronunciation in the list. (Pronunciation, read-only)

        Raises
        ------
        NoPronunciationError
            Raised if there are no pronunciations for this word.
        """
        if self._pronunciations:
            return self._pronunciations[0]
        else:
            raise NoPronunciationError(self.root)


class Entry:
    """An entry in a Reykunyu API response representing a single word in the input.

    Attributes
    ----------
    raw
    input
    answers
    best_answer
    suggestions

    Parameters
    ----------
    data : dict
        The raw data from Reykunyu.
    """
    def __init__(self, data: dict):
        self._data = data
        self._answers = []
        for answer in data.get("sì'eyng"):
            self._answers.append(Answer(answer))
        self._suggestions = data.get("aysämok")

    @property
    def raw(self) -> dict:
        """The raw data of the `Entry`. (dict, read-only)
        """
        return self._data

    @property
    def input(self) -> str:
        """The word as it was in the original input. (str, read-only)
        """
        return self._data.get("tìpawm")

    @property
    def answers(self) -> list[Answer]:
        """The list of possible meanings and their info for this `Entry`. (list[Answer], read-only)
        """
        return self._answers

    @property
    def best_answer(self) -> Answer:
        """The first `Answer` for this `Entry`. (Answer, read-only)
        """
        if self._answers:
            return self._answers[0]
        else:
            raise WordNotRecognizedError(self.input)

    @property
    def suggestions(self) -> list[str]:
        """The list of suggested corrections if the `Entry` is potentially misspelled. (list[str], read-only)"""
        return self._suggestions


class Response:
    """A response from the Reykunyu API for a particular input string.

    Parameters
    ----------
    input_text : str
        The original text sent to the Reykunyu API.
    data : list
        The raw data from Reykunyu.
    """
    def __init__(self, input_text: str, data: list):
        self._data = data
        self._input_text = input_text
        self._entries = []
        for entry in data:
            self._entries.append(Entry(entry))

    @property
    def raw(self) -> list:
        """The raw data of the `Response`. (list, read-only)
        """
        return self._data

    @property
    def input(self) -> str:
        """The original input sent to the Reykunyu API. (str, read-only)
        """
        return self._input_text

    @property
    def entries(self) -> list[Entry]:
        """Every `Entry` in the `Response`. Each `Entry` represents the response for a word in the input. (list[Entry], read-only)"""
        return self._entries

    def entry(self, index: int):
        """Returns the `Entry` at the specified index.

        Parameters
        ----------
        index : int
            The index of the `Entry`.

        Returns
        -------
        Entry
            The Entry at the specified index.
        """
        return self._entries[index]


class DictionaryPronunciation:
    """The pronunciation information for an entry in Reykunyu's Dictionary.

    Attributes
    ----------
    raw

    Parameters
    ----------
    data : dict
        The raw data from Reykunyu.
    """
    def __init__(self, data: dict):
        self._syllables = data.get("syllables").split('-')
        try:
            self._stressed_index = data.get("stressed") - 1
        except TypeError:
            self._stressed_index = 0

    @property
    def raw(self) -> tuple[list[str], int]:
        """The list of syllables and the index of the stressed syllable. (tuple[list[str], int], read-only)
        """
        return self._syllables, self._stressed_index

    def get(self, deliminator="-", prefix="", suffix="", capitalized=True):
        """Return the pronunciation as a string, with a variety of options for stress marking.

        Parameters
        ----------
        deliminator : str
            The string used to separate the syllables. Default is ``"-"``.
        prefix : str
            A string that will be added immediately before the stressed syllable. Default is ``""``.
        suffix : str
            A string that will be added immediately after the stressed syllable. Default is ``""``.
        capitalized : bool
            If ``True``, the stressed syllable will be capitalized. Default is ``True``.

        Returns
        -------
        str
            The pronunciation, with the stressed syllable marked in the manner configured.
        """
        syllables = self._syllables.copy()
        if capitalized:
            syllables[self._stressed_index] = syllables[self._stressed_index].upper()
        syllables[self._stressed_index] = prefix + syllables[self._stressed_index] + suffix
        return deliminator.join(syllables)


class DictionaryEntry:
    """A class representing an entry in a `Dictionary`.

    Attributes
    ----------
    raw
    translations
    part_of_speech
    pronunciations
    best_pronunciation

    Parameters
    ----------
    data : tuple [str, dict]
        The raw data of the `DictionaryEntry`. The first entry is the Na'vi word. The second entry is the dict V from Reykunyu.
    """
    def __init__(self, data: tuple[str, dict]):
        self._word = data[0].split(":")[0]
        self._data = data[1]
        self._translations = []
        for entry in data[1].get("translations"):
            self._translations.append(Translation(self._word, entry))
        self._pronunciations = []
        if data[1].get("pronunciation"):
            for pronunciation in data[1].get("pronunciation"):
                self._pronunciations.append(DictionaryPronunciation(pronunciation))

    @property
    def raw(self) -> tuple[str, dict]:
        """The raw data of the `DictionaryEntry`.
        Formatted as a tuple, where the first entry is the Na'vi word, and the second entry is the dict V from Reykunyu. (tuple[str, dict], read-only)
        """
        return self._word, self._data

    @property
    def translations(self) -> list[Translation]:
        """The list of translations for this word. (list[Translation], read-only)
        """
        return self._translations

    def translate(self, lang_code) -> list[str]:
        """Return all translations of a particular language.
        """
        translations = []
        for entry in self._translations:
            translations.append(entry.translate(lang_code))

        return translations

    @property
    def part_of_speech(self) -> str:
        """The part of speech of the word. (str, read-only)
        """
        return self._data.get("type")

    @property
    def pronunciations(self) -> list[DictionaryPronunciation]:
        """The list of pronunciations of the word. (list[DictionaryPronunciation], read-only)
        """
        return self._pronunciations

    @property
    def best_pronunciation(self):
        """The first pronunciation in the list. (Pronunciation, read-only)

        Raises
        ------
        NoPronunciationError
            Raised if there are no pronunciations for this word.
        """
        if self._pronunciations:
            return self._pronunciations[0]
        else:
            raise NoPronunciationError(self._word)
