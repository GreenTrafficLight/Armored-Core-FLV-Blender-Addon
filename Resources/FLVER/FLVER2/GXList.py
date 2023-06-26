class GXList :

    def __init__(self) -> None:
        self.items = []
        self.terminator_ID = 2147483647
        self.terminator_length = 0

    def read(self, br, header):
        if header.version < 0x20010:
            self.items.append(GXItem().read(br, header))
        else:
            id = 0
            while id != 2147483647 and id != -1:
                id = br.readUInt()
                self.items(GXItem().read(br, header))
            self.terminator_ID = br.readInt()
            br.readInt()
            self.terminator_length = br.readInt() - 0xC

class GXItem :

    def __init__(self) -> None:
        self.ID = 0
        self.unk_04 = 100
        self.data = []

    def read(self, br, header):
        if header.version < 0x20010:
            self.ID = br.readInt()
        else:
            self.ID = br.readBytes(4)
        self.unk_04 = br.readInt()
        length = br.readInt()
        data = br.readBytes(length - 0xC)


