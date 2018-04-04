from compiler.ast import LHSNode
from compiler.ast import Location

class VariableNode(LHSNode):
    location = None
    name = ''
    entity = None
    this_pointer = None

    def __init__(self, *args):
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

    @property
    def type(self):
        return self.entity.type

    @property
    def is_member(self):
        return self.this_pointer != None
    def accept(self, visitor):
        return visitor.visit(self)
