# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

class ParamError(Exception):
    def __init__(self, message: str="Request Param Error"):
        self.message = message

class TokenError(Exception):
    def __init__(self, message: str="Token Error"):
        self.message = message

class NotFound(Exception):
    def __init__(self, message: str="Not Found"):
        self.message = message