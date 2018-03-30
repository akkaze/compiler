import compiler
from compiler.ins import *
from compiler.ins.operand import *
from compiler.entity import *
from compiler.utils import *
from compiler.options import options
import copy
import logging

class InstructionEmmiter(object):
    function_entities = None
    global_scope = None
    global_inititalizer = None

    ins = None
    current_function = None
    is_in_leaf = False

    global_local_map = None
    used_global = None

    label_map = None
    tmp_counter = 0
    tmp_stack = None
    def __init__(self, ir_builder):
        self.global_local_map = dict()
        self.used_global = set()
        self.label_map = dict()
        self.tmp_stack = []
        self.ins = []
        self.global_scope = ir_builder.global_scope
        self.function_entities = ir_builder.function_entities
        for entity in ir_builder.ast.class_entities:
            for functiondef_node in entity.member_funcs:
                self.function_entities.append(functiondef_node.entity)
        self.global_initializer = ir_builder.global_initializer

    def emit(self):
        string_counter = 1
        for name, entity in self.global_scope.entities.items():
            if isinstance(entity, VariableEntity):
                entity.reference = Reference(entity.name, Reference.Type.GLOBAL)
            elif isinstance(entity, StringConstantEntity):
                string_counter += 1
                entiy.asm_name = STRING_CONSTANT_ASM_LABEL_PREFIX + \
                                str(string_counter)
        
        for function_entity in self.function_entities:
            self.current_function = function_entity
            self.tmp_stack = []
            function_entity.ins = self.emit_function(function_entity)
            function_entity.tmp_stack = self.tmp_stack

    def emit_function(self, entity):
        global options
        if entity.is_inlined:
            return
        call_size = len(entity.calls)
        for called in entity.calls:
            if called.is_inlined or called.is_libfunction:
                call_size -= 1
        if options.enable_leaf_function_optimization \
            and call_size == 0:
            self.is_in_leaf = True
            logging.error(entity.name + ' is leaf')
            self.used_global = set()
            for name, glob in self.global_scope.entities.items():
                if isinstance(glob, VariableEntity):
                    local = VariableEntity(glob.location, glob.type, \
                                'g_' + glob.name, None)
                    self.global_local_map[glob] = local
                    self.current_function.scope.insert(local)
                else:
                    self.is_in_leaf = False
        for parameter_entity in entity.params:
            parameter_entity.reference = Reference(parameter_entity)
            parameter_entity.source = Reference(parameter_entity.name + '_src', \
                Reference.Type.CANNOT_COLOR)
        for variable_entity in entity.all_local_variables():
            variable_entity.reference = Reference(variable_entity)
        entity.set_label_ins(self.get_label(entity.begin_label_ir.name), \
                            self.get_label(entity.end_label_ir.name))
        self.ins = []
        for ir in entity.irs:
            self.tmp_top = 0
            self.expr_depth = 0
            ir.accept(self)
        if self.is_in_leaf:
            for glob in self.used_global:
                self.ins.insert(0, Move(self.trans_entity(glob)).reference, \
                    glob.reference)
                self.ins.insert(len(self.ins), Move(glob.reference, \
                    self.trans_entity(glob).reference))
        return self.ins

    def is_powerof2(self, ir):
        if isinstance(ir, IntConst):
            x = ir.value
            return x == 1 or x == 2 or x == 4 or x == 8
        return False

    class AddressTuple(object):
        base = None
        index = None
        mul = 0
        add = 0
        def __init__(self, base, index, mul, add):
            self.base = base
            self.index = index
            self.mul = mul
            self.add = add

    mathch_simple_add = False
    def match_base_index_mul(self, expr):
        if not isinstance(expr, compiler.ir.Binary):
            return
        bin = expr
        base = None
        index = None
        matched = False
        if bin.operator == compiler.ir.Binary.BinaryOp.ADD:
            if isinstance(bin.right, Binary) and \
                bin.right.operator == compiler.ir.Binary.BinaryOp.MUL:
                base = bin.left
                right = bin.right
                if self.is_powerof2(right.right):
                    index = right.left
                    mul = right.right.value
                    matched = True
                elif self.is_powerof2(right.left):
                    index = right.right
                    mul = right.left.value
                    matched = True
            elif isinstance(bin.left, Binary) and \
                bin.left.operator == compiler.ir.Binary.BinaryOp.MUL:
                base = bin.right
                left = bin.left
                if self.is_powerof2(left.right):
                    index = left.left
                    mul = left.right.value
                    matched = True
                elif self.is_powerof2(left.left):
                    index = left.right
                    mul = left.left.value
                    matched = True
            elif self.match_simple_add:
                base = bin.left
                index = bin.right
                mul = 1
                matched = True
        if matched:
            return (base, index, mul)
        else:
            return
    
    def match_address(self, expr):
        global options
        if not options.enable_instruction_selection:
            return
        if not isinstance(expr, compiler.ir.Binary):
            return
        bin = expr
        base = None
        index = None
        mul = 1
        add = 0
        matched = False
        base_index_mul = None

        if bin.operator == compiler.ir.Binary.BinaryOp.ADD:
            if isinstance(bin.right, compiler.ir.IntConst):
                add = bin.right.value
                base_index_mul = self.match_base_index_mul(bin.left)
                if base_index_mul:
                    matched = True
                else:
                    base = bin.left
            elif isinstance(bin.left, compiler.ir.IntConst):
                add = bin.left.value
                base_index_mul = self.match_base_index_mul(bin.right)
                if base_index_mul:
                    matched = True
                else:
                    base = bin.right
            else:
                base_index_mul = self.match_base_index_mul(bin)
                if base_index_mul:
                    matched = True
            if base_index_mul:
                base = base_index_mul[0]
                index = base_index_mul[1]
                mul = base_index_mul[2]
        if matched:
            if base != None and self.match_address(base) != None:
                return
            if index != None and self.match_address(index) != None:
                return
            return AddressTuple(base, index, mul, add)
        else:
            return

    expr_depth = 0
    def visit_expr(self, ir):
        matched = False
        ret = None

        self.expr_depth += 1
        addr = None

        addr = self.match_address(ir)
        if addr:
            base = self.visit_expr(addr.base)
            index = None
            if addr.index:
                index = self.visit_expr(addr.index)
                index = self.eliminate_address(index)
            base = self.eliminate_address(base)
            
            ret = self.get_tmp()
            self.ins.append(Lea(ret, Address(base, index, \
                        addr.mul, addr.add)))
            matched = True
        if not matched:
            ret = ir.accept(self)
        self.expr_depth -= 1
        return ret

    def visit(self, ir):
        if isinstance(ir, compiler.ir.Addr):
            raise InternalError('')
        elif isinstance(ir, compiler.ir.Assign):
            dest = None
            if isinstance(ir.left, compiler.ir.Addr):
                dest = self.trans_entity(ir.left.entity).reference
            else:
                lhs = self.visit_expr(ir.left)
                lhs = self.eliminate_address(lhs)
                dest = Address(lhs)
            self.expr_depth += 1
            rhs = self.visit_expr(ir.right)
            self.expr_depth -= 1
            if dest.is_address and rhs.is_address:
                tmp = self.get_tmp()
                self.ins.append(Move(tmp, rhs))
                self.ins.append(Move(dest, tmp))
            else:
                self.ins.append(Move(dest, rhs))
            return
        elif isinstance(ir, compiler.ir.Binary):
            ret = None
            left = ir.left
            right = ir.right
            op = ir.operator

            if self.is_commutative(op) and \
                isinstance(left, compiler.ir.IntConst):
                t = left
                left = right
                right = t
            if op == compiler.ir.Binary.BinaryOp.MUL:
                if isinstance(right, IntConst) and \
                    self.log2(right.value) != -1:
                    op = compiler.ir.Binary.BinaryOp.LSHIFT
                    right = IntConst(math.log2(right.value))
            elif op == compiler.ir.Binary.BinaryOp.DIV:
                if isinstance(right, IntConst) and \
                    self.log2(right.value) != -1:
                    op = compiler.ir.Binary.BinaryOp.RSHIFT
                    right = IntConst(math.log2(right.value))
            ret = self.visit_expr(left)
            rrr = self.visit_expr(right)
            ret = self.add_binary(op, ret, rrr)
            return ret
        elif isinstance(ir, compiler.ir.Call):
            operands = []
            for arg in ir.args:
                self.expr_depth += 1
                arg = self.visit_expr(arg)
                if arg:
                    operands.append(arg)
                self.expr_depth -= 1
            ret = None
            call = Call(ir.entity, operands)
            if self.expr_depth != 0:
                ret = self.get_tmp()
                call.ret = ret
            self.ins.append(call)
            return ret
        elif isinstance(ir, compiler.ir.CJump):
            if isinstance(ir.cond, compiler.ir.Binary) and \
                self.is_compare_op(ir.cond.operator):
                left = self.visit_expr(ir.cond.left)
                right = self.visit_expr(ir.cond.right)
                type = None
                if ir.cond.operator == compiler.ir.Binary.BinaryOp.EQ:
                    type = CJump.Type.EQ
                elif ir.cond.operator == compiler.ir.Binary.BinaryOp.NE:
                    type = CJump.Type.NE
                elif ir.cond.operator == compiler.ir.Binary.BinaryOp.GT:
                    type = CJump.Type.GT
                elif ir.cond.operator == compiler.ir.Binary.BinaryOp.GE:
                    type = CJump.Type.GE
                elif ir.cond.operator == compiler.ir.Binary.BinaryOp.LT:
                    type = CJump.Type.LT
                elif ir.cond.operator == compiler.ir.Binary.BinaryOp.LE:
                    type = CJump.Type.LE
                else:
                    raise InternalError('invalid compare operator')
                 
                if left.is_address:
                    tmp = self.get_tmp()
                    self.ins.append(Move(tmp, left))
                    left = tmp
                    self.ins.append(CJump(left, right, type, \
                        self.get_label(ir.true_label.name), \
                        self.get_label(ir.false_label.name)))
                else:
                    cond = self.visit_expr(ir.cond)
                    if isinstance(cond, Immediate):
                        if cond.value != 0:
                            self.ins.append(Jump(self.get_label(\
                                ir.true_label.name)))
                        else:
                            self.ins.append(Jump(self.get_label(\
                                ir.false_label.name)))
                    else:
                        if cond.is_address:
                            tmp = self.get_tmp()
                            self.ins.append(Move(tmp, cond))
                            cond = tmp
                        self.ins.append(CJump(cond, self.get_label(\
                            ir.false_label.name)))
            return
        elif isinstance(ir, compiler.ir.Jump):
            self.ins.append(Jmp(self.get_label(ir.label.name)))
            return
        elif isinstance(ir, compiler.ir.Label):
            self.ins.append(self.get_label(ir.name))
            return
        elif isinstance(ir, compiler.ir.Return):
            if not ir.expr:
                self.ins.append(Return(None))
            else:
                ret = self.visit_expr(ir.expr)
                self.ins.append(Return(ret))
            return
        elif isinstance(ir, compiler.ir.Unary):
            ret = self.visit_expr(ir.expr)
            ret = self.get_lvalue(ret)
            if ir.operator == Unary.UnaryOp.MINUS:
                self.ins.append(Neg(ret))
            elif ir.operator == Unary.UnaryOp.BIT_NOT:
                self.ins.append(Not(ret))
            elif ir.operator == Unary.UnaryOp.LOGIC_NOT:
                self.ins.append(Xor(ret, Immediate(1)))
            else:
                raise InternalError('invalid operator ' \
                    + str(ir.operator))
            return ret
        elif isinstance(ir, compiler.ir.Mem):
            addr = self.match_address(ir.expr)
            if addr:
                base = self.visit_expr(addr.base)
                index = None
                if addr.index:
                    index = self.visit_expr(addr.index)
                    index = self.eliminate_address(index)
                base = self.eliminate_address(base)
                ret = self.get_tmp()

                self.ins.append(Move(ret, Address(\
                    base, index, addr.mul, addr.add)))
                return ret
            else:
                expr = self.visit_expr(ir.expr)
                expr = self.eliminate_address(expr)
                return Address(expr)
        elif isinstance(ir, compiler.ir.StrConst):
            return Immediate(ir.entity.asm_name)
        elif isinstance(ir, compiler.ir.IntConst):
            return Immediate(ir.value)
        elif isinstance(ir, compiler.ir.Var):
            if ir.entity.name == 'null':
                return Immediate(0)
            else:
                return self.trans_entity(ir.entity).reference


    def add_binary(self, operator, left, right):
        left = self.get_lvalue(left)
        if operator == compiler.ir.Binary.BinaryOp.ADD:
            self.ins.append(Add(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.SUB:
            self.ins.append(Sub(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.MUL:
            self.ins.append(Mul(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.DIV:
            self.ins.append(Div(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.MOD:
            self.ins.append(Mod(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.LOGIC_AND \
            and operator == compiler.ir.Binary.BinaryOp.BIT_AND:
            self.ins.append(And(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.LOGIC_OR \
            and operator == compiler.ir.Binary.BinaryOpOp.BIT_OR:
            self.ins.append(Or(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.BIT_XOR:
            self.ins.append(Xor(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.LSHIFT:
            self.ins.append(Sal(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.RSHIFT:
            self.ins.append(Sar(left, right))
        elif operator == compiler.ir.Binary.BinaryOp.EQ:
            self.ins.append(Cmp(left, right, Cmp.Operator.EQ))
        elif operator == compiler.ir.Binary.BinaryOp.NE:
            self.ins.append(Cmp(left, right, Cmp.Operator.NE))
        elif operator == compiler.ir.Binary.BinaryOp.GE:
            self.ins.append(Cmp(left, right, Cmp.Operator.GE))
        elif operator == compiler.ir.Binary.BinaryOp.GT:
            self.ins.append(Cmp(left, right, Cmp.Operator.GT))
        elif operator == compiler.ir.Binary.BinaryOp.LE:
            self.ins.append(Cmp(left, right, Cmp.Operator.LE))
        elif operator == compiler.ir.Binary.BinaryOp.LT:
            self.ins.append(Cmp(left, right, Cmp.Operator.LT))
        else:
            raise InternalError('invalid operator ' + str(operator))
        return left

    def get_label(self, name):
        ret = self.label_map.get(name)
        if not ret:
            ret = Label(name)
            self.label_map[name] = ret
        return ret

    def trans_entity(self, entity):
        if self.is_in_leaf:
            ret = self.global_local_map.get(entity)
            if ret:
                self.used_global.add(entity)
                return ret
        return entity

    def eliminate_address(self, operand):
        if isinstance(operand, Address) or (\
            isinstance(operand, Reference) and \
                operand.type == Reference.Type.GLOBAL):
            tmp = self.get_tmp()
            self.ins.append(Move(tmp, operand))
            return tmp
        else:
            return operand

    def get_lvalue(self, operand):
        operand = self.eliminate_address(operand)
        if isinstance(operand, Immediate) or (\
            isinstance(operand, Reference) and not operand.can_be_accumulator):
            ret = self.get_tmp()
            self.ins.append(Move(ret, operand))
            return ret
        return operand

    def log2(self, x):
        for i in range(30):
            if x == (1 << i):
                return i
        return -1

    def get_tmp(self):
        global options
        if options.enable_global_register_allocation:
            ref = Reference('ref_' + str(self.tmp_counter), \
                Reference.Type.UNKNOWN)
            self.tmp_counter += 1
            return ref
        else:
            if self.tmp_top >= len(self.tmp_stack):
                self.tmp_stack.append(Reference('ref_' + \
                    str(self.tmp_counter), Reference.Type.UNKNOWN))
            tmp = self.tmp_stack[self.tmp_top]
            self.tmp_top += 1
            return tmp

    def is_commutative(self, op):
        return op == compiler.ir.Binary.BinaryOp.ADD or  \
                 op == compiler.ir.Binary.BinaryOp.MUL or \
                 op == compiler.ir.Binary.BinaryOp.BIT_AND or \
                 op == compiler.ir.Binary.BinaryOp.BIT_OR or \
                 op == compiler.ir.Binary.BinaryOp.BIT_XOR or \
                 op == compiler.ir.Binary.BinaryOp.EQ or \
                 op == compiler.ir.Binary.BinaryOp.NE
    
    def is_compare_op(self, op):
        return op == compiler.ir.Binary.BinaryOp.EQ or \
                op == compiler.ir.Binary.BinaryOp.NE or \
                op == compiler.ir.Binary.BinaryOp.GT or \
                op == compiler.ir.Binary.BinaryOp.GE or \
                op == compiler.ir.Binary.BinaryOp.LT or \
                op == compiler.ir.Binary.BinaryOp.LE
