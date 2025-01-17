from compiler.ast.definition_node import DefinitionNode
from compiler.entity.class_entity import ClassEntity


class ClassDefNode(DefinitionNode):
    def __init__(self, entity):
        super().__init__(entity.location, entity.name)
        self.entity = entity

    def accept(self, visitor):
        return visitor.visit(self)
