#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


import unittest
from typing import List, Dict, Optional, Union
from s3py import LibS3Error, Name
from .s3_pprint import pprint_sys_line, pprint_param_line

# Forward declaration
def _add_sys_to_root(sys): pass

class Sys():

    def __init__(self, parent:'Sys', name:str) -> 'Sys':
        self._parent = parent
        self._name = Name(name)
        if(parent):
            parent.__add_sys(self)
        else:
            _add_sys_to_root(self)  # Add top-levels sys to the root 
        self._subsys = []
        self._params = []
        

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
    def type(self) -> str:
        return "sys"
    
    @property
    def parent(self) -> Optional['Sys']:
        return self._parent

    def __add_sys(self, sys):
        self._subsys.append(sys)


    def __add_param(self, param):
        self._params.append(param)


    def get_sys(self, name)-> 'Sys':
        for s in self._subsys:
            if( s.name == name ):
                return s
        raise  LibS3Error(f"Sys '{name}' not found in '{self.name}'!")


    def get_param(self, name)-> 'Param':
        for p in self._params:
            if( p.name == name ):
                return p
        raise  LibS3Error(f"Param '{name}' not found in '{self.name}'!")
    

    def __getitem__(self, name) -> Union['Param', 'Sys'] :
        try:
            return self.get_param(name)
        except:
            pass
        try:
            return self.get_sys(name)
        except:
            raise  LibS3Error(f"Item '{name}' not found!")
    

    def to_dict(self) -> dict:
        result = {}
        for param in self._params:
            result[param.name] = param.get()
        for sys in self._subsys:
            result[sys.name] = sys.to_dict()
        return result
    

    def to_flat_dict(self)-> List[dict]:
        pass


    def set(self, data : dict):
        for key, value in data.items():
            self[key].set(value)
            


    def _pprint(self, depth, index, type, size): 
        for param in self._params:
            print(pprint_param_line(param, depth, index, type, size))

        for sys in self._subsys:
            print(pprint_sys_line(sys, depth, index, type, size))
            sys._pprint(depth+1, index, type,  size)



    def pprint(self, index:bool = False, type:bool = False,  size:bool = False): 
        self._pprint(0, index, type,  size)


# Root system
_root = Sys(None, "/")

def _add_sys_to_root(sys):
    if sys != _root:
        _root._Sys__add_sys(sys)




# Run with: python -m unittest -v libs3.sys 
class TestSys(unittest.TestCase):

    def setUp(self):
        self.parent = Sys(None, "prnt")

    def test_nested_name(self):
        print(self.parent)
        self.assertEqual(self.parent.name, "prnt")

if __name__ == '__main__':
    unittest.main()