#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


import unittest
from s3py import LibS3Error

class Name:

    def __init__(self, new_name:str) -> 'Name':
        if(not new_name):
            raise LibS3Error("The Name of a Param/Sys can't be null initialized.")
        if(len(new_name) > 4):
            raise LibS3Error(f"Name '{new_name}' is too long, up to 4 chars allowed for a Name.")
        self._name = new_name
        chars = [b for b in new_name]  
        self._id = int.from_bytes(new_name.encode('utf-8'), "little") 

    @property
    def as_str(self) -> str:
        return self._name

    @property
    def as_int(self)-> int:
        return self._id

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __format__(self, spec) -> str:
        return self.__str__().__format__(spec)

    def _asdict (self):
        return self._name
    

    def __eq__(self, other:'Name') -> bool:

        if(isinstance(other, Name)):
            if(self.as_int == other.as_int):
                return True
        elif(isinstance(other, int)):
            if(self.as_int == other):
                return True
        elif(isinstance(other, str)):
            if(self.as_str == other):
                return True
        return False



# Run with: python -m unittest -v libs3.name 
class TestName(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()