from dis import Instruction

from abstract_syctax_tree import LsysBody
from .eval_visitor import Visitor as visitor

class TypeChecker(visitor):
    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        errors = []
        for instruction in program:
            errors.append(instruction.accept(TypeChecker(self.context)))


    