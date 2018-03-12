class SemanticError(Exception):
    def __init__(self, loc, msg):
        super().__init__(loc, msg)

