from enum import Enum

from ...Utilities import *

class BINDER:

    def __init__(self) -> None:
        pass

    class Format(Enum):

        none = 0
        big_endian = 1
        ids = 2
        names1 = 4
        names2 = 8
        long_offsets = 16
        compression = 32
        flag6 = 64
        flag7 = 128

    def readFormat(br, bit_big_endian):
        raw_format = br.readByte()
        reverse = bit_big_endian or (raw_format & 1) != 0 and (raw_format & 128) == 0
        return BINDER.Format(raw_format if reverse else reverseBits(raw_format))

    def readFileFlag(br, bit_big_endian):
        reverse = bit_big_endian
        raw_flags = br.readByte()
        return BINDER.Format(raw_flags if reverse else reverseBits(raw_flags))
        
    def hasIDs(format):

        return (format & BINDER.Format.ids) != 0

    def hasNames(format):

        return (format & (BINDER.Format.names1 | BINDER.Format.names2)) != 0

    def hasLongOffsets(format):

        return (format & BINDER.Format.long_offsets) != 0

    def hasCompression(format):

        return (format & BINDER.Format.compression) != 0