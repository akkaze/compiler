from compiler.ir import Instruction

class Call(Instruction):
    entity = None
    operands = None
    ret = None
    caller_save = None
    used_parameter_register = None

    def __init__(self, entity, operands):
        self.entity = entity
        self.operands = operands
        self.ret = None
    def replace_use(self, from, to):
        new_operands = []
        for operand in self.operands:
            new_operands.append(operand.replace(from, to))
        self.operands = new_operands

        new_param_reg = set()
        for reference in self.used_parameter_register:
            new_param_reg.add(reference.replace(from, to))
        self.used_parameter_register = new_param_reg

    def replace_def(self, from, to):
        if self.ret:
            self.ret = self.ret.replace(from, to)

    def calc_def_and_use(self):
        if self.ret:
            self.ddef |= self.ret.get_all_ref()
        if self.caller_save:
            self.ddef |= self.caller_save
        if self.used_parameter_register:
            for param_reg in self.used_parameter_register:
                self.use |= param_reg.get_all_ref()
        self.all_ref |= self.use
        self.all_ref |= self.ddef

    def __str__(self):
        args = ''
        for operand in self.operands:
            args += ', ' + str(operand)
        return ret + ' = call ' + self.entity.asm_name + args
