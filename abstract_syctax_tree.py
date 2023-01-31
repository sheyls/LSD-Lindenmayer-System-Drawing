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

    def check_semantics(self, logger):
        collector = TypeCollector()
        collector.visit(self, logger)
        builder = TypeBuilder(collector.context)
        builder.visit(self, logger)
        checker = TypeChecker(builder.visitor)
        checker.visit(self, logger)


class LsystemDeclaration(Node):
    def __init__(self, name, body_lsys) -> None:
        self.name = name
        self.body = body_lsys

class AxiomDefinition(Node):
    def __init__(self, axiom: str):
        self.axiom = axiom
        
class RulesDefinition(Node):
    def __init__(self, right_part, left_part) -> None:
        self.right_part = right_part
        self.left_part = left_part

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