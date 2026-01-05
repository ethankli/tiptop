import struct


class Datagram:
    def __init__(self, data: bytes = bytes(b"\x00\x00")):
        self.data = bytearray(data)
        self.length = 0

    def update_length(self):
        length = len(self.data) - 2
        if length > 0xFFFF:
            raise ValueError("Datagram length exceeds uint16 maximum")
        struct.pack_into("<H", self.data, 0, length)

    def add_int8(self, data: int):
        self.data += struct.pack("<b", data)
        self.update_length()
    
    def add_uint8(self, data: int):
        self.data += struct.pack("<B", data)
        self.update_length()
    
    def add_int16(self, data: int):
        self.data += struct.pack("<h", data)
        self.update_length()

    def add_uint16(self, data: int):
        self.data += struct.pack("<H", data)
        self.update_length()

    def add_int32(self, data: int):
        self.data += struct.pack("<i", data)
        self.update_length()
    
    def add_uint32(self, data: int):
        self.data += struct.pack("<I", data)
        self.update_length()

    def add_int64(self, data: int):
        self.data += struct.pack("<q", data)
        self.update_length()
    
    def add_uint64(self, data: int):
        self.data += struct.pack("<Q", data)
        self.update_length()
    
    def add_float32(self, data: float):
        self.data += struct.pack("<f", data)
        self.update_length()
    
    def add_float64(self, data: float):
        self.data += struct.pack("<d", data)
        self.update_length()

    def add_bool(self, data: bool):
        self.data += struct.pack("<?", data)
        self.update_length()

    def add_bytes(self, data: bytes):
        self.data += data
        self.update_length()

    def add_string(self, data: str = ""):
        encoded = data.encode("utf-8")
        self.add_uint16(len(encoded))
        self.data += encoded
        self.update_length()

    def add_server_header(self, to_channel: int, from_channel: int, msg_type: int):
        self.add_uint8(1)  # channel count
        self.add_uint64(to_channel)
        self.add_uint64(from_channel)
        self.add_uint16(msg_type)
        self.update_length()

    def get_data(self) -> bytes:
        return self.data
