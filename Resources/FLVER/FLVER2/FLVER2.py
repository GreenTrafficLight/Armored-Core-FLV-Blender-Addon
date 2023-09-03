from ....Utilities import *

from .Material import *

from ..Bone import *
from ..Dummy import *

class FLVER2:

    def __init__(self, header) -> None:
        self.header = header
        self.dummies = []
        self.materials = []
        self.bones = []
        self.meshes = []

    def read(self, br):

        for i in range(self.header.dummy_count):
            dummy = Dummy()
            dummy.read(br, self.version)
            self.dummies.append(dummy)

        GX_list_indices = {}
        GX_lists = [] 
        for i in range(self.header.material_count):
            material = Material()
            material.read(br, self, self.header, GX_lists, GX_list_indices)
            self.materials.append(material)

        for i in range(self.header.bone_count):
            bone = Bone()
            bone.read(br, self.header.unicode)
            self.bones.append(bone)

