#!/usr/bin/env python
__author__      = "Olman Quiros Jimenez"
__copyright__   = "Copyright 2024"
__license__     = "MIT"


from .protocol_message import RequestMessage, RequestCode



class CloneRequest(RequestMessage):
    '''
    Clone Request

    Get all Collections and Params from a Node
    '''
    def __init__(self) -> 'CloneRequest':
        super().__init__(RequestCode.CLONE)



class PullRequest(RequestMessage):
    '''
    Pull Request

    Synchronizes Collections of Remote Node given a commit hash.
    '''
    def __init__(self, commit_hash:str) -> 'CloneRequest':
        super().__init__(RequestCode.PULL)




class SubscribeRequest(RequestMessage):
    '''
    Subscribe Request

    Subscribes to a topic from a Remote Node.
    '''
    def __init__(self, topic:str) -> 'CloneRequest':
        super().__init__(RequestCode.SUBSCRIBE)
