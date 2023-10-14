import gzip

from .base import BinFile
from hydracore.utils.gzip import fix_gzip


class Heroes3SaveGameFile(BinFile):

    def __init__(self, filename: str):
        fix_gzip()
        super().__init__(filename)

    def load(self, filename: str):
        """
        Heroes 3 file is GZiped with a special version without CRC check
        """
        with gzip.GzipFile(filename, "rb") as f:
            self.data = bytearray(f.read())
        self.size = len(self.data)
        self.orig_data = self.data
        if not self.check():
            raise ValueError('File is not a Heroes3 Save Game')

    def save(self, filename: str):
        """
        Heroes 3 file is GZiped with a special version without CRC check
        """
        with gzip.GzipFile(filename, "wb") as f:
            f.write(bytes(self.data))

    def check(self):
        if self.data[0:5] == b'H3SVG':
            return True
        return False