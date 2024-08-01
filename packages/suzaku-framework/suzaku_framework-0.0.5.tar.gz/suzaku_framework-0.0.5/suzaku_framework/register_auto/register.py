# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from typing import Dict
from loguru import logger
from suzaku_framework.pathlib_auto.load_module import auto_load_from_group, get_group_file

# dict to object
class DeSerialize:
    def __init__(self, serialized_dict: Dict):
        self._serialized_dict = serialized_dict

    def __getattr__(self, name):
        if name in self._serialized_dict:
            return self._serialized_dict[name]
        raise AttributeError(f"Serialized dict'{name}' not found.")
    
class RegisterMeta:
    def __init__(self, meta_registry: Dict):
        self.meta_registry = meta_registry

    def __call__(self, cls):
        self.meta_registry[cls.__name__] = cls
        logger.info(f"Registered service: {cls.__name__}")
        return cls
    
def print_registered_services(meta_registry: Dict):
    for service_name, service_class in meta_registry.items():
        logger.info(f"Registered {service_name} from {service_class.__module__}")
        
def load_registered_services(meta_registry: Dict, meta_class: str):
    # auto load services
    service_files = get_group_file(meta_class)
    
    # auto load and rigister services
    services = auto_load_from_group(service_files)
    
    # print registered services
    print_registered_services(meta_registry)
    
    # service factory
    return  DeSerialize(meta_registry)
    
    
    
    
    
    
    