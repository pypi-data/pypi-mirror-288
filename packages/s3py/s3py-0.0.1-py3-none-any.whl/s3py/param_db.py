#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


import unittest
from typing import  Union

from s3py import LibS3Error, Sys, Param, ParamType, NamePath, Group, _root, _group_list
from .s3_pprint import  pprint_param_line
from threading import Lock



class SingletonMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ParamDB(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

        
    def print_tree(self, index:bool = False, type:bool = False,  size:bool = False):
        _root.pprint(index, type, size)

    def search_sys(self, path:Union[str, NamePath]):
        if isinstance(path, str):
            path = NamePath(path)

        cur_sys = _root
        for sys_name in path:
            cur_sys = cur_sys.get_sys(sys_name)
        return cur_sys
    

    def search_param(self, path:Union[str, NamePath]):
        if isinstance(path, str):
            path = NamePath(path)
        param_name = path.pop()
        sys = self.search_sys(path)
        return sys.get_param(param_name)


    def search_sys_by_idx(self, index:int):
        # TODO implement
        pass


    def search_param_by_idx(self, index:int):
        # TODO implement
        pass

    def spawn_param(self, parent:Sys, name:str, type: ParamType, capacity:int=1, default:str=None):
        # Check if param with the same name already exists, to avoid repeated params
        try:
            result = parent.get_param(name)
        except:
            result =  Param(parent, name, type, capacity, default)
        result.from_chars(default)
        return result


    def spawn(self, path:NamePath, type: ParamType, capacity:int=1, default:str=None):
        if isinstance(path, str):
            path = NamePath(path)

        if path.len < 2:
            raise LibS3Error("Path for spawning a parm shall contain at leas 2 names.")
        # Extract name of param
        param_name = path.pop()        
        # Create all required paren systems in path
        cur_sys = _root
        for sys_name in path:
            try:
                cur_sys = cur_sys.get_sys(sys_name)
            except:
                cur_sys = Sys(cur_sys, sys_name)
        # Create the param
        return self.spawn_param(cur_sys, param_name, type, capacity, default)


    def __spawn_from_dict(self, sys_as_dict:dict, parent:Sys):
        try:
            cur_sys = parent.get_sys(sys_as_dict["sys"])
        except:
            cur_sys = Sys(parent, sys_as_dict["sys"])

        if "params" in sys_as_dict.keys():
            for param in sys_as_dict["params"]:
                capacity = param["size"] if "size"in param.keys() else 1
                default = param["default"] if "default"in param.keys() else None
                self.spawn_param(cur_sys, param["param"], ParamType(param["type"]), capacity, default)
                # Add param to corresponding groups
                if "groups" in param.keys():
                    for group_name in param["groups"]:
                        try:
                            group = self.get_group(group_name)
                        except:
                            group = Group(group_name)
                        group.add_param(param)
                        

        if "subsys" in sys_as_dict.keys():
            for sys in sys_as_dict["subsys"]:
                self._ParamDB__spawn_from_dict(sys, cur_sys)


    def spawn_from_dict(self, sys_as_dict:dict):
        self._ParamDB__spawn_from_dict(sys_as_dict, _root)


    def pprint_groups(self):
        for name, group in _group_list.items():
            print(f"{group.name}[{group.len}]")
    

    def get_group(self, name) -> Group:
        try:
            return _group_list[name]
        except:
            raise LibS3Error(f"Group '{name}' not found.")


# Run with: python -m unittest -v libs3.param_db 
class TestParamDB(unittest.TestCase):

    def setUp(self):
        self.db = ParamDB()

    def test_spawn(self):
        param_one =  self.db.spawn("sys:one", ParamType.UINT8, 1, "12")
        self.assertEqual(param_one, self.db.search_param("sys:one"))
        self.assertEqual(12, self.db.search_param("sys:one").get())
        self.assertEqual("u8", self.db.search_param("sys:one").type)
        self.assertEqual(1, self.db.search_param("sys:one").size)

        param_two =  self.db.spawn("sys:two", ParamType.FLT32, 1, "12.24")
        self.assertEqual(param_two, self.db.search_param("sys:two"))
        self.assertEqual(12.24, self.db.search_param("sys:two").get())
        self.assertEqual("f32", self.db.search_param("sys:two").type)
        self.assertEqual(4, self.db.search_param("sys:two").size)


        param_two =  self.db.spawn("sys:sub:thre", ParamType.STR, 10, "Wololo")
        self.assertEqual(param_two, self.db.search_param("sys:sub:thre"))
        self.assertEqual("Wololo", self.db.search_param("sys:sub:thre").get())
        self.assertEqual("str", self.db.search_param("sys:sub:thre").type)
        self.assertEqual(10, self.db.search_param("sys:sub:thre").size)


    def test_spawn_from_dict(self):


        

        self.db.spawn_from_dict({"sys": "dict", 
                                 "params": [{"param":"one", "type": "i32", "default": "123" }], 
                                 "subsys": [
                                     {"sys": "sub",
                                      "params":[{"param":"two", "type": "str", "size": 10, "default": "Hohoho" }]}
                                 ]})

        self.assertEqual(123, self.db.search_param("dict:one").get())
        self.assertEqual("i32", self.db.search_param("dict:one").type)
        self.assertEqual(4, self.db.search_param("dict:one").size)

        self.assertEqual("Hohoho", self.db.search_param("dict:sub:two").get())
        self.assertEqual("str", self.db.search_param("dict:sub:two").type)
        self.assertEqual(10, self.db.search_param("dict:sub:two").size)



if __name__ == '__main__':
    unittest.main()