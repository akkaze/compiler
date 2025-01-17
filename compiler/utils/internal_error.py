from compiler.ast.location import Location

class InternalError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

