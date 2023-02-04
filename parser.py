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
#                      | TYPE ID EQUAL Assignable
#                      | ID EQUAL Assignable
#                      | BRUSH ID { Brush_body } END
#                                    
#  
#   Lsystem_body        : axiom: axiom_stmt COMMA rule -> replace_stmt
#
#   Ls_rules            : rule -> replace_stmt COMMA Ls_rules
#                       | rule -> replace_stmt
#
#   Brush_body          : size: int COMMA color: color COMMA speed: int
#
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



def p_assignable(p):
    ''' Assignable : VALUE'''
    
    p[0]=p[1]

def p_lsystem(p):
    '''
    Instruction : LSYS ID LBRACE Lsystem_body RBRACE
    
    '''

    p[0] = LsystemDeclaration(p[2], p[4])
\

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
    p[0] = LsysBody(AxiomDefinition(p[1]), p[5])

def p_lsystem_rules(p):
    '''
    Ls_rules : STRING ARROW STRING COMMA Ls_rules
             | STRING ARROW STRING
    '''

    if len(p) == 4:
        p[0] = [RulesDefinition(left_part=p[1],right_part=p[3])]
    elif len(p)==6:
        p[0] = [RulesDefinition(left_part=p[1],right_part=p[3])] + p[5]
        
def p_brush(p):
    '''
    Instruction : BRUSH ID LBRACE brush_body RBRACE
    '''
    p[0] = LsystemDeclaration(p[2], p[4])

def p_brush_body(p):
    '''
    Brush_body : size TWOPOINTS INT COMMA COLOR TWOPOINTS color COMMA SPPED TWOPOINTS int    
    '''
    p[0] = BrushBody(p[3], p[7], p[11])

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc.yacc(debug=True)

with open('script.lsystem')as file:
    data = file.read()

# lexer.input(data)
 
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)

ast = parser.parse(data)

for i in ast.statements:
    print(i)
    print()
    print(i.body.l_rules)
    print()
    print(i.body.axiom)
    print()
    print()
    for rule in i.body.l_rules:
        print(rule.left_part)
        print(rule.right_part)

