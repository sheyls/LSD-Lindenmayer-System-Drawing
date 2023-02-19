from __future__ import annotations
from curses import window
from distutils.log import error

import logging
import turtle
from matplotlib.style import context

from datetime import datetime
from PIL import Image
from numpy import False_ 

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

    def visit_repeatdeclaration(self, repeat_declaration):
        times = repeat_declaration.times_to_repeat
        if repeat_declaration.times_to_repeat.__class__ is str:
            times = self.context.resolve(repeat_declaration.times_to_repeat).value.value
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
        self.context.define(lsystem_declaration.name, LsystemInstance(self.context, lsystem_declaration.body)), #self.type))
        #print(self.context.symbols[lsystem_declaration.name].body.l_rules[0].right_part)
        print("ccc")


    def visit_brushdeclaration(self, brush_declaration):
        brush = turtle.Turtle()
        if brush_declaration.body.speed.__class__ is str:
            speed = self.context.resolve(brush_declaration.body.speed).value.value
        else:
            speed = brush_declaration.body.speed
        if brush_declaration.body.size.__class__ is str:
            size = self.context.resolve(brush_declaration.body.size).value.value
        else:
            size = brush_declaration.body.size
        self.context.define(brush_declaration.name, BrushInstance(self.context, speed = speed,size= size,color= brush_declaration.body.color,brush= brush)), #self.type))
        
       # print(self.context.symbols[brush_declaration.name].body.size)
        print("ddd")

    def visit_canvasdeclaration(self, canvas_declaration):
        canvas = turtle.Screen()
        if canvas_declaration.body.width.__class__ is str:
            width = self.context.resolve(canvas_declaration.body.width).value.value
        else:
            width = canvas_declaration.body.width
        if canvas_declaration.body.high.__class__ is str:
            high = self.context.resolve(canvas_declaration.body.high).value.value
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
            complexity = self.context.resolve(draw_node.complexity).value.value
        else:
            complexity = draw_node.complexity
        if draw_node.step_size.__class__ is str:
            forward_value = self.context.resolve(draw_node.step_size).value.value
        else:
            forward_value = draw_node.step_size
        if draw_node.angle.__class__ is str:
            draw_angle = self.context.resolve(draw_node.angle).value.value
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
        return Bool_Operations[binary_comparer.comparer](binary_comparer.left_expr.value,binary_comparer.right_expr.value)


        
class SemanticChecker(Visitor):

    def __init__(self, context) -> None:
        super().__init__(context)

    def visit_program(self, program):
        errors = []
        for instruction in program.instructions:
            errors += instruction.accept(SemanticChecker(self.context))
        return errors


    # Lsystems
    def visit_lsystemdeclaration(self, lsystem_declaration):
        # name, body
        errors = []
        lsystem = self.context.resolve(lsystem_declaration.name)
        if lsystem:
            errors += (f"Defined lsystem '{lsystem_declaration.name}'.")

        self.context.define(lsystem_declaration.name, LsystemInstance(self.context,lsystem_declaration.body)) # ver si esto esta bien
        lsystem_declaration.type = self.context.symbols[lsystem_declaration.name]

        lsysbody = lsystem_declaration.body
        errors += lsysbody.accept(SemanticChecker(self.context))
        return errors

    def visit_lsysbody(self, lsystem_definition) : # LsysBody es el nodo que se esta usando en el AST , no LsystemDefinition
        # axiom, rules
        errors = []
        axiom = lsystem_definition.axiom.axiom # el primero devuelve un Axiomdefinition
        rules = lsystem_definition.l_rules

        contain = False
        for i in range(len(axiom)):
            for rule in rules:
                if axiom[i] == rule.left:
                    contain = True 
        if not contain:
            errors += (f"Wrong definition of lsystem '{lsystem_definition}'.") # ver como accedo al nombre

        return errors                

    def visit_canvasdeclaration(self, canvas_declaration):
        # name, body
        errors = []
        canvas = self.context.resolve(canvas_declaration.name)

        if canvas:
            errors += (f"Defined canvas '{canvas_declaration.name}'.")

        body = canvas_declaration.body    

        high = body.high
        width = body.width
        color = body.high    

        self.context.define(canvas_declaration.name, CanvasInstance(self.context,color,width,high))  
        canvas_declaration.computed_type = self.context.symbols[canvas_declaration.name]

        errors += body.accept(SemanticChecker(self.context))
        return errors

    def visit_canvasbody(self, canvas_body):
        errors = []
        high = canvas_body.high
        width = canvas_body.width
        color = canvas_body.color

        if high.__class__ is str:
            high_type = self.context.resolve(high).name
            if high_type != None : # revisar esto
                if high_type != '_int':
                    errors += (f"Expected type _int for high.")
            else: errors += (f"Variable '{high}' not defined.")

        if width.__class__ is str:
            width_type = self.context.resolve(width).name
            if width_type != None : # revisar esto
                if width_type != '_int':
                    errors += (f"Expected type _int for width.")
            else: errors += (f"Variable '{width}' not defined.")

        # El color no se pone ???

        return errors



    def visit_brushdeclaration(self,brush_declaration):
        # name, body
        errors = []
        brush = self.context.resolve(brush_declaration.name)
        if brush: 
            errors += (f"Defined brush '{brush_declaration.name}'.")

        brush_body = brush_declaration.body
        size = brush_body.size
        color = brush_body.color
        speed = brush_body.speed    

        self.context.define(brush_declaration.name, BrushInstance(self.context,speed,size,color,brush))    
        brush_declaration.type = self.context.symbols[brush_declaration.name]

        errors += brush_body.accept(SemanticChecker(self.context)) 
        return errors

    def visit_brushbody(self, brush_body):
        # size, color, spped    
        errors = []
        size = brush_body.size
        speed = brush_body.speed
        color = brush_body.color 

        if size.__class__ is str:
            size_type = self.context.resolve(size).name
            if size_type != None : # revisar esto
                if size_type != '_int':
                    errors += (f"Expected type _int for size.")
            else: errors += (f"Variable '{size}' not defined.")

        if speed.__class__ is str:
            speed_type = self.context.resolve(speed).name
            if speed_type != None : # revisar esto
                if speed_type != '_int':
                    errors += (f"Expected type _int for speed.")
            else: errors += (f"Variable '{speed}' not defined.")

        return errors    

    def visit_draw(self, draw_node): # ver si aqui hay que mandar a revisar todo de nuevo
        # lsystem, brush, canvas, step_size, angle,complexity

        errors = []

        lsystem_type = self.context.resolve(draw_node.lsystem)
        if lsystem_type is not LsystemInstance:
            errors += (f"Expected type lsys.")
        else:
            errors += (f"Variable '{draw_node.lsystem}' not defined.")

        brush_type = self.context.resolve(draw_node.brush)
        if brush_type is not BrushInstance:
            errors += (f"Expected type brush.")
        else : 
            errors += (f"Variable'{draw_node.brush}' not defined.")  

        canvas_type = self.context.resolve(draw_node.canvas)
        if canvas_type is not CanvasInstance:
            errors += (f"Expected type canvas")
        else :
            errors += (f"Variable'{draw_node.canvas}' not defined.") 

        if draw_node.step_size.__class__ is str :
            size_type = self.context.resolve(draw_node.step_size).name
            if size_type != '_int':
                errors += (f"Expected type _int for size.")
            else:
                errors += (f"Variable '{draw_node.step_size}' not defined.")    

        if draw_node.angle.__class__ is str :
            size_type = self.context.resolve(draw_node.angle).name
            if size_type != '_int':
                errors += (f"Expected type _int for angle.")
            else:
                errors += (f"Variable '{draw_node.angle}' not defined.")  

        if draw_node.complexity.__class__ is str :
            size_type = self.context.resolve(draw_node.complexity).name
            if size_type != '_int':
                errors += (f"Expected type _int for complexity.")
            else:
                errors += (f"Variable '{draw_node.complexity}' not defined.")                    
                

        draw_node.computed_type = Type('void')             
        return errors

    def visit_add_rule(self, new_rule):
        # lsys_name, rule    
        errors = []
        lsys = self.context.resolve(new_rule.lsys_name)
        if lsys is None:
            errors += (f"Lsystem '{new_rule.lsys_name}' not defined.")
        
        new_rule.computed_type = Type('void')
        return errors

    def visit_variableassignment(self, var_assignment):
        # name, value
        errors = []
        errors += var_assignment.value.accept(SemanticChecker(self.context))
        var_type = self.context.resolve(var_assignment.name)
        if var_type is None:
            errors += (f"Variable '{var_assignment.name}' not defined.")
        else :
            if var_type.name != var_assignment.value.computed_type:
                errors += (f"Can't assign value {var_assignment.value} to variable '{var_assignment.name}'. Type '{var_type}' different to '{var_assignment.value.computed_type}'.")   

        var_assignment.computed_type = var_type  
        return errors       

    def visit_variabledeclaration(self, var_declaration):
        # type, name , value
        errors = []
        var_type = Type.get(var_declaration.type)
        errors += var_declaration.value.accept(SemanticChecker(self.context)) # ver si esta hecho el visit para esto y si esto sotve pa algo

        if var_declaration.name in self.context.symbols.keys():
            errors += (f"Defined variable '{var_declaration.name}'.")
        else:
            self.context.define(var_declaration.name, var_type)
        if var_declaration.value.computed_type != var_type.name:
            errors += (f"{var_declaration.value.type} not expected.")
                    
        var_declaration.computed_type = var_type
        return errors 

    def visit_assignable(self, assignable):
        assignable.computed_type = assignable.type


    def visit_binarycomparer(self, binary_comparer):
        errors += []
        errors += binary_comparer.left_expr.accept(SemanticChecker(self.context))
        errors += binary_comparer.right_expr.accept(SemanticChecker(self.context))
        
        if binary_comparer.left_expr.computed_type == Type.get('void') or binary_comparer.right_expr.computed_type == Type.get('void'):
            errors += (f"{'void'} expression not admissible for comparison.")
        
        if binary_comparer.left_expr.computed_type != binary_comparer.right_expr.computed_type:
            errors += ("Expressions to compare must be the same type.")
        
        if binary_comparer.comparer in ['>', '<', '>=', '<='] and binary_comparer.left_expr.computed_type is not Type.get('_int'):
            errors += (f"Invalid expression type for '{binary_comparer.comparer}' comparer.")
        
        binary_comparer.computed_type = Type.get('bool')
        return errors


                

            


    def visit_if_statement(self,if_declaration):
        # condition, instructions
        



        # if_declaration.condition.accept(TypeCollector(self.context))
        # if if_declaration.condition.computed_type is not Type.get('bool'):
        #     raise Exception(f"Given condition is not boolean.")
        
        # child_context: Context = self.context.make_child()
        # child_semantic_checker = TypeCollector(child_context)
        
        # if_declaration.computed_type= Type.get('void')
        
        # for line in if_declaration.instructions:
        #     line.accept(child_semantic_checker)
        #     cond = isinstance(line,If_Statement) or isinstance(line,RepeatDeclaration)
        #     if cond:
        #         if if_declaration.computed_type is not Type.get('void') and line.computed_type is not Type.get('void') :
        #             if if_declaration.computed_type is not line.computed_type:
        #                 raise Exception('Return type not valid')
        #         elif line.computed_type is not Type.get('void'):
        #             if_declaration.computed_type= line.computed_type
        #         #if isinstance(line,ReturnStatement): return
        pass
    
    
    def visit_repeatdeclaration(self, repeat_declaration):
        # times_to_repeat, instructions
        errors = []
        times = repeat_declaration.times_to_repeat
        instructions = repeat_declaration.instructions

        times_type = self.context.resolve(times)
        if times_type != '_int':
            errors += (f"Type expected _int, not '{times_type}' ")
        
        for instruction in instructions:
            errors += instruction.accept(SemanticChecker(self.context))
        return errors
