"""The main module of reykunyu-py. Most users should only need to import this module.
"""
import requests

import reykunyu_py.util
from reykunyu_py.util import Response, DictionaryEntry


def request(input_text: str) -> Response:
    """Return the response from the Reykunyu API for a particular Na'vi string.

    Parameters
    ----------
    input_text : str
        The text to send to the Reykunyu API.

    Returns
    -------
    Response
        The response from the Reykunyu API.
    """
    return Response(input_text, requests.get("https://reykunyu.wimiso.nl/api/fwew?t%C3%ACpawm=" + input_text).json())


raw_dictionary = requests.get("https://reykunyu.wimiso.nl/api/list/all").json()
"""The raw dictionary from Reykunyu. (dict, read-only)
"""
dictionary = {}
"""The abstracted list of words that Reykunyu recognizes. (dict[str, dict], read-only)
"""
for entry in raw_dictionary:
    dictionary[entry.get("na'vi")] = DictionaryEntry((entry.get("na'vi"), entry))


def get_from_dictionary(navi: str) -> DictionaryEntry:
    """Return the dictionary entry for the given Na'vi word.

    Parameters
    ----------
    navi : str
        The Na'vi word.

    Returns
    -------
    DictionaryEntry
        The dictionary entry for the word. If no entry is found, returns None.
    """
    return dictionary.get(navi)
