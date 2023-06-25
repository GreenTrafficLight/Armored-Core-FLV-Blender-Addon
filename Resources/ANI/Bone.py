from ...Utilities import *

class Bone:

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
            print(self.name)
            if self.name == "LTF7":
                print("test")
            br.seek(keyframe_data_offset)
            keyframe = Bone.KEYFRAME()
            keyframe.read(br)
            self.keyframe_data = keyframe
            print("\n")

    def compute_world_transform(self):

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
            br.seek(keyframes_information_offset)
            for i in range(keyframe_information_count):
                keyframe_information = Bone.KEYFRAME.INFORMATION()
                keyframe_information.time = br.readShort()
                print(version)
                if version == 1:
                    keyframe_information.translation_index = br.readUByte()
                    br.readUByte() 
                    br.readUByte() 
                    
                    keyframe_information.rotation_index = br.readUByte()
                    br.readUByte()
                    br.readUByte()
                elif version == 2:
                    keyframe_information.translation_index = br.readShort()
                    br.readShort()
                    br.readShort() 
                
                    keyframe_information.rotation_index = br.readShort()
                    br.readShort()
                    br.readShort()
                    br.readShort()
                elif version == 4:
                    keyframe_information.rotation_index = br.readShort()
                    br.readShort()
                    br.readShort() 
                else:
                    print("Unknown version")
                
                self.keyframe_informations.append(keyframe_information)

        class INFORMATION:

            def __init__(self) -> None:
                self.time = 0
                self.translation_index = -1
                self.rotation_index = -1
