from compiler.ast import DefinitionNode
from compiler.entity import ClassEntity

class ClassDefNode(DefinitionNode):
    entity = None
    def __init__(self, entity):
        super().__init__(entity.location, entity.name)
        self.entity = entity
    def accept(self, visitor):
        return visitor.visit(self)
