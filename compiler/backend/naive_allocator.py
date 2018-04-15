from compiler.ins.operand import *
from compiler.options import options
import logging

class NaiveAllocator:
    function_entities = None
    rax = None
    rbx = None
    rcx = None
    rdx = None
    rsi = None
    rdi = None
    rsp = None
    rbp = None
    registers = None
    param_registers = None
    def __init__(self, emitter, register_config):
        self.function_entities = emitter.function_entities
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

    def allocate(self):
        for function_entity in self.function_entities:
            self.allocate_function(function_entity)

    def allocate_function(self, entity):
        all_ref = entity.all_reference
        for bb in entity.bbs:
            for ins in bb.ins:
                for ref in ins.use:
                    ref.ref_times += 1
                    all_ref.add(ref)
                for ref in ins.ddef:
                    ref.ref_times += 1
                    all_ref.add(ref)
        to_sort = sorted(all_ref, key = lambda x: -x.ref_times)
        to_allocate = [1, 12, 13, 14, 15]
        if options.print_naive_allocator_info:
            logging.error('naive allocator : ' + entity.name)
        for i in range(len(to_sort)):
            if i < len(to_allocate):
                ref = to_sort[i]
                if ref.type == Reference.Type.GLOBAL:
                    continue

                ref.set_register(self.registers[to_allocate[i]])
                entity.reg_used.append(self.registers[to_allocate[i]])

                if options.print_naive_allocator_info:
                    logging.error(ref.name + ' -> ' + str(ref.reg))
        entity.reg_used.append(self.rbp)

        # === Frame layout === 
        # virtual stack
        # local variable
        # parameter
        # -----------------<-bp
        # save regs
        # return address
        lvar_base = 0
        stack_base = 0
        saved_temp_base = 0
        params = entity.params
        for i in range(len(params)):
            param = params[i]
            ref = param.reference
            if i < len(self.param_registers):
                lvar_base += param.type.size
                param.reference.set_offset(-lvar_base, self.rbp)
            else:
                ref.alias = param.source
        stack_base = lvar_base
        stack_base += entity.scope.locate_local_variable(\
                        lvar_base, options.STACK_VAR_ALIGNMENT_SIZE)
        for var in entity.scope.all_local_variables():
            var.reference.set_offset(-var.offset, self.rbp)

        tmp_stack = entity.tmp_stack
        saved_tmp_base = stack_base
        for i in range(len(tmp_stack)):
            tmp = tmp_stack[i]
            if tmp.is_unknown:
                saved_tmp_base += options.REG_SIZE
                tmp.set_offset(-saved_tmp_base, self.rbp)
        entity.local_variable_offset = saved_tmp_base
