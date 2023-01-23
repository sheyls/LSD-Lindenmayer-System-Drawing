
class Visitor(object):
    pass

class Eval(Visitor):
    def visit_lsystemdeclaration(self,lsystem):
        return

class Print(Visitor):
    def visit_lsystemdeclaration(self,lsystem):
        return lsystem.name


