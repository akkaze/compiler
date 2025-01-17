from compiler.entity import *
from compiler.ins import *
from compiler.ins.operand import *
from compiler.options import options
from compiler.entity.variable_entity import VariableEntity
from compiler.entity.string_const_entity import StringConstEntity
global options


class Translator:
    GLOBAL_PREFIX = '__global__'

    def __init__(self, emitter, register_config):
        self.asm = []
        self.function_entities = emitter.function_entities
        self.global_scope = emitter.global_scope
        self.global_initializer = emitter.global_initializer
        self.registers = register_config.registers
        self.param_registers = register_config.param_registers

        self.rax = self.registers[0]
        self.rbx = self.registers[1]
        self.rcx = self.registers[2]
        self.rdx = self.registers[3]
        self.rsi = self.registers[4]
        self.rdi = self.registers[5]
        self.rbp = self.registers[6]
        self.rsp = self.registers[7]

    def translate(self):
        self.add('global main')
        self.add("extern printf, scanf, puts, gets, sprintf, sscanf, getchar, strlen, strcmp, strcpy, strncpy, malloc, memcpy")
        self.add('section .data')
        for name, entity in self.global_scope.entities.items():
            if isinstance(entity, VariableEntity):
                self.add_label(Translator.GLOBAL_PREFIX + entity.name)
                self.add('dq 0')
            elif isinstance(entity, StringConstEntity):
                name = entity.asm_name
                value = entity.value
                self.add('dd ' + str(len(value)))
                self.add_label(name)
                tmp_str = 'db'
                for i in range(len(value)):
                    tmp_str += ' '
                    x = ord(value[i])
                    tmp_str += str(x)
                    tmp_str += ','
                tmp_str += ' 0'
                self.add(tmp_str)
        self.add('')

        self.add('section .text')
        for entity in self.function_entities:
            if entity.is_inlined:
                continue
            self.locate_frame(entity)
            self.add('ALIGN 16')
            self.translate_function(entity)
            self.add('')

        self.paste_libfunctions()
        return self.asm

    def locate_frame(self, entity):
        saved_reg_num = 0
        for reg in entity.reg_used:
            if reg.is_callee_save:
                saved_reg_num += 1
        param_base = 0
        lvar_base = param_base
        total = 0
        # last for retrun address
        source_base = saved_reg_num * options.REG_SIZE + \
            options.REG_SIZE
        params = entity.params
        for i in range(len(params)):
            param = params[i]
            ref = param.reference
            if i < len(self.param_registers):
                param.source.set_register(self.param_registers[i])
                if ref.is_unknown:
                    logging.info('unset parameter ' + ref.name)
            else:
                param.source.set_offset(source_base, self.rbp)
                source_base += param.type.size
                if ref.is_unknown:
                    ref.set_offset(param.source.offset,
                                   param.source.reg)
        total = lvar_base + entity.local_variable_offset
        total += (options.FRAME_ALIGNMENT_SIZE -
                  (total + options.REG_SIZE +
                   options.REG_SIZE * saved_reg_num) %
                  options.FRAME_ALIGNMENT_SIZE) % \
            options.FRAME_ALIGNMENT_SIZE

        entity.frame_size = total

    def translate_function(self, entity):
        self.add_label(entity.asm_name)
        start_pos = len(self.asm)
        for bb in entity.bbs:
            for ins in bb.ins:
                ins.accept(self)
            if bb.label == entity.end_label_ins:
                if len(entity.calls) != 0 and entity.frame_size != 0:
                    self.add('add', self.rsp, Immediate(entity.frame_size))
                for i in range(len(entity.reg_used) - 1, -1, -1):
                    reg = entity.reg_used[i]
                    if reg.is_callee_save:
                        self.add('pop', reg)
                self.add('ret')

        prologue = None
        backup = self.asm
        self.asm = []

        for reg in entity.reg_used:
            if reg.is_callee_save:
                self.add('push', reg)

        if self.rbp in entity.reg_used:
            self.add('mov', self.rbp, self.rsp)
        if len(entity.calls) != 0 and entity.frame_size != 0:
            self.add('sub', self.rsp, Immediate(entity.frame_size))

        if not options.enable_global_register_allocation:
            params = entity.params
            for param in params:
                if not param.reference == param.source:
                    if not param.reference.is_address:
                        self.add('mov', param.reference, param.source)
                    else:
                        self.add('mov', self.rcx, param.source)
                        self.add('mov', param.reference, self.rcx)
        self.add('')

        prologue = self.asm
        self.asm = backup
        for i in range(len(prologue)):
            self.asm.insert(start_pos + i, prologue[i])
        del prologue

    def add(self, *args):
        if len(args) == 1:
            self.asm.append('\t' + args[0])
        elif len(args) == 2:
            op = args[0]
            l = args[1]
            s = l.nasm
            if op == 'idiv':
                if l.is_address:
                    s = s.replace('qword', 'dword')
                else:
                    if s == 'rax' or s == 'rbx' or s == 'rcx' or \
                            s == 'rdx' or s == 'rsi' or s == 'rdi' or \
                            s == 'rsp' or s == 'rbp':
                        s = s.replace('r', 'e')
                    else:
                        s = s + 'd'
                self.asm.append('\t' + op + ' ' + s)
            else:
                self.asm.append('\t' + op + ' ' + l.nasm)
        elif len(args) == 3:
            op = args[0]
            l = args[1]
            r = args[2]
            if op == 'mov' and l.nasm == r.nasm:
                return
            else:
                self.asm.append('\t' + op + ' ' +
                                l.nasm + ', ' + r.nasm)

    def add_label(self, name):
        self.asm.append(name + ':')

    def add_jump(self, name):
        self.asm.append('\tjmp' + ' ' + name)

    def add_move(self, reg, operand):
        if operand.is_direct:
            self.add('mov', reg, operand)
        else:
            if operand.base.is_register:
                self.add('mov', reg, operand.base)
                self.add('mov', reg, Address(reg))
            elif operand.base.is_offset:
                self.add('mov', self.rcx, operand.base)
                self.add('mov', reg, Address(
                    self.rcx, operand.index, operand.mul, operand.add))
        return 0

    def left_can_be_memory(self, name):
        return name == 'add' or name == 'sub' or name == 'sor'

    def visit_compare(self, left, right):
        if left.is_direct and right.is_direct and \
                not (left.is_address and right.is_address):
            self.add('cmp', left, right)
        else:
            self.add_move(self.rax, left)
            if right.is_direct:
                self.add('cmp', self.rax, right)
            else:
                self.add_move(self.rdx, right)
                self.add('cmp', self.rax, self.rdx)

    def simplify_address(self, addr, reg1, reg2):
        if not addr.index:
            if addr.base.is_register:
                return 0
            else:
                self.add_move(reg1, addr.base)
                addr.base_nasm = reg1
                return 1
        else:
            if addr.base.is_register:
                if addr.index.is_register:
                    return 0
                else:
                    self.add_move(reg1, addr.index)
                    addr.index_nasm = reg1
            else:
                self.add_move(reg1, addr.base)
                addr.base_nasm = reg1
                if addr.index.is_register:
                    return 1
                else:
                    self.add_move(reg2, addr.index)
                    addr.index_nasm = reg2
                    return 2

    def is_address(self, operand):
        if isinstance(operand, Address):
            return True
        elif isinstance(operand, Reference):
            if operand.type == Reference.Type.SPECIAL:
                return False
            return not operand.is_register
        else:
            return False

    def visit(self, ins):
        if isinstance(ins, Bin) and \
                not (isinstance(ins, Div) or isinstance(ins, Mod) or isinstance(ins, Sal) or isinstance(ins, Sar)):
            left = ins.left
            right = ins.right
            name = ins.name
            if left.is_register or (left.is_direct and self.left_can_be_memory(name) and not right.is_address):
                if right.is_direct:
                    if left.is_address and right.is_address:
                        self.add_move(self.rax, right)
                        self.add(name, left, self.rax)
                    else:
                        self.add(name, left, right)
                else:
                    if right.base_only:
                        self.add_move(self.rax, right.base)
                        self.add(name, left, Address(self.rax))
                    else:
                        raise InternalError('Unhandled case in bin')
            else:
                if right.is_direct:
                    self.add_move(self.rax, left)
                    self.add(name, self.rax, right)
                    self.add('mov', left, self.rax)
                else:
                    self.add('mov', self.rax, left)
                    self.add_move(self.rdx, right)
                    self.add(name, self.rax, self.rdx)
        elif isinstance(ins, Div) or isinstance(ins, Mod):
            reg = None
            left = ins.left
            right = ins.right
            if isinstance(ins, Div):
                reg = self.rax
            else:
                reg = self.rdx
            self.add_move(self.rax, left)
            self.add('cdq')
            if isinstance(right, Address):
                right.show_size = True
            if right.is_direct and not isinstance(right, Immediate):
                self.add('idiv', right)
            else:
                self.add_move(self.rcx, right)
                self.add('idiv', self.rcx)
            if not options.enable_global_register_allocation:
                self.add('mov', left, reg)
        elif isinstance(ins, Neg):
            self.add('neg', ins.operand)
        elif isinstance(ins, Not):
            self.add('not', ins.operand)
        elif isinstance(ins, Sal) or isinstance(ins, Sar):
            if isinstance(ins.right, Immediate):
                self.add(ins.name + ' ' + ins.left.nasm +
                         ', ' + ins.right.nasm)
            else:
                self.add_move(self.rcx, ins.right)
                self.add(ins.name + ' ' + ins.left.nasm + ', cl')
        elif isinstance(ins, Cmp):
            left = ins.left
            right = ins.right
            self.visit_compare(left, right)
            set = ''

            op = ins.operator
            if op == Cmp.Operator.EQ:
                set = 'sete'
            elif op == Cmp.Operator.NE:
                set = 'setne'
            elif op == Cmp.Operator.GE:
                set = 'setge'
            elif op == Cmp.Operator.GT:
                set = 'setg'
            elif op == Cmp.Operator.LE:
                set = 'setle'
            elif op == Cmp.Operator.LT:
                set = 'setl'
            if options.enable_global_register_allocation:
                reg = left.reg
                self.add(set + ' ' + reg.low_name)
                self.add('movzx ' + reg.name + ', ' + reg.low_name)
            else:
                self.add(set + ' al')
                self.add('movzx rax, al')
                self.add('mov', left, self.rax)
        elif isinstance(ins, Move):
            is_add_left = self.is_address(ins.dest)
            is_add_right = self.is_address(ins.src)
            if options.enable_global_register_allocation:
                self.add('mov', ins.dest, ins.src)
            else:
                if is_add_left and is_add_right:
                    if isinstance(ins.src, Address) or isinstance(ins.dest, Address):
                        if isinstance(ins.src, Address):
                            self.simplify_address(
                                ins.src, self.rax, self.rdx)
                        self.add('mov', self.rdx, ins.src)
                        if isinstance(ins.dest, Address):
                            self.simplify_address(
                                ins.dest, self.rax, self.rcx)
                        self.add('mov', ins.dest, self.rdx)
                    else:
                        self.add_move(self.rcx, ins.src)
                        self.add('mov', ins.dest, self.rcx)
                else:
                    if isinstance(ins.dest, Address):
                        self.simplify_address(
                            ins.dest, self.rax, self.rcx)
                    if isinstance(ins.src, Address):
                        self.simplify_address(
                            ins.src, self.rax, self.rcx)
                    self.add('mov', ins.dest, ins.src)
        elif isinstance(ins, Lea):
            if not options.enable_global_register_allocation:
                self.simplify_address(ins.addr, self.rax, self.rcx)
            ins.addr.show_size = False
            if ins.dest.is_register:
                self.add('lea', ins.dest, ins.addr)
            else:
                self.add('lea', self.rax, ins.addr)
                self.add('mov', ins.dest, self.rax)
        elif isinstance(ins, Call):
            operands = ins.operands
            for i in range(len(operands) - 1, -1, -1):
                if i < len(self.param_registers):
                    self.add_move(self.param_registers[i], operands[i])
                else:
                    if operands[i].is_register:
                        self.add('push', operands[i])
                    else:
                        self.add_move(self.rax, operands[i])
                        self.add('push', self.rax)
            self.add('call ' + ins.entity.asm_name)
            if len(operands) > len(self.param_registers):
                self.add('add', self.rsp, Immediate(
                    (len(operands) - len(self.param_registers)) * options.REG_SIZE))
            if ins.ret:
                self.add('mov', ins.ret, self.rax)
        elif isinstance(ins, Return):
            if ins.ret:
                self.add_move(self.rax, ins.ret)
        elif isinstance(ins, CJump):
            if ins.type == CJump.Type.BOOL:
                if isinstance(ins.cond, Immediate):
                    if ins.cond.value != 0:
                        self.add_jump(ins.true_label.name)
                    else:
                        self.add_jump(ins.false_label.name)
                else:
                    if ins.cond.is_register:
                        self.add('test', ins.cond, ins.cond)
                    else:
                        self.add_move(self.rax, ins.cond)
                        self.add('test', self.rax, self.rax)
                    if ins.fall_through == ins.true_label:
                        self.add('jz ' + ins.false_label.name)
                    elif ins.fall_through == ins.false_label:
                        self.add('jnz ' + ins.true_label.name)
                    else:
                        self.add('jnz ' + ins.true_label.name)
                        self.add_jump(ins.false_label.name)
            else:
                name = ins.name
                left = ins.left
                right = ins.right
                if isinstance(left, Immediate):
                    t = left
                    left = right
                    right = t
                    name = CJump.relect(name)
                self.visit_compare(left, right)
                if ins.fall_through == ins.true_label:
                    name = CJump.not_name(name)
                    self.add(name + ' ' + ins.false_label.name)
                elif ins.fall_through == ins.false_label:
                    self.add(name + ' ' + ins.true_label.name)
                else:
                    self.add(name + ' ' + ins.true_label.name)
                    self.add_jump(ins.false_label.name)
        elif isinstance(ins, Jmp):
            self.add_jump(ins.dest.name)
        elif isinstance(ins, Label):
            self.add_label(ins.name)
        elif isinstance(ins, Push):
            if not ins.operand.is_register:
                raise InternalError('push ' +
                                    str(ins.operand) + ' is not register')
            self.add('push', ins.operand)
        elif isinstance(ins, Pop):
            if not ins.operand.is_register:
                raise InternalError('pop ' +
                                    str(ins.operand) + ' is not register')
            self.add('pop', ins.operand)

    def left_can_be_memory(self, name):
        return name == "add" or name == "sub" or name == "xor"

    def paste_libfunctions(self):
        from pathlib import Path
        cur_path = Path(__file__)
        lib_path = cur_path.parent.parent / 'lib' / 'lib.s'
        with open(lib_path) as lib_file:
            lib_lines = lib_file.readlines()
        self.add("\n;========== LIB BEGIN ==========")
        for lib_line in lib_lines:
            self.add(lib_line)
