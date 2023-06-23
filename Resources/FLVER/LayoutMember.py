from enum import Enum

from ...Utilities import *

class LayoutMember :

    def __init__(self) -> None:
        
        self.unk00 = 0
        self.type = None
        self.semantic = None
        self.index = 0

    def read(self, br, struct_offset):

        self.unk00 = br.readInt()
        br.readInt()
        self.type = LayoutMember.LayoutType(br.readUInt())
        self.semantic = LayoutMember.LayoutSemantic(br.readUInt())
        self.index = br.readInt()

    def get_size(self):

        if (self.type == LayoutMember.LayoutType.byte4A or self.type == LayoutMember.LayoutType.byte4B or self.type == LayoutMember.LayoutType.byte4C or self.type == LayoutMember.LayoutType.byte4D or self.type == LayoutMember.LayoutType.byte4E):
            return 4
        elif (self.type == LayoutMember.LayoutType.short2_to_float2):
            return 4
        elif (self.type == LayoutMember.LayoutType.uv):
            return 4
        elif (self.type == LayoutMember.LayoutType.uv_pair):
            return 8
        elif (self.type == LayoutMember.LayoutType.short_bone_indices):
            return 8
        elif (self.type == LayoutMember.LayoutType.short4_to_float4A or self.type == LayoutMember.LayoutType.short4_to_float4B):
            return 8
        elif (self.type == LayoutMember.LayoutType.float2):
            return 8
        elif (self.type == LayoutMember.LayoutType.float3):
            return 12
        elif (self.type == LayoutMember.LayoutType.float4):
            return 16

    class LayoutType(Enum):

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

    class LayoutSemantic(Enum):

        POSITION = 0
        BONE_WEIGHTS = 1
        BONE_INDICES = 2
        NORMAL = 3
        UV = 5
        TANGENT = 6
        BITANGENT = 7
        VERTEX_COLOR = 10
