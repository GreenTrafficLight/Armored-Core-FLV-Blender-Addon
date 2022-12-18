from ....Resources.FLVER.flver import *
from ....Utilities import *


class FLVER0_CLASS:

    def __init__(self) -> None:
        self.big_endian = False
        self.version = 0
        self.bounding_box_min = None
        self.bounding_box_max = None
        self.vertex_index_size = 0
        self.unicode = False
        self.unk4A = 0
        self.unk4B = 0
        self.unk4C = 0
        self.unk5C = 0

        self.dummies = []
        self.materials = []
        self.bones = []
        self.meshes = []

    def read(self, br):

        br.bytesToString(br.readBytes(6)).replace("\0", "")
        self.big_endian = br.bytesToString(br.readBytes(2)).replace("\0", "") == "B"

        if self.big_endian:
            br.endian = ">"

        self.version = br.readInt()
        data_offset = br.readInt()
        br.readInt()
        dummy_count = br.readInt()
        material_count = br.readInt()
        bone_count = br.readInt()
        mesh_count = br.readInt()
        br.readInt()
        self.bounding_box_min = Vector3.fromBytes(br.readBytes(12))
        self.bounding_box_max = Vector3.fromBytes(br.readBytes(12))
        br.readInt()
        br.readInt()
        self.vertex_index_size = br.readByte()
        unicode = br.readByte() == 1
        self.unk4A = br.readByte()
        self.unk4B = br.readByte()
        self.unk4C = br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        self.unk5C = br.readByte()
        br.readByte()
        br.readByte()
        br.readByte()
        br.readBytes(32)
        print(br.tell())

        for i in range(dummy_count):
            dummy = FLVER_CLASS.DUMMY()
            dummy.read(br, self.version)
            self.dummies.append(dummy)

        print(br.tell())

        for i in range(material_count):
            material = FLVER0_CLASS.MATERIAL()
            material.read(br, self)
            self.materials.append(material)

        for i in range(bone_count):
            bone = FLVER_CLASS.BONE()
            bone.read(br, False)
            self.bones.append(bone)

        print(br.tell())

        for i in range(mesh_count):
            mesh = FLVER0_CLASS.MESH()
            mesh.read(br, self, data_offset)
            self.meshes.append(mesh)

    class DUMMY :

        def __init__(self, br) -> None:
            
            pass

    class MATERIAL :

        def __init__(self) -> None:
            
            self.name = ""
            self.mtd = ""
            self.textures = []
            self.layouts = []

        def read(self, br, flv):

            name_offset = br.readInt()
            mtd_offset = br.readInt()
            textures_offset = br.readInt()
            layouts_offset = br.readInt()
            br.readInt()
            layout_header_offset = br.readInt()
            br.readInt()
            br.readInt()

            save_position = br.tell()

            save_position_textures_offset = br.tell()

            br.seek(name_offset)
            self.name = br.readString()
            br.seek(mtd_offset)
            self.mtd = br.readString()

            br.seek(textures_offset)
            texture_count = br.readByte()
            br.readByte()
            br.readByte()
            br.readByte()
            br.readInt()
            br.readInt()
            br.readInt()

            for i in range(texture_count):
                texture = FLVER0_CLASS.TEXTURE()
                texture.read(br, flv)
                self.textures.append(texture)
                

            br.seek(save_position_textures_offset)

            if layout_header_offset != 0:
                
                save_position_layout_header_offset = br.tell()
                
                br.seek(layout_header_offset)
                layout_count = br.readInt()
                br.readInt()
                br.readInt()
                br.readInt()
                for i in range(layout_count):
                    
                    layout_offset = br.readInt()
                    
                    save_position_layout_offset = br.tell()
                    
                    br.seek(layouts_offset)
                    layout = FLVER0_CLASS.BUFFER_LAYOUT()
                    layout.read(br)
                    self.layouts.append(layout)
                    
                    br.seek(save_position_layout_offset)

                br.seek(save_position_layout_header_offset)

            br.seek(save_position)

    class TEXTURE :

        def __init__(self) -> None:
            
            self.type = ""
            self.path = ""

        def read(self, br, flv):

            path_offset = br.readUInt()
            type_offset = br.readUInt()
            br.readUInt()
            br.readUInt()

            save_position = br.tell()

            br.seek(path_offset)
            self.path = br.readString()
            if type_offset > 0:
                br.seek(type_offset)
                self.type = br.readString()

            br.seek(save_position)

    class BUFFER_LAYOUT :

        def __init__(self) -> None:

            self.size = 0
            self.members = []

        def read(self, br):
            
            member_count = br.readUShort()
            struct_size =  br.readUShort()
            br.readUInt()
            br.readUInt()
            br.readUInt()

            struct_offset = 0
            capacity = member_count
            for i in range(member_count):

                member = FLVER_CLASS.LAYOUT_MEMBER()
                member.read(br, struct_offset)
                self.size += member.get_size()
                self.members.append(member)

    class MESH:

        def __init__(self) -> None:
            self.dynamic = 0
            self.material_index = 0
            self.unk02 = False
            self.unk03 = 0
            self.default_bone_index = 0
            self.bone_indices = []
            self.unk46 = 0
            self.vertex_indices = []
            self.vertices = []
            self.layout_index = []

        def read(self, br, flv, data_offset):

            self.dynamic = br.readByte()
            self.material_index = br.readByte()
            self.unk02 = br.readByte() == 1
            self.unk03 = br.readByte()

            vertex_index_count = br.readUInt()
            vertex_count = br.readUInt()
            self.default_bone_index = br.readUShort()
            for i in range(28):
                self.bone_indices.append(br.readUShort())
            self.unk46 = br.readUShort()
            br.readUInt()
            vertex_indices_offset = br.readUInt()
            buffer_data_length = br.readUInt()
            buffer_data_offset = br.readUInt()
            vertex_buffers_offset1 = br.readUInt() 
            vertex_buffers_offset2 = br.readUInt()
            br.readUInt()

            save_position_vertex_indices_offset = br.tell()

            br.seek(data_offset + vertex_indices_offset)

            if flv.vertex_index_size == 16:

                for i in range(vertex_index_count):
                    self.vertex_indices.append(br.readUShort())

            elif flv.vertex_index_size == 32:

                for i in range(vertex_index_count):
                    self.vertex_indices.append(br.readUInt()) 

            br.seek(save_position_vertex_indices_offset)

            if (vertex_buffers_offset1 == 0):
                buffer = FLVER0_CLASS.VERTEX_BUFFER()
                buffer.buffer_length = buffer_data_length
                buffer.buffer_offset = buffer_data_offset
                buffer.layout_index = 0
            else:
                save_position_vertex_buffers_offset1 = br.tell()

                br.seek(vertex_buffers_offset1)
                vertex_buffers1 = FLVER0_CLASS.VERTEX_BUFFER().read_vertex_buffers(br)

                buffer = vertex_buffers1[0]

                br.seek(save_position_vertex_buffers_offset1)

            if vertex_buffers_offset2 != 0:
                save_position_vertex_buffers_offset2 = br.tell()

                br.seek(vertex_buffers_offset2)
                vertex_buffers2 = FLVER0_CLASS.VERTEX_BUFFER().read_vertex_buffers(br)

                br.seek(save_position_vertex_buffers_offset2)

            save_position_buffer_offset = br.tell()

            br.seek(data_offset + buffer.buffer_offset)
            self.layout_index = buffer.layout_index
            layout = flv.materials[self.material_index].layouts[self.layout_index]

            uv_factor = 1024
            
            """
            for i in range(vertex_count):
                
                vertex = FLVER_CLASS.VERTEX()
                print(br.tell())
                vertex.read(br, layout, uv_factor)
                self.vertices.append(vertex)
            """
            self.vertices = FLVER_CLASS.VERTICES()
            self.vertices.read(br, layout, uv_factor, vertex_count)

            br.seek(save_position_buffer_offset)

    class VERTEX_BUFFER:

        def __init__(self) -> None:
            self.layout_index = 0
            self.buffer_length = 0
            self.buffer_offset = 0

        def read(self, br):

            self.layout_index = br.readInt()
            self.buffer_length = br.readInt()
            self.buffer_offset = br.readInt()
            br.readInt()

        def read_vertex_buffers(self, br):

            buffer_count = br.readInt()
            buffers_offset = br.readInt()
            br.readInt()
            br.readInt()

            buffers = []
            br.seek(buffers_offset)
            for i in range(buffer_count):
                buffer = FLVER0_CLASS.VERTEX_BUFFER()
                buffer.read(br)
                buffers.append(buffer)

            return buffers




