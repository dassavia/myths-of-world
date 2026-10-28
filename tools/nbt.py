"""Tiny writer for the gzip NBT format Minecraft uses for structure templates (.nbt). No dependencies."""
import gzip
import struct


class Byte(int):
    pass


class Short(int):
    pass


class Long(int):
    pass


class Float(float):
    pass


class IntList(list):
    """TAG_List of TAG_Int (block positions, sizes)."""


class DoubleList(list):
    """TAG_List of TAG_Double (entity positions)."""


def _tag_id(value):
    if isinstance(value, bool) or isinstance(value, Byte):
        return 1
    if isinstance(value, Short):
        return 2
    if isinstance(value, Long):
        return 4
    if isinstance(value, Float):
        return 5
    if isinstance(value, int):
        return 3
    if isinstance(value, float):
        return 6
    if isinstance(value, str):
        return 8
    if isinstance(value, (list, IntList, DoubleList)):
        return 9
    if isinstance(value, dict):
        return 10
    raise TypeError(f"cannot store {value!r} as NBT")


def _payload(value, out):
    tid = _tag_id(value)
    if tid == 1:
        out += struct.pack(">b", int(value))
    elif tid == 2:
        out += struct.pack(">h", value)
    elif tid == 3:
        out += struct.pack(">i", value)
    elif tid == 4:
        out += struct.pack(">q", value)
    elif tid == 5:
        out += struct.pack(">f", value)
    elif tid == 6:
        out += struct.pack(">d", value)
    elif tid == 8:
        data = value.encode("utf-8")
        out += struct.pack(">H", len(data)) + data
    elif tid == 9:
        if isinstance(value, IntList):
            inner = 3
            value = [int(v) for v in value]
        elif isinstance(value, DoubleList):
            inner = 6
            value = [float(v) for v in value]
        else:
            inner = _tag_id(value[0]) if value else 0
        out += struct.pack(">bi", inner, len(value))
        for item in value:
            _payload(item, out)
    elif tid == 10:
        for key, item in value.items():
            out += struct.pack(">b", _tag_id(item))
            _payload(key, out)
            _payload(item, out)
        out += b"\x00"


def write(path, root):
    out = bytearray()
    out += struct.pack(">b", 10)
    _payload("", out)
    _payload(root, out)
    with open(path, "wb") as f:
        # mtime=0 keeps the file identical between runs.
        f.write(gzip.compress(bytes(out), mtime=0))
