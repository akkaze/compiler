from compiler.typ.integer_type import IntegerType
from compiler.typ.class_type import ClassType
from compiler.typ.array_type import ArrayType
from compiler.typ.bool_type import BoolType
from compiler.typ.function_type import FunctionType
from compiler.typ.null_type import NullType
from compiler.typ.string_type import StringType
from compiler.typ.void_type import VoidType
from compiler.utils.libfunction import LibFunction, LIB_PREFIX
from compiler.entity.scope import Scope

bool_type = BoolType()
integer_type = IntegerType()
void_type = VoidType()
string_type = StringType()
null_type = NullType()


def initialize_string_type_builtin_function():
    StringType.operator_add = LibFunction(string_type,
                                          LIB_PREFIX + 'str_operator_add',
                                          [string_type, string_type]).entity
    StringType.operator_eq = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_eq',
                                         [string_type, string_type]).entity
    StringType.operator_ne = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_ne',
                                         [string_type, string_type]).entity
    StringType.operator_lt = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_lt',
                                         [string_type, string_type]).entity
    StringType.operator_gt = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_gt',
                                         [string_type, string_type]).entity
    StringType.operator_ge = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_ge',
                                         [string_type, string_type]).entity
    StringType.operator_le = LibFunction(string_type,
                                         LIB_PREFIX + 'str_operator_le',
                                         [string_type, string_type]).entity
    StringType.scope = Scope(True)
    StringType.scope.insert(LibFunction(integer_type, 'length',
                                        [string_type], LIB_PREFIX + 'str_length').entity)
    StringType.scope.insert(LibFunction(string_type, 'substring',
                                        [string_type, integer_type, integer_type], LIB_PREFIX + 'str_substring').entity)
    StringType.scope.insert(LibFunction(integer_type, 'parseInt',
                                        [string_type], LIB_PREFIX + 'str_parseInt').entity)
    StringType.scope.insert(LibFunction(integer_type, 'ord',
                                        [string_type, integer_type], LIB_PREFIX + 'str_ord').entity)
    StringType.scope.insert(StringType.operator_add)
    StringType.scope.insert(StringType.operator_lt)
    StringType.scope.insert(StringType.operator_eq)


def initialize_array_type_builtin_function():
    ArrayType.magic_array = ArrayType(null_type)
    ArrayType.scope = Scope(True)
    ArrayType.scope.insert(LibFunction(integer_type, 'size',
                                       [ArrayType.magic_array], LIB_PREFIX + 'array_size').entity)


def initialize_builtin_type():
    initialize_string_type_builtin_function()
    initialize_array_type_builtin_function()
