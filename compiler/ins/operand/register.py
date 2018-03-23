class Register(Operand):
    name = ''
    low_name = ''
    is_callee_save = False

    def __init__(self, name, low_name):
        self.name = name
        self.low_name = low_name
    @property
    def is_caller_save(self):
        return not self.is_callee_save
    def replace(self, from, to):
        return self
    def get_all_ref(self):
        return set()
    @property
    def nasm(self):
        return self.name
