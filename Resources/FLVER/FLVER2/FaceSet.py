class FaceSet:

    def __init__(self) -> None:
        self.flags = None
        self.triangle_strip = False
        self.cull_back_faces = True
        self.unk_06 = 0
        self.indices = []

    def read(self, br, header, header_index_size, data_offset):
        self.flags = br.readInt()
        self.triangle_strip = br.readInt() == 1
        self.cull_back_faces = br.readInt() == 1
        self.unk_06 = br.readShort()
        index_count = br.readInt()
        indices_offset = br.readInt()

        index_size = 0  
        if header.version > 0x20005:
            br.readInt()
            br.readInt()
            index_size = br.readInt()
            br.readInt()

        if index_size == 0:
            index_size = header_index_size

        if index_size == 8:
            save_position = br.tell()
            br.seek(data_offset + indices_offset, 0)
            br.seek(save_position, 0)

        elif index_size == 16:
            pass
        
        elif index_size == 32:
            pass
        
        
            


        