from ....Utilities import *

class FLVER0:

    def __init__(self) -> None:
        self.big_endian = False
        self.version = 0
        self.bounding_box_min = None
        self.bounding_box_max = None

    def read(self, br):

        br.bytesToString(br.readBytes(6)).replace("\0", "")
        self.big_endian = br.bytesToString(br.readBytes(2)).replace("\0", "") == "B"

        version = br.readInt()
        data_offset = br.readInt()
        br.readInt()
        dummy_count = br.readInt()
        material_count = br.readInt()
        bone_count = br.readInt()
        mesh_count = br.readInt()
        br.readInt()
        bounding_box_min = br.readInt()
        bounding_box_max = 0
        br.readInt()
        br.readInt()
        br.readByte()
        unicode = br.readByte() == 1
        br.readByte()
        br.readByte()
        br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        br.readByte()
        br.readByte()
        br.readByte()
        br.readByte()
        br.readBytes(32)

        for i in range(dummy_count):
            pass

        for i in range(material_count):
            pass

        for i in range(bone_count):
            pass

    class DUMMY :

        def __init__(self, br) -> None:
            
            pass

    class MATERIAL :

        def __init__(self, br, flv) -> None:
            
            self.name = ""
            self.mtd = ""
            self.textures = []
            self.layouts = []

            name_offset = br.readInt()
            mtd_offset = br.readInt()
            textures_offset = br.readInt()
            layouts_offset = br.readInt()
            br.readInt()
            layout_header_offset = br.readInt()
            br.readInt()
            br.readInt()

            br.seek(name_offset)
            self.name = br.readString()
            br.seek(mtd_offset)
            self.mtd = br.readString()

            br.seek(textures_offset)
            texture_count = br.readInt()
            br.readByte()
            br.readByte()
            br.readByte()
            br.readInt()
            br.readInt()
            br.readInt()

            for i in range(texture_count):
                self.textures.append(FLVER0.TEXTURE(br, flv))

            if layout_header_offset != 0:
                br.seek(layout_header_offset)
                layout_count = br.readInt()
                br.readInt()
                br.readInt()
                br.readInt()
                for i in range(layout_count):
                    layout_offset = br.readInt()
                    br.seek(layouts_offset)
                    self.layouts.append(FLVER0.BUFFER_LAYOUT(br))

    class TEXTURE :

        def __init__(self, br, flv) -> None:
            
            self.type = ""
            self.path = ""

            path_offset = br.readInt()
            type_offset = br.readInt()
            br.readInt()
            br.readInt()

            br.seek(path_offset)
            path = br.readString()
            if type_offset > 0:
                br.seek(type_offset)
                type = br.readString()

    class BUFFER_LAYOUT :

        def __init__(self, br) -> None:
            
            member_count = br.readShort()
            struct_size =  br.readShort()
            br.readInt()
            br.readInt()
            br.readInt()

            struct_offset = 0
            capacity = member_count
            






        


