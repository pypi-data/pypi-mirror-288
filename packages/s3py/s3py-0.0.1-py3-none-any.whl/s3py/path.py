#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


import unittest
from typing import List, Optional, Any
from s3py import LibS3Error


class Path:

    _stack = []
    separator_char=":"

    def __init__(self, init_list=List) -> None:
        if init_list:
            self._stack = init_list


    # @classmethod
    # def from_str(self, str_path:str, separator_char=':'):
    #     if not isinstance(str_path, str):
    #         raise LibS3Error("Path().from_str() expects a string as input.")
    #     return Path(str_path.split(separator_char))


    def push(self, element:Any) -> None:
        self._stack.append(element)


    def pop(self)  -> Optional[Any] :
        if len(self._stack):
            return self._stack.pop()
        else:
            raise LibS3Error("Path is empty.")

    def peek(self)  -> Optional[Any] :
        if len(self._stack):
            return self._stack[len(self._stack)-1]
        else:
            raise LibS3Error("Path is empty.")


    def __getitem__(self, index:int)  -> Optional[Any] :
        if index < len(self._stack):
            return self._stack[index]
        else:
            raise LibS3Error("Index out of is Path range.")

    @property
    def len(self) -> int:
        return len(self._stack)


    def __str__(self) -> str:
        return self.separator_char.join([x.__str__() for x in self._stack])
    

    def __repr__(self) -> str:
        return self.__str__()


    def __iter__(self):
        self._iter_idx = 0 
        return self
    
    def __next__(self):
        try:
            result = self._stack[self._iter_idx]
        except IndexError:
            raise StopIteration
        self._iter_idx += 1
        return result





class NamePath(Path):
    
    def __init__(self, str_path=str, separator_char=':') -> None:
        if not isinstance(str_path, str):
            raise LibS3Error("NamePath() expects a string as input.")
        super().__init__(str_path.split(separator_char))



    
 # Run with: python -m unittest -v libs3.path 
class TestPath(unittest.TestCase):


    
    def test_path_from_str(self):
        path = NamePath("uno:dos:tres")
        self.assertEqual(path.len, 3)
        self.assertEqual(path.pop(), "tres")
        self.assertEqual(path.len, 2)
        self.assertEqual(path.pop(), "dos")
        self.assertEqual(path.len, 1)
        self.assertEqual(path.pop(), "uno")
        self.assertEqual(path.len, 0)

    def test_path_iter(self):
        path = NamePath("uno:dos:tres")
        idx = 0
        for i in path:
            self.assertEqual(i, path[idx])
            idx += 1


if __name__ == '__main__':

    unittest.main()