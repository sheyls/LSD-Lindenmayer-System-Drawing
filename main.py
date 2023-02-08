from abstract_syctax_tree import *
from lang.visitor import *
from parser_1 import parser

class DSL:
    def main(self, file_name=None):
        if file_name != None:
            self.run_file(file_name)

    def run_file(self, file_name):
        code = ""

        with open('script.lsystem') as file:
            code = file.read()

        self.run(code)

    def run(self):
        program = parser.parse()
        st = Context()
        program.evaluate(st)
        print(st.symbols)


if __name__ == "__main__":
    dsl = DSL()
    dsl.main()
