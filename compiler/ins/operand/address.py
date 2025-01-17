from compiler.ins.operand import Operand
from compiler.utils.internal_error import InternalError

class Address(Operand):

    def __init__(self, *args):
        self.base = None
        self.index = None
        self.mul = 1
        self.add = 0
        self.show_size = True
        self.m_base_nasm = None
        self.m_index_nasm = None
        if len(args) == 1:
            self.base = args[0]
            if isinstance(self.base, Address):
                raise InternalError('nested address')
        elif len(args) == 4:
            self.base = args[0]
            self.index = args[1]
            self.mul = args[2]
            self.add = args[3]
            if isinstance(args[0], Address) or  isinstance(args[1], Address):
                raise InternalError('nested address')

    def get_all_ref(self):
        ret = set()
        if self.base:
            ret |= self.base.get_all_ref()
        if self.index:
            ret |= self.index.get_all_ref()
        return ret

    def replace(self, ffrom, to):
        if self.base:
            self.base = self.base.replace(ffrom, to)
        if self.index:
            self.index = self.index.replace(ffrom, to)
        return self

    @property
    def base_nasm(self):
        if self.m_base_nasm:
            return self.m_base_nasm
        else:
            return self.base
    @base_nasm.setter
    def base_nasm(self, value):
        self.m_base_nasm = value

    @property
    def index_nasm(self):
        if self.m_index_nasm:
            return self.m_index_nasm
        else:
            return self.index
    @index_nasm.setter
    def index_nasm(self, value):
        self.m_index_nasm = value

    @property
    def base_only(self):
        if self.base and self.index == None and self.mul == 1 and self.add == 0:
            return True
        return False

    @property
    def is_direct(self):
        if not self.base:
            return self.index.is_register
        if not self.index:
            return self.base.is_register
        else:
            return self.index.is_register and self.base.is_registr
    @property
    def is_address(self):
        return True
    @property
    def nasm(self):
        ret = ''
        gap = ''
        if self.show_size:
            ret += 'qword ['
        else:
            ret += '['
        if self.base:
            ret += gap + self.base_nasm.nasm
            gap = ' + '
        if self.index:
            ret += gap + self.index_nasm.nasm
            gap = ' + '
            if self.mul != 1:
                ret += ' * ' + str(self.mul)
        if self.add != 0:
            ret += gap + str(self.add)
        ret += ']'
        return ret

    def __hash__(self):
        hash_code = 0x93
        if self.base:
            hash_code *= hash(self.base)
        if self.index:
            hash_code *= hash(self.index)
        hash_code = hash_code * self.mul + self.add
        return hash_code

    def __eq__(self, o):
        if isinstance(o, Address):
            return self.base == o.base and self.index == o.index and \
                self.mul == o.mul and self.add == o.add
        return False

    def __str__(self):
        ret = ''
        gap = ''
        # if self.show_size:
        #     ret += 'qword ['
        # else:
        #     ret += '['
        ret += '['
        if self.base:
            ret += gap + str(self.base)
            gap = ' + '
        if self.index:
            ret += gap + str(self.index)
            gap = ' + '
            if self.mul != 1:
                ret += ' * ' + str(self.mul)
        if self.add != 0:
            ret += (gap + str(self.add))
        return ret + ']'
