import re

"""
The flow of entities is the following:

 Game -> [Template] -> Map -> Scenario -> Heroes
                                          Towns
                                          ....

                                          
So first comes the Game, specially version, then the Template if the map
was created by template, then map, then scenario.
"""


VERSIONS = {
    'sod': {
        'title': "Shadow of Death"
    },
    'hota': {
        'title': "Horn of the Abyss"
    },
    'hota17': {
        'title': "Horn of the Abyss with Factory"
    },
}


def check_version(ver):
    global VERSIONS
    if not VERSIONS[ver]:
        raise RuntimeError('Heroes 3 Version is wrong, available: ' +
                           [x for x, _ in VERSIONS.items()].join(', '))


LANGUAGE = 'en'
LANG_SET = False
LANG_DETECTED = False

SUPPORTED_LANGUAGES = ['en', 'ru']


def set_language(lang: str, detected: bool = False):
    global LANGUAGE, LANG_SET, LANG_DETECTED
    LANGUAGE = lang
    if detected:
        LANG_SET = True
    else:
        LANG_DETECTED = True


def auto_detect_language():
    global LANG_SET
    return not LANG_SET and not LANG_DETECTED


def detect_language(name: bytes):
    if re.match(b'^[\x00-\x90]+$', name):
        set_language('en', True)
    if re.match(b"""^[ '\xc0-\xff\xB8\xA8]+$""", name):
        set_language('ru', True)
    return False

def to_name(name: bytes) -> str:
    global LANGUAGE
    if LANGUAGE == 'ru':
        return name.decode('cp1251')
    return name


def from_name(name: str) -> bytes:
    global LANGUAGE
    if LANGUAGE == 'ru':
        return name.encode('cp1251')
    return name.encode('latin-1')


def identify_language(name: bytes) -> str:
    if re.match(b'^[\x00-\x90\x2c,\x2d\x3f]+$', name):
        return 'en'
    if re.match(b"""^[ '\xc0-\xff\xB8\xA8\x2c,\x2d\x3f]+$""", name):
        return 'ru'
    return False


def to_text(name: bytes) -> str:
    if identify_language(name) == 'ru':
        return name.decode('cp1251')
    return name.decode('latin-1')
