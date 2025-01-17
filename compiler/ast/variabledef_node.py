from compiler.ast import DefinitionNode

class VariableDefNode(DefinitionNode):
    def __init__(self, entity):
        super().__init__(entity.location, entity.name)
        self.entity = entity
    def accept(self, visitor):
        return visitor.visit(self)
