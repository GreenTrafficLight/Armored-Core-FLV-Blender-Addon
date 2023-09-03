from ....Utilities import *

from .Material import *
from .Mesh import *
from .Texture import *
from .VertexBuffer import *

from ..Bone import *
from ..Dummy import *

class FLVER0_CLASS:

    def __init__(self, header) -> None:
        self.header = header
        self.dummies = []
        self.materials = []
        self.bones = []
        self.meshes = []

    def read(self, br):

        for i in range(self.header.dummy_count):
            dummy = Dummy()
            dummy.read(br, self.header.version)
            self.dummies.append(dummy)

        print(br.tell())

        for i in range(self.header.material_count):
            material = Material()
            material.read(br, self)
            self.materials.append(material)

        print(br.tell())

        for i in range(self.header.bone_count):
            bone = Bone()
            bone.read(br, False)
            self.bones.append(bone)

        print(br.tell())

        for i in range(self.header.mesh_count):
            mesh = Mesh()
            mesh.read(br, self.header, self)
            self.meshes.append(mesh)


