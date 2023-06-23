from ...Utilities import *

from .Bone import *

class ANI_CLASS:

    def __init__(self) -> None:
        
        self.bones = []
        self.translations = []
        self.rotations = []
        self.max_frame_count = 0

    def read(self, br):

        header = br.readUInt()
        br.readUInt()
        self.max_frame_count = br.readUInt()
        bones_data_offset = br.readUInt()
        bone_count = br.readUInt()
        translations_data_offset = br.readUInt()
        rotations_data_offset = br.readUInt()
        translation_count = br.readUInt()
        rotation_count = br.readUInt()

        br.seek(bones_data_offset)
        for i in range(bone_count):
            br.seek(bones_data_offset + 244 * i)
            bone = Bone()
            bone.read(br)
            self.bones.append(bone)

        br.seek(translations_data_offset)
        for i in range(translation_count):
            self.translations.append(Vector((br.readFloat(), br.readFloat(), br.readFloat())))

        br.seek(rotations_data_offset)
        for i in range(rotation_count):
            self.rotations.append(Euler((br.readShort() / 1000, br.readShort() / 1000, br.readShort() / 1000), "XYZ"))

