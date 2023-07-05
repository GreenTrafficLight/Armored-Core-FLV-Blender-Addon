from abc import ABC, abstractmethod
from enum import Enum

import math

from mathutils import *

class MSB1 :

    def __init__(self) -> None:
        self.models = None
        self.parts = None

    def read(self, br):

        self.models = MSB1.MODEL_PARAM()
        self.models.read(br)
        events = MSB1.EVENT_PARAM()
        events.read(br)
        regions = MSB1.POINT_PARAM()
        regions.read(br)
        routes = MSB1.ROUTE_PARAM()
        routes.read(br)
        layers = MSB1.LAYER_PARAM()
        layers.read(br)
        self.parts = MSB1.PART_PRAM()
        self.parts.read(br)

    class PARAM(ABC):

        def __init__(self) -> None:
            self._name = ""

        @property
        def Name(self):
            return self._name

        @Name.setter
        def Name(self, value):
            self._name = value

        def read(self, br):

            br.readInt()
            name_offset = br.readInt()
            offset_count = br.readInt()
            entry_offsets = []
            for i in range(offset_count - 1):
                entry_offsets.append(br.readInt())
            next_param_offset = br.readInt()

            entries = []
            for offset in entry_offsets:
                br.seek(offset)
                entry = self.read_entry(br)
                entries.append(entry)

            br.seek(next_param_offset)

        @abstractmethod
        def read_entry(self, br):
            pass

    class ENTRY(ABC):

        def __init__(self) -> None:
            self._name = ""

        @property
        def Name(self):
            return self._name

        @Name.setter
        def Name(self, value):
            self._name = value

    class MODEL_TYPE(Enum):

        Map_Piece = 0
        Object = 1
        Enemy = 2
        Player = 4
        Collision = 5
        Navmesh = 6

    class MODEL_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            self.map_pieces = []
            self.objects = []
            self.enemies = []
            self.players = []
            self.collisions = []
            self.navmeshes = []

        def read_entry(self, br):
            save_position = br.tell()
            br.seek(4, 1)
            model_type = MSB1.MODEL_TYPE(br.readInt())
            br.seek(save_position)
            if model_type == MSB1.MODEL_TYPE.Map_Piece:
                map_piece = MSB1.MODEL()
                map_piece.read(br)
                self.map_pieces.append(map_piece)
            
            elif model_type == MSB1.MODEL_TYPE.Object:
                object = MSB1.MODEL()
                object.read(br)    
                self.objects.append(object)
            
            elif model_type == MSB1.MODEL_TYPE.Enemy:
                enemy = MSB1.MODEL()
                enemy.read(br)                  
                self.enemies.append(enemy)
            
            elif model_type == MSB1.MODEL_TYPE.Player:
                player = MSB1.MODEL()
                player.read(br)                       
                self.players.append(player)
            
            elif model_type == MSB1.MODEL_TYPE.Collision:
                collision = MSB1.MODEL()
                collision.read(br)             
                self.collisions.append(collision)   
            
            elif model_type == MSB1.MODEL_TYPE.Navmesh:
                navmesh = MSB1.MODEL()
                navmesh.read(br)      
                self.navmeshes.append(navmesh)

    class MODEL(ENTRY, ABC):
        
        def __init__(self) -> None:
            super().__init__()
            self._type = None
            self._name = ""
            self._sib_path = ""
            self._instance_count = 0

        @property
        def Type(self):
            return self._type

        @Type.setter
        def Type(self, value):
            self._type = value

        @property
        def Sib_Path(self):
            return self._sib_path

        @Sib_Path.setter
        def Sib_Path(self, value):
            self._sib_path = value

        @property
        def Instance_Count(self):
            return self._instance_count

        @Instance_Count.setter
        def Instance_Count(self, value):
            self._instance_count = value

        def read(self, br):
            start = br.tell()
            name_offset = br.readInt()
            self.Type = br.readInt()
            br.readInt()
            sib_offset = br.readInt()
            self.Instance_Count = br.readInt()
            br.readInt()
            br.readInt()
            br.readInt()

            br.seek(start + name_offset)
            self.Name = br.readString()

            br.seek(start + sib_offset)
            self.Sib_Path = br.readString()

    class EVENT_TYPE(Enum):

        Light = 0
        Sound = 1
        SFX = 2
        Wind = 3
        Treasure = 4
        Generator = 5
        Message = 6
        ObjAct = 7
        SpawnPoint = 8
        MapOffset = 9
        Navmesh = 10
        Environment = 11
        PseudoMultiplayer = 12

    class EVENT_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            pass

        def read_entry(self, br):
            save_position = br.tell()
            br.seek(8, 1)
            event_type = MSB1.EVENT_TYPE(br.readInt())
            br.seek(save_position)

    class POINT_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            pass

        def read_entry(self, br):
            pass

    class ROUTE_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            pass

        def read_entry(self, br):
            pass

    class LAYER_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            pass

        def read_entry(self, br):
            pass

    class PART_TYPE(Enum):

        Map_Piece = 0
        Object = 1
        Enemy = 2
        Player = 4
        Collision = 5
        Navmesh = 8
        Dummy_Object = 9
        Dummy_Enemy = 10
        Connect_Collision = 11

    class PART_PRAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            self.map_pieces = []
            self.objects = []
            self.enemies = []
            self.players = []
            self.collisions = []
            self.navmeshes = []
            self.dummy_objects = []
            self.dummy_enemies = []
            self.connect_collisions = []

        def read_entry(self, br):
            save_position = br.tell()
            br.seek(4, 1)
            model_type = MSB1.PART_TYPE(br.readInt())
            br.seek(save_position)
            if model_type == MSB1.PART_TYPE.Map_Piece:
                map_piece = MSB1.PART()
                map_piece.read(br)
                self.map_pieces.append(map_piece)
            
            elif model_type == MSB1.PART_TYPE.Object:
                object = MSB1.PART()
                object.read(br)    
                self.objects.append(object)
            
            elif model_type == MSB1.PART_TYPE.Enemy:
                enemy = MSB1.PART()
                enemy.read(br)                  
                self.enemies.append(enemy)
            
            elif model_type == MSB1.PART_TYPE.Player:
                player = MSB1.PART()
                player.read(br)                       
                self.players.append(player)
            
            elif model_type == MSB1.PART_TYPE.Collision:
                collision = MSB1.PART()
                collision.read(br)             
                self.collisions.append(collision)   
            
            elif model_type == MSB1.PART_TYPE.Navmesh:
                navmesh = MSB1.PART()
                navmesh.read(br)      
                self.navmeshes.append(navmesh)

            elif model_type == MSB1.PART_TYPE.Dummy_Object:
                dummy_object = MSB1.PART()
                dummy_object.read(br)      
                self.dummy_objects.append(dummy_object)

    class PART(ENTRY, ABC):

        def __init__(self) -> None:
            super().__init__()
            self._type = None
            self._model_name = ""
            self._model_index = 0
            self._sib_path = ""
            self._position = None
            self._rotation = None
            self._scale = None
            self._draw_groups = []
            self._disp_groups = []
            self._entity_ID = 0
            self._light_ID = 0
            self._fog_ID = 0
            self._scatter_ID = 0
            self._lens_flare_ID = 0
            self._shadow_ID = 0
            self._dof_ID = 0
            self._tone_map_ID = 0
            self._tone_correct_ID = 0
            self._lantern_ID = 0
            self._lod_param_ID = 0
            self._is_shadow_src = 0
            self._is_shadow_dest = 0
            self._is_shadow_only = 0
            self._draw_by_reflect_cam = 0
            self._draw_only_reflect_cam = 0
            self._use_depth_bias_float = 0
            self._disable_point_light_effet = 0

        @property
        def Type(self):
            return self._type

        @property
        def Model_Name(self):
            return self._model_name

        @property
        def Model_Index(self):
            return self._model_index

        @Model_Index.setter
        def Model_Index(self, value):
            self._model_index = value

        @property
        def Sib_Path(self):
            return self._sib_path

        @Sib_Path.setter
        def Sib_Path(self, value):
            self._sib_path = value

        @property
        def Position(self):
            return self._position 

        @Position.setter
        def Position(self, value):
            self._position = value

        @property
        def Rotation(self):
            return self._rotation

        @Rotation.setter
        def Rotation(self, value):
            self._rotation = value

        @property
        def Scale(self):
            return self._scale

        @Scale.setter
        def Scale(self, value):
            self._scale = value

        @property
        def Draw_Groups(self):
            return self._draw_groups

        @Draw_Groups.setter
        def Draw_Groups(self, value):
            self._draw_groups = value      

        @property
        def Disp_Groups(self):
            return self._disp_groups

        @Disp_Groups.setter
        def Disp_Groups(self, value):
            self._disp_groups = value

        @property
        def Entity_ID(self):
            return self._entity_ID

        @property
        def Light_ID(self):
            return self._light_ID

        @property
        def Fog_ID(self):
            return self._fog_ID

        @property
        def Scatter_ID(self):
            return self._scatter_ID

        @property
        def Lens_Flare_ID (self):
            return self._lens_flare_ID

        @property
        def ShadowID(self):
            return self._shadow_ID

        @property
        def Dof_ID(self):
            return self._dof_ID

        @property
        def Tone_Map_ID(self):
            return self._tone_map_ID   

        @property
        def Tone_Correct_ID(self):
            return self._tone_correct_ID   

        @property
        def LanternID(self):
            return self._lantern_ID 
        
        @property
        def LodParamID(self):
            return self._lod_param_ID

        @property
        def Is_Shadow_Src(self):
            return self._is_shadow_src

        @property
        def Is_Shadow_Dest(self):
            return self._is_shadow_dest

        @property
        def Is_Shadow_Only(self):
            return self._is_shadow_only

        @property
        def Draw_By_Reflect_Cam(self):
            return self._draw_by_reflect_cam

        @property
        def Draw_Only_Reflect_Cam(self):
            return self._draw_only_reflect_cam

        @property
        def Use_Depth_Bias_Float(self):
            return self._use_depth_bias_float

        @property
        def Disable_Point_Light_Effect(self):
            return self._disable_point_light_effet

        def read(self, br):
            start = br.tell()
            name_offset = br.readInt()
            self._type = br.readUInt()
            br.readInt()
            self.Model_Index = br.readInt()
            sib_offset = br.readInt()
            self.Position = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.Rotation = Euler((math.radians(br.readFloat()), math.radians(br.readFloat()), math.radians(br.readFloat())), "XYZ")
            self.Scale = Vector((br.readFloat(), br.readFloat(), br.readFloat()))
            self.Draw_Groups = [br.readInt(), br.readInt(), br.readInt(), br.readInt()]
            self.Disp_Groups = [br.readInt(), br.readInt(), br.readInt(), br.readInt()]
            entity_data_offset = br.readInt()
            type_data_offset = br.readInt()

            br.seek(start + name_offset)
            self.Name = br.readString()

            br.seek(start + sib_offset)
            self.Sib_Path = br.readString()

            br.seek(start + entity_data_offset)

            br.seek(start + type_data_offset)

                
