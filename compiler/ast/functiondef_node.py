from compiler.ast import DefinitionNode
from compiler.entity import FunctionEntity

class FunctionDefNode(DefinitionNode):
    entity = None
    def __init__(self, entity):
        super().__init__(entity.location, entity.name)
        self.entity = entity


