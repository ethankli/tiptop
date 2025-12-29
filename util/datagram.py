import struct


class Datagram:
    def __init__(self, data: bytes = bytes()):
        self.data = bytearray(data)

    def add_int8(self, data: int):
        self.data += struct.pack("<b", data)
    
    def add_uint8(self, data: int):
        self.data += struct.pack("<B", data)
    
    def add_int16(self, data: int):
        self.data += struct.pack("<h", data)

    def add_uint16(self, data: int):
        self.data += struct.pack("<H", data)

    def add_int32(self, data: int):
        self.data += struct.pack("<i", data)
    
    def add_uint32(self, data: int):
        self.data += struct.pack("<I", data)

    def add_int64(self, data: int):
        self.data += struct.pack("<q", data)
    
    def add_uint64(self, data: int):
        self.data += struct.pack("<Q", data)
    
    def add_float32(self, data: float):
        self.data += struct.pack("<f", data)
    
    def add_float64(self, data: float):
        self.data += struct.pack("<d", data)

    def add_bool(self, data: bool):
        self.data += struct.pack("<?", data)
    
    def add_channel(self, data: int):
        self.add_uint64(data)

    def add_doid(self, data: int):
        self.add_uint32(data)

    def add_zone(self, data: int):
        self.add_uint32(data)

    def add_bytes(self, data: bytes):
        self.data += data

    def get_data(self) -> bytearray:
        return self.data
