from __future__ import annotations

import logging
from matplotlib.style import context

from sympy import content

from lang.context import Context
from lang.type import *
class Visitor(object):
    def __init__(self, context) -> None:
        self.context = context

class Eval(Visitor):

    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        for instruction in program.instructions:
            instruction.accept(Eval(self.context))

    def visit_lsystemdeclaration(self, lsystem_declaration):
        self.context.define(lsystem_declaration.name, LsystemInstance(self.context, lsystem_declaration.body)), #self.type))
        print("ccc")

    def visit_axiomdefinition(self, axiom_definition):
        pass

    def visit_rulesdefinition(self, rules_definiton):
        pass

    def visit_lsystemdefinition(self, lsystem_definition):
        pass

    def visit_variableassignment(self, var_assignment):
        variable = self.context.resolve(var_assignment.name)
        #esto solo pincha si el valor de las variables son tipos puros
        variable.value = var_assignment
        print('bbb')

    def visit_variabledeclaration(self, var_declaration):
        #esto solo pincha si el valor de las variables son tipos puros  
        self.context.define(var_declaration.name, Instance(Type.get(var_declaration.type), var_declaration.value))
        print('aaaa')

class TypeCollector(Visitor):

    context: Context

    def visit_program(self, program):
        self.context = Context()

        for classDef in program.classes:
            self.visit(classDef)
    
    
    def visit_lsystemdefinition(self, lsystem_definition):
        self.context.create_type(lsystem_definition.name)

class TypeBuilder:
    
    context: Context
    current_type: Type

    def visit_program(self, program):
        for classDef in program.classes:
            self.visit(classDef)

    def visit_lsystemdefinition(self, lsystem_definition):
        self.currentType = self.context.get_type(lsystem_definition.name)
        
        for attrDef in lsystem_definition.attributes:
            self.visit(attrDef)

        for methodDef in lsystem_definition.methods:
            self.visit(methodDef)

class TypeChecker:
    context: Context

    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if node.left.computed_type != node.right.computed_type:
            logging.error("Type mismatch")
            node.computed_type = None
        else:
            node.computed_type = node.left.computed_type