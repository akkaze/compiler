from compiler.utils import SemanticError
from compiler.entity import VariableEntity, FunctionEntity

class Scope(object):
    entities = None
    children = None
    parent = None
    is_top_level = False
    
    def __init__(self, arg):
        self.children = []
        self.entities = dict()
        if isinstance(arg, bool):
            self.is_top_level = True
        elif isinstance(arg, Scope):
            self.parent = arg
            self.is_top_level = (arg == None)
            if self.parent:
                self.parent.add_children(self)
    
    def insert(self, entity):
        if self.entities.get(entity.name):
            raise SemanticError(entity.location, "duplicated symbol:" \
                                + entity.name)
        self.entities[entity.name] = entity
    
    def lookup(self, name):
        entity = self.entities.get(name)
        if not entity:
            if self.is_top_level:
                return None
            else:
                return self.parent.lookup(name)
        else:
            return entity
    
    def lookup_current_level(self, name):
        return self.entities.get(name)
    
    def add_children(self, s):
        return self.children.append(s)
    
    def locate_local_variable(self, base, align):
        offset = 0
        for name, entity in self.entities.items():
            if isinstance(entity, VariableEntity):
                offset += entity.type.size
                entity.offset = offset + base
                offset += (align - offset % align) % align
        
        maxi = 0
        for child in self.children:
            tmp = child.locate_local_variable(base + offset, align)
            if tmp > maxi:
                maxi = tmp
        return offset + maxi
    
    # set offset in class 
    def locate_member(self, align):
        offset = 0
        for name, entity in self.entities.items():
            if not isinstance(entity, FunctionEntity):
                entity.offset = offset
                offset += entity.size
                offset += (align - offset % align) % align
        return offset
    
    # all variable entities
    def all_local_variables(self):
        ret = []
        for name, entity in self.entities.items():
            if isinstance(entity, VariableEntity):
                ret.append(entity)
        for child in self.children:
            ret.extend(child.all_local_variables())
        return ret
    # all entities
    def gather_all(self):
        ret = []
        for name, entity in self.entities.items():
            if isinstance(entity, FunctionEntity):
                if not entity.is_libfunction:
                    ret.extend(entity.params)
            ret.append(entity)
        
        for child in self.children:
            ret.extend(child.all_local_variables())
        return ret
