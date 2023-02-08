from __future__ import annotations

from typing import Dict, List

from lang.context import Context

import turtle


class Type:
    types = {}

    def __init__(self, name: str):
        self.name = name
        self.attributes: Dict[str, Attribute] = {}
        Type.types[name] = self
        
    @staticmethod
    def get(type_name: str):
        if type_name not in Type.types.keys():
            raise KeyError(f"'{type_name}' type not found ")
        return Type.types[type_name]
        
    def get_attribute(self, name: str) -> Attribute:
        if name not in self.attributes.keys():
            return None
        return self.attributes[name]
    
    def define_attribute(self, name: str, type: Type) -> bool:
        if name in self.attributes.keys():
            return False        
        self.attributes[name] = Attribute(name, type)
        return True
    
    def __str__(self) -> str:
        return self.name

class Attribute:
    def __init__(self, name: str, type: Type) -> None:
        self.name = name
        self.type = type


class Instance:
    def __init__(self, type: Type, value):
        self.type = type
        self.value = value
        
class LsystemInstance:
    def __init__(self, context: Context, body) -> None:
        self.context = context
        #self.type = type lsystem
        self.body = body

class BrushInstance:
    def __init__(self, context: Context, body, brush) -> None:
        self.context = context

        brush.speed(body.speed)
        brush.pensize(body.size)
        brush.color(body.color)
        brush.left(90)
        brush.hideturtle()
    
        self.brush = brush

class CanvasInstance:
    def __init__(self, context: Context, body, canvas) -> None:
        self.context = context

        canvas.bgcolor(body.color)
        canvas.screensize(body.width, body.high)
        
        self.canvas = canvas

        

#Internal types
_lsystem = Type('lsystem')
_int = Type('_int')
_string = Type('string')
_brush = Type('brush')
_canvas = Type('canvas')
_color = Type('color')
_angle = Type('angle')
