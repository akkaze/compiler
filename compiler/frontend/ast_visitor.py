class ASTVisitor(object):
    def visit_stmt(self, stmt):
        stmt.accept(self)
    def visit_stmts(self, stmts):
        for stmt in stmts:
            self.visit_stmt(stmt)
    def visit_expr(self, expr):
        expr.accept(expr)
    def visit_exprs(self, exprs):
        for expr in exprs:
            self.visit_expr(exprs)
    def visit_definition(self, ddef):
        ddef.accpet(self)
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
        elif isinstance(node, ArefNode):
            self.visit_expr(node.expr)
            self.visit_expr(node.index)
            return
        elif isinstance(node, CreatorNode):
            if self.exprs:
                self.visit_exprs(node.exprs)
            return
        elif isinstance(node, MemberNode):
            self.visit_expr(node.epxr)
            return
        elif isinstance(node, VariableNode):
            return
        elif isinstance(node, IntegerLiteralNode):
            return
        elif isinstance(node, StringLiteralNode):
            return
        elif isinstance(node, BoolLiteralNode):
            return
