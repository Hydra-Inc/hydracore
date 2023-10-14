import struct

from dataclasses import dataclass
from typing import Optional


@dataclass
class Chunk():
    blob: bytes                        # chunk of blobl offset
    start: int                         # offset of this chunk in ORIGINAL buffer
    end: int                           # end offset of this CHUNK in ORIGINAL buffer
    orig_blob: Optional[bytes] = None  # store original blob

    @staticmethod
    def New(blob: bytes, start: int, end: int):
        return Chunk(blob, start, end, None)

    @staticmethod
    def NewAndKeep(blob: bytes, start: int, end: int):
        return Chunk(blob, start, end, blob)

    def to_uint(self, off: int, length: int) -> int:
        """
        Get the uint at offset

        off - offset from the begin of the blob
        length - how much to extract
        """
        fmt = {1: "<B", 2: "<H", 4: "<L", 8: "<Q"}[length]
        return struct.unpack(fmt, self.blob[off:off+length])[0]

    def to_byte(self, off: int) -> int:
        return self.to_uint(off, 1)
    
    def to_short(self, off: int) -> int:
        return self.to_uint(off, 2)
    
    def to_long(self, off: int) -> int:
        return self.to_uint(off, 4)

    def to_long_long(self, off: int) -> int:
        return self.to_uint(off, 8)
    
    def put_uint(self, num: int, off: int, length: int) -> int:
        """
        Put uint to offset in blob

        off - offset from the begin of the blob
        length - how much to write
        """
        fmt = {1: "<B", 2: "<H", 4: "<L", 8: "<Q"}[length]
        self.blob[off:off+length] = bytearray(struct.pack(fmt, num))

    def put_byte(self, x: int, off: int):
        return self.put_uint(x, off, 1)
    
    def put_short(self, x: int, off: int):
        return self.put_uint(x, off, 2)
    
    def put_long(self, x: int, off: int):
        return self.put_uint(x, off, 4)

    def put_long_long(self, x: int, off: int):
        return self.put_uint(x, off, 8)
    
    def put_str(self, x: bytes, off: int, max: int):
        if len(x) > max:
            raise ValueError(f'String {x} larger than max allowed {max} for patching')
        self.blob[off:off+len(x)] = x
        self.blob[off+len(x):off+max+1] = [0x00 for _ in range(max-len(x)+1)] 
        

    def dump(self, filename: str, start: Optional[int] = None, end: Optional[int] = None) -> int:
        """
        Dump contents of the chunk to the requested file
        """
        with open(filename, "wb") as f:
            b = bytes(self.blob[start:end])
            f.write(b)
        return len(b)