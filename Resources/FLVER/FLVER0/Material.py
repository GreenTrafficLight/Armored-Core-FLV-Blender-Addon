from ....Utilities import *

from .BufferLayout import *
from .Texture import *

class Material:

    def __init__(self) -> None:
        
        self.name = ""
        self.mtd = ""
        self.textures = []
        self.layouts = []

    def read(self, br, flv):

        little_endian_layout = False

        name_offset = br.readInt()
        mtd_offset = br.readInt()
        textures_offset = br.readInt()
        layouts_offset = br.readInt()
        br.readInt()
        layout_header_offset = br.readInt() # to fix with little endian

        """
        if layout_header_offset < 0:
            little_endian_layout = True
            br.endian = "<"
            br.seek(-4, 1)
            layout_header_offset = br.readInt()
            br.endian = ">"
        """

        br.readInt()
        br.readInt()

        save_position = br.tell()

        save_position_textures_offset = br.tell()

        br.seek(name_offset)
        self.name = br.readString()
        br.seek(mtd_offset)
        self.mtd = br.readString()

        br.seek(textures_offset)
        texture_count = br.readByte()
        br.readByte()
        br.readByte()
        br.readByte()
        br.readInt()
        br.readInt()
        br.readInt()

        for i in range(texture_count):
            texture = Texture()
            texture.read(br, flv)
            self.textures.append(texture)
            

        br.seek(save_position_textures_offset)

        if layout_header_offset != 0:

            #if little_endian_layout == True:
                #br.endian = "<"
            
            save_position_layout_header_offset = br.tell()
            
            br.seek(layout_header_offset)
            layout_count = br.readInt()
            br.readInt()
            br.readInt()
            br.readInt()
            for i in range(layout_count):
                
                layout_offset = br.readInt()
                
                save_position_layout_offset = br.tell()

                #if little_endian_layout == True:
                    #br.endian = ">"
                
                br.seek(layouts_offset)
                layout = BufferLayout()
                layout.read(br)
                self.layouts.append(layout)

                #if little_endian_layout == True:
                    #br.endian = "<"
                
                br.seek(save_position_layout_offset)
            
            #if little_endian_layout == True:
                #br.endian = ">"

            br.seek(save_position_layout_header_offset)

        br.seek(save_position)
