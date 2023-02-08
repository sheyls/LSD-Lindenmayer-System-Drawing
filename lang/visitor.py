from __future__ import annotations
from curses import window

import logging
import turtle
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
        #print(self.context.symbols[lsystem_declaration.name].body.l_rules[0].right_part)
        print("ccc")


    def visit_brushdeclaration(self, brush_declaration):
        brush = turtle.Turtle()
        self.context.define(brush_declaration.name, BrushInstance(self.context, brush_declaration.body, brush)), #self.type))
        
       # print(self.context.symbols[brush_declaration.name].body.size)
        print("ddd")

    def visit_canvasdeclaration(self, canvas_declaration):
        canvas = turtle.Screen()
        self.context.define(canvas_declaration.name, CanvasInstance(self.context, canvas_declaration.body, canvas)), #self.type))
        
        #print(self.context.symbols[brush_declaration.name].body.size)
        print("eee")

    def visit_draw(self, draw_node):

        window = self.context.resolve(draw_node.canvas).canvas
        lsystem = self.context.resolve(draw_node.lsystem).body
        brush = self.context.resolve(draw_node.brush).brush

        curve = lsystem.axiom.axiom.lower()
        for _ in range(draw_node.complexity):
            print(curve)
            for rule in lsystem.l_rules:
                print(curve)
                print(rule.right)
                print(rule.left)
                curve = curve.replace(rule.left.lower(), rule.right)  
            curve = curve.lower()
        
        for rule in lsystem.l_rules:
                curve = curve.replace(rule.right, "")
                print(curve)
        print(curve)

        stack = []
        for c in curve:
            if c == 'f':
                brush.forward(5)
            elif c == 'g':
                brush.penup()
                brush.forward(5)
                brush.pendown()
            elif c == '+':
                brush.left(draw_node.angle)
            elif c == '-':
                brush.right(draw_node.angle)
            elif c == '[':
                pos = brush.position()
                stack.append(pos)
                ang = brush.heading()
                stack.append(ang)

                #brush.push()
            elif c == ']':
                #brush.penup()
                ang = stack.pop()
                pos = stack.pop()
                brush.up()
                brush.setheading(ang)
                brush.goto(pos)
                brush.down()
                #brush.setpos(stack[-1])
                #brush.pendown()
                #brush.pop()


        print("qbola")
        window.exitonclick()

    def visit_variableassignment(self, var_assignment):
        variable = self.context.resolve(var_assignment.name)
        #esto solo pincha si el valor de las variables son tipos puros
        variable.value = var_assignment
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