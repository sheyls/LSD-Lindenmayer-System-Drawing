from lang.context import Context
from lang.visitor import Eval
from lexer import lexer
from parser import parser

filename = 'test2.lsystem'

with open('scripts/' + filename) as file :
    data = file.read()
    lexer.input(data)

ast = parser.parse(data)

#type_checker = Eval(Context())
c =  Context()
ast.accept(Eval(c))

