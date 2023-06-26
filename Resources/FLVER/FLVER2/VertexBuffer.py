from ....Utilities import *

from ..Vertices import *

class VertexBuffer:

    def __init__(self) -> None:
        self.layout_index = 0

        self.vertex_size = 0
        self.buffer_index = 0
        self.vertex_count = 0
        self.buffer_offset = 0

    def read(self, br):

        self.buffer_index = br.readInt()
        self.layout_index = br.readInt()
        self.vertex_size = br.readInt()
        self.vertex_count = br.readInt()
        br.readInt()
        br.readInt()
        br.readInt()
        self.buffer_offset = br.readInt()

    def read_vertex_buffers(self, br, layouts, vertex_count, data_offset, header):

        layout = layouts[self.layout_index]

        br.seek(data_offset + self.buffer_offset, 0)
        uv_factor = 1024
        if (header.version >= 0x2000F):
            uv_factor = 2048

        vertices = Vertices()
        vertices.read(br, layout, uv_factor, vertex_count)

        self.vertex_size = -1
        self.buffer_index = -1
        self.vertex_count = -1
        self.buffer_offset = -1

