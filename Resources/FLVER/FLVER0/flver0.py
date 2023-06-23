from ....Utilities import *

from .Material import *
from .Mesh import *
from .Texture import *
from .VertexBuffer import *

from ..Bone import *
from ..Dummy import *

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
        self.bounding_box_min = (br.readFloat(), br.readFloat(), br.readFloat())
        self.bounding_box_max = (br.readFloat(), br.readFloat(), br.readFloat())
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
            dummy = Dummy()
            dummy.read(br, self.version)
            self.dummies.append(dummy)

        print(br.tell())

        for i in range(material_count):
            material = Material()
            material.read(br, self)
            self.materials.append(material)

        print(br.tell())

        for i in range(bone_count):
            bone = Bone()
            bone.read(br, False)
            self.bones.append(bone)

        print(br.tell())

        for i in range(mesh_count):
            mesh = Mesh()
            mesh.read(br, self, data_offset)
            self.meshes.append(mesh)


