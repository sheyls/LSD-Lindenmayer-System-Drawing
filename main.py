from lang.context import Context
from lang.visitor import Eval
from parser_1 import parser


with open('script.lsystem') as file:
    data = file.read()

ast = parser.parse(data)

#type_checker = Eval(Context())
c =  Context()
ast.accept(Eval(c))

