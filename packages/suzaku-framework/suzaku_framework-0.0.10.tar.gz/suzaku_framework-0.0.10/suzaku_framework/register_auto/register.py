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
        # logger.info(f"Registered: {cls.__name__}")
        return cls
    
def print_registered_services(meta_registry: Dict, meta_module: str = None):
    if meta_module:
        logger.info(f'Load {meta_module} Factory...')
    for service_name, service_class in meta_registry.items():
        if meta_module:
            message = f"Registered {meta_module} {service_name} from {service_class.__module__}"
        else:
            message = f"Registered {service_name} from {service_class.__module__}"
        logger.info(message)

# register meta and load
def load_registered_services_from_meta(meta_registry: Dict, meta_class: str, meta_module: str = None):
    # auto load services
    service_files = get_group_file(meta_class)
    
    # auto load and rigister services
    auto_load_from_group(service_files)
    
    # print registered services
    print_registered_services(meta_registry, meta_module)
    
    # service factory
    return  DeSerialize(meta_registry)

def load_registered_services(meta_registry: Dict, meta_module: str = None):
    # print registered services
    print_registered_services(meta_registry, meta_module)
    
    # service factory and return
    return  DeSerialize(meta_registry)