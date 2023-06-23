from ....Utilities import *

class VertexBuffer:

    def __init__(self) -> None:
        self.layout_index = 0
        self.buffer_length = 0
        self.buffer_offset = 0

    def read(self, br):

        self.layout_index = br.readInt()
        self.buffer_length = br.readInt()
        self.buffer_offset = br.readInt()
        br.readInt()

    def read_vertex_buffers(self, br):

        buffer_count = br.readInt()
        buffers_offset = br.readInt()
        br.readInt()
        br.readInt()

        buffers = []
        br.seek(buffers_offset)
        for i in range(buffer_count):
            buffer = VertexBuffer()
            buffer.read(br)
            buffers.append(buffer)

        return buffers
