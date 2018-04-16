class Operand(object):
    nasm = 'operand'

    def get_all_ref(self):
        pass
    def replace(self, ffrom, to):
        pass
    @property
    def is_register(self):
        return False
    @property
    def is_direct(self):
        return False
    @property
    def is_address(self):
        return False
    @property
    def is_const_int(self):
        return False
