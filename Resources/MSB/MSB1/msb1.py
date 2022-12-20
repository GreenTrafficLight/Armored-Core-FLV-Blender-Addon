from abc import ABC, abstractmethod

class MSB1 :

    def __init__(self) -> None:
        pass

    def read(self, br):

        pass

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

    class MODEL_PARAM(PARAM):

        