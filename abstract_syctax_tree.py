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
        child_context: Context = context.make_child()
        for parameter in self.parameters:
            child_context.define(parameter[1], Instance(Type.get(parameter[0]), None))
        context.define(self.name, LsystemInstance(child_context, self.type, self.parameters, self.body))