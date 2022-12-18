from ...Binder import *

from ....Utilities import *

class BND3: 

    def __init__(self) -> None:
        pass

    def readHeader(self, br):

        br.bytesToString(br.readBytes(4)).replace("\0", "")
        version = br.bytesToString(br.readBytes(8)).replace("\0", "")

        bit_big_endian = br.getBoolean(0xE)

        format = BINDER.readFormat(br, bit_big_endian)
        big_endian = br.readByte() == 1
        br.readByte()
        br.readByte()

        file_count = br.readInt()
        br.readInt()
        unk18 = br.readInt()
        br.readInt()

        file_headers = []
        for i in range(file_count):
            binder_file_header = BINDER_FILE_HEADER()
            binder_file_header.readBinder3FileHeader(br, format, bit_big_endian)
            file_headers.append(binder_file_header)

        return file_headers
