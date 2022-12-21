from abc import ABC, abstractmethod
from enum import Enum

class MSB1 :

    def __init__(self) -> None:
        pass

    def read(self, br):

        models = MSB1.MODEL_PARAM()

    class PARAM(ABC):

        def __init__(self) -> None:
            pass

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

            br.seek(next_param_offset)

        @abstractmethod
        def read_entry(self):
            pass

    class ENTRY(ABC):

        def __init__(self) -> None:
            self.name = ""

    class MODEL_TYPE(Enum):

        map_piece = 0
        object = 1
        enemy = 2
        player = 4
        collision = 5
        navmesh = 6

    class MODEL_PARAM(PARAM):

        def __init__(self) -> None:
            super().__init__()
            self.map_pieces = []
            self.objects = []
            self.enemies = []
            self.players = []

        def read(self, br):
            br.seek(4, 1)
            Type = MSB1.MODEL_TYPE(br.readInt())
            if Type == MSB1.MODEL_TYPE.map_piece:
                self.map_pieces.append(MSB1.MODEL().read(br))

        def read_entry(self):
            pass

    class MODEL(ENTRY):
        
        def __init__(self) -> None:
            super().__init__()
            self.Name = ""
            self.Sib_path = ""
            self.instance_count = 0

        def read(self, br):
            start = br.tell()
            name_offset = br.readInt()
            type = br.readInt()
            br.readInt()
            sib_offset = br.readInt()
            self.instance_count = br.readInt()
            br.readInt()
            br.readInt()
            br.readInt()

            br.seek(start + name_offset)
            self.Name = br.readString()

            br.seek(start + sib_offset)
            self.Sib_path = br.readString()