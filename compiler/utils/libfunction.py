from compiler.type import Type

LIB_PREFIX = '__lib_'
class LibFunction(object):
    entity = None
    
    def __init__(return_type, name, param_types, asm_name = None):
        param_entities = []
        if param_types:
            for param_type in param_types:
                param_entities.append(ParameterEntity(
                                        None, param_type, None))
        entity = FunctionEntity(None, return_type, 
                        name, param_entities, None)
        entity.is_libfunction = True
        if asm_name:
            entity.asm_name = asm_name
