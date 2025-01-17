from compiler.ast import Node

class StmtNode(Node):
    def __init__(self, loc):
        super().__init__()
        self.location = loc
        
    def accept(self, visitor):
        pass
