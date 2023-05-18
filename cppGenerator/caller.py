import ctypes
import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', 'build', 'libRandomGenLib.so'))


lib = ctypes.CDLL(lib_path)

lib.GetGenerator.restype = ctypes.c_void_p
lib.StartGenerator.argtypes = [ctypes.c_void_p, ctypes.c_longlong]
lib.TryGen.restype = ctypes.c_int32
lib.TryGen.argtypes = [ctypes.c_void_p]
lib.FreeGen.argtypes = [ctypes.c_void_p]


class Generator:
    def __init__(self):
        self._gen = lib.GetGenerator()


    def SetSeed(self, seed: int):
        lib.StartGenerator(self._gen, seed)

    def TryGen(self):
        num = lib.TryGen(self._gen)
        if num == -1:
            return None
        return num
    def __del__(self):
        lib.FreeGen(self._gen)
