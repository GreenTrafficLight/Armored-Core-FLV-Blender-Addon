from ....Utilities import *

class Material:

    def __init__(self) -> None:
        
        self.name = ""
        self.MTD = ""
        self.flags = 0
        self.textures = []
        self.GX_index = -1
        self.unk_18 = 0
        self.texture_index = 0
        self.texture_count = 0

    def read(self, br, header, GX_lists, GX_list_indices):

        name_offset = br.readInt()
        mtd_offset = br.readInt()
        textures_count = br.readInt()
        texture_index = br.readInt()
        flags = br.readInt()
        GX_offset = br.readInt()
        unk_18 = br.readInt()
        br.readInt()

        save_position = br.tell()

        br.seek(name_offset)
        self.name = br.readString()
        br.seek(mtd_offset)
        self.mtd = br.readString()

        br.seek(save_position, 0)

        if GX_offset == 0:
            GX_index = -1
        else:

            save_position = br.tell()
            br.seek(GX_offset, 0)
            GX_list_indices[GX_offset] = len(GX_lists)
            #GX_lists.append()
            br.seek(save_position, 0)