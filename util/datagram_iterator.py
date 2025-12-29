import struct

from util.datagram import Datagram


class DatagramIterator:
    def __init__(self, datagram: Datagram):
        self.datagram = datagram

    def get_int8(self) -> int:
        value = struct.unpack("<b", self.datagram.data[:1])[0]
        self.datagram.data = self.datagram.data[1:]
        return value

    def get_uint8(self) -> int:
        value = struct.unpack("<B", self.datagram.data[:1])[0]
        self.datagram.data = self.datagram.data[1:]
        return value

    def get_int16(self) -> int:
        value = struct.unpack("<h", self.datagram.data[:2])[0]
        self.datagram.data = self.datagram.data[2:]
        return value

    def get_uint16(self) -> int:
        value = struct.unpack("<H", self.datagram.data[:2])[0]
        self.datagram.data = self.datagram.data[2:]
        return value

    def get_int32(self) -> int:
        value = struct.unpack("<i", self.datagram.data[:4])[0]
        self.datagram.data = self.datagram.data[4:]
        return value
    
    def get_uint32(self) -> int:
        value = struct.unpack("<I", self.datagram.data[:4])[0]
        self.datagram.data = self.datagram.data[4:]
        return value
    
    def get_int64(self) -> int:
        value = struct.unpack("<q", self.datagram.data[:8])[0]
        self.datagram.data = self.datagram.data[8:]
        return value
    
    def get_uint64(self) -> int:
        value = struct.unpack("<Q", self.datagram.data[:8])[0]
        self.datagram.data = self.datagram.data[8:]
        return value
    
    def get_float32(self) -> float:
        value = struct.unpack("<f", self.datagram.data[:4])[0]
        self.datagram.data = self.datagram.data[4:]
        return value

    def get_float64(self) -> float:
        value = struct.unpack("<d", self.datagram.data[:8])[0]
        self.datagram.data = self.datagram.data[8:]
        return value
    
    def get_bool(self) -> bool:
        value = struct.unpack("<?", self.datagram.data[:1])[0]
        self.datagram.data = self.datagram.data[1:]
        return value

    def get_channel(self) -> int:
        return self.get_uint64()
    
    def get_doid(self) -> int:
        return self.get_uint32()
    
    def get_zone(self) -> int:
        return self.get_uint32()
    
    def get_bytes(self, length: int) -> bytes:
        value = self.datagram.data[:length]
        self.datagram.data = self.datagram.data[length:]
        return value
