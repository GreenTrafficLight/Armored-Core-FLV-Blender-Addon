from ....Utilities import *

class Texture:

    def __init__(self) -> None:
        
        self.type = ""
        self.path = ""

    def read(self, br, flv):

        path_offset = br.readUInt()
        type_offset = br.readUInt()
        br.readUInt()
        br.readUInt()

        save_position = br.tell()

        br.seek(path_offset)
        self.path = br.readString()
        if type_offset > 0:
            br.seek(type_offset)
            self.type = br.readString()

        br.seek(save_position)

