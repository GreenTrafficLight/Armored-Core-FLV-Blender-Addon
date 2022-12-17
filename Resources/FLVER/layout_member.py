from enum import Enum

class LAYOUT_MEMBER :

    def __init__(self) -> None:
        
        self.unk00 = 0
        self.type = None
        self.semantic = None
        self.index = 0

        class LAYOUT_TYPE(Enum):

            float2 = 0x1
            float3 = 0x2
            float4 = 0x3
            byte4A = 0x10
            byte4B = 0x11
            short2_to_float2 = 0x12
            byte4C = 0x13
            uv = 0x15
            uv_pair = 0x16
            short_bone_indices = 0x18
            short4_to_float4A = 0x1A
            short4_to_float4B = 0x2E
            byte4E = 0x2F
            edge_compressed = 0xF0

        class LAYOUT_SEMANTIC(Enum):

            position = 0
            bone_weights = 1
            bone_indices = 2
            normal = 3
            uv = 5
            tangent = 6
            bitangent = 7
            vertex_color = 10