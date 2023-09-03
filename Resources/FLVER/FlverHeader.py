class FlverHeader:

    def __init__(self) -> None:
        self.big_endian = False
        self.version = 0x20014
        self.data_offset = 0
        self.dummy_count = 0
        self.material_count = 0
        self.bone_count = 0
        self.mesh_count = 0
        self.vertex_buffer_count = 0
        self.bounding_box_min = None
        self.bounding_box_max = None
        self.unicode = True
        self.unk_4A = 0
        self.unk_4C = 0
        self.unk_5C = 0
        self.unk_5D = 0
        self.unk_68 = 0

    def read(self, br):

        br.bytesToString(br.readBytes(6)).replace("\0", "")
        self.big_endian = br.bytesToString(br.readBytes(2)).replace("\0", "") == "B"

        if self.big_endian:
            br.endian = ">"

        self.version = br.readInt()
        
        self.data_offset = br.readInt()
        br.readInt()
        self.dummy_count = br.readInt()
        self.material_count = br.readInt()
        self.bone_count = br.readInt()
        self.mesh_count = br.readInt()
        self.vertex_buffer_count = br.readInt()

        self.bounding_box_min = (br.readFloat(), br.readFloat(), br.readFloat())
        self.bounding_box_max = (br.readFloat(), br.readFloat(), br.readFloat())
        
        br.readInt()
        br.readInt()
        
        self.vertex_index_size = br.readByte()
        self.unicode = br.readByte() == 1
        self.unk4A = br.readByte()
        self.unk4B = br.readByte()
        self.unk4C = br.readInt()
        
        self.face_set_count = br.readInt()
        self.buffer_layout_count = br.readInt()
        self.texture_count = br.readInt()
        
        self.unk5C = br.readByte()
        self.unk5D = br.readByte()
        br.readByte()
        br.readByte()

        br.readBytes(32)