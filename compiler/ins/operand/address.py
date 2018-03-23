class Address(Operand):
    base = None
    index = None
    mul = 1
    add = 0
    show_size = True
    base_nasm = None
    index_nasm = None
    def __init__(self, *args):
        if len(args) == 1:
            self.base = args[0]
            if isinstance(base, Address):
                raise InternalError('nested address')
        elif len(args) == 4:
            self.base = args[0]
            self.index = args[1]
            self.mul = args[2]
            self.add = args[3]

            if isinstance(args[0], Address) or  \
                isinstance(args[1], Address):
                raise InternalError('nested address')
    def get_all_ref(self):
        ret = set()
        if self.base:
            ret |= self.base.get_all_ref()
        if self.index:
            ret |= self.index.get_all_ref()
        return ret

    def replace(self, from, to):
        if self.base:
            self.base = self.base.replace(from, to)
        elif self.index:
            self.index = self.index.replace(from, to)
        return self

    @property
    def base_nasm(self):
        if self.base_nasm:
            return self.base_nasm
        else:

            return base
    @property
    def base_only(self):
        if self.base and self.index and \
            self.mul == 1 and self.add == 0:
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
        return ret + ']'

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
        return ret + ']'
