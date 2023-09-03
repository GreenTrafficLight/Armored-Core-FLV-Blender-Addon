from .LayoutMember import *

from ...Utilities import *

class Vertices:

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
        self.unknowns = []
        self.has_already_bone_indices = False

    def read(self, br, layout, uv_factor, vertex_count):

        save_position = br.tell()

        position = 0

        for member in layout.members:

            if (member.semantic == LayoutMember.LayoutSemantic.POSITION):

                if (member.type == LayoutMember.LayoutType.float3):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.positions.append(Vector((br.readFloat(), br.readFloat(), br.readFloat())))
                    
                    position += 12
                    
                elif (member.type == LayoutMember.LayoutType.float4):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.position.append(Vector((br.readFloat(), br.readFloat(), br.readFloat())))
                        br.readFloat()
                    
                    position += 16
                
            elif (member.semantic == LayoutMember.LayoutSemantic.BONE_WEIGHTS):

                if (member.type == LayoutMember.LayoutType.byte4A):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bone_weights.append([br.readByte() / 127, br.readByte() / 127, br.readByte() / 127, br.readByte() / 127])

                    position += 4

                elif (member.type == LayoutMember.LayoutType.byte4C):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bone_weights.append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                    position += 4

                elif (member.type == LayoutMember.LayoutType.uv_pair or member.type == LayoutMember.LayoutType.short4_to_float4A):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bone_weights.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])

                    position += 8

            elif (member.semantic == LayoutMember.LayoutSemantic.BONE_INDICES):

                if (member.type == LayoutMember.LayoutType.byte4B or member.type == LayoutMember.LayoutType.byte4E):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bone_indices.append([br.readUByte(), br.readUByte(), br.readUByte(), br.readUByte()])

                    position += 4

                elif (member.type == LayoutMember.LayoutType.short2_to_float2):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        [br.readUByte(), br.readUByte(), br.readUByte()]
                        self.bone_indices.append(br.readUByte())

                    position += 4

                elif (member.type == LayoutMember.LayoutType.short_bone_indices):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bone_indices.append([br.readUShort(), br.readUShort(), br.readUShort(), br.readUShort()])

                    position += 8
                
                self.has_already_bone_indices = True

            elif (member.semantic == LayoutMember.LayoutSemantic.NORMAL):

                if (member.type == LayoutMember.LayoutType.float3):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.normals.append([br.readFloat(), br.readFloat(), br.readFloat()])

                    position += 12

                elif (member.type == LayoutMember.LayoutType.float4):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.normals.append([br.readFloat(), br.readFloat(), br.readFloat()])
                        w = br.readFloat()
                        self.normal_ws.append(int(w))

                    position += 16

                elif (member.type == LayoutMember.LayoutType.byte4A or member.type == LayoutMember.LayoutType.byte4B or member.type == LayoutMember.LayoutType.byte4C or member.type == LayoutMember.LayoutType.byte4D or member.type == LayoutMember.LayoutType.byte4E):
                    
                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)                        
                        self.normals.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])
                        self.normal_ws.append(br.readUByte())

                    position += 4

                elif (member.type == LayoutMember.LayoutType.short2_to_float2):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        if not self.has_already_bone_indices:     
                            self.bone_indices.append(br.readUByte())
                        else:
                            w = br.readByte() / 127
                        z, y, x = br.readByte() / 127, br.readByte() / 127, br.readByte() / 127
                        self.normals.append(Vector((x, y, z)).normalized())

                    position += 4

                elif (member.type == LayoutMember.LayoutType.short4_to_float4A or member.type == LayoutMember.LayoutType.short4_to_float4B):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)    
                        self.normals.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])
                        self.normal_ws.append(br.readUShort())

                    position += 8

            elif (member.semantic == LayoutMember.LayoutSemantic.UV):

                if (member.type == LayoutMember.LayoutType.float2):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readFloat(), br.readFloat()])

                    position += 8

                elif (member.type == LayoutMember.LayoutType.float3):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readFloat(), br.readFloat(), br.readFloat()])

                    position += 12

                elif (member.type == LayoutMember.LayoutType.float4):
                    
                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readFloat(), br.readFloat()])
                        self.uvs.append([br.readFloat(), br.readFloat()])

                    position += 16

                elif (member.type == LayoutMember.LayoutType.byte4A or member.type == LayoutMember.LayoutType.byte4B or member.type == LayoutMember.LayoutType.short2_to_float2 or member.type == LayoutMember.LayoutType.byte4C or member.type == LayoutMember.LayoutType.uv):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readShort() / uv_factor, br.readShort() / uv_factor])

                    position += 4

                elif (member.type == LayoutMember.LayoutType.uv_pair):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readShort() / uv_factor, br.readShort() / uv_factor])
                        self.uvs.append([br.readShort() / uv_factor, br.readShort() / uv_factor])

                    position += 8

                elif (member.type == LayoutMember.LayoutType.short4_to_float4B):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.uvs.append([br.readShort() / uv_factor, br.readShort() / uv_factor, br.readShort() / uv_factor])
                        br.readShort()

                    position += 8

            elif (member.semantic == LayoutMember.LayoutSemantic.TANGENT):

                if (member.type == LayoutMember.LayoutType.float4):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.tangents.append(Vector4.fromBytes(br.readBytes(16)))

                    position += 16

                elif (member.type == LayoutMember.LayoutType.byte4A or member.type == LayoutMember.LayoutType.byte4B or member.type == LayoutMember.LayoutType.byte4C or member.type == LayoutMember.LayoutType.byte4D or member.type == LayoutMember.LayoutType.byte4E):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.tangents.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])

                    position += 4

                elif (member.type == LayoutMember.LayoutType.short4_to_float4A):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.tangents.append([br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767, br.readUShort() / 32767])

                    position += 8

            elif (member.semantic == LayoutMember.LayoutSemantic.BITANGENT):

                if (member.type == LayoutMember.LayoutType.byte4A or member.type == LayoutMember.LayoutType.byte4B or member.type == LayoutMember.LayoutType.byte4C or member.type == LayoutMember.LayoutType.byte4D or member.type == LayoutMember.LayoutType.byte4E):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.bitangents.append([(br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127, (br.readUByte() - 127) / 127])

                    position += 4

            elif (member.semantic == LayoutMember.LayoutSemantic.VERTEX_COLOR):

                if (member.type == LayoutMember.LayoutType.float4):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.colors.append([br.readFloat(), br.readFloat(), br.readFloat(), br.readFloat()])

                    position += 16

                elif (member.type == LayoutMember.LayoutType.byte4A or member.type == LayoutMember.LayoutType.byte4C):

                    for i in range(vertex_count):
                        br.seek(save_position + layout.size * i + position)
                        self.colors.append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

                    position += 4
