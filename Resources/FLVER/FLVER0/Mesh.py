from ....Utilities import *

from ..Vertices import *

from .VertexBuffer import *

class Mesh:

    def __init__(self) -> None:
        self.dynamic = 0
        self.material_index = 0
        self.unk02 = False
        self.unk03 = 0
        self.default_bone_index = 0
        self.bone_indices = []
        self.unk46 = 0
        self.vertex_indices = []
        self.vertices = []
        self.layout_index = []

    def read(self, br, flv, data_offset):

        self.dynamic = br.readByte()
        self.material_index = br.readByte()
        self.unk02 = br.readByte() == 1
        self.unk03 = br.readByte()

        vertex_index_count = br.readUInt()
        vertex_count = br.readUInt()
        self.default_bone_index = br.readUShort()
        for i in range(28):
            self.bone_indices.append(br.readUShort())
        self.unk46 = br.readUShort()
        br.readUInt() # Vertex indices length
        vertex_indices_offset = br.readUInt()
        buffer_data_length = br.readUInt()
        buffer_data_offset = br.readUInt()
        vertex_buffers_offset1 = br.readUInt() 
        vertex_buffers_offset2 = br.readUInt()
        br.readUInt()

        save_position_vertex_indices_offset = br.tell()

        br.seek(data_offset + vertex_indices_offset)

        if flv.vertex_index_size == 16:

            for i in range(vertex_index_count):
                self.vertex_indices.append(br.readUShort())

        elif flv.vertex_index_size == 32:

            for i in range(vertex_index_count):
                self.vertex_indices.append(br.readUInt()) 

        br.seek(save_position_vertex_indices_offset)

        if (vertex_buffers_offset1 == 0):
            buffer = VertexBuffer()
            buffer.buffer_length = buffer_data_length
            buffer.buffer_offset = buffer_data_offset
            buffer.layout_index = 0
        else:
            save_position_vertex_buffers_offset1 = br.tell()

            br.seek(vertex_buffers_offset1)
            vertex_buffers1 = VertexBuffer().read_vertex_buffers(br)

            buffer = vertex_buffers1[0]

            br.seek(save_position_vertex_buffers_offset1)

        if vertex_buffers_offset2 != 0:
            save_position_vertex_buffers_offset2 = br.tell()

            br.seek(vertex_buffers_offset2)
            vertex_buffers2 = VertexBuffer().read_vertex_buffers(br)

            br.seek(save_position_vertex_buffers_offset2)

        save_position_buffer_offset = br.tell()

        br.seek(data_offset + buffer.buffer_offset)
        self.layout_index = buffer.layout_index
        layout = flv.materials[self.material_index].layouts[self.layout_index]

        uv_factor = 2048
        
        self.vertices = Vertices()
        self.vertices.read(br, layout, uv_factor, vertex_count)

        br.seek(save_position_buffer_offset)