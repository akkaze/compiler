from compiler.ast import LHSNode
from compiler.ast import Location

class VariableNode(LHSNode):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.entity = args[0]
        elif len(args) == 2:
            if isinstance(args[0], Location):
                self.location = args[0]
                self.name = args[1]
            else:
                self.entity = args[0]
                self.location = args[1]
                self.name = args[0].name
        self.this_pointer = None
        
    @property
    def type(self):
        return self.entity.type

    @property
    def is_member(self):
        return self.this_pointer != None
    def accept(self, visitor):
        return visitor.visit(self)

    def __str__(self):
        return self.name