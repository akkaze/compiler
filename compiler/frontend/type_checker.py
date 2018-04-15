from compiler.frontend import ASTVisitor
from compiler.ast import *
from compiler.entity import *
from compiler.type import *
from compiler.utils import *

class TypeChecker(ASTVisitor):
    bool_type = BoolType()
    integer_type = IntegerType()
    string_type = StringType()

    loop_depth = 0
    current_function = None
    scope = None
    malloc_func = None

    def __init__(self, scope):
        self.scope = scope
        self.malloc_func = self.scope.lookup_current_level( \
                                    LIB_PREFIX + 'malloc')
    @staticmethod
    def check_compatibility(loc, real, expect, is_expected):
        if not real.is_compatible(expect):
            message = ''
            if is_expected:
                message += 'Invalid type ' + str(real) +  \
                            ', expecting ' + str(expect)
            else:
                message += 'Incompatible type ' + str(real) +  \
                            ', and ' + str(expect)
            raise SemanticError(loc, message)
    def visit(self, node):
        if isinstance(node, FunctionDefNode):
            self.current_function = node.entity
            if not self.current_function.is_constructor and \
                not self.current_function.return_type:
                raise SemanticError(node.location, \
                    'expecting a return type')
                self.visit_stmt(node.entity.body)
                self.current_function = None
                return
        elif isinstance(node, VariableDefNode):
            init = node.entity.initializer
            if init:
                self.visit_expr(init)
                TypeChecker.check_compatibility(node.location, \
                    init.type, node.entity.type, False)
            if node.entity.type.is_void:
                raise SemanticError(node.location, 'Cannot \
                    set void type for variable')
            return
        elif isinstance(node, IfNode):
            self.visit_expr(node.cond)
            if node.then_body:
                self.visit_stmt(node.then_body)
            if node.else_body:
                self.visit_stmt(node.else_body)
            TypeChecker.check_compatibility(node.location, \
                node.cond.type, self.bool_type, True)
            return
        elif isinstance(node, WhileNode):
            self.visit_expr(node.cond)
            if node.body:
                self.loop_depth += 1
                self.visit_stmt(node.body)
                self.loop_depth -= 1
            TypeChecker.check_compatibility(node.location, \
                node.cond.type, self.bool_type, True)
            return
        elif isinstance(node, ForNode):
            if node.init:
                self.visit_expr(node.init)
            if node.cond:
                self.visit_expr(node.cond)
                TypeChecker.check_compatibility(node.location, \
                    node.cond.type, self.bool_type, True)
            if node.init:
                self.visit_expr(node.incr)
            if node.then_body:
                self.loop_depth += 1
                self.visit_stmt(node.body)
                self.loop_depth -= 1
            return
        elif isinstance(node, BreakNode):
            if self.loop_depth <= 0:
                raise SemanticError(node.location, 'unexpected break')
            return
        elif isinstance(node, ContinueNode):
            if self.loop_depth <= 0:
                raise SemanticError(node.location, 'unexpected continue')
            return
        elif isinstance(node, ReturnNode):
            if not self.current_function:
                raise SemanticError(node.location, \
                    'caannot return outside function')
            if self.current_function.is_constructor:
                if node.expr:
                    raise SemanticError(node.location, \
                        'cannot return in constructor')
            else:
                if node.expr:
                    self.visit_expr(node.expr)
                    TypeChecker.check_compatibility(node.location, \
                        node.expr.type, \
                        self.current_function.return_type, True)
                else:
                    if not self.current_function.return_type.is_void:
                        raise SemanticError(node.location, \
                            'cannot return to void')
            return
        elif isinstance(node, AssignNode):
            self.visit_expr(node.lhs)
            self.visit_expr(node.rhs)
            if not node.lhs.is_assignable:
                raise SemanticError(node.location, \
                    'LHS of \'=\' is not assignable')
            TypeChecker.check_compatibility(node.location, 
                node.lhs.type, node.rhs.type, False)
            return
        elif isinstance(node, UnaryOpNode):
            self.visit_expr(node.expr)
            expect = None
            op = node.operator
            if op == UnaryOpNode.UnaryOp.PRE_INC or \
                op == UnaryOpNode.UnaryOp.PRE_DEC or \
                op == UnaryOpNode.UnaryOp.SUF_INC or \
                op == UnaryOpNode.UnaryOp.SUF_DEC or \
                op == UnaryOpNode.UnaryOp.MINUS or \
                op == UnaryOpNode.UnaryOp.ADD or \
                op == UnaryOpNode.UnaryOp.BIT_NOT:
                expect = self.integer_type
            elif op == UnaryOpNode.UnaryOp.LOGIC_NOT:
                expect = self.bool_type
            else:
                raise InternalError('invalid operator ' + str(op))
            TypeChecker.check_compatibility(node.location, \
                node.expr.type, expect, True)
            if isinstance(node, PrefixOpNode):
                if op == UnaryOpNode.UnaryOp.PRE_INC or \
                    op == UnaryOpNode.UnaryOp.PRE_DEC:
                    node.is_assignable = True
                return
            elif isinstance(node, SuffixOpNode):
                if not node.expr.is_assignable:
                    raise SemanticError(node.location, \
                        'lvalue is needed')
                return
        elif isinstance(node, BinaryOpNode):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            ltype = node.left.type
            rtype = node.right.type
            op = node.operator
            if op == BinaryOpNode.BinaryOp.MUL or \
                op == BinaryOpNode.BinaryOp.DIV or \
                op == BinaryOpNode.BinaryOp.MOD or \
                op == BinaryOpNode.BinaryOp.SUB or \
                op == BinaryOpNode.BinaryOp.LSHIFT or \
                op == BinaryOpNode.BinaryOp.RSHIFT or \
                op == BinaryOpNode.BinaryOp.BIT_AND or \
                op == BinaryOpNode.BinaryOp.BIT_XOR or \
                op == BinaryOpNode.BinaryOp.BIT_OR:
                TypeChecker.check_compatibility(node.left.location, \
                    ltype, self.integer_type, True)
                TypeChecker.check_compatibility(node.right.location, \
                    rtype, self.integer_type, True)
                node.type = ltype
            elif op == BinaryOpNode.BinaryOp.GT or \
                    op == BinaryOpNode.BinaryOp.LE or \
                    op == BinaryOpNode.BinaryOp.GE or \
                    op == BinaryOpNode.BinaryOp.LT:
                TypeChecker.check_compatibility(node.left.location, \
                    ltype, rtype, False)
                if not ltype.is_full_comparable and \
                    not rtype.is_full_comparable:
                    raise SemanticError(node.location, \
                        'Cannot compare twp ' + str(ltype))
                node.type = self.bool_type
            elif op == BinaryOpNode.BinaryOp.EQ or \
                op == BinaryOpNode.BinaryOp.NE:
                TypeChecker.check_compatibility(node.location, \
                    ltype, rtype, True)
                if not ltype.is_half_comparable and \
                    not rtype.is_half_comparable:
                    raise SemanticError(node.location, \
                        'Cannot compare two ' + str(ltype))
                node.type = self.bool_type
            elif op == BinaryOpNode.BinaryOp.LOGIC_AND or \
                op == BinaryOpNode.BinaryOp.LOGIC_OR:
                TypeChecker.check_compatibility(node.left.location, \
                    ltype, self.bool_type, True)
                TypeChecker.check_compatibility(node.right.location, \
                    rtype, self.bool_type, True)
                node.type = ltype
            elif op == BinaryOpNode.BinaryOp.ADD:
                TypeChecker.check_compatibility(node.location, \
                    ltype, rtype, True)
                if not ltype.is_integer and not ltype.is_string:
                    raise SemanticError(node.location, \
                        'Cannot add two ' + str(ltype))
                node.type = ltype
            else:
                raise InternalError('invalid operator ' + str(node.operator))
            return
        elif isinstance(node, FuncallNode):
            self.visit_expr(node.expr)
            type = node.expr.type
            if not type.is_function:
                raise SemanticError(node.location, 'invalid type : ' \
                    + str(type) + ' expecting function')
            entity = type.entity
            if self.current_function:
                self.current_function.add_call(entity)
            params = entity.params
            exprs = node.args
            base = 0
            if isinstance(node.expr, MemberNode) or \
                (isinstance(node, VariableNode) and \
                node.expr.is_member):
                base = 1
            if len(params) - base != len(exprs):
                raise SemanticError(node.location, \
                    'Incompatible parameter number : ' + \
                    str(len(exprs) + ', expecting ' + len(params) - base))
            for i in range(base, len(params)):
                expr = exprs[i - base]
                self.visit_expr(expr)
                TypeChecker.check_compatibility(expr.location, \
                    expr.type, params[i].type, True)

            if base != 0:
                if isinstance(node.expr, MemberNode):
                    node.add_thispointer(node.expr.expr)
                else:
                    node.add_thispointer(VariableNode( \
                        self.current_function.params[0]))
            return
        elif isinstance(node, ArefNode):
            self.visit_expr(node.expr)
            self.visit_expr(node.index)
            if not node.expr.type.is_array:
                raise SemanticError(node.location, 'invalid reference of '\
                    + str(node.expr.type) + ', expecting an array')
            TypeChecker.check_compatibility(node.index.location, node.index.type, \
                self.integer_type, True)
            node.type = node.expr.type.base_type
            return
        elif isinstance(node, CreatorNode):
            if self.current_function:
                self.current_function.add_call(self.malloc_func)
            if node.exprs:
                for expr in node.exprs:
                    self.visit_expr(expr)
                    TypeChecker.check_compatibility(expr.location, \
                        expr.type, self.integer_type, True)
            return
        elif isinstance(node, MemberNode):
            self.visit_expr(node.expr)
            type = node.expr.type
            if type.is_class:
                entity = type.entity
                member = entity.scope.lookup_current_level(node.member)
                if not member:
                    raise SemanticError(node.location, \
                        'Cannot resolve member :' +  str(node.member))
                node.entity = member
                node.type = member.type
            elif type.is_array or type.is_string:
                member = None
                if type.is_array:
                    member = ArrayType.scope.lookup_current_level(\
                            node.member)
                else:
                    member = StringType.scope.lookup_current_level(\
                            node.member)
                if not member:
                    raise SemanticError(node.location, \
                        'Cannot resolve member : ' + node.member)
                node.entity = member
            else:
                raise SemanticError(node.location, 'Invalid get member \
                        operation : ' + str(node.expr.type) + \
                        ', expecting class, array or string')
            return
        return super().visit(node)
