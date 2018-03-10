from compiler.ast import StmtNode

class DefinitionNode(StmtNode):
    name = ''
    def __init__(self, loc, name):
        super().__init__(loc)
        self.name = name

    
