from compiler.ast import *
from compiler.entity import *

class ASTVisitor(object):
    def visit_stmt(self, stmt):
        return stmt.accept(self)
    def visit_stmts(self, stmts):
        for stmt in stmts:
            self.visit_stmt(stmt)
    def visit_expr(self, expr):
        return expr.accept(self)
    def visit_exprs(self, exprs):
        for expr in exprs:
            self.visit_expr(expr)
    def visit_definition(self, ddef):
        ddef.accept(self)
    def visit_definitions(self, ddefs):
        for ddef in ddefs:
            self.visit_definition(ddef)
    def visit(self, node):
        if isinstance(node, BlockNode):
            self.visit_stmts(node.stmts)
            return
        elif isinstance(node, ExprStmtNode):
            self.visit_expr(node.expr)
            return
        elif isinstance(node, IfNode):
            self.visit_expr(node.cond)
            if node.then_body:
                self.visit_expr(node.then_body)
            if node.else_body:
                self.visit_expr(node.else_body)
            return
        elif isinstance(node, WhileNode):
            self.visit_expr(node.cond)
            if node.body:
                self.visit_stmt(node.body)
            return
        elif isinstance(node, ForNode):
            if node.init:
                self.visit_expr(node.init)
            if node.cond:
                self.visit_expr(node.cond)
            if node.incr:
                self.visit_expr(node.incr)
            if node.body:
                self.visit_stmt(node.body)
            return
        elif isinstance(node, BreakNode):
            return
        elif isinstance(node, ContinueNode):
            return
        elif isinstance(node, ReturnNode):
            if node.expr:
                self.visit_expr(node.expr)
            return
        elif isinstance(node, ClassDefNode):
            self.visit_stmts(node.entity.member_vars)
            self.visit_stmts(node.entity.member_funcs)
            return
        elif isinstance(node, FunctionDefNode):
            self.visit_stmt(node.entity.body)
            return
        elif isinstance(node, VariableDefNode):
            if node.entity.initializer:
                self.visit_expr(node.entity.initializer)
            return
        elif isinstance(node, AssignNode):
            self.visit_expr(node.lhs)
            self.visit_expr(node.rhs)
            return
        elif isinstance(node, BinaryOpNode):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            return
        elif isinstance(node, LogicalOrNode):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            return
        elif isinstance(node, LogicalAndNode):
            self.visit_expr(node.left)
            self.visit_expr(node.right)
            return
        elif isinstance(node, UnaryOpNode):
            self.visit_expr(node.expr)
            return
        elif isinstance(node, FuncallNode):
            self.visit_expr(node.expr)
            self.visit_exprs(node.args)
            return
        elif isinstance(node, ArefNode):
            self.visit_expr(node.expr)
            self.visit_expr(node.index)
            return
        elif isinstance(node, CreatorNode):
            if self.exprs:
                self.visit_exprs(node.exprs)
            return
        elif isinstance(node, MemberNode):
            self.visit_expr(node.expr)
            return
        elif isinstance(node, VariableNode):
            return
        elif isinstance(node, IntegerLiteralNode):
            return
        elif isinstance(node, StringLiteralNode):
            return
        elif isinstance(node, BoolLiteralNode):
            return
