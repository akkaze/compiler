from compiler.ast import Node

class StmtNode(Node):
    location = None
    def __init__(self, loc):
        self.location = loc

