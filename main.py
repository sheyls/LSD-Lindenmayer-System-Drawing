from lang.context import Context
from lang.visitor import Eval, SemanticChecker
from lexer import lexer
from parser import parser

filename = 'testchecker.lsystem'
filename = 'script.lsystem'
filename = 'myscript.lsystem'
filename = 'test1.lsystem'

with open('scripts/' + filename) as file :
    data = file.read()
    lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

ast = parser.parse(data)

#type_checker = Eval(Context())
c =  Context()
#ast.accept(SemanticChecker(c))
ast.accept(Eval(c))

