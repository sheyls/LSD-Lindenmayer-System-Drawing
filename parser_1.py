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
#                      | #All the valid instructions here
#                                    
#  
#   Lsystem_body        : axiom: axiom_stmt, Ls_rules
#
#   Ls_rules            : rule -> replace_stmt, 
#                       | Ls_rules
#                       | Epsilon?
#
#   Assigmen            : VALUE
#
#   Type                : TYPE
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

def p_type(p):
    '''Type : TYPE'''

def p_assignable(p):
    ''' Assignable : VALUE'''
    
    p[0]=p[1]

def p_lsystem(p):
    '''
    Instruction : LSYS ID LBRACE Lsystem_body RBRACE
                | ID EQUAL Assignable
                | TYPE ID EQUAL Assignable
    '''
    if len(p) == 6:
        p[0] = LsystemDeclaration(p[2], p[4])
    elif len(p)==5:
        p[0] = VariableDeclaration(p[1],p[2],p[4])
    elif len(p)==4:
        p[0] = VariableAssignment(p[1],p[3])
    

def p_body(p):
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
        

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc.yacc(debug=True)

with open('script.lsystem')as file:
    data = file.read()


ast = parser.parse(data)

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

