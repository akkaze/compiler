from compiler.ins import Instruction

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
        super().__init__()
    def replace_use(self, ffrom, to):
        new_operands = []
        for operand in self.operands:
            new_operands.append(operand.replace(ffrom, to))
        self.operands = new_operands

        new_param_reg = set()
        for reference in self.used_parameter_register:
            new_param_reg.add(reference.replace(ffrom, to))
        self.used_parameter_register = new_param_reg

    def replace_def(self, ffrom, to):
        if self.ret:
            self.ret = self.ret.replace(ffrom, to)

    def calc_def_and_use(self):
        if self.ret:
            self.m_ddef |= self.ret.get_all_ref()
        if self.caller_save:
            self.m_ddef |= self.caller_save
        for operand in self.operands:
            self.m_use |= operand.get_all_ref()
        if self.used_parameter_register:
            for param_reg in self.used_parameter_register:
                self.m_use |= param_reg.get_all_ref()
        self.m_all_ref |= self.m_use
        self.m_all_ref |= self.m_ddef

    def accept(self, translator):
        return translator.visit(self)
 
    def __str__(self):
        args = ''
        for operand in self.operands:
            args += ', ' + str(operand)
        ret_str = ''
        if self.ret:
            ret_str = str(self.ret)
        else:
            ret_str = 'none'
        return ret_str + ' = call ' + \
            self.entity.asm_name + args
