from __future__ import annotations

from typing import Dict, List

from lang.context import Context


class Type:
    types = {}

    def __init__(self, name: str):
        self.name = name
        self.attributes: Dict[str, Attribute] = {}
        self.methods: Dict[str, Method] = {}
        Type.types[name] = self
        
    @staticmethod
    def get(type_name: str):
        if type_name not in Type.types.keys():
            raise KeyError(f"'{type_name}' not found in PFQL types.")
        return Type.types[type_name]
        
    def get_attribute(self, name: str) -> Attribute:
        if name not in self.attributes.keys():
            return None
        return self.attributes[name]

    def get_method(self, name: str) -> Method:
        if name not in self.methods.keys():
            return None
        return self.methods[name]
    
    def define_attribute(self, name: str, type: Type) -> bool:
        if name in self.attributes.keys():
            return False        
        self.attributes[name] = Attribute(name, type)
        return True
        
    def define_method(self, name: str, return_type: Type, args: List[str], arg_types: List[Type]) -> bool:
        if name in self.methods.keys() or len(args) != len(arg_types):
            return False
        attributes = [Attribute(args[i], arg_types[i]) for i in range(len(args))]
        self.methods[name] = Method(name, return_type, attributes)
        return True
    
    def __str__(self) -> str:
        return self.name

class Attribute:
    def __init__(self, name: str, type: Type) -> None:
        self.name = name
        self.type = type


class Method:
    def __init__(self, name: str, return_type: Type, args: List[Attribute]) -> None:
        self.name = name
        self.return_type = return_type
        self.args = args

class Instance:
    def __init__(self, type: Type, value):
        self.type = type
        self.value = value
        
class LsystemInstance:
    def __init__(self, context: Context, body) -> None:
        self.context = context
        self.body = body