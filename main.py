from lang.context import Context
from lang.visitor import Eval, TypeCollector
from lexer import lexer
from parser_1 import parser

filename = 'myscript.lsystem'
filename = 'test.lsystem'
filename = 'testchecker.lsystem'

with open('scripts/' + filename) as file :
    data = file.read()
    lexer.input(data)

ast = parser.parse(data)

#type_checker = Eval(Context())
c =  Context()
ast.accept(TypeCollector(c))
ast.accept(Eval(c))

