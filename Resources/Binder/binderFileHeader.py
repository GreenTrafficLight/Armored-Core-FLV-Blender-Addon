from .binder import *

class BINDER_FILE_HEADER:

    def __init__(self) -> None:
        self.Flags = None
        self.ID = -1
        self.Name = ""
        self.Compression_type = None
        self.Compressed_size = 0
        self.Uncompressed_size = 0
        self.Data_offset = 0

    def readBinder3FileHeader(self, br, format, bit_big_endian):

        self.Flags = BINDER.readFileFlag(br, bit_big_endian)
        br.readByte()
        br.readByte()
        br.readByte()

        self.Compressed_size = br.readInt()

        if BINDER.hasLongOffsets(format):
            self.Data_offset = br.readLong()
        else:
            self.Data_offset = br.readInt()
            
        if BINDER.hasIDs(format):
            self.ID = br.readInt()

        if BINDER.hasNames(format):
            name_offset = br.readInt()
            save_position_name_offset = br.tell()
            br.seek(name_offset)
            self.Name = br.readString()
            br.seek(save_position_name_offset)

        if BINDER.hasCompression(format):
            self.Uncompressed_size = br.readInt()

        

