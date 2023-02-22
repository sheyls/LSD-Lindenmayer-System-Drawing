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
from abstract_syctax_tree import *

class Visitor(object):
    def __init__(self, context) -> None:
        self.context = context

class Eval(Visitor):

    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        for instruction in program.instructions:
            instruction.accept(Eval(self.context))

    def visit_assignable(self, assignable):
        return assignable.value

    def visit_arithmeticop(self, arithmetic_node):
        if arithmetic_node.left.__class__ is str:
            left = self.context.resolve(arithmetic_node.left).value
        else:
            left = arithmetic_node.left.accept(Eval(self.context))

        if  arithmetic_node.right.__class__ is str:
            right = self.context.resolve(arithmetic_node.right).value
        else:
            right = arithmetic_node.right.accept(Eval(self.context))
        return Operator[arithmetic_node.operator](left, right)

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
                instruction.accept(Eval(child_context))
        print("SE ACABO EL REPEAT....................................................................................................................")        



    def visit_lsystemdeclaration(self, lsystem_declaration):
        variable = self.context.resolve(lsystem_declaration.name)
        if variable == None:
            self.context.define(lsystem_declaration.name, LsystemInstance(self.context, lsystem_declaration.body)), #self.type))
        else:
            self.context.define(variable, LsystemInstance(self.context, lsystem_declaration.body)), #self.type))

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
        if brush_declaration.body.color.__class__ is str:
            color = self.context.resolve(brush_declaration.body.color).value
        else:
            color = brush_declaration.body.color
        self.context.define(brush_declaration.name, BrushInstance(self.context, speed = speed,size= size,color=color,brush= brush)), #self.type))
        
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
        if canvas_declaration.body.color.__class__ is str:
            color = self.context.resolve(canvas_declaration.body.color).value
        else:
            color = canvas_declaration.body.color
        self.context.define(canvas_declaration.name, CanvasInstance(self.context, color,width,high, canvas)), #self.type))
        
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
                # Push current drawing state into the stack
                pos = brush.position()
                stack.append(pos)
                ang = brush.heading()
                stack.append(ang)

                #brush.push()
            elif c == ']':
                # Pop current drawing state into the stack
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
                #  Increment turning angle by turning angle increment 
                draw_angle = draw_angle + 10
            elif c =='$':
                # Decrement turning angle by turning angle increment
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


    def visit_add_rule(self, new_rule):
        lsys = self.context.resolve(new_rule.lsys_name)
        lsys.body.l_rules.append(new_rule.rule)
        print('kkk')

    def visit_change_axiom(self, new_axiom):
        lsys = self.context.resolve(new_axiom.lsys_name)
        lsys.body.axiom = new_axiom.axiom
        print('popopo')


    def visit_variableassignment(self, var_assignment):
        variable = self.context.resolve(var_assignment.name)
        #esto solo pincha si el valor de las variables son tipos puros
        variable.value = var_assignment.value.accept(Eval(self.context))
        print('bbb')

    def visit_variabledeclaration(self, var_declaration):
        #esto solo pincha si el valor de las variables son tipos puros  
        self.context.define(var_declaration.name, Instance(Type.get(var_declaration.type), var_declaration.value.accept(Eval(self.context))))
        print('aaaa')

    def visit_if_statement(self, if_statement):
        if not if_statement.condition.__class__ is str:
            if not if_statement.condition.accept(Eval(self.context)):
                return
        elif if_statement.condition=='false':
            return
        else:
            cond = self.context.resolve(if_statement.condition).value
            if cond == 'false':
                return
        child_context: Context = self.context.make_child()
        for line in if_statement.instructions:
            line.accept(Eval(child_context))
    


    def visit_if_else_statement(self, if_statement):
        child_context: Context = self.context.make_child()

        if not if_statement.condition.__class__ is str:
            if not if_statement.condition.accept(Eval(self.context)):
                for line in if_statement.instructions_false:
                    line.accept(Eval(child_context))
                return

        elif if_statement.condition=='false':
            for line in if_statement.instructions_false:
                line.accept(Eval(child_context))
            return

        for line in if_statement.instructions_true:
            line.accept(Eval(child_context))

    def visit_binarycomparer(self, binary_comparer):
        left = binary_comparer.left_expr
        
        if left.__class__ is str:
            left = self.context.resolve(left).value
        else: 
            left = left.accept(Eval(self.context))
        
        right = binary_comparer.right_expr
        if right.__class__ is str:
            right = self.context.resolve(right).value
        else:
            right = right.accept(Eval(self.context))
        return Bool_Operator[binary_comparer.comparer](left, right)


class SemanticChecker(Visitor):

    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        for instruction in program.instructions:
            instruction.accept(SemanticChecker(self.context))
    
    
    def visit_lsystemdefinition(self, lsystem_definition):
        lsystem = self.context.resolve(lsystem_definition.name)
        if lsystem: 
            raise Exception(f"Defined lsystem '{lsystem_definition.name}'.")
        
        self.context.define(lsystem_definition.name,LsystemInstance)
        
        lsystem_definition.computed_type = self.context.symbols[lsystem_definition.name]

    def visit_lsystemdeclaration(self,lsystem_declaration):
        lsystem = self.context.resolve(lsystem_declaration.name)
        if lsystem: 
            raise Exception(f"Defined lsystem '{lsystem_declaration.name}'.")
        
        axiom = lsystem_declaration.body.axiom.axiom
        rules = lsystem_declaration.body.l_rules

        contain = False
        for i in range(len(axiom)):
            for rule in rules:
                if axiom[i] == rule.left:
                    contain = True 
        if not contain:
            raise Exception(f"Wrong definition of lsystem '{lsystem_declaration.name}'.")

        self.context.define(lsystem_declaration.name,LsystemInstance)
        lsystem_declaration.computed_type = self.context.symbols[lsystem_declaration.name]
        
    def visit_if_statement(self,if_declaration):
        if isinstance(if_declaration.condition, BinaryComparer):
            if_declaration.condition.accept(SemanticChecker(self.context))
            if if_declaration.condition.computed_type is not Type.get('bool'):
                raise Exception(f"Given condition is not boolean.")
 
        child_context: Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)
        
        if_declaration.computed_type= Type.get('void')
        
        for line in if_declaration.instructions:
            line.accept(child_semantic_checker)
    
    def visit_repeatdeclaration(self, repeat_declaration):
        if isinstance(repeat_declaration.times_to_repeat,str):
            _type = self.context.resolve(repeat_declaration.times_to_repeat)
            if _type.name != '_int':
                raise Exception(f"Given condition is not _int.")
        
        repeat_declaration.computed_type = Type.get('void')
       
        child_context: Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)
       
        for line in repeat_declaration.instructions:
          line.accept(child_semantic_checker)
            
    
    def visit_brushdeclaration(self, brush_declaration):
        brush = self.context.resolve(brush_declaration.name)
        if brush: 
            raise Exception(f"Defined brush '{brush_declaration.name}'.")

        if brush_declaration.body.speed.__class__ is str:
            try:
                speed_type = self.context.resolve(brush_declaration.body.speed).name
                if speed_type != '_int':
                    raise Exception(f"Expected type _int for speed.")
            except:
                raise Exception(f"Variable '{brush_declaration.body.speed}' not defined.")

        if brush_declaration.body.size.__class__ is str:
            try:
                size_type = self.context.resolve(brush_declaration.body.size).name
                if size_type != '_int':
                    raise Exception(f"Expected type _int for size.")
            except:
                raise Exception(f"Variable '{brush_declaration.body.size}' not defined.")


        self.context.define(brush_declaration.name,BrushInstance)
        brush_declaration.computed_type = self.context.symbols[brush_declaration.name]

    def visit_canvasdeclaration(self, canvas_declaration):
        canvas = self.context.resolve(canvas_declaration.name)
        if canvas: 
            raise Exception(f"Defined lsystem '{canvas_declaration.name}'.")
        
        if canvas_declaration.body.high.__class__ is str:
            try :
                high_type = self.context.resolve(canvas_declaration.body.high).name
                if high_type != 'int':
                    raise Exception(f"Expected type int for high.")
            except:
                raise Exception(f"Variable '{canvas_declaration.body.high}' not defined.")

        if canvas_declaration.body.width.__class__ is str:
            try:
                width_type = self.context.resolve(canvas_declaration.body.width).name
                if width_type != 'int':
                    raise Exception(f"Expected type int for width.")
            except:
                raise Exception(f"Variable '{canvas_declaration.body.width}' not defined.")

        self.context.define(canvas_declaration.name,CanvasInstance)
        canvas_declaration.computed_type = self.context.symbols[canvas_declaration.name]

    def visit_draw(self, draw_node):
        try:
            lsystem_type = self.context.resolve(draw_node.lsystem)
            if lsystem_type is not LsystemInstance:
                raise Exception(f"Expected type lsys.")
        except:
                raise Exception(f"Variable '{draw_node.lsystem}' not defined.")
        
        try:
            brush_type = self.context.resolve(draw_node.brush)
            if brush_type is not BrushInstance:
                raise Exception(f"Expected type brush.")
        except:
            raise Exception(f"Variable'{draw_node.brush}' not defined.")

        try:
            canvas_type = self.context.resolve(draw_node.canvas)
            if canvas_type is not CanvasInstance:
                raise Exception(f"Expected type canvas")
        except:
            raise Exception(f"Variable'{draw_node.canvas}' not defined.")
        
        #esto hay que pensarlo mejor
        draw_node.computed_type = Type('void')


    def visit_draw_id(self, draw_node):
        try:
            lsystem_type = self.context.resolve(draw_node.lsystem)
            if lsystem_type is not LsystemInstance:
                raise Exception(f"Expected type lsys.")
        except:
                raise Exception(f"Variable '{draw_node.lsystem}' not defined.")
        
        try:
            brush_type = self.context.resolve(draw_node.brush)
            if brush_type is not BrushInstance:
                raise Exception(f"Expected type brush.")
        except:
            raise Exception(f"Variable'{draw_node.brush}' not defined.")

        try:
            canvas_type = self.context.resolve(draw_node.canvas)
            if canvas_type is not CanvasInstance:
                raise Exception(f"Expected type canvas")
        except:
            raise Exception(f"Variable'{draw_node.canvas}' not defined.")
        

        if draw_node.step_size.__class__ is str:
            try:
                size_type = self.context.resolve(draw_node.step_size).name
                if size_type != 'int':
                    raise Exception(f"Expected type _int for size.")
            except:
                raise Exception(f"Variable '{draw_node.step_size}' not defined.")

        if draw_node.angle.__class__ is str:
            try:
                angle_type = self.context.resolve(draw_node.angle).name
                if angle_type != 'float':
                    raise Exception(f"Expected type float for angle.")
            except:
                raise Exception(f"Variable '{draw_node.angle}' not defined.")

        if draw_node.complexity.__class__ is str:
            try:
                complexity_type = self.context.resolve(draw_node.complexity).name
                if complexity_type != 'int':
                    raise Exception(f"Expected type int for complexity.")
            except:
                raise Exception(f"Variable '{draw_node.complexity}' not defined.")

        #esto hay que pensarlo mejor
        draw_node.computed_type = Type('void')

    def visit_add_rule(self,new_rule):
        lsys = self.context.resolve(new_rule.lsys_name)
        if lsys is None:
            raise Exception(f"Lsystem '{new_rule.lsys_name}' not defined.")

        #esto hay que pensarlo mejor
        new_rule.computed_type = Type('void')

    
    def visit_variableassignment(self, var_assignment):
        var_assignment.value.accept(SemanticChecker(self.context))
        var_type = self.context.resolve(var_assignment.name)
        if var_type is None:
            raise Exception(f"Variable '{var_assignment.name}' not defined.")
        if var_type.name != var_assignment.value.computed_type:
            raise Exception(f"Can't assign value {var_assignment.value} to variable '{var_assignment.name}'. Type '{var_type}' different to '{var_assignment.value.computed_type}'.")
        var_assignment.computed_type = var_type

    def visit_variabledeclaration(self, var_declaration):
        var_type = Type.get(var_declaration.type)
        var_declaration.value.accept(SemanticChecker(self.context))

        if var_declaration.name in self.context.symbols.keys():
            raise Exception(f"Defined variable '{var_declaration.name}'.")
        else:
            self.context.define(var_declaration.name, var_type)
        if var_declaration.value.computed_type != var_type.name:
            raise Exception(f"{var_declaration.value.type} not expected.")
        
        var_declaration.computed_type = var_type
        
    def visit_assignable(self, assignable):
        assignable.computed_type = assignable.type

    def visit_binarycomparer(self, binary_comparer):
        binary_comparer.left_expr.accept(SemanticChecker(self.context))
        binary_comparer.right_expr.accept(SemanticChecker(self.context))
        
        if binary_comparer.left_expr.computed_type == Type.get('void') or binary_comparer.right_expr.computed_type == Type.get('void'):
            raise Exception(f"{'void'} expression not admissible for comparison.")
        
        if binary_comparer.left_expr.computed_type != binary_comparer.right_expr.computed_type:
            raise Exception("Expressions to compare must be the same type.")
        
        if binary_comparer.comparer in ['>', '<', '>=', '<='] and binary_comparer.left_expr.computed_type is not Type.get('_int'):
            raise Exception(f"Invalid expression type for '{binary_comparer.comparer}' comparer.")
        
        binary_comparer.computed_type = Type.get('bool')
