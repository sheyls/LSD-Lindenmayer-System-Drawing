import regex as re
from lexer import lexer

y = re.compile(r'->')
x = y.search("kskwk->rrt")

filename = 's2.lsystem'

with open('scripts/' + filename) as file :
    data = file.read()
    lexer.input(data)



while True :
    tok = lexer.token()
    if not tok :
        break
    #print(tok.type, tok.value, tok.lineno, tok.lexpos)   
    print(tok) 


