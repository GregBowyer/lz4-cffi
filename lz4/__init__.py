from cffi import FFI
from os.path import dirname
from os.path import join as pthjoin
from os.path import relpath

ffi = FFI()

ffi.cdef("int LZ4_compress   (const char*, char*, int);")
ffi.cdef("int LZ4_decompress_safe (const char*, char*, int, int);")
ffi.cdef("int LZ4_compressHC (const char*, char*, int);")
ffi.cdef("int LZ4_compressBound (int);")

path = dirname(__file__)
lz4_files = ['lz4.c', 'lz4hc.c', 'xxhash.c']
sources = [relpath(pthjoin(path, p)) for p in lz4_files]
_lz4 = ffi.verify(sources=sources)


def _store_le32(c, x):
    c[0] = chr(x & 0xff)
    c[1] = chr((x >> 8) & 0xff)
    c[2] = chr((x >> 16) & 0xff)
    c[3] = chr((x >> 24) & 0xff)


def _load_le32(c):
    return ord(c[0])      | \
        (ord(c[1]) << 8)  | \
        (ord(c[2]) << 16) | \
        (ord(c[3]) << 24)

HDR_SIZE = 4
INT_MAX = 2 ** 31


def _compress_with(compressor, source):
    source_size = len(source)

    dest_size = HDR_SIZE + _lz4.LZ4_compressBound(source_size)
    dest = ffi.new("char[]", dest_size)
    actual_size = 0

    _store_le32(dest, source_size)
    if source_size > 0:
        osize = compressor(source, dest + HDR_SIZE, source_size)
        actual_size = HDR_SIZE + osize

    return (dest, actual_size)


def _compress(source):
    return _compress_with(_lz4.LZ4_compress, source)


def _compressHC(source):
    return _compress_with(_lz4.LZ4_compressHC, source)


def _uncompress(source):
    source_size = len(source)

    if source_size < HDR_SIZE:
        raise ValueError("input too short")

    dest_size = _load_le32(source)
    if dest_size > INT_MAX or dest_size < 0:
        raise ValueError("invalid size in header: %d - 0x%x"
                         % (dest_size, dest_size))

    dest = ffi.new("char[]", dest_size)
    osize = _lz4.LZ4_decompress_safe(source[4:], dest,
                                     source_size - HDR_SIZE, dest_size)
    if osize < 0:
        raise ValueError("corrupt input at byte %d" % -osize)
    return (dest, dest_size)


def compress(source):
    data, size = _compress(source)
    return ffi.buffer(data, size)[:]


def compressHC(source):
    data, size = _compressHC(source)
    return ffi.buffer(data, size)[:]


def uncompress(source):
    data, size = _uncompress(source)
    return ffi.buffer(data, size)[:]

loads = decompress = uncompress
dumps = compress

__all__ = ['compress', 'compressHC', 'uncompress', 'decompress', 'loads', 'dumps']
