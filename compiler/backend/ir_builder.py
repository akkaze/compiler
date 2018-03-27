from compiler.frontend import ASTVisitor
from compiler.ast import *
from compiler.entity import *
from compiler.ir import *
from compiler.utils import *
from compiler.options import options
from compiler.type import *
import copy
import logging

class IRBuilder(ASTVisitor):
    stmts = None
    ast = None
    expr_depth = 2
    max_depth = 0
    scope_stack = None
    current_scope = None
    current_function = None

    global_initializer = None

    const_pointer_size = IntConst(4)
    const_legth_size = IntConst(4)
    const_one = IntConst(1)
    const_zero = IntConst(0)

    malloc_func = None
    printInt_func = None
    printlnInt_func = None
    print_func = None
    println_func = None

    def __init__(self, ast):
        self.test_label_stack = []
        self.end_label_stack = []
        self.assign_table = dict()
        self.in_dependency = dict()
        self.tmp_stack = []
        self.scope_stack = []
        self.global_initializer = []
        self.stmts = []
        self.global_stack = []
        self.inline_map = []
        self.inline_return_label = []
        self.inline_return_var = []
        self.inline_no_use = Var(VariableEntity(None, None, None, None))
        self.ast = ast
        self.malloc_func = ast.scope.lookup_current_level( \
                                    LIB_PREFIX + 'malloc')
        self.printInt_func = ast.scope.lookup_current_level( \
                                    LIB_PREFIX + 'printInt')
        self.printlnInt_func = ast.scope.lookup_current_level( \
                                    LIB_PREFIX + 'printlnInt')
        self.print_func = ast.scope.lookup_current_level( \
                                    LIB_PREFIX + 'print')
        self.println_func = ast.scope.lookup_current_level( \
                                    LIB_PREFIX + 'println')
        self.scope_stack.append(ast.scope)

    inline_ct = 0
    inline_mode = 0
    inline_no_use = None 
    inline_map = None
    inline_return_label = None
    inline_return_var = None
    def inline_function(self, entity, return_var, args):
        return_label = Label()
        map = dict()
        self.inline_map.append(map)
        self.inline_return_label.append(return_label)
        self.inline_return_var.append(return_var)
        
        scope = Scope(self.current_scope)
        i = 0
        # copy parameters. and assign init
        for param in entity.params:
            clone = VariableEntity(param.location, param.type,
                        param.name + '_inline_' + str(self.inline_ct), None)
            self.inline_ct += 1
            scope.insert(clone)
            map[param] = clone
            self.add_assign(Var(clone), args[i])
            i += 1
        self.current_scope = scope
        self.scope_stack.append(self.current_scope)

        self.inline_mode += 1
        self.visit(entity.body)
        self.add_label(return_label, 'inline_return_' + entity.name)
        self.inline_mode -= 1

        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]

        self.inline_map.pop()
        self.inline_return_label.pop()
        self.inline_return_var.pop()

    def generate_ir(self):
        global options
        for class_entity in self.ast.class_entities:
            class_entity.init_offset(options.CLASS_MEMBER_ALIGNMENT_SIZE)

        if options.enable_function_inline:
            for function_entity in self.ast.function_entities:
                function_entity.check_inlinable()
            for class_entity in self.ast.class_entities:
                for functiondef_node in class_entity.member_funcs:
                    pass
        
        for function_entity in self.ast.function_entities:
            self.tmp_stack = []
            self.tmp_top = 0
            if function_entity.name != 'main':
                function_entity.asm_name = entity_name + '__func__'
            self.compile_function(function_entity)

        for class_entity in self.ast.class_entities:
            for functiondef_node in class_entity.member_funcs:
                self.tmp_stack = []
                self.tmp_top = 0
                self.current_function = functiondef_node.entity

                func = functiondef_node.entity
                func.asm_name = class_entity.name + '_' + func.name + '__func__'
                self.compile_function(func)

    def compile_function(self, entity):
        if entity.is_inlined:
            return
        begin = Label()
        end = Label()
        entity.set_label_ir(begin, end)

        self.add_label(begin, entity.name + '_begin')

        if entity.name == 'main':
            for node in self.ast.definition_nodes:
                if isinstance(node, VariableDefNode):
                    self.visit(node)
        self.visit(entity.body)
        if not isinstance(self.stmts[-1], Jump):
            self.stmts.append(Jump(end))
        self.add_label(end, entity.name + '_end')
        entity.irs = self.fetch_stmts()
    not_use_tmp = False
    assign_table = None
    in_dependency = None
    def clear_assign_table(self):
        self.assign_table = dict()
        self.in_dependency = dict()
    def get_dependency(self, node):
        ret = set()
        if isinstance(node, BinaryOpNode):
            ret |= self.get_dependency(node.left)
            ret |= self.get_dependency(node.right)
        elif isinstance(node, VariableNode):
            ret.add(node.entity)
        return ret
    def visit(self, node):
        global options
        if isinstance(node, FunctionDefNode):
            raise InternalError('invaild call to visit FunctionDefNode')
        elif isinstance(node, ClassDefNode):
            raise InternalError('invaild call to visit ClassDefNode')
        elif isinstance(node, VariableDefNode):
            init = node.entity.initializer
            if init:
                if options.enable_output_irrelevant_elimination and \
                    node.entity.is_output_irrelevant:
                    if options.print_remove_info:
                        logging.error('remove init ' + str(node.location))
                else:
                    assign = ExprStmtNode(node.location, AssignNode( \
                                VariableNode(node.entity, node.location), init))
                    self.visit(assign)
            return
        elif isinstance(node, BlockNode):
            new_scope = node.scope
            if self.inline_mode > 0:
                new_scope = Scope(self.current_scope)
                map = inline_map[-1]

                for entity in node.scope.entities.values:
                    if isinstance(entity, VariableEntity):
                        clone = copy.deepcopy(entity)
                        news_scope.insert(clone)
                        map[entity] = clone
            self.current_scope = new_scope
            self.scope_stack.append(self.current_scope)

            for stmt in node.stmts:
                stmt.accept(self)
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            return
        elif isinstance(node, IfNode):
            then_label = Label()
            else_label = Label()
            end_label = Label()

            if not node.else_body:
                self.add_cjump(node.end, then_label, end_label)
                self.add_label(then_label, 'if_then')
                if node.then_body:
                    self.visit(node.then_body)
                self.add_label(end_label, 'if_end')
            else:
                self.add_cjump(node.cond, then_label, else_label)
                self.add_label(then_label, 'if_then')
                if node.then_body:
                    self.visit(node.then_body)
                self.stmts.append(Jump(end_label))
                self.add_label(else_label, 'if_else')
                if node.else_body:
                    self.visit(node.else_body)
                self.add_label(end_label, 'if_end')
            return
        elif isinstance(node, WhileNode):
            if options.enable_output_irrelevant_elimination and \
                node.is_output_irrelevant:
                if options.print_remove_info:
                    logging.error('! remove while ' + str(node.location))
                    return
                self.visit_loop(None, node.cond, None, node.body)
                return
        elif isinstance(node, ForNode):
            if options.enable_output_irrelevant_elimination and \
                node.is_output_irrelevant:
                if options.print_remove_info:
                    logging.error('! remove for ' + str(node.location))
                    return
                self.visit_loop(node.init, node.cond, node.incr, node.body)
                return
        elif isinstance(node, ContinueNode):
            self.clear_assign_table()
            self.stmts.append(Jump(self.test_label_stack[-1]))
            return
        elif isinstance(node, BreakNode):
            self.clear_assign_table()
            self.stmts.append(Jump(self.end_label_stacl[-1]))
            return
        elif isinstance(node, ReturnNode):
            self.clear_assign_table()
            self.visit_expr(None)
            self.expr_depth += 1
            if self.inline_mode > 0:
                if node.expr != None and \
                    self.inline_return_var[-1] != self.inline_no_use:
                    self.add_assign(self.inline_return_var[-1], \
                        self.visit_expr(node.expr))
                    self.stmts.append(Jump(self.inline_return_label[-1]))
                else:
                    if node.expr:
                        self.stmts.append(Return(self.visit_expr(node.expr)))
                    else:
                        self.stmts.append(Return(None))
                    self.stmts.append(\
                        Jump(self.current_function.end_label_ir))
            self.expr_depth += 1
            return
        elif isinstance(node, ExprStmtNode):
            self.visit_expr(node.expr)
            return
        elif isinstance(node, AssignNode):
            lhs = self.visit_expr(node.lhs)
            rhs = None
            if not self.need_return and \
                options.enable_output_irrelevant_elimination and \
                node.is_output_irrelevant:
                if options.print_remove_info:
                    logging.error('! remove assign ' + str(node.location))
                return
            if options.enable_common_assign_elimination and \
                isinstance(lhs, Var):
                entity = lhs.entity
                ret = self.expr_hashing(node.rhs)
                if ret[0] and not isinstance(node.rhs, IntegerLiteralNode):
                    same = self.assign_table.get(ret.second)
                    if not same:
                        for dep in self.get_dependency(node.rhs):
                            self.in_dependency.append(dep)
                        self.assign_table[ret.second] = entity
                    else:
                        rhs = Var(same)
            if not rhs:
                self.not_use_tmp = True
                rhs = self.visit_expr(node.rhs)
                self.not_use_tmp = False
            self.add_assign(lhs, rhs)
            return lhs
        elif isinstance(node, BinaryOpNode):
            lhs = node.left
            rhs = node.right
            if not self.need_return:
                return
            if isinstance(lhs, IntConst) and isinstance(rhs, IntConst):
                lvalue = lhs.value
                rvalue = rhs.value
                op = node.operator
                if op == ADD:
                    return IntConst(lvalue + rvalue)
                elif op == SUB:
                    return IntConst(lvalue - rvalue)
                elif op == MUL:
                    return IntConst(lvalue * rvalue)
                elif op == DIV:
                    return IntConst(lvalue / rvalue)
                elif op == MOD:
                    return IntConst(lvalue % rvalue)
                elif op == LSHIFT:
                    return IntConst(lvalue << rvalue)
                elif op == RSHIFT:
                    return IntConst(lvalue >> rvalue)
                elif op == BIT_AND:
                    return IntConst(lvalue & rvalue)
                elif op == BIT_XOR:
                    return IntConst(lvalue ^ rvalue)
                elif op == BIT_OR:
                    return IntConst(lvalue | rvalue)
                elif op == GT:
                    if lvalue > rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == LT:
                    if lvalue < rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == GE:
                    if lvalue >= rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == LE:
                    if lvalue <= rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == EQ:
                    if lvalue == rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == NE:
                    if lvalue != rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
               
                else:
                    raise InternalError('')
        elif isinstance(node, LogicalAndNode):
            goon = Label()
            end = Label()
            tmp = self.new_int_tmp()
            self.add_assign(tmp, self.visit_expr(node.left))
            self.stmts.append(CJump(tmp, goon, end))
            self.add_label(goon, 'goon')
            self.add_assign(tmp, self.visit_expr(node.right))
            self.add_label(end, 'end')
            if self.need_return:
                return tmp
            else:
                return
        elif isinstance(node, LogicalOrNode):
            goon = Label()
            end = Label()
            tmp = self.new_int_tmp()
            self.add_assign(tmp, self.visit_expr(node,left))
            self.stmts.append(CJump(tmp, end, goon))
            self.add_label(goon, 'goon')
            self.add_assign(tmp, self.visit_expr(node.right))
            self.add_label(end, 'end')
            if self.need_return:
                return tmp
            else:
                return
        elif isinstance(node, FuncallNode):
            self.clear_assign_table()
            entity = node.function_type.entity
            
            if options.enable_print_expanding:
                if entity.name == 'print':
                    self.expand_print(node.args[0], false, true)
                    return 
                elif entity.name == 'println':
                    self.expand_print(node.args[0]. true, true)
            args = []
            for expr_node in node.args:
                args.append(self.visit_expr(expr_node))

            if (options.enable_function_inline and entity.is_inlined) or \
                (options.enable_self_inline and \
                entity == self.current_function and
                entity.can_be_self_inline(self.inline_mode)): 
                if options.print_inline_info and \
                    entity == self.current_function:
                    logging.error(entity.name + ' is self expanded')
                if self.need_return:
                    tmp = self.new_int_tmp()
                    self.inline_function(entity, tmp, args)
                    return tmp
                else:
                    self.inline_function(entity, self.inline_nouse, args)
            else:
                if self.need_return:
                    if self.not_use_tmp:
                        return Call(entity, args)
                    else:
                        tmp = self.new_int_tmp()
                        self.add_assign(tmp, Call(entity, args))
                        return tmp
                else:
                    self.stmts.append(Call(entity, args))
            return
        elif isinstance(node, IntegerLiteralNode):
            return IntConst(node.value)
        elif isinstance(node, StringLiteralNode):
            if not self.ast.scope.loockup(node.entity.name):
                self.ast.scope.insert(node.entity)
            return StrConst(node.entity)
        elif isinstance(node, BoolLiteralNode):
            if node.value == True:
                return IntConst(1)
            else:
                return IntConst(0)
        elif isinstance(node, ArefNode):
            base = self.visit_expr(node.expr)
            index = self.visit_expr(node.index)
            sizeof = node.expr.type.base_type.size

            if isinstance(index, IntConst):
                return Mem(Binary(base, BinaryOp.ADD, \
                        IntConst(sizeof * index).value))
            else:
                return Mem(Binary(base, BinaryOp.ADD, \
                        Binary(index, BinaryOp.MUL, IntConst(sizeof))))
        elif isinstance(node, VariableNode):
            if node.is_member:
                base = Var(node.this_pointer)
                offset = node.entity.offset

                if offset == 0:
                    return Mem(base)
                else:
                    return Mem(Binary(base, BinaryOp.ADD, \
                            IntConst(offset)))
            else:
                if self.inline_mode > 0:
                    entity = self.inline_map[-1][node.entity]
                    if entity:
                        return Var(entity)
                    else:
                        return Var(node.entity)
                else:
                    return Var(node.entity)
        elif isinstance(node, MemberNode):
            base = self.visit_expr(node.expr)
            offset = node.entity.offset
            if offset == 0:
                return Mem(base)
            else:
                return Mem(Binary(base, BinaryOp.ADD, IntConst(offset)))
        elif isinstance(node, CreatorNode):
            self.clear_assign_table()
            if isinstance(node.type, ArrayType):
                base_type = node.type.base_type
                deep_type = node.type.deep_type
                pointer = self.new_int_tmp()
                constructor = None
                if len(node.exprs) == node.total and \
                    isinstance(deept_type, ClassType):
                    constructor = deep_type.entity.constructor
                self.expand_creator(node.exprs, pointer, 0, \
                                    base_type, constructor)
                if self.need_return:
                    return pointer
                else:
                    return
            else:
                entity = node.type.entity
                tmp = self.new_int_tmp()
                self.add_assign(tmp, Call(self.malloc_func, \
                                [IntConst(entity.size)]))
                if entity.constructor:
                    self.stmts.append(Call(entity.constructor, [tmp]))
                if self.need_return:
                    return tmp
                else:
                    return
        elif isinstance(node, UnaryOpNode):
            op = node.operator
            if op == UnaryOp.ADD:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(node.expr.value)
                else:
                    return self.visit_expr(node.expr)
            elif op == UnaryOp.MINUS:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(-node.expr.value)
                else:
                    return Unary(UnaryOp.MINUS, \
                                self.visit_expr(node.expr))
            elif op == UnaryOp.BIT_NOT:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(~node.expr.value)
                else:
                    return Unary(UnaryOp.BIT_NOT, \
                                self.visit_expr(node.expr))
            elif op == UnaryOp.LOGIC_NOT:
                if isinstance(node.expr, IntegerLiteralNode):
                    if node.expr.value == 1:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                else:
                    return Unary(UnaryOp.LOGIC_NOT, \
                                self.visit_expr(node.expr))
        super().visit(node)
    
    def visit_expr(self, node):
        if self.expr_depth == 0:
            self.tmp_top = 0
            self.max_depth = 0
        if not node:
            return
        self.expr_depth += 1
        if self.max_depth < self.expr_depth:
            self.max_depth = self.expr_depth
        expr = node.accept(self)
        self.expr_depth -= 1
        return expr
#        elif isinstance(node, StmtNode):
#            node.accept(self)

    def expand_creator(self, expr, base, now, type, constructor):
        tmps = self.new_int_tmp()
        tmpi = self.new_int_tmp()
        sizeof = IntConst(type.size)
        self.add_assign(tmps, self.visit_expr(exprs[now]))
        self.add_assign(base, Call(self.malloc_func, [Binary( \
                    Binary(tmps, BinaryOp.MUL, sizeof), \
                    BinaryOp.ADD, const_length_size)]))
        self.add_assign(Mem(base), tmps)
        self.add_assign(base, Binary(base, BinaryOp.ADD, \
                        self.const_length_size))
        if len(exprs) > now + 1:
            self.add_assign(tmpi, self.const_zero)
            test_label = Label()
            begin_label = Label()
            end_label = Label()

            self.stmts.append(Jump(test_label))
            self.add_label(begin_label, 'creator_loop_begin')
            self.expand_creator(exprs, Mem(Binary(baase, BinaryOp.ADD, \
                                Binary(tmpi, BinaryOp.MUL, sizeof))), \
                                type.base_type, constructor)
            self.add_assign(tmpi, Binary(tmpi, BinaryOp.ADD, \
                            self.const_one))
            self.add_label(test_label, 'creator_loop_test')
            self.stmts.append(CJump(Binary(tmpi, BinaryOp.LT, \
                            tmps), begin_label, end_label))
            self.add_label(end_label, 'creator_loop_end')
        elif len(exprs) == now + 1 and isinstance(type, ClassType):
            self.add_assign(tmpi, self.const_zero)
            test_label = Label()
            begin_label = Label()
            end_label = Label()

            self.stmts.append(Jump(test_label))
            self.add_label(begin_label, 'creator_loop_begin')
            tmp_address = self.new_tmp_int()
            self.add_assign(tmp_address, Binary(base, BinaryOp.ADD, \
                            Binary(tmpi, BinaryOp.MUL, sizeof)))
            self.add_assign(Mem(tmp_address), \
                            Call(self.malloc_func, [sizeof]))
            if constructor:
                self.stmts.append(Call(constructor, [Mem(tmp_address)]))
            self.add_assign(tmpi, Binary(tmpi, BinaryOp.ADD, \
                            self.const_one))
            self.add_label(test_label, 'creator_loop_test')
            self.stmts.append(CJump(Binary(tmpi, BinaryOp.LT, tmps), \
                            begin_label, end_label))
            self.add_label(end_label, 'creator_loop_end')
    test_label_stack = None
    end_label_stack = None
    def visit_loop(self, init, cond, incr, body):
        self.clear_assign_table()
        if init:
            self.visit_expr(init)
        test_label = Label()
        begin_label = Label()
        end_label = Label()
        self.stmts.append(Jump(test_label))
        self.add_label(begin_label, 'loop_begin')
        self.test_label_stack.append(test_label)
        self.end_label_stack.append(end_label)
        if body:
            self.visit_stmt(body)
        if incr:
            self.visit_expr(incr)
        self.end_label_stack.pop()
        self.test_label_stack.pop()
        if cond:
            self.add_cjump(cond, begin_label, end_label)
        else:
            self.stmts.append(Jump(begin_label))
        self.add_label(end_label, 'loop_end')
    def expr_hashing(self, node):
        if isinstance(node, BinaryOpNode):
            left = self.expr_hashing(node.left)
            right = self.expr_hashing(node.right)
            if left[0] and right[0]:
                hash_code = hash(node.operator)
                hash_code += left[1]
                hash_code += right[1] ^ 0x5D
                return (True, hash_code)
            else:
                return (False, 0)
        elif isinstance(node, VariableNode):
            return (True, hash(node,entity))
        elif isinstance(node, IntegerLiteralNode):
            return (True, hash(node.value))
        else:
            return (False, 0)
    @property
    def need_return(self):
        return self.expr_depth > 1
    def fetch_stmts(self):
        ret = self.stmts
        self.stmts = []
        return ret
    def get_address(self, expr):
        if isinstance(expr, Var):
            return Addr(expr.entity)
        elif isinstance(expr, Mem):
            return expr.expr
        else:
            raise InternalError('get address on an invalid type')
    def add_assign(self, lhs, rhs):
        global options
        if options.enable_common_assign_elimination and \
            isinstance(lhs, Var):
            if lhs.entity in self.in_dependency:
                self.clear_assign_table()
        self.stmts.append(Assign(self.get_address(lhs), rhs))
    label_counter = 0
    def add_label(self, label, name):
        label.name = name + str(self.label_counter)
        self.label_counter += 1
        self.stmts.append(label)
    def add_cjump(self, cond, true_label, false_label):
        global options
        if options.enable_cjump_optimization:
            if isinstance(cond, BinaryOpNode):
                node = cond
                goon = Label()
                op = cond.operator
                if op == LOGIC_AND:
                    self.add_cjump(node.left, goon, flase_label)
                    self.add_label(goon, 'goon')
                    self.add_cjump(node.right, goon, flase_label)
                elif op == LOGIC_OR:
                    self.add_cjump(node.left, true_label, goon)
                    self.add_label(goon, 'goon')
                    self.add_cjump(node.right, true_label, false_label)
                else:
                    self.visit_expr(None)
                    self.expr_depth += 1
                    self.stmts.append(CJump(self.visit(cond), 
                                        true_label, false_label))
                    self.expr_depth -= 1
            elif isinstance(cond, UnaryOpNode) and cond.oprator == LOG_NOT:
                self.add_cjump(cond.expr, false_label, true_label)
            elif isinstance(cond, BoolLiteralNode):
                if cond.value:
                    self.stmts.append(Jump(true_label))
                else:
                    self.stmts.append(Jump(false_label))
            else:
                self.visit_expr(None)
                self.expr_depth += 1
                self.stmts.append(CJump(self.visit_expr(cond),
                                    true_label, false_label))
                self.expr_depth -= 1
        else:
            self.visit_expr(None)
            self.expr_depth += 1
            self.stmts.append(CJump(self.visit_expr(cond), 
                                    true_label, false_label))
            self.expr_depth -= 1

    tmp_stack = None
    tmp_top = 0
    new_int_tmp_counter = 0
    def new_int_tmp(self):
        global options
        if options.enable_global_register_allocation:
            tmp = VariableEntity(None, IntegerType(),
                                'tmp' + str(self.new_int_tmp_counter), None)
            self.new_int_tmp_counter += 1
            return Var(tmp)
        else:
            if self.tmp_top >= len(self.tmp_stack):
                tmp = VariableEntity(None, IntegerType(),
                                'tmp' + self.tmp_top, None)
            self.current_function.scope.insert(tmp)
            self.tmp_stack.append(Var(tmp))
            tmp = self.tmp_stack[self.tmp_top]
            self.tmp_top += 1
            return tmp

    @property
    def global_scope(self):
        return self.ast.scope
    @property
    def function_entities(self):
        return self.ast.function_entities
