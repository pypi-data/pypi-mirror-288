#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"




def pprint_param_line(param, depth, index:bool, type:bool, size:bool) -> str:
     result = ""
     if index != False:
          result += "{:<5}".format(param.index)

     if type != False:
          result += "{:<5}".format(param.type)

     if size != False:
          result += "{:<5}".format(param.size)

     result += "| " * depth
     result += param.name
     result += ":\t{}".format(param.get())
     return result



def pprint_sys_line(obj, depth, index:bool, type:bool, size:bool) -> str:
     result = ""
     if index != False:
          result += "{:<5}".format(obj.index)

     if type != False:
          result += "{:<5}".format(obj.type)

     if size != False:
          result += "{:<5}".format(obj.size)

     result += "| " * depth
     result += obj.name
     return result