import operator
from abc import ABC, abstractmethod
from typing import List
from lang.context import Context
from lang.type import *



class Node(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.computed_type = None
        
    @abstractmethod
    def evaluate(self, context: Context):
        pass

    def accept(self, visitor):
        method_name = 'visit_{}'.format(self.__class__.__name__.lower())
        visit = getattr(visitor,method_name)
        return visit(self)
    
class Program(Node):
    def __init__(self, statements: List[Node]) -> None:
        self.statements = statements
    def evaluate(self, context: Context):
        for statement in self.statements:
            statement.evaluate(context)


class LsystemDeclaration(Node):
    def __init__(self, name, body_lsys) -> None:
        self.name = name
        self.body = body_lsys
        
    def evaluate(self, context: Context):
        pass
        #child_context: Context = context.make_child()
        #for parameter in self.parameters:
        #    child_context.define(parameter[1], Instance(Type.get(parameter[0]), None))
        #context.define(self.name, LsystemInstance(child_context, self.type, self.parameters, self.body))

class RuleDefinition(Node):
    def __init__(self, right_part, left_part) -> None:
        self.right_part = right_part
        self.left_part = left_part
        
    def evaluate(self, context: Context):
        pass

class LsystemDefinition(Node):
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules

    def evaluate(self, context: Context):
        pass

class VariableAssignment(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class VariableDeclaration(Node):
    def __init__(self, type, name, value) -> None:
        self.type = type
        self.name = name
        self.value = value