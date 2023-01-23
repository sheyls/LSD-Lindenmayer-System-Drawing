import regex as re
from lexer import lexer
from parser import parser

y = re.compile(r'->')
x = y.search("kskwk->rrt")

filename = 's2.lsystem'

with open('scripts/' + filename) as file :
    data = file.read()
    #lexer.input(data)
    ast = parser.parse(data)




# tokens = []
# while True :
#     tok = lexer.token()
#     tokens.append(tok)
#     if not tok :
#         break
#     #print(tok.type, tok.value, tok.lineno, tok.lexpos)   




