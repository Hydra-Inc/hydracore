import gzip

PATCHED = False

def patch_gzip_for_partial():
    """
    Replaces gzip.GzipFile._read_eof with a version not throwing CRC error.
    for decompressing partial files.
    """

    def read_eof_py3(self):
        self._read_exact(8)

        # Gzip files can be padded with zeroes and still have archives.
        # Consume all zero bytes and set the file position to the first
        # non-zero byte. See http://www.gzip.org/#faq8
        c = b"\x00"
        while c == b"\x00":
            c = self._fp.read(1)
        if c:
            self._fp.prepend(c)

    def read_eof_py2(self):
        # Gzip files can be padded with zeroes and still have archives.
        # Consume all zero bytes and set the file position to the first
        # non-zero byte. See http://www.gzip.org/#faq8
        c = "\x00"
        while c == "\x00":
            c = self.fileobj.read(1)
        
        if c:
            self.fileobj.seek(-1, 1)

    readercls = getattr(gzip, "_GzipReader", gzip.GzipFile)  # Py3/Py2
    readercls._read_eof = read_eof_py2 if readercls is gzip.GzipFile else read_eof_py3


def fix_gzip():
    global PATCHED
    if PATCHED:
        return
    patch_gzip_for_partial()
    