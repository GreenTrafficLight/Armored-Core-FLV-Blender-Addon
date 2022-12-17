from enum import Enum

from ...Utilities import *

class FLVER_CLASS:

    def __init__(self) -> None:
        pass

    class BONE:
        
        def __init__(self) -> None:
            
            self.name = ""
            self.parent_index = -1
            self.child_index = -1
            self.next_sibling_index = -1
            self.previous_sibling_index = -1
            self.translation = None
            self.rotation = None
            self.scale = None
            self.bouding_box_min = None
            self.bouding_box_max = None
            self.unk_3C = 0

        def read(self, br, unicode):

            self.translation = Vector3.fromBytes(br.readBytes(12))
            name_offset = br.readInt()
            self.rotation = Vector3.fromBytes(br.readBytes(12))
            self.parent_index = br.readShort()
            self.child_index = br.readShort()
            self.scale = Vector3.fromBytes(br.readBytes(12))
            self.next_sibling_index = br.readShort()
            self.previous_sibling_index = br.readShort()
            self.bouding_box_min = Vector3.fromBytes(br.readBytes(12))
            self.unk_3C = br.readInt()
            self.bouding_box_max = Vector3.fromBytes(br.readBytes(12))
            br.seek(0x34, 1)
            save_position = br.tell()
            br.seek(name_offset)
            self.name = br.readString()
            br.seek(save_position)

    class LAYOUT_MEMBER :

        def __init__(self) -> None:
            
            self.unk00 = 0
            self.type = None
            self.semantic = None
            self.index = 0

        def read(self, br, struct_offset):

            self.unk00 = br.readInt()
            br.readInt()
            self.type = FLVER_CLASS.LAYOUT_MEMBER.TYPE(br.readUInt())
            self.semantic = FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC(br.readUInt())
            self.index = br.readInt()

        def get_size(self):

            if (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):
                return 4
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short2_to_float2):
                return 4
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv):
                return 4
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv_pair):
                return 8
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short_bone_indices):
                return 8
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A or self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4B):
                return 8
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float2):
                return 8
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):
                return 12
            elif (self.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):
                return 16

        class TYPE(Enum):

            float2 = 0x1
            float3 = 0x2
            float4 = 0x3
            byte4A = 0x10
            byte4B = 0x11
            short2_to_float2 = 0x12
            byte4C = 0x13
            byte4D = 0x14
            uv = 0x15
            uv_pair = 0x16
            short_bone_indices = 0x18
            short4_to_float4A = 0x1A
            short4_to_float4B = 0x2E
            byte4E = 0x2F
            edge_compressed = 0xF0

        class SEMANTIC(Enum):

            position = 0
            bone_weights = 1
            bone_indices = 2
            normal = 3
            uv = 5
            tangent = 6
            bitangent = 7
            vertex_color = 10

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

            for member in layout.members:

                if (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.position):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        self.position = (br.readFloat(), br.readFloat(), br.readFloat())

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        self.position = (br.readFloat(), br.readFloat(), br.readFloat())
                        br.readFloat()

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.edge_compressed):

                        pass

                    else:

                        pass

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bone_weights):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A):

                        self.bone_weights = (br.readByte() / 127, br.readByte() / 127, br.readByte() / 127, br.readByte() / 127)

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C):

                        self.bone_weights = (br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255)

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv_pair or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A):

                         self.bone_weights = (br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767)

                    else:
                        pass

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bone_indices):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        self.bone_indices = (br.readUByte(), br.readUByte(), br.readUByte(), br.readUByte())

                    elif (member.Type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short_bone_indices):

                        self.bone_indices = (br.readUShort(), br.readUShort(), br.readUShort(), br.readUShort())

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.normal):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        self.normal = (br.readFloat(), br.readFloat(), br.readFloat())

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        self.normal = (br.readFloat(), br.readFloat(), br.readFloat())
                        w = br.readFloat()
                        self.normal_w = int(w)

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):
                
                        self.normal = ((br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127)
                        self.normal_w = br.readUByte()

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short2_to_float2):

                        self.normal_w = br.readUByte()
                        z, y, x = br.readByte() / 127, br.readByte() / 127, br.readByte() / 127
                        self.normal = (x, y, z)

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4B):

                        self.normal = (br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767)
                        self.normal_w = br.readUShort()

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.uv):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float2):

                        self.uvs.append((br.readFloat(), br.readFloat()))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        self.uvs.append = ((br.readFloat(), br.readFloat(), br.readFloat()))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        self.uvs.append((br.readFloat(), br.readFloat()))
                        self.uvs.append((br.readFloat(), br.readFloat()))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short2_to_float2 or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv):

                        self.uvs.append((br.readUShort() / uv_factor, br.readUShort() / uv_factor))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv_pair):

                        self.uvs.append((br.readUShort() / uv_factor, br.readUShort() / uv_factor))
                        self.uvs.append((br.readUShort() / uv_factor, br.readUShort() / uv_factor))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4B):

                        self.uvs.append((br.readUShort() / uv_factor, br.readUShort() / uv_factor, br.readUShort() / uv_factor))
                        br.readUShort()

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.tangent):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        self.tangent.append((Vector4.fromBytes(br.readBytes(16))))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        self.tangent.append(((br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127))

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A):

                        self.tangent.append((br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767))

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bitangent):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        self.bitangent = ((br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127)

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.vertex_color):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        self.colors.append([br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat()])

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C):

                        self.colors.append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

    class VERTICES:

        def __init__(self) -> None:
            self.positions = []
            self.bone_weights = []
            self.bone_indices = []
            self.normals = []
            self.normal_ws = []
            self.uvs = []
            self.tangents = []
            self.bitangents = []
            self.colors = []

        def read(self, br, layout, uv_factor, vertex_count):

            save_position = br.tell()

            position = 0

            for member in layout.members:

                if (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.position):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.positions.append([br.readFloat(), br.readFloat(), br.readFloat()])
                        
                        position += 12
                        
                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.position.append([br.readFloat(), br.readFloat(), br.readFloat()])
                            br.readFloat()
                        
                        position += 16
                    
                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bone_weights):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bone_weights.append([br.readByte() / 127, br.readByte() / 127, br.readByte() / 127, br.readByte() / 127])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bone_weights.append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv_pair or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bone_weights.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])

                        position += 8

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bone_indices):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bone_indices.append([br.readUByte(), br.readUByte(), br.readUByte(), br.readUByte()])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short_bone_indices):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bone_indices.append([br.readUShort(), br.readUShort(), br.readUShort(), br.readUShort()])

                        position += 8

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.normal):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.normals.append([br.readFloat(), br.readFloat(), br.readFloat()])

                        position += 12

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.normals.append([br.readFloat(), br.readFloat(), br.readFloat()])
                            w = br.readFloat()
                            self.normal_ws.append(int(w))

                        position += 16

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):
                        
                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)                        
                            self.normals.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])
                            self.normal_ws.append(br.readUByte())

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short2_to_float2):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)     
                            self.normal_ws.append(br.readUByte())
                            z, y, x = br.readByte() / 127, br.readByte() / 127, br.readByte() / 127
                            self.normals.append([x, y, z])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4B):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)    
                            self.normals.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])
                            self.normal_ws.append(br.readUShort())

                        position += 8

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.uv):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float2):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readFloat(), br.readFloat()])

                        position += 8

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float3):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readFloat(), br.readFloat(), br.readFloat()])

                        position += 12

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):
                        
                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readFloat(), br.readFloat()])
                            self.uvs.append([br.readFloat(), br.readFloat()])

                        position += 16

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short2_to_float2 or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readUShort() / uv_factor, br.readUShort() / uv_factor])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.uv_pair):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readUShort() / uv_factor, br.readUShort() / uv_factor])
                            self.uvs.append([br.readUShort() / uv_factor, br.readUShort() / uv_factor])

                        position += 8

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4B):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.uvs.append([br.readUShort() / uv_factor, br.readUShort() / uv_factor, br.readUShort() / uv_factor])
                            br.readUShort()

                        position += 8

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.tangent):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.tangents.append(Vector4.fromBytes(br.readBytes(16)))

                        position += 16

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.tangents.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])

                        position += 4

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.short4_to_float4A):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.tangents.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])

                        position += 8

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.bitangent):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4B or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4D or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4E):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.bitangents.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])

                        position += 4

                elif (member.semantic == FLVER_CLASS.LAYOUT_MEMBER.SEMANTIC.vertex_color):

                    if (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.float4):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.colors.append([br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat()])

                        position += 16

                    elif (member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4A or member.type == FLVER_CLASS.LAYOUT_MEMBER.TYPE.byte4C):

                        for i in range(vertex_count):
                            br.seek(save_position + layout.size * i + position)
                            self.colors.append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                        position += 4
