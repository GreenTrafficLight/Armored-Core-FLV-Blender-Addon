from ....Utilities import *
from ...FLVER import *

class FLVER0:

    def __init__(self) -> None:
        self.big_endian = False
        self.version = 0
        self.bounding_box_min = None
        self.bounding_box_max = None
        self.dummies = []
        self.materials = []
        self.bones = []
        self.meshes = []

    def read(self, br):

        br.bytesToString(br.readBytes(6)).replace("\0", "")
        self.big_endian = br.bytesToString(br.readBytes(2)).replace("\0", "") == "B"

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
            self.materials.append(FLVER0.MATERIAL().read(br, self))

        for i in range(bone_count):
            self.bones.append(FLVER.BONE().read(br, False))

        for i in range(mesh_count):
            pass

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

        def read(self, br, flv):

            path_offset = br.readInt()
            type_offset = br.readInt()
            br.readInt()
            br.readInt()

            br.seek(path_offset)
            self.path = br.readString()
            if type_offset > 0:
                br.seek(type_offset)
                self.type = br.readString()

    class BUFFER_LAYOUT :

        def __init__(self) -> None:

            self.members = []

        def read(self, br):
            
            member_count = br.readShort()
            struct_size =  br.readShort()
            br.readInt()
            br.readInt()
            br.readInt()

            struct_offset = 0
            capacity = member_count
            for i in range(member_count):

                member = FLVER.LAYOUT_MEMBER()
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

            vertex_index_count = br.readInt()
            vertex_count = br.readInt()
            self.default_bone_index = br.readShort()
            for i in range(28):
                self.bone_indices.append(br.readShort())
            self.unk46 = br.readShort()
            br.readInt()
            vertex_indices_offset = br.readInt()
            buffer_data_length = br.readInt()
            buffer_data_offset = br.readInt()
            vertex_buffers_offset1 = br.readInt() 
            vertex_buffers_offset2 = br.readInt()
            br.readInt()

            if flv.vertex_index_size == 16:

                br.seek(data_offset + vertex_indices_offset)
                for i in range(vertex_index_count):
                    self.vertex_indices.append(br.readShort())

            elif flv.vertex_index_size == 32:

                br.seek(data_offset + vertex_indices_offset)
                for i in range(vertex_index_count):
                    self.vertex_indices.append(br.readInt()) 

            if (vertex_buffers_offset1 == 0):
                buffer = FLVER0.VERTEX_BUFFER()
                buffer.buffer_length = buffer_data_length
                buffer.buffer_offset = buffer_data_offset
                buffer.layout_index = 0
            else:
                br.seek(vertex_buffers_offset1)
                vertex_buffers1 = FLVER0.VERTEX_BUFFER.read_vertex_buffers(self, br)
            
                buffer = vertex_buffers1[0]

            if vertex_buffers_offset2 != 0:
                br.seek(vertex_buffers_offset2)
                vertex_buffers2 = FLVER0.VERTEX_BUFFER.read_vertex_buffers(self, br)

            br.seek(data_offset + buffer.buffer_offset)
            self.layout_index = buffer.layout_index
            layout = flv.materials[self.material_index].layouts[self.layout_index]

            uv_factor = 1024
            
            for i in range(vertex_count):
                pass

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
                buffers.append(FLVER0.VERTEX_BUFFER().read(br))

            return buffers

    class VERTEX:

        def __init__(self) -> None:
            self.position = None
            self.bone_weights = None
            self.bone_indices = None
            self.normal = None
            self.normal_w = 0
            self.uvs = []
            self.tangent = []
            self.bitangent = None
            self.colors = []

        def read(self, br, layout, uv_factor):

            for member in layout:

                if (member.semantic == FLVER.LAYOUT_MEMBER.SEMANTIC.position):

                    if (member.type == FLVER.LAYOUT_MEMBER.TYPE.float3):

                        self.position = (br.readFloat(), br.readFloat(), br.readFloat())

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.float4):

                        self.position = (br.readFloat(), br.readFloat(), br.readFloat())
                        br.readFloat()

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.edge_compressed):

                        pass

                    else:

                        pass

                elif (member.semantic == FLVER.LAYOUT_MEMBER.SEMANTIC.bone_weights):

                    if (member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4A):

                        self.bone_weights = (br.readByte() / 127, br.readByte() / 127, br.readByte() / 127, br.readByte() / 127)

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4C):

                        self.bone_weights = (br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255)

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.uv_pair or member.type == FLVER.LAYOUT_MEMBER.TYPE.short4_to_float4A):

                         self.bone_weights = (br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767)

                    else:
                        pass

                elif (member.semantic == FLVER.LAYOUT_MEMBER.SEMANTIC.bone_indices):

                    if (member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4E):

                        self.bone_indices = (br.readUByte(), br.readUByte(), br.readUByte(), br.readUByte())

                    elif (member.Type == FLVER.LAYOUT_MEMBER.TYPE.short_bone_indices):

                        self.bone_indices = (br.readUShort(), br.readUShort(), br.readUShort(), br.readUShort())

                elif (member.semantic == FLVER.LAYOUT_MEMBER.SEMANTIC.normal):

                    if (member.type == FLVER.LAYOUT_MEMBER.TYPE.float3):

                        self.normal = (br.readFloat(), br.readFloat(), br.readFloat())

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.float4):

                        self.normal = (br.readFloat(), br.readFloat(), br.readFloat())
                        w = br.readFloat()
                        self.normal_w = int(w)

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER.LAYOUT_MEMBER.TYPE.byte4E):
                
                        self.normal = ((br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127)
                        self.normal_w = br.readUByte()

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.short2_to_float2):

                        self.normal_w = br.readUByte()
                        z, y, x = br.readByte() / 127, br.readByte() / 127, br.readByte() / 127
                        self.normal = (x, y, z)

                    elif (member.type == FLVER.LAYOUT_MEMBER.TYPE.short4_to_float4A or member.type == FLVER.LAYOUT_MEMBER.TYPE.short4_to_float4B):

                        self.normal = (br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767)
                        self.normal_w = br.readUShort()


