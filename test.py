import regex as re

y = re.compile(r'\#([a,b,c,d,e,f]|\d){6}')
x = y.search("#5aaa")

print(x)