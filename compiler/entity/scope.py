from compliler.utils.semantic_error import *

class Scope(object):
    entities = dict()
    children = []
    parent = None
    is_top_level = False
    
    def __init__(self, parent):
        self.parent = parent
        self.is_top_level = (parent == None)
        if self.parent != None:
            parent.add_children(self)
    
    def insert(self, entity):
        if self.entities.get(entity.name) != None:
            raise SemanticError(entity.location, "duplicated symbol:" +
                                                    entity.name)
        self.entities[entity.name] = entity
    
    def lookup(self, name):
        entity = self.entities.get(name)
        if entity == None:
            return self.is_top_level ? None : self.parent.lookup(name)
        else:
            return entity
    
    def loopup_current_level(self, name):
        return self.entities.get(name)
    
    def add_children(self, s):
        return self.children.append(s)
    
    def locate_local_variable(base, align):
        offset = 0
        for name, entity in entities.items():
            if isinstance(entity, VariableEntity):
                offset += entity.type.size()
                entity.set_offset(offset + base)
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
        for name, entity in entities.items():
            if !isinstance(entity, FunctionEntity):
                entity.set_offset(offset)
                offset += entity.size()
                offset += (align - offset % align) % align
        return offset
    
    # all variable entities
    def all_local_variables(self):
        ret = []
        for name, entity in entities.items(():
            if isinstance(entity, VariableEntity):
                ret.append(entity)
        for child in children:
            ret.extend(child.all_local_variables())
        return ret
    # all entities
    def gather_all(self):
        ret = []
        for name, entity in entities.items():
            if isinstance(entity, FunctionEntity):
                if not entity.is_libfunction():
                    ret.extend(entity.params())
            ret.append(entity)
        
        for child in children:
            ret.extend(child.all_local_variables())
        return ret
