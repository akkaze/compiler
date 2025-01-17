from compiler.ast import StmtNode

class DefinitionNode(StmtNode):
    def __init__(self, loc, name):
        super().__init__(loc)
        self.name = name

    def accept(self, visitor):
        return visitor.visit(self) 
