from __future__ import annotations
from curses import window

import logging
import turtle
from matplotlib.style import context

from datetime import datetime
from PIL import Image 

from lang.context import Context
from lang.type import *

from tools import *


class Visitor(object):
    def __init__(self, context) -> None:
        self.context = context

class Eval(Visitor):

    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        for instruction in program.instructions:
            instruction.accept(Eval(self.context))

    def visit_if_statement(self,if_declaration):
        if if_declaration.condition:
            for instruction in if_declaration:
                instruction.acceot(Eval(self.context))

    def visit_binary_comparer(self,left_expr, comparer, roght_expr):
        return             



    def visit_repeatdeclaration(self, repeat_declaration):
        times = repeat_declaration.times_to_repeat
        if repeat_declaration.times_to_repeat.__class__ is str:
            times = self.context.resolve(repeat_declaration.times_to_repeat).value
        else:
            times = repeat_declaration.times_to_repeat
        instructions = repeat_declaration.instructions
        child_context: Context = self.context.make_child()

        for i in range(times):
            print("ESTA ES LA VEZ", i +1, "DEL REPEAT..................................................................................................")
            for instruction in instructions:
                instruction.accept(Eval(self.context))
        print("SE ACABO EL REPEAT....................................................................................................................")        



    def visit_lsystemdeclaration(self, lsystem_declaration):
        self.context.define(lsystem_declaration.name, LsystemInstance(self.context, lsystem_declaration.body)), #self.type))
        #print(self.context.symbols[lsystem_declaration.name].body.l_rules[0].right_part)
        print("ccc")


    def visit_brushdeclaration(self, brush_declaration):
        brush = turtle.Turtle()
        if brush_declaration.body.speed.__class__ is str:
            speed = self.context.resolve(brush_declaration.body.speed).value
        else:
            speed = brush_declaration.body.speed
        if brush_declaration.body.size.__class__ is str:
            size = self.context.resolve(brush_declaration.body.size).value
        else:
            size = brush_declaration.body.size
        self.context.define(brush_declaration.name, BrushInstance(self.context, speed, size, brush_declaration.body.color, brush)), #self.type))
        
       # print(self.context.symbols[brush_declaration.name].body.size)
        print("ddd")

    def visit_canvasdeclaration(self, canvas_declaration):
        canvas = turtle.Screen()
        if canvas_declaration.body.width.__class__ is str:
            width = self.context.resolve(canvas_declaration.body.width).value
        else:
            width = canvas_declaration.body.width
        if canvas_declaration.body.high.__class__ is str:
            high = self.context.resolve(canvas_declaration.body.high).value
        else:
            high = canvas_declaration.body.high
        self.context.define(canvas_declaration.name, CanvasInstance(self.context, canvas_declaration.body.color,width,high, canvas)), #self.type))
        
        #print(self.context.symbols[brush_declaration.name].body.size)
        print("eee")

    def auxiliar(sel, window, lsystem,brush,complexity,forward_value, draw_angle):
        curve = lsystem.axiom.axiom.lower()
        for _ in range(complexity):
            print("Este es el axioma",curve)
            for rule in lsystem.l_rules:
                print(curve)
                print("Estoy probando")
                print()
                print(rule.left,rule.right)
                #print(rule.left)
                curve = curve.replace(rule.left.lower(), rule.right)  
            curve = curve.lower()
        
        for rule in lsystem.l_rules:
                curve = curve.replace(rule.right, "")
                print(curve)
        print(curve)

        stack = []
        meaning_of_plus_and_minus = True
        for c in curve:
            if c == 'f':
                brush.forward(forward_value)
            elif c == 'g':
                brush.penup()
                brush.forward(forward_value)
                brush.pendown()
            elif c == '+': # if meaning_of_plus_and_minus id False that means the meaning of the symbols are turned
                if meaning_of_plus_and_minus:
                    # Turn left by turning angle
                    brush.left(draw_angle)
                else:
                    # the meaning is turned
                    brush.right(draw_angle)
                
            elif c == '-':
                if meaning_of_plus_and_minus:
                    # Turn right by turning angle
                    brush.right(draw_angle)
                else:    
                    brush.left(draw_angle)
                
            elif c == '[':
                # Push current drawing state onto the stack
                pos = brush.position()
                stack.append(pos)
                ang = brush.heading()
                stack.append(ang)

                #brush.push()
            elif c == ']':
                # Pop current drawing state onto the stack
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
            elif c == '#':
                # Increment the line width by line width increment
                brush.pensize(brush.pensize() + 0.5)
            elif c == '!': 
                # Decrement the line width by line width increment
                brush.pensize(brush.pensize() - 0.5)
            elif c == '{':
                # Open a polygon
                c = 9
            elif c == '}':
                # Close a polygon and fill it with fill colour
                d = 9
            elif c == '>':
                # Multiply the line length by the line length scale factor
                forward_value = forward_value * 1.36
            elif c == '<':
                # Divide the line length by the line length scale factor
                forward_value = forward_value / 1.36
            elif c == '&':
                # Swap the meaning of + and -  
                meaning_of_plus_and_minus = not meaning_of_plus_and_minus
            elif c == '%':
                # Decrement turning angle by turning angle increment 
                draw_angle = draw_angle + 10
            elif c =='$':
                # Increment turning angle by turning angle increment
                draw_angle = draw_angle - 10                            




        # date = (datetime.now()).strftime("%d%b%Y-%H%M%S") 
        # fileName = 'posta-' + date
        # brush.getscreen().getcanvas().postscript(file= fileName+'.eps')
        # img = Image.open(fileName + '.eps') 
        # img.save(fileName + '.jpg')  
 
        print("qbola")
        #window.exitonclick()
        
    def visit_draw(self, draw_node):

        window = self.context.resolve(draw_node.canvas).canvas
        lsystem = self.context.resolve(draw_node.lsystem).body
        brush = self.context.resolve(draw_node.brush).brush
        complexity = draw_node.complexity
        forward_value = draw_node.step_size
        draw_angle = draw_node.angle

        self.auxiliar(window,lsystem,brush,complexity,forward_value,draw_angle)

    def visit_draw_id(self, draw_node):
        window = self.context.resolve(draw_node.canvas).canvas
        lsystem = self.context.resolve(draw_node.lsystem).body
        brush = self.context.resolve(draw_node.brush).brush

        if draw_node.complexity.__class__ is str:
            complexity = self.context.resolve(draw_node.complexity).value
        else:
            complexity = draw_node.complexity
        if draw_node.step_size.__class__ is str:
            forward_value = self.context.resolve(draw_node.step_size).value
        else:
            forward_value = draw_node.step_size
        if draw_node.angle.__class__ is str:
            draw_angle = self.context.resolve(draw_node.angle).value
        else: 
            draw_angle = draw_node.angle
        
        self.auxiliar(window,lsystem,brush,complexity,forward_value,draw_angle)


    def visit_add_rule(self,new_rule):
        lsys = self.context.resolve(new_rule.lsys_name)
        lsys.body.l_rules.append(new_rule.rule)
        print('kkk')


    def visit_variableassignment(self, var_assignment):
        variable = self.context.resolve(var_assignment.name)
        #esto solo pincha si el valor de las variables son tipos puros
        variable.value = var_assignment.value
        print('bbb')

    def visit_variabledeclaration(self, var_declaration):
        #esto solo pincha si el valor de las variables son tipos puros  
        self.context.define(var_declaration.name, Instance(Type.get(var_declaration.type), var_declaration.value))
        print('aaaa')

    def visit_if_statement(self, if_statement):
        if not if_statement.condition.__class__ is str:
            if not if_statement.condition.accept(Eval(self.context)):
                return
        elif if_statement.condition=='false':
            return
        child_context: Context = self.context.make_child()
        for line in if_statement.instructions:
            line.accept(Eval(child_context))

    def visit_binarycomparer(self, binary_comparer):
        return Bool_Operations[binary_comparer.comparer](binary_comparer.left_expr,binary_comparer.right_expr)

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