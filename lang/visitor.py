from __future__ import annotations

from lang.context import Context
from lang.type import *
class Visitor(object):
    pass

class Eval(Visitor):

    def visit_program(self, program):
        for instruction in program.instructions:
            instruction.accept(Eval())

    def visit_lsystemdeclaration(self, lsystem_declaration):
        print('ssss')

    def visit_axiomdefinition(self, axiom_definition):
        pass

    def visit_rulesdefinition(self, rules_definiton):
        pass

    def visit_lsystemdefinition(self, lsystem_definition):
        pass

    def visit_variableassignment(self, var_assignment):
        variable = Context.resolve(self.name)
        #esto solo pincha si el valor de las variables son tipos puros
        new_value = var_assignment.value
        variable.value = new_value
        print('bbb')

    def visit_variabledeclaration(self, var_declaration):
        #esto solo pincha si el valor de las variables son tipos puros  
        Context.define(var_declaration.name, Instance(Type.get(var_declaration.type), var_declaration.value))
        print('aaaa')