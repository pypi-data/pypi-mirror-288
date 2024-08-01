# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from suzaku_framework.register_auto.register import RegisterMeta

# global service registry
service_registry = {}
# global model registry
model_registry = {}
# global schema registry
schema_registry = {}

# derector to register service
def register_service(cls):
    return RegisterMeta(service_registry)(cls)

# derector to register model
def register_model(cls):
    return RegisterMeta(model_registry)(cls)

# derector to register schema
def register_schema(cls):
    return RegisterMeta(schema_registry)(cls)