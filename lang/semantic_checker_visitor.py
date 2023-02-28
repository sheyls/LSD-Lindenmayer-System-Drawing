from unicodedata import name
from .eval_visitor import *
from tools import *

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
            update_errs(errors, (f"Defined lsystem '{lsystem_declaration.name}'.")) 

        self.context.define(lsystem_declaration.name, Type('lsys')) # ver si esto esta bien
        lsystem_declaration.type = self.context.symbols[lsystem_declaration.name]

        axiom = lsystem_declaration.body.axiom.axiom # el primero devuelve un Axiomdefinition
        rules = lsystem_declaration.body.l_rules

        contain = False
        for i in range(len(axiom)):
            for rule in rules:
                if axiom[i] == rule.left:
                    contain = True 
        if not contain:
            update_errs(errors,(f"Wrong definition of lsystem'.")) # ver como accedo al nombre     
      
        return errors
               

    def visit_canvasdeclaration(self, canvas_declaration):
        # name, body
        errors = []
        canvas = self.context.resolve(canvas_declaration.name)

        if canvas:
            errors.append(f"Defined canvas '{canvas_declaration.name}'.")

        body = canvas_declaration.body    

        high = body.high
        width = body.width
        color = body.high    

        self.context.define(canvas_declaration.name, Type('canvas'))  
        canvas_declaration.computed_type = self.context.symbols[canvas_declaration.name]

        update_errs(errors,body.accept(SemanticChecker(self.context)))
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
                    update_errs(errors, f"Expected type _int for high.")
            else: update_errs(errors,(f"Variable '{high}' not defined."))

        if width.__class__ is str:
            width_type = self.context.resolve(width).name
            if width_type != None : # revisar esto
                if width_type != 'int':
                    update_errs(errors,f"Expected type int for width.")
            else: update_errs(errors,f"Variable '{width}' not defined.")

        if color.__class__ is str and color[0] != '#':
            color_type = self.context.resolve(color).name
            if color_type != None:
                if color_type !='col':
                    update_errs(errors, f"Excpected type color for color.")
            else: update_errs(errors,f"Variable '{color}' not defined.")
            

        return errors



    def visit_brushdeclaration(self,brush_declaration):
        # name, body
        errors = []
        brush = self.context.resolve(brush_declaration.name)
        if brush: 
            update_errs(errors, f"Defined brush '{brush_declaration.name}'.")

        brush_body = brush_declaration.body
        size = brush_body.size
        color = brush_body.color
        speed = brush_body.speed    

        self.context.define(brush_declaration.name, Type('brush'))    
        brush_declaration.type = self.context.symbols[brush_declaration.name]

        update_errs(errors, brush_body.accept(SemanticChecker(self.context))) 
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
                if size_type != 'int':
                    update_errs(errors,f"Expected type int for size.")
            else: 
                update_errs(errors,f"Variable '{size}' not defined.")

        if speed.__class__ is str:
            speed_type = self.context.resolve(speed).name
            if speed_type != None : # revisar esto
                if speed_type != 'int':
                    update_errs(errors,f"Expected type int for speed.")
            else: 
                update_errs(errors,f"Variable '{speed}' not defined.")

        
        if color.__class__ is str and color[0] != '#':
            color_type = self.context.resolve(color).name
            if color_type != None:
                if color_type !='col':
                    update_errs(errors, f"Excpected type color for color.")
            else: update_errs(errors,f"Variable '{color}' not defined.")

        return errors    

    def visit_draw(self, draw_node): # ver si aqui hay que mandar a revisar todo de nuevo
        # lsystem, brush, canvas, step_size, angle,complexity

        errors = []

        lsystem_type = self.context.resolve(draw_node.lsystem)
        if lsystem_type.name != 'lsys':
            update_errs(errors,f"Expected type lsys.")
        
        brush_type = self.context.resolve(draw_node.brush)
        if brush_type.name != 'brush':
            update_errs(errors,f"Expected type brush.")

        canvas_type = self.context.resolve(draw_node.canvas)
        if canvas_type.name != 'canvas':
            update_errs(errors,f"Expected type canvas")

        if draw_node.step_size.__class__ is str :
            size_type = self.context.resolve(draw_node.step_size).name
            if size_type != 'int':
                update_errs(errors,f"Expected type int for size.") 

        if draw_node.angle.__class__ is str :
            size_type = self.context.resolve(draw_node.angle).name
            if size_type != 'int' and size_type != 'float':
                update_errs(errors,f"Expected type int ot type float for angle.")

        if draw_node.complexity.__class__ is str :
            size_type = self.context.resolve(draw_node.complexity).name
            if size_type != 'int':
                update_errs(errors,f"Expected type int for complexity.")                  
                
        draw_node.computed_type = Type('void')             
        return errors

    def visit_add_rule(self, new_rule):
        # lsys_name, rule    
        errors = []
        lsys = self.context.resolve(new_rule.lsys_name)
        if lsys is None:
            update_errs(errors,f"Lsystem '{new_rule.lsys_name}' not defined.")
        
        new_rule.computed_type = Type('void')
        return errors

    def visit_variableassignment(self, var_assignment):
        # name, value
        errors = []
        update_errs(errors, var_assignment.value.accept(SemanticChecker(self.context)))
        var_type = self.context.resolve(var_assignment.name)
        if var_type is None:
            update_errs(errors,f"Variable '{var_assignment.name}' not defined.")
        else :
            if var_type.name != var_assignment.value.computed_type.name:
                update_errs(errors,f"Can't assign value {var_assignment.value.value} to variable '{var_assignment.name}'. Type '{var_type}' different to '{var_assignment.value.computed_type}'.")   

        var_assignment.computed_type = var_type  
        return errors       

    def visit_variabledeclaration(self, var_declaration):
        # type, name , value
        errors = []
        var_type = Type.get(var_declaration.type)
        update_errs(errors, var_declaration.value.accept(SemanticChecker(self.context))) # ver si esta hecho el visit para esto y si esto sotve pa algo

        if var_declaration.name in self.context.symbols.keys():
            update_errs(errors, f"Defined variable '{var_declaration.name}'.")
        else:
            self.context.define(var_declaration.name, var_type)
        if var_declaration.value.computed_type.name != var_type.name:
            update_errs(errors, f"{var_declaration.value.computed_type} not expected.")
                    
        var_declaration.computed_type = var_type
        return errors 

    def visit_assignable(self, assignable):
        assignable.computed_type = assignable.type
        return None


    def visit_binarycomparer(self, binary_comparer):
        errors = []
        left = binary_comparer.left_expr
        if left.__class__ is str:
            left = self.context.resolve(left)
        else:
            update_errs(errors, left.accept(SemanticChecker(self.context)))
            left = left.computed_type
        
        right = binary_comparer.right_expr
        if right.__class__ is str:
            right = self.context.resolve(right)
        else:
            update_errs(errors,right.accept(SemanticChecker(self.context)))
            right = right.computed_type
        
        if left == Type.get('void') or right == Type.get('void'):
            update_errs(errors, f"{'void'} expression not admissible for comparison.")
        
        if left != right:
            update_errs(errors, f"Expressions to compare must be the same type.")
        
        if binary_comparer.comparer in ['(>)', '(<)', '>=', '<='] and left is not Type.get('int'):
            update_errs(errors,f"Invalid expression type for '{binary_comparer.comparer}' comparer.")
        
        binary_comparer.computed_type = Type.get('bool')
        return errors


    def visit_arithmeticop(self, arithmeticOp):
        # left, operator, right
        errors = []
        if arithmeticOp.left.__class__ is str:
            left_type = self.context.resolve(arithmeticOp.left).name
            if left_type != "float" and left_type != "int":
                update_errs(errors,f"{left_type.name}'not expected.'") 
        else:
            update_errs(errors, arithmeticOp.left.accept(SemanticChecker(self.context)))
            left_type = arithmeticOp.left.computed_type
        
        if arithmeticOp.right.__class__ is str:
            right_type = self.context.resolve(arithmeticOp.right).name
            if right_type != "float" and right_type != "int":
                update_errs(errors,f"{left_type.name}'not expected.'")
        else:
            update_errs(errors,arithmeticOp.right.accept(SemanticChecker(self.context)))
            right_type = arithmeticOp.right.computed_type

        if left_type == 'float' or right_type == 'float':
            arithmeticOp.computed_type = Type('float')
        
        arithmeticOp.computed_type = Type('int')
        
        return errors

    def visit_if_else_statement(self, if_else_statement):
        # condition, instructions_true, instructions_false
        errors = []
        if not isinstance(if_else_statement.condition, str):
            update_errs(errors, if_else_statement.condition.accept(SemanticChecker(self.context))) # que hace esto
            if if_else_statement.condition.computed_type is not Type.get('bool'):
                update_errs(errors, f"Given condition is not boolean")

        child_context:Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)      

        if_else_statement.computed_type = Type.get('void')  

        for line in if_else_statement.instructions_true:
            update_errs(errors, line.accept(child_semantic_checker))

        for line in if_else_statement.instructions_false:
            update_errs(errors, line.accept(child_semantic_checker))        
        return errors


    def visit_if_statement(self,if_declaration):
        errors = []
        if not isinstance(if_declaration.condition, str):
            update_errs(errors, if_declaration.condition.accept(SemanticChecker(self.context)))
            if if_declaration.condition.computed_type is not Type.get('bool'):
                update_errs(errors, f"Given condition is not boolean.")

        child_context:Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)

        if_declaration.computed_type = Type.get('void')

        for line in if_declaration.instructions:
            update_errs(errors, line.accept(child_semantic_checker))

        return errors
    
    def visit_repeatdeclaration(self, repeat_declaration):
        # times_to_repeat, instructions
        errors = []
        times = repeat_declaration.times_to_repeat
        instructions = repeat_declaration.instructions
        if repeat_declaration.times_to_repeat.__class__ is str:
            times_type = self.context.resolve(times)
        else: 
            times_type = Type.get('int')
        if times_type.name != 'int':
            update_errs(errors,f"Type expected int, not '{times_type}' ")
        
        for instruction in instructions:
            update_errs(errors, instruction.accept(SemanticChecker(self.context))) 
        return errors

    def visit_change_axiom(self, p):
        return []