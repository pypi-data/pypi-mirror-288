#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


from typing import Any
import unittest
from datetime import datetime
from s3py import LibS3Error, Name, Sys, Path
from enum import Enum
import struct


class ParamType(Enum):
    BOOL   = "bool"
    UINT8  = "u8"
    INT8   = "i8"
    UINT16 = "u16"
    INT16  = "i16"
    UINT32 = "u32"
    INT32  = "i32"
    UINT64 = "u64"
    INT64  = "i64"
    FLT32  = "f32"
    FLT64  = "f64"
    DATE   = "date"
    STR    = "str"
    BLOB   = "blob"


    @property
    def encode_specifier(self):
        specifiers = {
            ParamType.BOOL.value   : "B",
            ParamType.UINT8.value  : "B",
            ParamType.INT8.value   : "b",
            ParamType.UINT16.value : "H",
            ParamType.INT16.value  : "h",
            ParamType.UINT32.value : "I",
            ParamType.INT32.value  : "i",
            ParamType.UINT64.value : "Q",
            ParamType.INT64.value  : "q",
            ParamType.FLT32.value  : "f",
            ParamType.FLT64.value  : "f",
            ParamType.DATE.value   : "",
            ParamType.STR.value    : "",
            ParamType.BLOB.value   : "",    
        }
        return specifiers[self.value]

    @property
    def underling_class(self):
        classes = {
            ParamType.BOOL.value   : bool,
            ParamType.UINT8.value  : int,
            ParamType.INT8.value   : int,
            ParamType.UINT16.value : int,
            ParamType.INT16.value  : int,
            ParamType.UINT32.value : int,
            ParamType.INT32.value  : int,
            ParamType.UINT64.value : int,
            ParamType.INT64.value  : int,
            ParamType.FLT32.value  : float,
            ParamType.FLT64.value  : float,
            ParamType.DATE.value   : datetime,
            ParamType.STR.value    : str,
            ParamType.BLOB.value   : bytearray,    
        }
        return classes[self.value]


    def get_size(self, capacity):
        classes = {
            ParamType.BOOL.value   : 1,
            ParamType.UINT8.value  : 1,
            ParamType.INT8.value   : 1,
            ParamType.UINT16.value : 2,
            ParamType.INT16.value  : 2,
            ParamType.UINT32.value : 4,
            ParamType.INT32.value  : 4,
            ParamType.UINT64.value : 8,
            ParamType.INT64.value  : 8,
            ParamType.FLT32.value  : 4,
            ParamType.FLT64.value  : 8,
            ParamType.DATE.value   : 8,
            ParamType.STR.value    : 1,
            ParamType.BLOB.value   : 1,    
        }
        return classes[self.value] * capacity



class Param:

    def __init__(self, parent: Sys, name:str, type: ParamType, capacity: int, value) -> 'Param':
        if(not isinstance(parent, Sys)):
            raise LibS3Error("Param's first argument must be of type Sys.")
        self._parent = parent
        self._name = Name(name)
        self._type  = type
        capacity = 1 if capacity == 0 else capacity
        self._size  = type.get_size(capacity)
        self._underling = type.underling_class
        self._be_encode_specifier = ">"+type.encode_specifier
        self._le_encode_specifier = "<"+type.encode_specifier
        self._value = value
        
        # Append to parent
        parent._Sys__add_param(self)

    @property
    def name(self) -> str:
        return self._name.as_str
    
    def get_name(self) -> Name:
        return self._name

    @property
    def index(self) -> int:
        return 0
        # TODO Implement

    @property
    def type(self)->str:
        return self._type.value

    @property
    def size(self)->str:
        return self._size

    @property
    def parent(self) -> Sys:
        return self._parent

    def get(self) -> Any:
        return self._value

    def set(self, value: Any):
        if(self._underling != type(value)):
            raise LibS3Error(f"Mismatching types, when trying to set Param '{self.name}' of type {self._underling}, with '{value}' of type {type(value)}.")
        self._value = value
            

    def path(self) -> Path:
        reverse = [self.name]
        parent = self.parent
        while parent is not None:
            reverse.append(parent.name)
            parent = parent.parent
        reverse.reverse()
        return Path(reverse)

    def to_chars(self) -> str:
        return self.__str__()


    def from_chars(self, value:str):
        try:
            self.set(self._underling(value))
        except:
            raise LibS3Error(f"Invalid data format when decoding param '{self.name}'.")


    def encode(self, to_big_endian:bool=False) -> bytes:
        if(to_big_endian):
            return struct.pack(self._be_encode_specifier, self._value)
        else:
            return struct.pack(self._le_encode_specifier, self._value)


    def decode(self, value:bytes, from_big_endian:bool=False):
        if from_big_endian:
            self._value, = struct.unpack( self._be_encode_specifier, value)
        else:
            self._value, = struct.unpack( self._le_encode_specifier, value)
        
        

    def __str__(self) -> str:
        return f"{self._value}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, spec) -> str:
        return self.__str__().__format__(spec)

    def _asdict (self):
        return self._value





class ParamBool(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.BOOL, 1, value=value)


class ParamU8(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.UINT8, 1, value=value)


class ParamI8(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.INT8, 1,  value=value)


class ParamU16(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.UINT16, 1, value=value)


class ParamI16(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.INT16, 1,  value=value)


class ParamU32(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.UINT32, 1, value=value)


class ParamI32(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.INT32, 1, value=value)


class ParamU64(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.UINT64, 1, value=value)


class ParamI64(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.INT64, 1, value=value)


class ParamF32(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.FLT32, 1, value=value)


class ParamF64(Param):
    def __init__(self, parent: Sys, name: str, value=0) -> Param:
        super().__init__(parent, name, ParamType.FLT64, 1, value=value)


class ParamStr(Param):
    def __init__(self, parent: Sys, name: str, capacity:int, value="") -> Param:
        super().__init__(parent, name, ParamType.STR, capacity, value=value)

    def encode(self, to_big_endian:bool=False) -> bytes:
        return self._value.encode()

    def decode(self, value:bytes, from_big_endian:bool=False):
        self._value = value.decode()

class ParamBlob(Param):
    def __init__(self, parent: Sys, name: str, capacity:int, value=0) -> Param:
        super().__init__(parent, name, ParamType.BLOB, capacity, value=value)


    # TODO implement

    def encode(self, to_big_endian:bool=False) -> bytes:
        return self._value

    def decode(self, value:bytes, from_big_endian:bool=False):
        self._value = value



# Run with: python -m unittest -v libs3.param 
class TestParam(unittest.TestCase):

    def setUp(self):
        self.sys     = Sys(None, "sys")
        self.put_u8  = ParamU8(self.sys,  "u8",  1)
        self.put_i8  = ParamI8(self.sys,  "i8",  -1)
        self.put_u16 = ParamU16(self.sys, "u16", 123)
        self.put_i16 = ParamI16(self.sys, "i16", -123)
        self.put_u32 = ParamU32(self.sys, "u32", 123)
        self.put_i32 = ParamI32(self.sys, "i32", -123)
        self.put_u64 = ParamU64(self.sys, "u64", 123)
        self.put_i64 = ParamI64(self.sys, "i64", -123)
        self.put_f32 = ParamF32(self.sys, "f32", 4.20)
        self.put_f64 = ParamF64(self.sys, "f64", 4.20)
        self.put_str = ParamStr(self.sys, "str", 32, "Hi, Im libs3!")
        self.put_byt = ParamBlob(self.sys, "byt", 10, b'\x01\x02\x03\x04')
        self.subsys      = Sys(self.sys, "sub")
        self.sub_put_u8  = ParamU8(self.subsys,  "sub8",  1)

    def test_name(self):       
        self.assertEqual(self.put_u16.name, "u16")
        self.assertEqual(self.put_f32.name, "f32")
        self.assertEqual(self.put_str.name, "str")

    def test_wrong_formed(self):
        with self.assertRaises(LibS3Error):
            wrong_param = ParamU8("some", 1)
        with self.assertRaises(LibS3Error):
            wrong_param = ParamU8(self.sys, "", 1)

    def test_type(self):       
        self.assertEqual(self.put_u16.type, "u16")
        self.assertEqual(self.put_f32.type, "f32")
        self.assertEqual(self.put_str.type, "str")


    def test_set_get(self):
        self.put_u16.set(1010)
        self.put_f32.set(0.9898)
        self.put_str.set("Hi, you!!")

        self.assertEqual(self.put_u16.get(), 1010)
        self.assertEqual(self.put_f32.get(), 0.9898)
        self.assertEqual(self.put_str.get(), "Hi, you!!")


    def test_to_chars(self):
        self.put_u16.set(321)
        self.put_f32.set(0.42)
        self.put_str.set("Byee!!")

        self.assertEqual(self.put_u16.to_chars(), "321")
        self.assertEqual(self.put_f32.to_chars(), "0.42")
        self.assertEqual(self.put_str.to_chars(), "Byee!!")


    def test_from_chars(self):
        self.put_u16.from_chars("4321")
        self.put_f32.from_chars("0.4321")
        self.put_str.from_chars("Something else!!")

        self.assertEqual(self.put_u16.get(), 4321)
        self.assertEqual(self.put_f32.get(), 0.4321)
        self.assertEqual(self.put_str.get(), "Something else!!")


    def test_encode_little(self):
        self.put_u16.set(0x321)
        self.put_i16.set(-321) ## FEBF
        self.put_f32.set(1.23456)  # 1.23456 -> IEEE 754 -> 
        self.put_str.set("Byee!!")


        self.assertEqual(self.put_u16.encode(), b"\x21\x03")
        self.assertEqual(self.put_i16.encode(), b"\xbf\xfe")
        self.assertEqual(self.put_f32.encode(), b"\x10\x06\x9e\x3f")
        self.assertEqual(self.put_str.encode(), b"Byee!!")



    def test_encode_big(self):
        self.put_u16.set(0x321)
        self.put_i16.set(-321) ## FEBF
        self.put_f32.set(1.23456)  # 1.23456 -> IEEE 754 
        self.put_str.set("Byee!!")


        self.assertEqual(self.put_u16.encode(True), b"\x03\x21")
        self.assertEqual(self.put_i16.encode(True), b"\xfe\xbf")
        self.assertEqual(self.put_f32.encode(True), b"\x3f\x9e\x06\x10")
        self.assertEqual(self.put_str.encode(True), b"Byee!!")


    def test_decode_little(self): 
        self.put_u16.decode(b"\x94\x26") # = 9876
        self.put_i16.decode(b"\x6c\xd9") # = -9876
        self.put_f32.decode(b"\x19\x04\x1e\x41")  # = 9.876 411e0419
        self.put_str.decode(b"Hi again!!")


        self.assertEqual(self.put_u16.get(), 9876)
        self.assertEqual(self.put_i16.get(), -9876)
        self.assertAlmostEqual(self.put_f32.get(), 9.876, places=4)
        self.assertEqual(self.put_str.get(), "Hi again!!")



    def test_decode_big(self): 
        self.put_u16.decode(b"\x26\x94", True) # = 9876
        self.put_i16.decode(b"\xd9\x6c", True) # = -9876
        self.put_f32.decode(b"\x41\x1e\x04\x19", True)  # = 9.876 411e0419
        self.put_str.decode(b"Hi again!!", True)


        self.assertEqual(self.put_u16.get(), 9876)
        self.assertEqual(self.put_i16.get(), -9876)
        self.assertAlmostEqual(self.put_f32.get(), 9.876, places=4)
        self.assertEqual(self.put_str.get(), "Hi again!!")


    def test_decode_path(self): 
        path = self.put_u8.path()
        self.assertEqual(path.len, 2)
        self.assertEqual(path.__str__(), "sys:u8")

        path = self.sub_put_u8.path()
        self.assertEqual(path.len, 3)
        self.assertEqual(path.__str__(), "sys:sub:sub8")


    def test_mismatch_type(self):
        with self.assertRaises(LibS3Error):
            self.put_u16.set(1.23)
        with self.assertRaises(LibS3Error):
            self.put_f32.set(123)
        with self.assertRaises(LibS3Error):
            self.put_str.set(123)

if __name__ == '__main__':
    unittest.main()