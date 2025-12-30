import struct
from io import BytesIO

from util.datagram import Datagram


class DatagramIterator:
    def __init__(self, datagram: Datagram):
        self.data = BytesIO(datagram.get_data())

    def get_int8(self) -> int:
        raw = self.data.read(1)
        if len(raw) < 1:
            raise EOFError("Not enough data to read int8")
        return struct.unpack("<b", raw)[0]

    def get_uint8(self) -> int:
        raw = self.data.read(1)
        if len(raw) < 1:
            raise EOFError("Not enough data to read uint8")
        return struct.unpack("<B", raw)[0]

    def get_int16(self) -> int:
        raw = self.data.read(2)
        if len(raw) < 2:
            raise EOFError("Not enough data to read int16")
        return struct.unpack("<h", raw)[0]

    def get_uint16(self) -> int:
        raw = self.data.read(2)
        if len(raw) < 2:
            raise EOFError("Not enough data to read uint16")
        return struct.unpack("<H", raw)[0]

    def get_int32(self) -> int:
        raw = self.data.read(4)
        if len(raw) < 4:
            raise EOFError("Not enough data to read int32")
        return struct.unpack("<i", raw)[0]
    
    def get_uint32(self) -> int:
        raw = self.data.read(4)
        if len(raw) < 4:
            raise EOFError("Not enough data to read uint32")
        return struct.unpack("<I", raw)[0]
    
    def get_int64(self) -> int:
        raw = self.data.read(8)
        if len(raw) < 8:
            raise EOFError("Not enough data to read int64")
        return struct.unpack("<q", raw)[0]
    
    def get_uint64(self) -> int:
        raw = self.data.read(8)
        if len(raw) < 8:
            raise EOFError("Not enough data to read uint64")
        return struct.unpack("<Q", raw)[0]
    
    def get_float32(self) -> float:
        raw = self.data.read(4)
        if len(raw) < 4:
            raise EOFError("Not enough data to read float32")
        return struct.unpack("<f", raw)[0]

    def get_float64(self) -> float:
        raw = self.data.read(8)
        if len(raw) < 8:
            raise EOFError("Not enough data to read float64")
        return struct.unpack("<d", raw)[0]
    
    def get_bool(self) -> bool:
        raw = self.data.read(1)
        if len(raw) < 1:
            raise EOFError("Not enough data to read bool")
        return struct.unpack("<?", raw)[0]
    
    def get_string(self) -> str:
        length = self.get_uint16()
        raw = self.data.read(length)
        if len(raw) < length:
            raise EOFError("Not enough data to read string")
        return raw.decode('utf-8')
    
    def get_channel(self) -> int:
        return self.get_uint64()
    
    def get_doid(self) -> int:
        return self.get_uint32()
    
    def get_zone(self) -> int:
        return self.get_uint32()
    
    def get_data(self) -> bytes:
        return self.data.read()
    
    def get_bytes(self, length: int) -> bytes:
        raw = self.data.read(length)
        if len(raw) < length:
            raise EOFError(f"Not enough data to read {length} bytes")
        return raw
