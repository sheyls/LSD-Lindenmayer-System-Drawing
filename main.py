from abstract_syctax_tree import *
from lang.visitor import *


a = LsystemDeclaration('A', "A->+FF+F")
print(a.accept(Print()))