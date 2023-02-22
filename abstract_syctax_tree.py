from abc import ABC, abstractmethod
from typing import List
from lang.context import Context
from lang.type import *
from lang.eval_visitor import *
from tools import *

class Node(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.computed_type = None

    def accept(self, visitor):
        method_name = 'visit_{}'.format(self.__class__.__name__.lower())
        visit = getattr(visitor,method_name)
        return visit(self)
    
class Program(Node):
    def __init__(self, instructions: List[Node]) -> None:
        self.instructions = instructions

class ArithmeticOp(Node):
    def __init__(self, left, operator, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right
class LsystemDeclaration(Node):
    def __init__(self, name, body_lsys) -> None:
        self.name = name
        self.body = body_lsys

class BrushDeclaration(Node):
    def __init__(self, name, body_brush) -> None:
        self.name = name
        self.body = body_brush

class BrushBody(Node):
    def __init__(self, size, color, speed) -> None:
        self.size = size
        self.color = color
        self.speed = speed

class CanvasDeclaration(Node):
    def __init__(self, name, body_canvas) -> None:
        self.name = name
        self.body = body_canvas

class CanvasBody(Node):
    def __init__(self, high, width, color) -> None:
        self.high = high
        self.width = width
        self.color = color

class LsysBody(Node):
    def __init__(self, axiom, l_rules) -> None:
        self.axiom = axiom
        self.l_rules = l_rules

class AxiomDefinition(Node):
    def __init__(self, axiom: str):
        self.axiom = axiom
        
class RulesDefinition(Node):
    def __init__(self, right_part, left_part) -> None:
        self.right = right_part
        self.left = left_part

class LsystemDefinition(Node):
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules

class VariableAssignment(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class Add_rule(Node):
    def __init__(self, lsys_name, rule) -> None:
        self.lsys_name = lsys_name
        self.rule = rule
class Change_axiom(Node):
    def __init__(self, lsys_name, axiom) -> None:
        self.lsys_name = lsys_name
        self.axiom = axiom

class VariableDeclaration(Node):
    def __init__(self, type, name, value) -> None:
        self.type = type
        self.name = name
        self.value = value

class RepeatDeclaration(Node):
    def __init__(self, times_to_repeat, instructions ) -> None:
        self.times_to_repeat = times_to_repeat
        self.instructions = instructions 

class Repeat_Body(Node):
    def __init__(self, instructions) -> None:
        self.instructions = instructions

class If_Statement(Node):
    def __init__(self,condition, instructions) -> None:
        self.condition = condition
        self.instructions = instructions

class If_Else_Statement(Node):
    def __init__(self,condition, instructions_true, instructions_false) -> None:
        self.condition = condition
        self.instructions_true = instructions_true
        self.instructions_false = instructions_false

class BinaryComparer(Node):
    def __init__(self, left_expr, comparer, right_expr) -> None:
        self.left_expr = left_expr
        self.comparer = comparer
        self.right_expr = right_expr        

class Draw(Node):
    def __init__(self, lsystem, brush, canvas, step_size, angle, complexity) -> None:
        self.lsystem = lsystem
        self.brush = brush
        self.canvas = canvas
        self.step_size = step_size
        self.angle = angle
        self.complexity = complexity

class Assignable(Node):
    def __init__(self,value,type):
        self.value = value
        self.type = Type.get(type.lower())