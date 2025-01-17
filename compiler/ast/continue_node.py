from compiler.ast import StmtNode


class ContinueNode(StmtNode):

    def __init__(self, loc):
        super().__init__(loc)
