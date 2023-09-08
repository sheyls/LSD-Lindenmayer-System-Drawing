from __future__ import annotations
import turtle
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
            for instruction in instructions:
                instruction.accept(Eval(child_context))

    def visit_lsystemdeclaration(self, lsystem_declaration):
        variable = self.context.resolve(lsystem_declaration.name)
        if variable == None:
            self.context.define(lsystem_declaration.name, LsystemInstance(self.context, lsystem_declaration.body))
        else:
            self.context.define(variable, LsystemInstance(self.context, lsystem_declaration.body))


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
        if brush_declaration.body.color.__class__ is str and brush_declaration.body.color[0] != '#':
            color = self.context.resolve(brush_declaration.body.color).value
        else:
            color = brush_declaration.body.color
        self.context.define(brush_declaration.name, BrushInstance(self.context, speed = speed,size= size,color=color,brush= brush)), #self.type))
        

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
        if canvas_declaration.body.color.__class__ is str and canvas_declaration.body.color[0] != '#':
            color = self.context.resolve(canvas_declaration.body.color).value
        else:
            color = canvas_declaration.body.color
        self.context.define(canvas_declaration.name, CanvasInstance(self.context, color,width,high, canvas)), #self.type))


    def auxiliar(sel, window, lsystem,brush, complexity, forward_value, draw_angle):
        curve = lsystem.axiom.axiom.lower()
        for _ in range(complexity):
            for rule in lsystem.l_rules:
                curve = curve.replace(rule.left.lower(), rule.right)  
            curve = curve.lower()
        
        for rule in lsystem.l_rules:
                curve = curve.replace(rule.right, "")
    

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
              
                ang = stack.pop()
                pos = stack.pop()
                brush.up()
                brush.setheading(ang)
                brush.goto(pos)
                brush.down()
             
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

    def visit_change_axiom(self, new_axiom):
        lsys = self.context.resolve(new_axiom.lsys_name)
        lsys.body.axiom = new_axiom.axiom

    def visit_variableassignment(self, var_assignment):
        variable = self.context.resolve(var_assignment.name)
        variable.value = var_assignment.value.accept(Eval(self.context))

    def visit_variabledeclaration(self, var_declaration):
        self.context.define(var_declaration.name, Instance(Type.get(var_declaration.type), var_declaration.value.accept(Eval(self.context))))

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