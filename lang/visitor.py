#from __future__ import annotations

import logging

from lang.context import Context
from lang.type import *
class Visitor(object):
    pass

class Eval(Visitor):

    def visit_program(self, program, context):
        for instruction in program.instructions:
            instruction.accept(Eval(context))

    def visit_lsystemdeclaration(self, lsystem_declaration,context):
        print('ssss')

    def visit_axiomdefinition(self, axiom_definition,context):
        pass

    def visit_rulesdefinition(self, rules_definiton,context):
        pass

    def visit_lsystemdefinition(self, lsystem_definition,context):
        pass

    def visit_variableassignment(self, var_assignment,context):
        variable = context.resolve(self.name)
        #esto solo pincha si el valor de las variables son tipos puros
        #context.define(variable.name,var_assignment)
        new_value = var_assignment.value
        variable.value = new_value
        print('bbb')

    def visit_variabledeclaration(self, var_declaration,context):
        #esto solo pincha si el valor de las variables son tipos puros  
        context.define(self.name, var_declaration.value)
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