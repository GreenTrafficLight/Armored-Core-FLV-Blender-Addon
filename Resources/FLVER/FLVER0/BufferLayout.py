from ..LayoutMember import *

class BufferLayout :

    def __init__(self) -> None:

        self.size = 0
        self.members = []

    def read(self, br):
        
        member_count = br.readUShort()
        struct_size =  br.readUShort()
        br.readUInt()
        br.readUInt()
        br.readUInt()

        struct_offset = 0
        capacity = member_count
        for i in range(member_count):

            member = LayoutMember()
            member.read(br, struct_offset)
            self.size += member.get_size()
            self.members.append(member)

