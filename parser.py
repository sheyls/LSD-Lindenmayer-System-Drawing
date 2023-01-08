import ply.yacc as yacc
import lexer

tokens = lexer.tokens

# Whrite grammar
# Write each method of grammar

# -----------------------------------------------------------------------------
#   Grammar
#
#   Program          : StatementList
# -----------------------------------------------------------------------------

"""
Example:

def p_expression_plus(p):
     'expression : expression PLUS term'
     #   ^            ^        ^    ^
     #  p[0]         p[1]     p[2] p[3]
 
     p[0] = p[1] + p[3]
     
"""

def p_error(p):
    raise Exception(f"Syntax error at '{p.value}', line {p.lineno} (Index {p.lexpos}).")

# Build the parser
parser = yacc()