import ply.yacc as yacc
import lexer 
from abstract_syctax_tree import *
import os

tokens = lexer.tokens

# Whrite grammar
# Write each method of grammar

# -----------------------------------------------------------------------------
#   Grammar
#
#   Program             : InstructionList
#
#   InstructionList    :   Instruction END
#                      |   Instruction END  InstructionList
#
#   Instruction        : LSYS ID { Lsystem_body } END
#                      | Type ID EQUAL Assignable
#                      | ID EQUAL Assignable
#                      | BRUSH ID { Brush_body } END
#                      | CANVAS ID { Canvas_body } END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA int COMMA int COMMA int RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA ID COMMA int COMMA int RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA int COMMA ID COMMA int RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA int COMMA int COMMA ID RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA ID COMMA ID COMMA int RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA ID COMMA int COMMA ID RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA int COMMA ID COMMA ID RPAREN END
#                      | DRAW LPAREN Lsys COMMA brush COMMA canvas COMMA ID COMMA ID COMMA ID RPAREN END
#                      | ADD_RULE LPAREN ID(lsys) COMMS STRING(left_part) COMMA STRING(right_part) RPAREN END
#                      | REPEAT int { InstructionList } END
#                      | REAPEAT ID { InstructionList} END
#                      | IF ( Condition ) { InstructionList } END
#                                    
#   Lsystem_body        : axiom: axiom_stmt COMMA rule -> replace_stmt
#
#   Ls_rules            : rule -> replace_stmt COMMA Ls_rules
#                       | rule -> replace_stmt
#
#   Brush_body          : size: int COMMA color: color COMMA speed: int
#                       | size: ID COMMA color: color COMMA speed: ID
#                       | size: ID COMMA color: color COMMA speed: int
#                       | size: int COMMA color: color COMMA speed: ID
#
#   Canvas_body          : size: int COMMA int COMMA color: color
#                        | size: ID COMMA int COMMA color: color
#                        | size: int COMMA ID COMMA color: color
#                        | size: ID COMMA ID COMMA color: color
#
#   Condition            : Assignable GEQUAL Assignable
#                        | Assignable LEQUAL Assignable
#                        | Assignable EQUALEQUAL Assignable
#                        | Assignable GRATER Assignable
#                        | Assignable LESS Assignable
#                        | BOOL
# -----------------------------------------------------------------------------
"""
Example:

def p_expression_plus(p):
     'expression : expression PLUS term'
     #   ^            ^        ^    ^
     #  p[0]         p[1]     p[2] p[3]
 
     p[0] = p[1] + p[3]
     
"""
def p_program(p):
    '''
    Program : InstructionList
    '''
    p[0] = Program(p[1])

def p_instruction_list(p):
    '''
    InstructionList : Instruction END InstructionList
                   | Instruction END
    '''
    if (len(p) == 4):
        p[0] = [p[1]] + p[3]
    elif (len(p) == 3):
        p[0] = [p[1]]


#def p_type(p):
#    '''Type : TYPE'''
#    p[0]=p[1]

def p_assignable(p):
    ''' Assignable : INT'''
    
    p[0]=p[1]

def p_lsystem(p):
    '''
    Instruction : LSYS ID LBRACE Lsystem_body RBRACE
    
    '''

    p[0] = LsystemDeclaration(p[2], p[4])


def p_variables(p):
    '''
    Instruction : ID EQUAL Assignable 
                | TYPE ID EQUAL Assignable
    '''
    if len(p)==5:
        p[0] = VariableDeclaration(p[1],p[2],p[4])
    elif len(p)==4:
        p[0] = VariableAssignment(p[1],p[3])



def p_lsystem_body(p):
    '''
    Lsystem_body : AXIOM TWOPOINTS STRING COMMA Ls_rules
                
    '''
    p[0] = LsysBody(AxiomDefinition(p[3]), p[5])

def p_lsystem_rules(p):
    '''
    Ls_rules : STRING ARROW STRING COMMA Ls_rules
             | STRING ARROW STRING
    '''

    if len(p) == 4:
        p[0] = [RulesDefinition(left_part=p[1],right_part=p[3])]
    elif len(p)==6:
        p[0] = [RulesDefinition(left_part=p[1],right_part=p[3])] + p[5]
        
def p_add_rule(p):
    '''Instruction : ADD_RULE LPAREN ID COMMA STRING COMMA STRING RPAREN'''
    
    p[0] = Add_rule(p[3],RulesDefinition(left_part=p[5],right_part=p[7]))


def p_brush(p):
    '''
    Instruction : BRUSH ID LBRACE Brush_body RBRACE
    '''
    p[0] = BrushDeclaration(p[2], p[4])

def p_brush_body(p):
    '''
    Brush_body : SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT    
    Brush_body : SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT 
               | SIZE TWOPOINTS INT COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS ID
               | SIZE TWOPOINTS ID COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS INT
               | SIZE TWOPOINTS ID COMMA COLOR TWOPOINTS COL COMMA SPEED TWOPOINTS ID  
    '''
    p[0] = BrushBody(p[3], p[7], p[11])

def p_canvas(p):
    '''
    Instruction : CANVAS ID LBRACE Canvas_body RBRACE
    '''
    p[0] = CanvasDeclaration(p[2], p[4])

def p_canvas_body(p):
    '''
    Canvas_body : HIGH TWOPOINTS INT COMMA WIDTH TWOPOINTS INT COMMA COLOR TWOPOINTS COL    
    Canvas_body : HIGH TWOPOINTS INT COMMA WIDTH TWOPOINTS INT COMMA COLOR TWOPOINTS COL 
                | HIGH TWOPOINTS ID COMMA WIDTH TWOPOINTS ID COMMA COLOR TWOPOINTS COL
                | HIGH TWOPOINTS INT COMMA WIDTH TWOPOINTS ID COMMA COLOR TWOPOINTS COL
                | HIGH TWOPOINTS ID COMMA WIDTH TWOPOINTS INT COMMA COLOR TWOPOINTS COL   
    '''
    p[0] = CanvasBody(p[3], p[7], p[11])

def p_draw_id(p):
    '''
    Instruction : DRAW LPAREN ID COMMA ID COMMA ID COMMA ID COMMA ID COMMA ID RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA ID COMMA INT COMMA INT RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA ID COMMA INT RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA INT COMMA ID RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA ID COMMA ID COMMA INT RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA ID COMMA INT COMMA ID RPAREN 
                | DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA ID COMMA ID RPAREN 
    '''

    p[0] = Draw_ID(p[3], p[5], p[7], p[9], p[11], p[13])

def p_draw(p):
    '''
    Instruction : DRAW LPAREN ID COMMA ID COMMA ID COMMA INT COMMA INT COMMA INT RPAREN
    '''
    p[0] = Draw(p[3], p[5], p[7], p[9], p[11], p[13])

def p_repeat(p):
    '''Instruction : REPEAT INT LBRACE InstructionList RBRACE'''
    '''
    Instruction : REPEAT INT LBRACE InstructionList RBRACE
                | REPEAT ID LBRACE InstructionList RBRACE    
    '''

    p[0] = RepeatDeclaration(p[2],p[4])

def p_if(p):
   '''
   Instruction : IF LPAREN Condition RPAREN LBRACE InstructionList RBRACE
   '''    
   p[0] = If_Statement(p[3],p[6])

def p_condition(p):
    '''
    Condition : Assignable GEQUAL Assignable
              | Assignable LEQUAL Assignable
              | Assignable EQUALEQUAL Assignable
              | Assignable GREATER Assignable
              | Assignable LESS Assignable
              | BOOL
    '''    
    if len(p)==2:
        p[0] = p[1]

    else:
        p[0] = BinaryComparer(p[1],p[2],p[3])     


def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc.yacc(debug=True)

#with open('script.lsystem')as file:
#    data = file.read()

# lexer.input(data)
 
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)

#ast = parser.parse(data)

# for i in ast.instructions:
#     print(i)
#     print()
#     print(i.body.l_rules)
#     print()
#     print(i.body.axiom)
#     print()
#     print()
#     for rule in i.body.l_rules:
#         print(rule.left_part)
#         print(rule.right_part)

