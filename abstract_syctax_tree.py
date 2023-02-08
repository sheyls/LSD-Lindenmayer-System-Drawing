import operator
from abc import ABC, abstractmethod
from typing import List
from lang.context import Context
from lang.type import *
from lang.visitor import *



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

    def check_semantics(self):
        collector = TypeCollector()
        collector.visit(self)
        builder = TypeBuilder(collector.context)
        builder.visit(self)
        checker = TypeChecker(builder.visitor)
        checker.visit(self)


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
        
<<<<<<< HEAD
    def evaluate(self, context: Context):
        pass
        #child_context: Context = context.make_child()
        #for parameter in self.parameters:
        #    child_context.define(parameter[1], Instance(Type.get(parameter[0]), None))
        #context.define(self.name, LsystemInstance(child_context, self.type, self.parameters, self.body))
class LsystemBody(Node):
    def __init__(self, axiom, axiom_prod, rules) -> None:
        self.axiom = axiom
        self.axiom_prod = axiom_prod
        self.rules = rules



        

class RuleDefinition(Node):
    def __init__(self, right_part, left_part, *args) -> None:
        self.right_part = right_part
        self.left_part = left_part
        
    def evaluate(self, context: Context):
        pass
=======
class RulesDefinition(Node):
    def __init__(self, right_part, left_part) -> None:
        self.right = right_part
        self.left = left_part
>>>>>>> dev-sh

class LsystemDefinition(Node):
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules

class VariableAssignment(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class VariableDeclaration(Node):
    def __init__(self, type, name, value) -> None:
        self.type = type
        self.name = name
        self.value = value

class Draw(Node):
    def __init__(self, lsystem, brush, canvas, angle, complexity) -> None:
        self.lsystem = lsystem
        self.brush = brush
        self.canvas = canvas
        self.angle = angle
        self.complexity = complexity