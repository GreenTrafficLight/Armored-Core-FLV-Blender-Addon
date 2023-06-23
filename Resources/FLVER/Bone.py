from ...Utilities import *

class Bone:
    
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

        self.translation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
        name_offset = br.readInt()
        self.rotation = Euler((br.readFloat(), br.readFloat(), br.readFloat()), "XYZ")
        self.parent_index = br.readShort()
        self.child_index = br.readShort()
        self.scale = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
        self.next_sibling_index = br.readShort()
        self.previous_sibling_index = br.readShort()
        self.bouding_box_min = (br.readFloat(), br.readFloat(), br.readFloat())
        self.unk_3C = br.readInt()
        self.bouding_box_max = (br.readFloat(), br.readFloat(), br.readFloat())
        br.seek(0x34, 1)
        save_position = br.tell()
        br.seek(name_offset)
        self.name = br.readString()
        br.seek(save_position)

    def compute_world_transform(self):

        return Matrix.Translation(self.translation) @ self.rotation.to_matrix().to_4x4() @ Matrix.Scale(1, 4, self.scale)
