import ply.lex as lex

# Keywords
reserved = {
    'canvas'     : 'CANVAS',
    'draw'       : 'DRAW',
    'brush'      : 'BRUSH',
    'lsystem'    : 'LSYSTEM',
    'left'       : 'LEFT',
    'right'      : 'RIGHT',
    'line'       : 'LINE',
    'nill'       : 'NILL',
    'axiom'      : 'AXIOM',
    'rule'       : 'RULE',
    'push'       : 'PUSH',
    'pop'        : 'POP',
    'while'      : 'WHILE',
    'if'         : 'IF',
    'not'        : 'NOT',
    'else'       : 'ELSE',
    'and'        : 'AND',
    'or'         : 'OR',
    'true'       :'TRUE',
    'false'      :'FALSE',
    'break'      :'BREAK'
}

# List of token names. 
tokens = (
   'STRING',

   'PLUS',
   'MINUS',
   'MULTIPLY',
   'DIFFER',
   'ID',
   'INT',
   'FLOAT',
   'ANGLE',
   'COLOR',  
   'EQUALEQUAL',
   'GEQUAL',
   'LEQUAL',
   'LESS',
   'GREATER',

   
   'LPAREN',
   'RPAREN',
   'EQUAL',
   'COMMA',
   'END',
   'LBRACE',
   'RBRACE'
   
)


# Regular expression rules for simple tokens
t_STRING = r'"(\w|\s)*"'


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIFFER = r'\\'

t_EQUALEQUAL = r'=='
t_GEQUAL = r'>='
t_LEQUAL = r'<='
t_LESS = r'<'
t_GREATER = r'>'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL= r'='
t_COMMA= r','
t_END= r';'
t_TWOPOINTS= r':'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLOR = r'\#([a,b,c,d,e,f]|\d){6}'

def t_ARROW(t):
    r'->'
    return t.value

def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except:
        t.value = 0
        t_error(t) 
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ANGLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    if t.value > 360 or t.value < -360:
        t_error(t)
    else:
        return t   


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters
t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise Exception(f"Invalid token '{t.value[0]}' at line {t.lineno} (Index {t.lexpos}).")

def find_column(input, token):
    '''
        Compute column.
        Input is the input text string.
        Token is a token instance.
    '''
    
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

tokens= list(reserved.values()) + list(tokens)

lexer = lex.lex(debug=True)

data = "7 + 8"
lexer.input(data)


while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)