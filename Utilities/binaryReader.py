import struct
import numpy as np

class BinaryReader:

    def __init__(self, data, endian="<"):
        self.data = data
        self.endian = endian
        
        self.seek(0)

    def seek(self, offset, option=0):
        if option == 1:
            self.data.seek(offset, 1)
        elif option == 2:
            self.data.seek(offset, 2)
        else:
            self.data.seek(offset, 0)

    def tell(self):
        return self.data.tell()

    def read(self, size):
        return self.data.read(size)

    def readChar(self):
        return struct.unpack(self.endian + "c", self.read(1))[0]

    def readByte(self):
        return struct.unpack(self.endian + "b", self.read(1))[0]

    def readUByte(self):
        return struct.unpack(self.endian + "B", self.read(1))[0]

    def readShort(self):
        return struct.unpack(self.endian + "h", self.read(2))[0]

    def readUShort(self):
        return struct.unpack(self.endian + "H", self.read(2))[0]

    def readInt(self):
        return struct.unpack(self.endian + "i", self.read(4))[0]

    def readUInt(self):
        return struct.unpack(self.endian + "I", self.read(4))[0]

    def readLong(self):
        return struct.unpack(self.endian + "l", self.read(8))[0]

    def readULong(self):
        return struct.unpack(self.endian + "L", self.read(8))[0]

    def readBytes(self, size):
        ret = bytearray()
        for i in range(size):
            ret.append(struct.unpack(self.endian + "B", self.read(1))[0])
        return bytes(ret)

    def readFloat(self):
        return struct.unpack(self.endian + "f", self.read(4))[0]

    def read_floats(self, n):
        floats = []
        for i in range(n):
            floats.append(self.readFloat())
        return floats

    def readHalfFloat(self):
        return float(np.frombuffer(self.read(2), dtype="<e")[0])

    def readDouble(self):
        return struct.unpack(self.endian + "d", self.read(8))[0]


    def readString(self, encoding="utf-16"):
        b_array = []

        while True:
            character = self.readChar()
            if character == b"\x00" and encoding == "utf-8":
                break
            elif character == b"\x00" and encoding == "utf-16":
                if b_array != [] and b_array[-1] == b"\x00":
                    break

            b_array.append(character)

        string =  [item for item in b_array if item != b'\x00']

        return b''.join(string).decode('utf-8')

    def bytesToString(self, byteArray, encoding="utf-8"):
        try:
            return byteArray.decode(encoding)
        except:
            string = ""
            for b in byteArray:
                if b < 127:
                    string += chr(b)
            return string

    def getBoolean(self, offset):
        save_position = self.tell()
        self.seek(offset)
        boolean = self.readByte() == 1
        self.seek(save_position)

        return boolean

