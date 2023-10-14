import re

from typing import List, Iterator, Match, Tuple, Optional

from .chunk import Chunk

# --------------------------------------------------------------- Interface --


class BinFileBase:

    def load(self, filename: str):
        """
        Load binary data from file

        filename - name of the file to load our binary data
        """
        raise NotImplementedError()

    def save(self, filename: str):
        """
        Save binary data to file as in original format

        filename - name of the file to store our binary data
        """
        raise NotImplementedError()

    def dump(self, filename: str):
        """
        Dump binary data to file for hex comparizon and debug
        E.g. if the file for zipped, this function dumps unzipped data.
        And save() stores the zipped file as required.

        filename - name of the file to store our binary data
        """
        raise NotImplementedError()

    def patch(self, chunk: Chunk, same_length: bool = True):
        """
        Patch RAW data from chunk

        chunk - arry of bytes with location and etc
        same_length - we expect chunk should be same length
        """
        raise NotImplementedError()

    def patch_bytes(self, start: int, end: int, data: bytearray, same_length: bool = True):
        """
        Patch RAW data from start index to end index with the array of bytes

        start, end - start and end index of the segment to patch
        data - bytes, can be longer or shorter than the patched segment.
        """
        raise NotImplementedError()

    def get_diff(self) -> List:
        """
        Get diffs of the current binary data with the original ones,
        returns list of different indexes in format [from, to]
        """
        raise NotImplementedError()

    def regex_search(self, regex, extra=0) -> Iterator[Chunk]:
        """
        Returns iterator which iterate over the bin data using Regex search

        Each elements is in format of tuple:
          (data, start, end)

        extra - returns extra data around the found location
                extra in bytes
        """
        raise NotImplementedError()

    def substr_search(self, substr: bytes, extra=0) -> Iterator[Chunk]:
        """
        Iterates over file and locates the substr and yeilds each found location

        Each element is in format of tuple:
          (data, start, end)

        extra - returns extra data around the found location
                extra in bytes
        """
        raise NotImplementedError()

    def check(self) -> bool:
        """
        Checks that a binary file is okay
        """
        raise NotImplementedError()

    @property
    def binary_data(self) -> bytes:
        """
        Returns the data array
        """
        raise NotImplementedError()

# ---------------------------------------------------------- Implementation --


class BinFile(BinFileBase):

    def __init__(self, filename: str):
        self.filename = filename
        self.data = None
        self.orig_data = None
        self.size = 0
        self.load(filename)

    def check(self) -> bool:
        return True

    def load(self, filename: str):
        with open(filename, "rb") as f:
            self.data = bytearray(f.read())
        self.size = len(self.data)
        self.orig_data = self.data

    def save(self, filename: str):
        with open(filename, "wb") as f:
            f.write(bytes(self.data))

    def dump(self, filename: str):
        with open(filename, "wb") as f:
            f.write(bytes(self.data))

    def patch(self, chunk: Chunk, same_length: bool = True):
        self.patch_bytes(chunk.start, chunk.end, chunk.blob,
                         same_length=same_length)

    def patch_bytes(self, start: int, end: int, data: bytearray, same_length: bool = True):
        if same_length:
            self.data[start:end] = data
        else:
            self.data = self.data[0:start] + data + self.data[end:]
            self.size = len(self.data)

    def get_diff(self) -> List:
        raise NotImplementedError()

    def regex_search(self, regex, extra: Optional[int] = None) -> Iterator[Tuple[Chunk, Match]]:
        pos = 0
        m = re.search(regex, self.data)
        while m:
            start, end = m.span()
            start_r = start_g = pos + start
            end_r = end_g = pos + end

            if extra:
                start_r -= extra
                if start_r < 0:
                    start = 0
                end_r += extra
                if end_r >= len(self.data):
                    end_r = len(self.data)

            blob = bytearray(self.data[start_r:end_r])
            yield (Chunk.New(blob, start_r, end_r), m)
            # pos = start_g + 1
            pos = end_g
            m = re.search(regex, self.data[pos:])

    def substr_search(self, substr: bytes, extra: Optional[int] = None) -> Iterator[Chunk]:
        pos = 0
        m = self.data.find(substr, pos)
        while m >= 0:
            start = m
            end = m + len(substr)
            start_r = start
            end_r = end
            if extra:
                start_r -= extra
                if start_r < 0:
                    start = 0
                end_r += extra
                if end_r >= len(self.data):
                    end_r = len(self.data)
            blob = bytearray(self.data[start_r:end_r])
            yield Chunk.New(blob, start_r, end_r)
            pos = end
            m = self.data.find(substr, pos)

    @property
    def binary_data(self) -> bytes:
        return self.data