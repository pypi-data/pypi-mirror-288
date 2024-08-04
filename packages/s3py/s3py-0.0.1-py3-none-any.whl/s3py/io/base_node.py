#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"

import socket
from typing import Dict

def recvall(sock: socket.socket) -> bytearray:
    '''
    Helper function to recv n bytes or return None if EOF is hit
    ''' 
    BUFF_SIZE = 1024
    data = bytearray()
    while True:
        part = sock.recv(BUFF_SIZE)
        data.extend(part)
        if len(part) < BUFF_SIZE:
            break
    return data





class BaseNode():
    def __init__(self, name:str, ip_addr:str='localhost', port:int=4200) -> 'BaseNode':
        self._ip_addr     = ip_addr
        self._port        = port
        super(BaseNode, self).__init__(name)

    def __repr__(self) -> str:
        return f"Node( '{self._name}', ip_addr='{self._ip_addr}', port={self._port}, items={self.items()})"


    def show(self):
        print(f"Node '{self._name}': (ip_addr='{self._ip_addr}', port={self._port})")
        if self.items():
            for k in self.items():
                print(f"\t{k}")
        else:
            print("\t...no items...")


    def load(self, data:Dict):
        for k, v in data.items():
            self[k] = v
            

