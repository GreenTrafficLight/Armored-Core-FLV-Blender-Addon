from ..LayoutMember import *

class BufferLayout :

    def __init__(self) -> None:

        self.size = 0
        self.members = []

    def read(self, br):
        
        member_count = br.readInt()
        br.readUInt()
        br.readUInt()
        member_offset = br.readUInt()

        save_position = br.tell()
        br.seek(member_offset, 0)

        struct_offset = 0
        capacity = member_count
        for i in range(member_count):

            member = LayoutMember()
            member.read(br, struct_offset)
            struct_offset += member.get_size()
            self.members.append(member)

        br.seek(save_position, 0)

