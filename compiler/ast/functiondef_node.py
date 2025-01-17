from compiler.ast.definition_node import DefinitionNode
from compiler.entity.function_entity import FunctionEntity

class FunctionDefNode(DefinitionNode):
    entity = None
    def __init__(self, entity):
        super().__init__(entity.location, entity.name)
        self.entity = entity
    def accept(self, visitor):
        return visitor.visit(self)
