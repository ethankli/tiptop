from util.datagram import Datagram
from util.datagram_iterator import DatagramIterator


def main():
    # Create a datagram and add various data types
    datagram = Datagram()
    datagram.add_int8(-5)
    datagram.add_uint8(250)
    datagram.add_int16(-30000)
    datagram.add_uint16(60000)
    datagram.add_int32(-2000000000)
    datagram.add_uint32(4000000000)
    datagram.add_int64(-9000000000000000000)
    datagram.add_uint64(18000000000000000000)
    datagram.add_float32(3.14)
    datagram.add_float64(2.718281828459045)
    datagram.add_bool(True)

    # Create an iterator to read back the data
    iterator = DatagramIterator(datagram)

    assert iterator.get_int8() == -5
    assert iterator.get_uint8() == 250
    assert iterator.get_int16() == -30000
    assert iterator.get_uint16() == 60000
    assert iterator.get_int32() == -2000000000
    assert iterator.get_uint32() == 4000000000
    assert iterator.get_int64() == -9000000000000000000
    assert iterator.get_uint64() == 18000000000000000000
    assert abs(iterator.get_float32() - 3.14) < 1e-6
    assert abs(iterator.get_float64() - 2.718281828459045) < 1e-12
    assert iterator.get_bool() is True

    print("All tests passed!")

if __name__ == "__main__":
    main()
