from ...Utilities import *

class ANI_CLASS:

    def __init__(self) -> None:
        
        self.bones = []
        self.translations = []
        self.rotations = []

    def read(self, br):

        header = br.readUInt()
        br.readUInt()
        max_frame_count = br.readUInt()
        bones_data_offset = br.readUInt()
        bone_count = br.readUInt()
        translations_data_offset = br.readUInt()
        rotations_data_offset = br.readUInt()
        translation_count = br.readUInt()
        rotation_count = br.readUInt()

        br.seek(bones_data_offset)
        for i in range(bone_count):
            br.seek(bones_data_offset + 244 * i)
            bone = ANI_CLASS.BONE()
            bone.read(br)
            self.bones.append(bone)

        br.seek(translations_data_offset)
        for i in range(translation_count):
            self.translations.append(Vector((br.readFloat(), br.readFloat(), br.readFloat())))

        br.seek(rotations_data_offset)
        for i in range(rotation_count):
            self.rotations.append(Euler((br.readFloat(), br.readFloat(), br.readFloat()), "XYZ"))

    class BONE:

        def __init__(self) -> None:
            self.name = ""
            self.parent_index = 0
            self.child_index = 0
            self.next_sibling_index = 0
            self.previous_sibling_index = 0
            self.keyframe_data = None

        def read(self, br):
            name_offset = br.readUInt()
            save_position = br.tell()
            br.seek(name_offset)
            self.name = br.readString()
            br.seek(save_position)
            br.readUInt()
            br.readShort()
            br.readShort()
            self.parent_index = br.readShort()
            self.child_index = br.readShort()
            self.next_sibling_index = br.readShort()
            self.previous_sibling_index = br.readShort()
            self.translation = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.rotation = Euler((br.readFloat(), br.readFloat(), br.readFloat()), "XYZ")
            self.scale = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            print(br.tell())
            keyframe_data_offset = br.readUInt()
            if keyframe_data_offset != 0:
                br.seek(keyframe_data_offset)
                keyframe = ANI_CLASS.BONE.KEYFRAME()
                keyframe.read(br)
                self.keyframe_data = keyframe
    
        def computeWorldTransform(self):

            return Matrix.Translation(self.translation) @ self.rotation.to_matrix().to_4x4() @ Matrix.Scale(1, 4, self.scale)

        class KEYFRAME:
            
            def __init__(self) -> None:
                
                self.keyframe_informations = []

                self.bounding_box_min = None
                self.bounding_box_max = None

            def read(self, br):
                keyframes_information_offset = br.readUInt()
                keyframe_information_count = br.readUInt()
                version = br.readUInt()
                self.bounding_box_min = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
                self.bounding_box_max = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
                for i in range(keyframe_information_count):
                    keyframe_information = ANI_CLASS.BONE.KEYFRAME.INFORMATION()
                    if version == 1:
                        br.readUShort()
                        br.readUShort()
                        br.readUShort()
                        br.readUShort()
                    elif version == 2:
                        keyframe_information.time_translation = br.readUShort()
                        keyframe_information.translation_index = br.readUShort()
                        keyframe_information.time_rotation = br.readUShort()
                        keyframe_information.rotation_index = br.readUShort()
                        br.seek(8, 1)
                    elif version == 4:
                        keyframe_information.time_translation = br.readUShort()
                        keyframe_information.translation_index = br.readUShort()
                        keyframe_information.time_rotation = br.readUShort()
                        keyframe_information.rotation_index = br.readUShort()
                    else:
                        print("Unknown version")

                    self.keyframe_informations.append(keyframe_information)

            class INFORMATION:

                def __init__(self) -> None:
                    self.time_translation = 0
                    self.translation_index = 0
                    self.time_rotation= 0
                    self.rotation_index = 0

