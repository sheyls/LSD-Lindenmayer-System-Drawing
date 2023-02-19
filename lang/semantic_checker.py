from unicodedata import name
from .visitor import *

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
            errors.append(f"Defined lsystem '{lsystem_declaration.name}'.")

        self.context.define(lsystem_declaration.name, LsystemInstance(self.context,lsystem_declaration.body)) # ver si esto esta bien
        lsystem_declaration.type = self.context.symbols[lsystem_declaration.name]

        lsysbody = lsystem_declaration.body
        errors.append(lsysbody.accept(SemanticChecker(self.context)))
        return errors

    def visit_lsysbody(self, lsystem_body) : # LsysBody es el nodo que se esta usando en el AST , no LsystemDefinition
        # axiom, rules
        errors = []
        axiom = lsystem_body.axiom.axiom # el primero devuelve un Axiomdefinition
        rules = lsystem_body.l_rules

        contain = False
        for i in range(len(axiom)):
            for rule in rules:
                if axiom[i] == rule.left:
                    contain = True 
        if not contain:
            errors.append(f"Wrong definition of lsystem'.") # ver como accedo al nombre

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

        self.context.define(canvas_declaration.name, Type('canvas'))  
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

        self.context.define(brush_declaration.name, Type('brush'))    
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
                if size_type != 'int':
                    errors.append(f"Expected type int for size.")
            else: errors.append(f"Variable '{size}' not defined.")

        if speed.__class__ is str:
            speed_type = self.context.resolve(speed).name
            if speed_type != None : # revisar esto
                if speed_type != 'int':
                    errors.append(f"Expected type int for speed.")
            else: errors.append(f"Variable '{speed}' not defined.")

        return errors    

    def visit_draw(self, draw_node): # ver si aqui hay que mandar a revisar todo de nuevo
        # lsystem, brush, canvas, step_size, angle,complexity

        errors = []

        lsystem_type = self.context.resolve(draw_node.lsystem)
        if lsystem_type is not LsystemInstance:
            errors.append(f"Expected type lsys.")
        else:
            errors.append(f"Variable '{draw_node.lsystem}' not defined.")

        brush_type = self.context.resolve(draw_node.brush)
        if brush_type is not BrushInstance:
            errors.append(f"Expected type brush.")
        else : 
            errors.append(f"Variable'{draw_node.brush}' not defined.")  

        canvas_type = self.context.resolve(draw_node.canvas)
        if canvas_type is not CanvasInstance:
            errors.append(f"Expected type canvas")
        else :
            errors.append(f"Variable'{draw_node.canvas}' not defined.") 

        if draw_node.step_size.__class__ is str :
            size_type = self.context.resolve(draw_node.step_size).name
            if size_type != 'int':
                errors.append(f"Expected type _int for size.")
            else:
                errors.append(f"Variable '{draw_node.step_size}' not defined.")    

        if draw_node.angle.__class__ is str :
            size_type = self.context.resolve(draw_node.angle).name
            if size_type != 'int':
                errors.append(f"Expected type _int for angle.")
            else:
                errors.append(f"Variable '{draw_node.angle}' not defined.")  

        if draw_node.complexity.__class__ is str :
            size_type = self.context.resolve(draw_node.complexity).name
            if size_type != 'int':
                errors.append(f"Expected type _int for complexity.")
            else:
                errors.append(f"Variable '{draw_node.complexity}' not defined.")                    
                

        draw_node.computed_type = Type('void')             
        return errors

    def visit_add_rule(self, new_rule):
        # lsys_name, rule    
        errors = []
        lsys = self.context.resolve(new_rule.lsys_name)
        if lsys is None:
            errors.append(f"Lsystem '{new_rule.lsys_name}' not defined.")
        
        new_rule.computed_type = Type('void')
        return errors

    def visit_variableassignment(self, var_assignment):
        # name, value
        errors = []
        errors += var_assignment.value.accept(SemanticChecker(self.context))
        var_type = self.context.resolve(var_assignment.name)
        if var_type is None:
            errors.append(f"Variable '{var_assignment.name}' not defined.")
        else :
            if var_type.name != var_assignment.value.computed_type:
                errors.append(f"Can't assign value {var_assignment.value} to variable '{var_assignment.name}'. Type '{var_type}' different to '{var_assignment.value.computed_type}'.")   

        var_assignment.computed_type = var_type  
        return errors       

    def visit_variabledeclaration(self, var_declaration):
        # type, name , value
        errors = []
        var_type = Type.get(var_declaration.type)
        errors.append( var_declaration.value.accept(SemanticChecker(self.context))) # ver si esta hecho el visit para esto y si esto sotve pa algo

        if var_declaration.name in self.context.symbols.keys():
            errors.append(f"Defined variable '{var_declaration.name}'.")
        else:
            self.context.define(var_declaration.name, var_type)
        if var_declaration.value.computed_type != var_type.name:
            errors.append(f"{var_declaration.value.type} not expected.")
                    
        var_declaration.computed_type = var_type
        return errors 

    def visit_assignable(self, assignable):
        assignable.computed_type = assignable.type
        return ''


    def visit_binarycomparer(self, binary_comparer):
        errors = []
        errors.append(binary_comparer.left_expr.accept(SemanticChecker(self.context)))
        errors.append(binary_comparer.right_expr.accept(SemanticChecker(self.context)))
        
        if binary_comparer.left_expr.computed_type == Type.get('void') or binary_comparer.right_expr.computed_type == Type.get('void'):
            errors.append(f"{'void'} expression not admissible for comparison.")
        
        if binary_comparer.left_expr.computed_type != binary_comparer.right_expr.computed_type:
            errors.append("Expressions to compare must be the same type.")
        
        if binary_comparer.comparer in ['(>)', '(<)', '>=', '<='] and binary_comparer.left_expr.computed_type is not Type.get('_int'):
            errors.append(f"Invalid expression type for '{binary_comparer.comparer}' comparer.")
        
        binary_comparer.computed_type = Type.get('bool')
        return errors


    def visit_arithmeticop(self, arithmeticOp):
        # left, operator, right
        errors = []

        # que pasa si left o right son Aop

        left_type = self.context.resolve(arithmeticOp.left)
        right_type = self.context.resolve(arithmeticOp.right)

        arithmeticOp.computed_type = Type('int')
        return ''

    def visit_if_else_statement(self, if_else_statement):
        # condition, instructions_true, instructions_false
        errors = []
        if isinstance(if_else_statement.condition, BinaryComparer):
            if_else_statement.condition.accept(SemanticChecker(self.context)) # que hace esto
            if if_else_statement.condition.computed_type is not Type.get('bool'):
                errors.apped(f"Given condition is not boolean")

        child_context:Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)      

        if_else_statement.computed_type = Type.get('void')  

        if if_else_statement.condition:
            for line in if_else_statement.instructions_true:
                errors.append(line.accept(child_semantic_checker))
        else :
            for line in if_else_statement.instructions_false:
                errors.append(line.accept(child_semantic_checker))        
        return errors
            


    def visit_if_statement(self,if_declaration):
        errors = []
        if isinstance(if_declaration.condition, BinaryComparer):
            if_declaration.condition.accept(SemanticChecker(self.context))
            if if_declaration.condition.computed_type is not Type.get('bool'):
                errors.append(f"Given condition is not boolean.")

        child_context:Context = self.context.make_child()
        child_semantic_checker = SemanticChecker(child_context)

        if_declaration.computed_type = Type.get('void')

        for line in if_declaration.instructions:
            errors.append(line.accept(child_semantic_checker))

        return errors
    
    def visit_repeatdeclaration(self, repeat_declaration):
        # times_to_repeat, instructions
        errors = []
        times = repeat_declaration.times_to_repeat
        instructions = repeat_declaration.instructions

        times_type = self.context.resolve(times)
        if times_type != '_int':
            errors.append(f"Type expected int, not '{times_type}' ")
        
        for instruction in instructions:
            errors.append(instruction.accept(SemanticChecker(self.context))) 
        return errors
