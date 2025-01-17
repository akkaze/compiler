from compiler.entity.function_entity import FunctionEntity
from compiler.entity.parameter_entity import ParameterEntity

LIB_PREFIX = '__lib_'
class LibFunction(object):
    entity = None
    
    def __init__(self, return_type, name, param_types, asm_name = None):
        param_entities = []
        if param_types:
            for param_type in param_types:
                param_entities.append(ParameterEntity(
                                        None, param_type, None))
        self.entity = FunctionEntity(None, return_type, 
                        name, param_entities, None)
        self.entity.is_libfunction = True
        if asm_name:
            self.entity.asm_name = asm_name
