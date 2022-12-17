from enum import Enum

from ...Utilities import *

class FLVER:

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
            self.name = br.readString()


    class LAYOUT_MEMBER :

        def __init__(self) -> None:
            
            self.unk00 = 0
            self.type = None
            self.semantic = None
            self.index = 0

        def read(self, br, struct_offset):

            self.unk00 = br.readInt()
            br.readInt()
            self.type = FLVER.LAYOUT_MEMBER.TYPE.br.readInt()
            self.semantic = FLVER.LAYOUT_MEMBER.SEMANTIC.br.readInt()
            self.index = br.readInt()

        class TYPE(Enum):

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

        class SEMANTIC(Enum):

            position = 0
            bone_weights = 1
            bone_indices = 2
            normal = 3
            uv = 5
            tangent = 6
            bitangent = 7
            vertex_color = 10