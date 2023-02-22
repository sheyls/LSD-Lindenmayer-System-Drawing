from lang.context import Context
from lang.visitor import Eval
from lang.semantic_checker import SemanticChecker
from parser_1 import parser

print("Insert a script name: ")
file_name = input()

with open('scripts/' + file_name + '.lsystem', 'r') as file:
    data = file.read()

ast = parser.parse(data)
c =  Context()

errors = ast.accept(SemanticChecker(c))
if len(errors)==0:
    ast.accept(Eval(Context()))
else :
    print(errors)