from abstract_syctax_tree import *
from lang.visitor import *

a = LsystemDeclaration('A', "A->+FF+F")
d = VariableDeclaration('_int', 'var', 12)
c = VariableAssignment('var',10)

b = Program([a,d,c])
b.accept(Eval())