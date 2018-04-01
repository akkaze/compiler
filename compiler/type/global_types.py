from compiler.type import BoolType, IntegerType, VoidType, StringType, NullType

bool_type = BoolType()
integer_type = IntegerType()
void_type = VoidType()
string_type = StringType()
null_type = NullType()

def initialize_builtin_type():
    string_type.initialize_builtin_function()
    array_type.initialize_builtin_function()
