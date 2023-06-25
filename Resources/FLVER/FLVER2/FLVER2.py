from ....Utilities import *

from .Material import *

from ..Dummy import *

class FLVER2:

    class FLVERHeader :

        def __init__(self) -> None:
            self.big_endian = False
            self.version = 0x20014
            self.bounding_box_min = None
            self.bounding_box_max = None
            self.unicode = True
            self.unk_4A = 0
            self.unk_4C = 0
            self.unk_5C = 0
            self.unk_5D = 0
            self.unk_68 = 0

    def __init__(self) -> None:
        self.dummies = []
        self.materials = []
        self.bones = []
        self.meshes = []

    def read(self, br):

        header = FLVER2.FLVERHeader()

        br.bytesToString(br.readBytes(6)).replace("\0", "")
        header.big_endian = br.bytesToString(br.readBytes(2)).replace("\0", "") == "B"

        if header.big_endian:
            br.endian = ">"

        header.version = br.readInt()
        
        data_offset = br.readInt()
        br.readInt()
        dummy_count = br.readInt()
        material_count = br.readInt()
        bone_count = br.readInt()
        mesh_count = br.readInt()
        vertex_buffer_count = br.readInt()

        header.bounding_box_min = (br.readFloat(), br.readFloat(), br.readFloat())
        header.bounding_box_max = (br.readFloat(), br.readFloat(), br.readFloat())

        br.readInt()
        br.readInt()

        vertex_index_size = br.readByte()
        header.unicode = br.readByte() == 1
        header.unk_4A = br.readByte()
        br.readByte()

        header.unk_4C = br.readInt()

        face_set_count = br.readInt()
        buffer_layout_count = br.readInt()
        texture_count = br.readInt()
        
        header.unk_5C = br.readByte()
        header.unk_5D = br.readByte()
        br.readByte()
        br.readByte()

        br.readInt()
        br.readInt()
        header.unk_68 = br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        print(br.tell())

        for i in range(dummy_count):
            dummy = Dummy()
            dummy.read(br, self.version)
            self.dummies.append(dummy)

        GX_list_indices = {}
        GX_lists = [] 
        for i in range(material_count):
            material = Material()
            material.read(br, self, header, GX_lists, GX_list_indices)
            self.materials.append(material)

