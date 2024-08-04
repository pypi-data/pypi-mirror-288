#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


import unittest
from typing import List, Dict
from s3py import  Sys
from s3py.param import *
from .s3_pprint import  pprint_param_line


_group_list = dict()

class Group():

    def __init__(self, name:str, param_list: List[Param] = None) -> 'Group':
        self._name = name
        self._size = 0
        if param_list:
            self._list = param_list
            for param in self._list:
                if not isinstance(param, Param):
                    raise LibS3Error("Elements in Group initializer list must be subclass of Param.")
                self._size += param.size
            # Add to group list
            _group_list[name] = self
        else:
            self._list = []

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def len(self) -> int:
        '''
        Number of elements in Group
        '''
        return len(self._list)

    @property
    def size(self) -> int:
        '''
        Sum of sizes of all Group's parameters
        '''
        return self._size


    def add_param(self, param:Param):
        if not isinstance(param, Param):
            raise LibS3Error("Elements to add to a Group must be subclass of Param.")
        if param not in self._list:
            self._list.append(Param)
            self._size += param.size


    def pprint(self, index:bool = False, type:bool = False,  size:bool = False): 
        for param in self._list:
            print(f"{param.path()}:\t{param.get()}")



    def encode(self, to_big_endian:bool=False) -> bytearray:
        result = bytearray(self.size)
        idx = 0
        
        for param in self._list:
            result[idx:idx+param.size] = param.encode(to_big_endian)
            idx += param.size
        return result


    def decode(self, value:bytes, from_big_endian:bool=False) -> int:
        result = 0
        idx = 0
        
        if len(value) < self.size:
            return result

        for param in self._list:
            param.decode(value[idx:idx+param.size], from_big_endian)
            result += 1
            idx += param.size
        return result





# Run with: python -m unittest -v libs3.group 
class TestParam(unittest.TestCase):
    def setUp(self):
        self.sys     = Sys(None, "sys")
        self.put_u16 = ParamI16(self.sys, "u16")
        self.put_i16 = ParamI16(self.sys, "i16")
        self.put_f32 = ParamF32(self.sys, "f32")
        self.put_str = ParamStr(self.sys, "str", 10)

        self.test_group = Group("test_group", [
            self.put_u16,
            self.put_i16,
            self.put_f32,
            self.put_str
        ])

    def test_size(self): 
        self.assertEqual(self.test_group.len, 4)
        self.assertEqual(self.test_group.size, 18)

    def test_decode_little(self): 

        self.put_u16.set(0)
        self.put_i16.set(0)
        self.put_f32.set(0.0)
        self.put_str.set("")

        data = b"\x94\x26\x6c\xd9\x19\x04\x1e\x41Hi again!!"

        self.assertEqual(self.test_group.decode(data), 4)

        self.assertEqual(self.put_u16.get(), 9876)
        self.assertEqual(self.put_i16.get(), -9876)
        self.assertAlmostEqual(self.put_f32.get(), 9.876, places=4)
        self.assertEqual(self.put_str.get(), "Hi again!!")




    def test_decode_big(self): 
        self.put_u16.set(0)
        self.put_i16.set(0)
        self.put_f32.set(0.0)
        self.put_str.set("")

        data = b"\x26\x94\xd9\x6c\x41\x1e\x04\x19Hi again!!"

        self.assertEqual(self.test_group.decode(data, True), 4)

        self.assertEqual(self.put_u16.get(), 9876)
        self.assertEqual(self.put_i16.get(), -9876)
        self.assertAlmostEqual(self.put_f32.get(), 9.876, places=4)
        self.assertEqual(self.put_str.get(), "Hi again!!")



    def test_encode_little(self): 

        self.put_u16.set(9876)
        self.put_i16.set(-9876)
        self.put_f32.set(9.876)
        self.put_str.set("Hi again!!")

        expected = b"\x94\x26\x6c\xd9\x19\x04\x1e\x41Hi again!!"

        self.assertEqual(self.test_group.encode(), expected)


    def test_encode_big(self): 

        self.put_u16.set(9876)
        self.put_i16.set(-9876)
        self.put_f32.set(9.876)
        self.put_str.set("Hi again!!")

        expected = b"\x26\x94\xd9\x6c\x41\x1e\x04\x19Hi again!!"

        self.assertEqual(self.test_group.encode(True), expected)

if __name__ == '__main__':
    unittest.main()