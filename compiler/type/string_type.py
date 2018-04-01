from compiler.type import Type

STRING_CONSTANT_PREFIX = '__string_constant'

class StringType(Type):
    DEFAULT_SIZE = 8
    operator_and = None
    operator_eq = None
    operator_ne = None
    operator_lt = None
    operator_gt = None
    operator_ge = None
    operator_le = None
    scope = None
   
    @property
    def size(self):
        return self.DEFAULT_SIZE
    @property
    def is_string(self):
        return True
    def is_compatible(self, other):
        return other.is_string()
    @property
    def is_full_comparable(self):
        return True
    @property
    def is_half_comparable(self):
        return True
    def __str__(self):
        return 'string'
    @staticmethod 
    def initialize_builtin_function():
        StringType.operator_add = LibFunction(string_type, \
                    [string_type, string_type], \
                    LIB_PREFIX + 'str_operator_add').entity 
        StringType.operator_eq = LibFunction(string_type, 
                    [string_type, string_type],
                    LIB_PREFIX + 'str_operator_eq').entity 
        StringType.operator_ne = LibFunction(string_type, 
                    LIB_PREFIX + 'str_operator_ne',
                    [string_type, string_type]).entity
        StringType.operator_lt = LibFunction(string_type, 
                    [string_type, string_type],
                    LIB_PREFIX + 'str_operator_lt'); 
        StringType.operator_gt = LibFunction(string_type,  \
                    [string_type, string_type], \
                    LIB_PREFIX + 'str_operator_gt').entity 
        StringType.operator_ge = LibFunction(string_type, \
                    [string_type, string_type], \
                    LIB_PREFIX + 'str_operator_ge').entity 
        StringType.operator_le = LibFunction(string_type, \
                    [string_type, string_type], \
                    LIB_PREFIX + 'str_operator_le').entity 
        StringType.scope = Scope(True)
        StringType.scope.insert(LibFunction(integer_type, 'length', \
                    [string_type], LIB_PREFIX + 'str_length').entity)
        StringType.scope.insert(LibFunction(integer_type, 'substring', \
                    [string_type], LIB_PREFIX + 'str_substring').entity)
        StringType.scope.insert(LibFunction(integer_type, 'parseInt', \
                    [string_type], LIB_PREFIX + 'str_parseInt').entity)
        StringType.scope.insert(LibFunction(integer_type, 'ord', \
                    [string_type], LIB_PREFIX + 'str_ord').entity)
        StringType.scope.insert(StringType.operator_add)
        StringType.scope.insert(StringType.operator_lt)
        StringType.scope.insert(StringType.operator_eq)
