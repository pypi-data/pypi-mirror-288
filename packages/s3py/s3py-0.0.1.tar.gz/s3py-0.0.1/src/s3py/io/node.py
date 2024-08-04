#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"

import socket
import pickle
import threading
from typing import Dict, List, Any, Union

from s3py import LibS3Error, Param, Sys, Group, Param
from s3py.io import RequestMessage, ResponseMessage, RequestCode, ResponseCode
from .base_node import *





class Node(BaseNode):
    '''
    Node class.
    '''
    def __init__(self, name:str, ip_addr:str='localhost', port:int=4200, containers:List[Union[Param,Sys,Group]]=None) -> 'Node':
        super().__init__(name, ip_addr, port)
        for obj in containers:
            self.add(obj)

    def __setitem__(self, key, value) -> None:
        return self.add(value)

    def add(self, obj:Union[Param, Sys, Group]):
        '''
        Add a 'Param', 'Collection' or 'Group' to node.
        '''
        if type(obj) ==  Param or type(obj) == Sys or type(obj) == Group:
            return super().__setitem__(obj.name, obj)
        else:
            raise LibS3Error(f"Invalid type of object to add to Node '{self._name}'.  Object has to be 'Collection' or 'Group'.")



    def _handle_get(self, request:RequestMessage):
        try:
            param = self.query(request.args["param"])
            response_payload = {'value': param.get(),
                                'type': param.type
                                }
            return ResponseCode.OK, response_payload
        except:
            return ResponseCode.INVALID_REQUEST, {}


    def _handle_set(self, request:RequestMessage):
        try:
            param = self.query(request.args["param"])
            param.decode(request.args["value"])
            response_payload = {'value': param.get(),
                                'type': param.type
                                }
            return ResponseCode.OK, response_payload
        except Exception as e:
            response_code, response_payload = ResponseCode.INVALID_REQUEST, {}
            print(e)
            return ResponseCode.INVALID_REQUEST, {}


    def _handle_clone(self, request):
        try:
            response_payload = self.copy()
            return ResponseCode.OK, response_payload
        except Exception as e:
            response_code, response_payload = ResponseCode.INVALID_REQUEST, {}
            return ResponseCode.INVALID_REQUEST, {}



    def _handle_pull(self, request):
        pass



    def _handle_subscribe(self, request):
        pass



    def request_handler(self, cli_sock: socket.socket, cli_addr:List):
        try:
            while True:
                data =  recvall(cli_sock)
                request = pickle.loads(data)
                print(f"[*] From {cli_addr[0]}: {RequestCode(request.code).name} request, args: {request.args}")
                response_code    = None
                response_payload = None
                # Lookup Request handler
                if request.code == RequestCode.GET.value:
                    response_code, response_payload = self._handle_get(request)
                elif request.code == RequestCode.SET.value:
                    response_code, response_payload = self._handle_set(request)
                elif request.code == RequestCode.CLONE.value:
                    response_code, response_payload = self._handle_clone(request)
                elif request.code == RequestCode.PULL.value:
                    response_code, response_payload = self._handle_pull(request)
                elif request.code == RequestCode.SUBSCRIBE.value:
                    response_code, response_payload = self._handle_subscribe(request)
                else:
                    response_code, response_payload = ResponseCode.INVALID_REQUEST, {}
                # Write back to the client
                response = pickle.dumps(ResponseMessage(response_code, response_payload))
                cli_sock.sendall(response)
        except EOFError:
            print(f"[*] Client at {cli_addr[0]} disconnected.")
        finally:
            cli_sock.close()



    def serve_forever(self):
        '''
        Start Node as Server.
        '''   
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self._ip_addr, self._port))
        self.server.listen(5)
        print(f"[*] Node '{self._name}' listening at {self._ip_addr}:{self._port}...")
        while True:
            cli_sock, cli_addr = self.server.accept()
            print(f"[*] Accepted connection from: {cli_addr[0]}:{cli_addr[1]}")
            client_handler = threading.Thread(target = self.request_handler, args=(cli_sock, cli_addr))
            client_handler.start()
    


class RemoteNode(BaseNode):
    '''
    RemoteNode to locally instantiate a Node 'living' in another virtual/physical context.
    '''
    def __init__(self, name:str, ip_addr:str='localhost', port:int=4200) -> 'RemoteNode':
        super().__init__(name, ip_addr, port)
        self.connect()

    def _transaction(self, request: RequestMessage) -> Dict:
        payload = pickle.dumps(request)     
        self.sock.send(payload)
        response = recvall(self.sock)
        if len(response):
            response = pickle.loads(response)
            print(f"From Server: {ResponseCode(response.code).name} response, args: {response.args}")
            return response
        else:
            return {}

    def __setitem__(self, key, value) :
        return super().__setitem__(key, value)


    def __getitem__(self, key):
        return super().__getitem__(key)

    def connect(self):
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.connect((self._ip_addr, self._port))

    def disconnect(self):
        self.sock.close()

    def get(self, param_path:str):
        response = self._transaction(RequestMessage(RequestCode.GET, 
                                                    { "param":param_path}))
        return response.args['value']

    def set(self, param_path:str, value:Any):
        response = self._transaction(RequestMessage(RequestCode.SET, 
                                                    { "param":param_path, 
                                                      "value":value}))
        


    def clone(self):
        response = self._transaction(RequestMessage(RequestCode.CLONE))
        self.load(response.args)

    def pull(self):
        args ={}
        for k, v in self.items():
            args[k] = v.get_commit()
        response = self._transaction(RequestMessage(RequestCode.PULL))

    def subscribe(self):
        response = self._transaction(RequestMessage(RequestCode.SUBSCRIBE))
