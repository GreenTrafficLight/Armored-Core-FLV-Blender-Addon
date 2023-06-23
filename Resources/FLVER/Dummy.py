from ...Utilities import *

class Dummy:

    def __init__(self) -> None:
        self.Position = None
        self.Forward = None
        self.Upward = None
        self.Reference_ID = 0
        self.Parent_bone_index = -1
        self.Attach_bone_index = -1
        self.Color = None
        self.Flag1 = False
        self.Use_upward_vector = False
        self.Unk30 = 0
        self.Unk34 = 0

    def read(self, br, version):

        self.Position = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
        if version == 0x20010:
            self.Color = (br.readByte(), br.readByte(), br.readByte(), br.readByte())
        else:
            self.Color = (br.readByte(), br.readByte(), br.readByte(), br.readByte())
        self.Forward = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
        self.Reference_ID = br.readShort()
        self.Parent_bone_index = br.readShort()
        self.Upward = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
        self.Attach_bone_index = br.readShort()
        self.Flag1 = br.readByte()
        self.Use_upward_vector = br.readByte() == 1
        self.Unk30 = br.readInt()
        self.Unk34 = br.readInt()
        br.readInt()
        br.readInt()
    