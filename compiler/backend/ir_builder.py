from compiler.frontend.ast_visitor import ASTVisitor
from compiler.ast import *
from compiler.entity import *
from compiler.ir import *
from compiler.ir.binary import *
from compiler.utils import *
from compiler.options import options
from compiler.typ.integer_type import IntegerType
from compiler.typ.class_type import ClassType
from compiler.typ.array_type import ArrayType
from compiler.typ.string_type import StringType
from compiler.ast.block_node import BlockNode
from compiler.ast.if_node import IfNode
from compiler.ast.while_node import WhileNode
from compiler.ast.for_node import ForNode
from compiler.ast.functiondef_node import FunctionDefNode
from compiler.ast.binaryop_node import BinaryOpNode
from compiler.ast.funcall_node import FuncallNode
from compiler.ast.stringliteral_node import StringLiteralNode
from compiler.entity.scope import Scope
from compiler.utils.libfunction import LIB_PREFIX
from compiler.entity.variable_entity import VariableEntity
from compiler.entity.string_const_entity import StringConstEntity
from compiler.utils.internal_error import InternalError
import copy
import logging

global options


class IRBuilder(ASTVisitor):
    def __init__(self, ast):
        self.test_label_stack = []
        self.end_label_stack = []
        self.assign_table = dict()
        self.in_dependency = set()
        self.tmp_stack = []
        self.scope_stack = []
        self.global_initializer = []
        self.stmts = []
        self.global_stack = []
        self.expr_depth = 0
        self.inline_ct = 0
        self.inline_mode = 0
        self.inline_map = []
        self.inline_return_label = []
        self.inline_return_var = []
        self.inline_no_use = Var(VariableEntity(None, None, None, None))
        self.ast = ast
        self.const_length_size = IntConst(4)
        self.const_one = IntConst(1)
        self.const_zero = IntConst(0)

        self.not_use_tmp = False
        self.malloc_func = ast.scope.lookup_current_level(
            LIB_PREFIX + 'malloc')
        self.printInt_func = ast.scope.lookup_current_level(
            LIB_PREFIX + 'printInt')
        self.printlnInt_func = ast.scope.lookup_current_level(
            LIB_PREFIX + 'printlnInt')
        self.print_func = ast.scope.lookup_current_level('print')
        self.println_func = ast.scope.lookup_current_level('println')
        self.scope_stack.append(ast.scope)

    def expand_print(self, arg, newline, last):
        if isinstance(arg, FuncallNode) and arg.function_type.entity.name == 'toString':
            x = self.visit_expr(arg.args[0])
            print_func = None
            if newline and last:
                print_func = self.printlnInt_func
            else:
                print_func = self.printInt_func
            self.stmts.append(Call(print_func, [x]))
        elif isinstance(arg, BinaryOpNode) and arg.operator == BinaryOpNode.BinaryOp.ADD:
            self.expand_print(arg.left, newline, False)
            self.expand_print(arg.right, newline, last)
        else:
            x = self.visit_expr(arg)
            print_func = None
            if newline and last:
                print_func = self.println_func
            else:
                print_func = self.print_func
            self.stmts.append(Call(print_func, [x]))

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

        self.not_use_tmp = False
        self.assign_table = dict()
        self.in_dependency = set()

    def generate_ir(self):
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
            self.current_function = function_entity
            if function_entity.name != 'main':
                function_entity.asm_name = function_entity.name + '__func__'
            else:
                function_entity.asm_name = 'main'

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

    def clear_assign_table(self):
        self.assign_table = dict()
        self.in_dependency = set()

    def get_dependency(self, node):
        ret = set()
        if isinstance(node, BinaryOpNode):
            ret |= self.get_dependency(node.left)
            ret |= self.get_dependency(node.right)
        elif isinstance(node, VariableNode):
            ret.add(node.entity)
        return ret

    def visit(self, node):
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
                        logging.info('! remove init ' + str(node.location))
                else:
                    assign = ExprStmtNode(node.location, AssignNode(
                        VariableNode(node.entity, node.location), init))
                    self.visit(assign)
            return
        elif isinstance(node, BlockNode):
            new_scope = node.scope
            if self.inline_mode > 0:
                new_scope = Scope(self.current_scope)
                map = self.inline_map[-1]

                for name, entity in node.scope.entities.items():
                    if isinstance(entity, VariableEntity):
                        clone = copy.deepcopy(entity)
                        new_scope.insert(clone)
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
            if node.else_body == None:
                self.add_cjump(node.cond, then_label, end_label)
                self.add_label(then_label, 'if_then')
                if node.then_body:
                    self.visit_stmt(node.then_body)
                self.add_label(end_label, 'if_end')
            else:
                self.add_cjump(node.cond, then_label, else_label)
                self.add_label(then_label, 'if_then')
                if node.then_body:
                    self.visit_stmt(node.then_body)
                self.stmts.append(Jump(end_label))
                self.add_label(else_label, 'if_else')
                if node.else_body:
                    self.visit_stmt(node.else_body)
                self.add_label(end_label, 'if_end')
            return
        elif isinstance(node, WhileNode):
            if options.enable_output_irrelevant_elimination and \
                    node.is_output_irrelevant:
                if options.print_remove_info:
                    logging.info('! remove while ' + str(node.location))
                    return
            self.visit_loop(None, node.cond, None, node.body)
            return
        elif isinstance(node, ForNode):
            if options.enable_output_irrelevant_elimination and \
                    node.is_output_irrelevant:
                if options.print_remove_info:
                    logging.info('! remove for ' + str(node.location))
                    return
            self.visit_loop(node.init, node.cond, node.incr, node.body)
            return
        elif isinstance(node, ContinueNode):
            self.clear_assign_table()
            self.stmts.append(Jump(self.test_label_stack[-1]))
            return
        elif isinstance(node, BreakNode):
            self.clear_assign_table()
            self.stmts.append(Jump(self.end_label_stack[-1]))
            return
        elif isinstance(node, ReturnNode):
            self.clear_assign_table()
            self.visit_expr(None)
            self.expr_depth += 1
            if self.inline_mode > 0:
                if node.expr != None and \
                        self.inline_return_var[-1] != self.inline_no_use:
                    self.add_assign(self.inline_return_var[-1],
                                    self.visit_expr(node.expr))
                self.stmts.append(Jump(self.inline_return_label[-1]))
            else:
                if node.expr:
                    self.stmts.append(Return(self.visit_expr(node.expr)))
                else:
                    self.stmts.append(Return(None))
                self.stmts.append(
                    Jump(self.current_function.end_label_ir))
            self.expr_depth -= 1
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
                    logging.info('! remove assign ' + str(node.location))
                return
            if options.enable_common_assign_elimination and isinstance(lhs, Var):
                entity = lhs.entity
                ret = self.expr_hashing(node.rhs)
                if ret[0] and not isinstance(node.rhs, IntegerLiteralNode):
                    same = self.assign_table.get(ret[1])
                    if not same:
                        for dep in self.get_dependency(node.rhs):
                            self.in_dependency.add(dep)
                        self.assign_table[ret[1]] = entity
                    else:
                        rhs = Var(same)
            if not rhs:
                self.not_use_tmp = True
                rhs = self.visit_expr(node.rhs)
                self.not_use_tmp = False
            self.add_assign(lhs, rhs)
            return lhs
        elif isinstance(node, BinaryOpNode) and not isinstance(node, LogicalAndNode) and not isinstance(node, LogicalOrNode):
            lhs = self.visit_expr(node.left)
            rhs = self.visit_expr(node.right)
            if not self.need_return:
                return
            if isinstance(lhs, IntConst) and isinstance(rhs, IntConst):
                lvalue = lhs.value
                rvalue = rhs.value
                op = node.operator
                if op == BinaryOpNode.BinaryOp.ADD:
                    return IntConst(lvalue + rvalue)
                elif op == BinaryOpNode.BinaryOp.SUB:
                    return IntConst(lvalue - rvalue)
                elif op == BinaryOpNode.BinaryOp.MUL:
                    return IntConst(lvalue * rvalue)
                elif op == BinaryOpNode.BinaryOp.DIV:
                    return IntConst(int(lvalue / rvalue))
                elif op == BinaryOpNode.BinaryOp.MOD:
                    return IntConst(lvalue % rvalue)
                elif op == BinaryOpNode.BinaryOp.LSHIFT:
                    return IntConst(lvalue << rvalue)
                elif op == BinaryOpNode.BinaryOp.RSHIFT:
                    return IntConst(lvalue >> rvalue)
                elif op == BinaryOpNode.BinaryOp.BIT_AND:
                    return IntConst(lvalue & rvalue)
                elif op == BinaryOpNode.BinaryOp.BIT_XOR:
                    return IntConst(lvalue ^ rvalue)
                elif op == BinaryOpNode.BinaryOp.BIT_OR:
                    return IntConst(lvalue | rvalue)
                elif op == BinaryOpNode.BinaryOp.GT:
                    if lvalue > rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == BinaryOpNode.BinaryOp.LT:
                    if lvalue < rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == BinaryOpNode.BinaryOp.GE:
                    if lvalue >= rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == BinaryOpNode.BinaryOp.LE:
                    if lvalue <= rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == BinaryOpNode.BinaryOp.EQ:
                    if lvalue == rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                elif op == BinaryOpNode.BinaryOp.NE:
                    if lvalue != rvalue:
                        return IntConst(1)
                    else:
                        return IntConst(0)

                else:
                    raise InternalError('')
            if isinstance(lhs, StrConst) and isinstance(rhs, StrConst):
                lvalue = lhs.entity
                rvalue = rhs.entity
                op = node.operator
                if op == BinaryOpNode.BinaryOp.ADD:
                    join = lvalue.value + rvalue.value
                    entity = self.ast.scope.lookup(
                        StringType.STRING_CONST_PREFIX + join)
                    if not entity:
                        entity = StringConstEntity(
                            node.location, StringType(), join, None)
                        self.ast.scope.insert(entity)
                    return StrConst(entity)
                else:
                    raise InternalError('')
            if not node.left.type.is_string:
                op = None
                if node.operator == BinaryOpNode.BinaryOp.ADD:
                    op = Binary.BinaryOp.ADD
                elif node.operator == BinaryOpNode.BinaryOp.SUB:
                    op = Binary.BinaryOp.SUB
                elif node.operator == BinaryOpNode.BinaryOp.MUL:
                    op = Binary.BinaryOp.MUL
                elif node.operator == BinaryOpNode.BinaryOp.DIV:
                    op = Binary.BinaryOp.DIV
                elif node.operator == BinaryOpNode.BinaryOp.MOD:
                    op = Binary.BinaryOp.MOD
                elif node.operator == BinaryOpNode.BinaryOp.LSHIFT:
                    op = Binary.BinaryOp.LSHIFT
                elif node.operator == BinaryOpNode.BinaryOp.RSHIFT:
                    op = Binary.BinaryOp.RSHIFT
                elif node.operator == BinaryOpNode.BinaryOp.BIT_AND:
                    op = Binary.BinaryOp.BIT_AND
                elif node.operator == BinaryOpNode.BinaryOp.BIT_OR:
                    op = Binary.BinaryOp.BIT_OR
                elif node.operator == BinaryOpNode.BinaryOp.BIT_XOR:
                    op = Binary.BinaryOp.BIT_XOR
                elif node.operator == BinaryOpNode.BinaryOp.LOGIC_AND:
                    op = Binary.BinaryOp.BIT_AND
                elif node.operator == BinaryOpNode.BinaryOp.LOGIC_OR:
                    op = Binary.BinaryOp.BIT_OR
                elif node.operator == BinaryOpNode.BinaryOp.GT:
                    op = Binary.BinaryOp.GT
                elif node.operator == BinaryOpNode.BinaryOp.LT:
                    op = Binary.BinaryOp.LT
                elif node.operator == BinaryOpNode.BinaryOp.GE:
                    op = Binary.BinaryOp.GE
                elif node.operator == BinaryOpNode.BinaryOp.LE:
                    op = Binary.BinaryOp.LE
                elif node.operator == BinaryOpNode.BinaryOp.EQ:
                    op = Binary.BinaryOp.EQ
                elif node.operator == BinaryOpNode.BinaryOp.NE:
                    op = Binary.BinaryOp.NE
                else:
                    raise SemanticError(node.location,
                                        'unsupported operator for int : ' + str(node.operator))
                return Binary(lhs, op, rhs)
            else:
                if node.operator == BinaryOpNode.BinaryOp.ADD:
                    return Call(StringType.operator_add, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.GT:
                    return Call(StringType.operator_gt, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.LT:
                    return Call(StringType.operator_gt, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.GE:
                    return Call(StringType.operator_ge, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.LE:
                    return Call(StringType.operator_le, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.EQ:
                    return Call(StringType.operator_eq, [lhs, rhs])
                elif node.operator == BinaryOpNode.BinaryOp.NE:
                    return Call(StringType.operator_ne, [lhs, rhs])
                else:
                    raise SemanticError(node.location,
                                        'unsupported operator for int : ' + str(node.operator))
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
            self.add_assign(tmp, self.visit_expr(node.left))
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
                    self.expand_print(node.args[0], False, True)
                    return
                elif entity.name == 'println':
                    self.expand_print(node.args[0], True, True)
                    return
            args = []
            for expr_node in node.args:
                args.append(self.visit_expr(expr_node))
            if (options.enable_function_inline and entity.is_inlined) or \
                (options.enable_self_inline and
                 entity == self.current_function and
                 entity.can_be_self_inline(self.inline_mode)):
                if options.print_inline_info and \
                        entity == self.current_function:
                    logging.info(entity.name + ' is self expanded')
                if self.need_return:
                    tmp = self.new_int_tmp()
                    self.inline_function(entity, tmp, args)
                    return tmp
                else:
                    self.inline_function(entity, self.inline_no_use, args)
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
            if not self.ast.scope.lookup(node.entity.name):
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
                return Mem(Binary(base, Binary.BinaryOp.ADD,
                                  IntConst(sizeof * index.value)))
            else:
                return Mem(Binary(base, Binary.BinaryOp.ADD,
                                  Binary(index, Binary.BinaryOp.MUL, IntConst(sizeof))))
        elif isinstance(node, VariableNode):
            if node.is_member:
                base = Var(node.this_pointer)
                offset = node.entity.offset
                if offset == 0:
                    return Mem(base)
                else:
                    return Mem(Binary(base, Binary.BinaryOp.ADD,
                                      IntConst(offset)))
            else:
                if self.inline_mode > 0:
                    if node.entity in self.inline_map[-1]:
                        return Var(self.inline_map[-1][node.entity])
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
                return Mem(Binary(base, Binary.BinaryOp.ADD, IntConst(offset)))
        elif isinstance(node, CreatorNode):
            self.clear_assign_table()
            if isinstance(node.type, ArrayType):
                base_type = node.type.base_type
                deep_type = node.type.deep_type
                pointer = self.new_int_tmp()
                constructor = None
                if len(node.exprs) == node.total and isinstance(deep_type, ClassType):
                    constructor = deep_type.entity.constructor
                self.expand_creator(node.exprs, pointer, 0, base_type, constructor)
                if self.need_return:
                    return pointer
                else:
                    return
            else:
                entity = node.type.entity
                tmp = self.new_int_tmp()
                self.add_assign(tmp, Call(self.malloc_func,
                                [IntConst(entity.size)]))
                if entity.constructor:
                    self.stmts.append(Call(entity.constructor, [tmp]))
                if self.need_return:
                    return tmp
                else:
                    return
        elif isinstance(node, UnaryOpNode):
            op = node.operator
            if op == UnaryOpNode.UnaryOp.ADD:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(node.expr.value)
                else:
                    return self.visit_expr(node.expr)
            elif op == UnaryOpNode.UnaryOp.MINUS:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(-node.expr.value)
                else:
                    return Unary(Unary.UnaryOp.MINUS,
                                 self.visit_expr(node.expr))
            elif op == UnaryOpNode.UnaryOp.BIT_NOT:
                if isinstance(node.expr, IntegerLiteralNode):
                    return IntConst(~node.expr.value)
                else:
                    return Unary(Unary.UnaryOp.BIT_NOT,
                                 self.visit_expr(node.expr))
            elif op == UnaryOpNode.UnaryOp.LOGIC_NOT:
                if isinstance(node.expr, IntegerLiteralNode):
                    if node.expr.value == 1:
                        return IntConst(1)
                    else:
                        return IntConst(0)
                else:
                    return Unary(Unary.UnaryOp.LOGIC_NOT,
                                  self.visit_expr(node.expr))
            elif op == UnaryOpNode.UnaryOp.PRE_INC or \
                    op == UnaryOpNode.UnaryOp.PRE_DEC:
                opr = None
                if op == UnaryOpNode.UnaryOp.PRE_INC:
                    opr = Binary.BinaryOp.ADD
                else:
                    opr = Binary.BinaryOp.SUB
                if True or isinstance(node.expr, VariableNode):
                    expr = self.visit_expr(node.expr)
                    self.add_assign(expr,
                                    Binary(expr, opr, self.const_one))
                    if self.need_return:
                        return expr
                    else:
                        return
            elif op == UnaryOpNode.UnaryOp.SUF_INC or \
                    op == UnaryOpNode.UnaryOp.SUF_DEC:
                opr = None
                if op == UnaryOpNode.UnaryOp.SUF_INC:
                    opr = Binary.BinaryOp.ADD
                else:
                    opr = Binary.BinaryOp.SUB
                expr = self.visit_expr(node.expr)
                if True or isinstance(node.expr, VariableNode):
                    if self.need_return:
                        tmp = self.new_int_tmp()
                        self.add_assign(tmp, expr)
                        self.add_assign(expr,
                                        Binary(expr, opr, self.const_one))
                        return tmp
                    else:
                        self.add_assign(expr,
                                        Binary(expr, opr, self.const_one))
                        return
            else:
                raise InternalError(node.location,
                                    'invalid operator ' + str(op))
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

    #   new int a[s][s2][];
    #   s = expr[now];
    #   p = malloc(s * pointerSize + lengthSize);
    #   *p = s;
    #   p += 4;
    #   for (int i = 0; i < s; i++) {  /-----
    #       s2 = expr[now + 1]
    #       p[i] = malloc(s2 * pointerSize + lengthSize);
    #       *(p[i]) = s2;
    #       p[i] += 4;
    #       for (int i2 = 0; i2 < s2; i++) { /-----
    #           s3 = expr[now + 2];
    #           p[i][i2] = malloc(s3 * elementSize + lengthSize);
    #           *(p[i][i2]) = s3;
    #           p[i][i2] += 4;
    #           // alloc memory for class
    #           for (int i3 = 0; i3 < s3; i3++)  /-----
    #               p[i][i2][i3] = malloc(classSize);
    #               constructor(p[i][i2][i3]) ; if has
    #       }
    #   }

    def expand_creator(self, exprs, base, now, type, constructor):
        tmps = self.new_int_tmp()
        tmpi = self.new_int_tmp()
        sizeof = IntConst(type.size)
        self.add_assign(tmps, self.visit_expr(exprs[now]))
        self.add_assign(base, Call(self.malloc_func, [Binary(
            Binary(tmps, Binary.BinaryOp.MUL, sizeof),
            Binary.BinaryOp.ADD, self.const_length_size)]))
        self.add_assign(Mem(base), tmps)
        self.add_assign(base, Binary(base, Binary.BinaryOp.ADD,
                        self.const_length_size))
        if len(exprs) > now + 1:
            self.add_assign(tmpi, self.const_zero)
            test_label = Label()
            begin_label = Label()
            end_label = Label()

            self.stmts.append(Jump(test_label))
            self.add_label(begin_label, 'creator_loop_begin')
            self.expand_creator(exprs, Mem(Binary(base, Binary.BinaryOp.ADD,
                                Binary(tmpi, Binary.BinaryOp.MUL, sizeof))),
                                now + 1, type.base_type, constructor)
            self.add_assign(tmpi, Binary(tmpi, Binary.BinaryOp.ADD,
                            self.const_one))
            self.add_label(test_label, 'creator_loop_test')
            self.stmts.append(CJump(Binary(tmpi, Binary.BinaryOp.LT,
                                           tmps), begin_label, end_label))
            self.add_label(end_label, 'creator_loop_end')
        elif len(exprs) == now + 1 and isinstance(type, ClassType):
            self.add_assign(tmpi, self.const_zero)
            test_label = Label()
            begin_label = Label()
            end_label = Label()

            self.stmts.append(Jump(test_label))
            self.add_label(begin_label, 'creator_loop_begin')
            tmp_address = self.new_int_tmp()
            self.add_assign(tmp_address, Binary(base, Binary.BinaryOp.ADD,
                            Binary(tmpi, Binary.BinaryOp.MUL, sizeof)))
            self.add_assign(Mem(tmp_address),
                            Call(self.malloc_func, [sizeof]))
            if constructor:
                self.stmts.append(Call(constructor, [Mem(tmp_address)]))
            self.add_assign(tmpi, Binary(tmpi, Binary.BinaryOp.ADD,
                            self.const_one))
            self.add_label(test_label, 'creator_loop_test')
            self.stmts.append(CJump(Binary(tmpi, Binary.BinaryOp.LT, tmps),
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
        self.add_label(test_label, 'loop_test')
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
            return (True, hash(node.entity))
        elif isinstance(node, IntegerLiteralNode):
            return (True, hash(node.value))
        else:
            return (False, 0)

    @property
    def need_return(self):
        return (self.expr_depth > 1)

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
        if options.enable_common_assign_elimination and \
                isinstance(lhs, Var):
            if lhs.entity in self.in_dependency:
                self.clear_assign_table()
        self.stmts.append(Assign(self.get_address(lhs), rhs))
    label_counter = 0

    def add_label(self, label, name):
        label.name = name + '_' + str(self.label_counter)
        self.label_counter += 1
        self.stmts.append(label)

    def add_cjump(self, cond, true_label, false_label):
        if options.enable_cjump_optimization:
            if isinstance(cond, BinaryOpNode):
                node = cond
                goon = Label()
                op = cond.operator
                if op == BinaryOpNode.BinaryOp.LOGIC_AND:
                    self.add_cjump(node.left, goon, false_label)
                    self.add_label(goon, 'goon')
                    self.add_cjump(node.right, true_label, false_label)
                elif op == BinaryOpNode.BinaryOp.LOGIC_OR:
                    self.add_cjump(node.left, true_label, goon)
                    self.add_label(goon, 'goon')
                    self.add_cjump(node.right, true_label, false_label)
                else:
                    self.visit_expr(None)
                    self.expr_depth += 1
                    self.stmts.append(CJump(self.visit_expr(cond),
                                            true_label, false_label))
                    self.expr_depth -= 1
            elif isinstance(cond, UnaryOpNode) and \
                    cond.operator == Unary.UnaryOp.LOGIC_NOT:
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
        if options.enable_global_register_allocation:
            tmp = VariableEntity(None, IntegerType(),
                                 'tmp' + str(self.new_int_tmp_counter), None)
            self.new_int_tmp_counter += 1
            self.current_function.scope.insert(tmp)
            return Var(tmp)
        else:
            if self.tmp_top >= len(self.tmp_stack):
                tmp = VariableEntity(None, IntegerType(),
                                     'tmp' + str(self.tmp_top), None)
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
