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
#   InstructionList    :  Instruction END  InstructionList
#                      |  Instruction END
#
<<<<<<< Updated upstream
#   Instruction        : lsystem ID { Lsystem_body } 
=======
#   Instruction        :  lsystem ID { Lsystem_body }
#                      |  ID EQUAL Assignable 
>>>>>>> Stashed changes
#                      | #All the valid instructions here
#
#   Assignable         : int
#                                    
#  
#   Lsystem_body        : axiom: axiom_stmt, Ls_rules
#
#   Ls_rules            : rule -> replace_stmt, 
#                       | Ls_rules
#                       | Epsilon?
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
    InsructionList : Instruction END InstructionList
                   | Instruction END
    '''
    if (len(p) == 4):
        p[0] = [p[1]] + p[3]
    elif (len(p) == 3):
        p[0] = [p[1]]

def p_lsystem(p):
    '''
<<<<<<< Updated upstream
    Instrucion : LSYSTEM ID LBRACE Body RBRACE
=======
    Instruction : LSYS ID LBRACE Lsystem_body RBRACE
>>>>>>> Stashed changes
    '''
    if len(p) == 6:
        p[0] = LsystemDeclaration(p[2], p[4])

def p_body(p):
    '''
    Lsystem_body : AXIOM TWOPOINTS STRING COMMA Ls_rules
                
    '''
    pass

def p_lsystem_rules(p):
    '''
    Ls_rules : STRING ARROW STRING COMMA Ls_rules
             | STRING ARROW STRING

    '''
    if len(p) == 4:
<<<<<<< Updated upstream
        pass
=======
        p[0] = [RulesDefinition( p[1], p[3] )]
    
    if len(p) == 6:
        p[0] = [RulesDefinition( p[1], p[3] )].append(p[5])

def p_assignable(p):
    '''
    Assignable : INT
    '''
    p[0]= p[1]


def p_variable(p):
    '''
    Instruction : ID EQUAL Assignable
    '''

    if len(p) == 5:
        p[0] = VariableDeclaration(p[1], p[2], p[4])
    elif len(p) == 4:
        p[0] = VariableAssignment(p[1], p[3])

>>>>>>> Stashed changes

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc()