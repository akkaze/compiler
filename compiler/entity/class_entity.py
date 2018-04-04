from compiler.type import ClassType
from compiler.entity import Entity

class ClassEntity(Entity):
    member_vars = []
    member_funcs = []
    scope = None
    constructor = None
    class_type = None
    size = 0

    def __init__(self, loc, name, member_vars, member_funcs):
        super().__init__(loc, ClassType(name), name)
        self.member_vars = member_vars
        self.member_funcs = member_funcs
        self.type.entity = self
    
    
    def init_offset(self, alignment):
        self.size = self.scope.locate_member(alignment)
    
    def __str__(self):
        return 'class entity : ' + self.name
