from ....Utilities import *

from ..Vertices import *

from .VertexBuffer import *

class Mesh:

    def __init__(self) -> None:
        self.dynamic = 0
        self.material_index = 0
        self.default_bone_index = -1
        self.bone_indices = []
        self.face_sets = 0
        self.vertex_buffers = []
        self.vertices = []
        self.bounding_box = []
        self.face_set_indices = []
        self.vertex_buffer_indices = []

    def read(self, br, header):

        self.dynamic = br.readByte()
        br.readByte()
        br.readByte()
        br.readByte()

        self.material_index = br.readInt()
        br.readInt()
        br.readInt()
        self.default_bone_index = br.readInt()
        bone_count = br.readInt()
        bounding_box_offset = br.readInt()
        bone_offset = br.readInt()
        face_set_count = br.readInt()
        face_set_offset = br.readInt()
        vertex_buffer_count = br.readInt()
        vertex_buffer_offset = br.readInt()

        if (bounding_box_offset != 0):

            save_position = br.tell()
            br.seek(bounding_box_offset, 0)

            br.seek(save_position, 0)

        br.seek(bone_offset, 0)
        for i in range(bone_count):
            self.bone_indices.append(br.readInt())

        br.seek(face_set_offset, 0)
        for i in range(face_set_count):
            self.face_set_indices.append(br.readInt())

        br.seek(vertex_buffer_offset, 0)
        for i in range(vertex_buffer_count):
            self.vertex_buffer_indices.append(br.readInt())