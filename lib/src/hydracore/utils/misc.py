import re

def strip_name(name: bytes):
    rgx_strip = re.compile(br"[\x00-\x19]")
    return rgx_strip.sub(b"", name)
