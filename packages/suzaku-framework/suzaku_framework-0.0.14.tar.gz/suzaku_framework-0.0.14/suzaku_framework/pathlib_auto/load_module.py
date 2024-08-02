# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

import sys
import importlib
from pathlib import Path
from typing import Dict, List

def get_group_file(member_name: str ="endpoint.py"):
    data = []
    # current_dir = Path(__file__).parent
    current_dir = Path.cwd()
    for path in current_dir.glob('**/*.py'):
         if path.is_file() and path.name == member_name:
            if 'src' in path.parts:
                src_index = path.parts.index('src')
                src_subpath = path.parts[src_index:]
                object_path = '.'.join(src_subpath)
                data.append(object_path.replace('.py', ''))
    return data

def auto_load_from_group(module_names:List[str]):
    imported_modules = {}
    for module_name in module_names:
        try:
            # 假设模块文件名和模块名相同，只是扩展名为.py
            module_file = module_name.replace('.', '/') + '.py'
            module = import_module_from_string(module_name, module_file)
            imported_modules[module_name] = module
        except ImportError as e:
            print(f"Failed to import module {module_name}: {e}")
    return imported_modules

def import_module_from_string(module_name: str, path: str):
    # 将相对路径转换为绝对路径
    absolute_path = Path(path).resolve()
    
    # 假设每个模块文件都在其自己的目录中，目录名即为模块名
    module_path = absolute_path.parent.__str__().replace('\\', '/')
    
    # 将模块路径添加到sys.path中
    sys.path.append(module_path)
    
    try:
        # 动态导入模块
        module = importlib.import_module(module_name)
        return module
    finally:
        # 导入完成后，从sys.path中移除模块路径
        sys.path.remove(module_path)
