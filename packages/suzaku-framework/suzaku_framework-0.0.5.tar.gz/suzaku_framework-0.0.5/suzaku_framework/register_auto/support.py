# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from suzaku_framework.register_auto.register import RegisterMeta

# global service registry
service_registry = {}

# derector to register service
def register_service(cls):
    return RegisterMeta(service_registry)(cls)