#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


from enum import Enum
from pickle import GET
 


class RequestCode(Enum):
    GET         = 1
    SET         = 2
    CLONE       = 3
    PULL        = 4
    SUBSCRIBE   = 5


class ResponseCode(Enum):
    OK                  = 1
    INVALID_REQUEST     = 2 
    INVALID_ARGS        = 3
    SERVER_ERROR        = 4



class RequestMessage:
    code:int = 0
    args:str = None


    def __init__(self, code:RequestCode, args:dict={}) -> 'RequestMessage':
        self.code = code.value
        self.args = args




class ResponseMessage:
    code:int = 0
    args:str = None

    def __init__(self, code:ResponseCode, args:dict={}) -> 'ResponseMessage':
        self.code = code.value
        self.args = args