import ply.yacc as yacc
import lexer
from abstract_syctax_tree import *

tokens = lexer.tokens

# Whrite grammar
# Write each method of grammar

# -----------------------------------------------------------------------------
#   Grammar
#
#   Program             : InstructionList
#
#   InstructionList    :  Instruction END InstructionList
#                      |  Instruction END
#
#   Instruction        : lsystem ID { Lsystem_body } 
#                      | #All the valid instructions here
#                                    
#  
#   Lsystem_body        : axiom: axiom_stmt COMMA rule -> replace_stmt
#
#   Ls_rules            : rule -> replace_stmt COMMA Ls_rules
#                       | rule -> replace_stmt
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
    Program : InsructionList
    '''
    p[0] = Program(p[1])

def p_instruction_list(p):
    '''
    InsructionList : Instruction END InstructionList
                   | Instruction END
    '''
    if (len(p) == 4):
        p[0] = [p[1]] + p[3]

    elif (len(p) == 3):
        p[0] = [p[1]]

def p_lsystem(p):
    '''
    Instrucion : LSYSTEM ID LBRACE Body RBRACE
    '''
    p[0] = LsystemDeclaration(p[2], p[4])

def p_lsystem_body(p):
    '''
    Lsystem_body : AXIOM TWOPOINTS STRING COMMA Ls_rules
                
    '''
    p[0] = LsystemDefinition ( p[3], p[5] )

def p_lsystem_rules(p):
    '''
    Ls_rules : STRING ARROW STRING COMMA ls_rules
             | STRING ARROW STRING

    '''
    if len(p) == 4:
        p[0] = [RuleDefinition( p[1], p[3] )]
    
    if len(p) == 6:
        p[0] = [RuleDefinition( p[1], p[3] )].append(p[5])

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc()