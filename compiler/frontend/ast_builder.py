from antlr4 import *

class ASTBuilder(ParseTreeVisitor):
    ast = None
    self.map = dict()
    def exitCompilationUnit(ctx):
        definition_nodes = []
        function_entities = []
        class_entities = []
        variable_entities = []

        for paser_rule_ctx in ctx.getTypedRuleContexts(ParserRuleContext):
            definition_node = self.map[paser_rule_ctx]
            definition_nodes.append(node)
            if isinstance(node, FunctionDefNode):
                function_entites.append(node)
            elif isinstance(node, VaraibleDefNode):
                variable_entities.append(node)
            elif isinstance(node, ClassDefNode):
                class_entities.append(node)
            else:
                raise InternalError('Invalid definition node ' + node.name)

        ast = AST(definition_nodes, class_entites, 
                functon_enties, variable_entities)

    def exitClassDefinition(ctx):
        vars = []
        funcs = []
        name = ctx.name.getText()

        for item in ctx.variableDefinition():
            vars.append(self.map[item])
        constructor = None
        for item in ctx.functionDefinition():
            node = self.map[item]
            funcs.append(node)
            entity = node.entity()
            if entity.is_constructor():
                constuctor = entity
                if entity.name != CONSTUCTOR_NAME + name:
                    raise SemanticError(Location(ctx.name), 
                                        'wrong namee of constructor' + 
                                        entity.name + 'and' + 
                                        CONSTRUCTOR_NAME + name)
        entity = ClassEntity(Location(ctx.name), name, vars, funcs)
        entity.constructor = constructor
        self.map[ctx] = entity

    def exitFunctionDefinition(ctx):
        params = []
        for item in ctx.parameter():
            node = self.map[item]
            params.append(node)
        entity = None
        if ctx.res == None:
            entity = FunctionEntity(Location(ctx.name), ClassType(ctx.name.getText()),
                                    CONSTURCTOR_NAME + ctx.name.getTxt(),
                                    params, self.map[ctx.block()])
            entity.contructor = True
        else:
            entity = FunctionEntity(Location(ctx.name), self.map[ctx.ret],
                                    ctx.name.getTxt(),
                                    params, self.map[ctx.block()])
        
    def exitVariableDefinition(ctx):
        entity = VariableEntity(Location(ctx.Indentifier(), self.map[ctx.typeType()])),
                                ctx.Identifier().getText(), get_expr(ctx.expression())
        self.map[ctx] = VariableDefNode(entity)
    def exitParameter(ctx):
        self.map[ctx] = ParameterEntity(Location(ctx), self.map[ctx.typeType()],
                                    ctx.Indentifier().getText())
    def exitPrimitiveType(ctx):
        stype = ctx.type.getText()
        if stype == 'bool':
            type = BoolType()
            break
        elif stype == 'int':
            type = IntegerType()
            break
        elif stype == 'void':
            type = VoidType()
            break
        elif stype == 'string':
            type = StringType()
            break
        else:
            raise InternalError('Invalid  type ' + stype)
        self.map[ctx] = type

    def exitTypeType(ctx):
        baseType = None
        if ctx.Identifier() != None:
            base_type = ClassType(ctx.Indentifier.getText())
        else:
            base_type = self.map[ctx.primitiveType()]
        dimension = ctx.getChildCount() - 1 // 2
        if dimension == 0:
            self.map[ctx] = base_type
        else:
            self.map[ctx] = ArrayType(base_type, dimension)
    def exitBlock(self, ctx):
        stmts = []
        for item : ctx.statement():
            stmt_node = self.get_stmt(item)
            if stmt != None:
                stmts.append(stmt)
        self.map[ctx] = BlockNode(Location(ctx), stmts)
    def exitBlockStmt(self, ctx):
        self.map[ctx] = self.map[ctx.block()]
    def exitVarDefStmt(self, ctx):
        self.map[ctx] = self.map[ctx.variableDefinition()]
    def exitIfStmt(self, ctx):
        self.map[ctx] = IfNode(Location(ctx), self.get_expr(ctx.expression()),
                            self.get_stmt(ctx.statement(0),
                            self.get_stmt(ctx.statement(1))))
    def exitForStmt(self, ctx):
        self.map[ctx] = ForNode(Location(ctx), self.get_expr(ctx.init),
                            self.get_expr(ctx.cond), self.get_expr(ctx.incr),
                            self.ctx.statement())
    def exitWhileStmt(self, ctx):
        self.map[ctx] = WhileNode(Location(ctx), self.get_expr(ctx.expression()),
                            self.get_stmt(ctx.statement()))
    def exitRetureStmt(self, ctx):
        self.map[ctx] = ReturnNode(Location(ctx), self.get_expr(ctx.expression()))
    def exitBreakStmt(self, ctx):
        self.map[ctx] = BreakNode(Location(ctx))
    def exitContinueStmt(self, ctx):
        self.map[ctx] = ContinueNode(Location(ctx))
    def exitExprStmt(self, ctx):
        self.map[ctx] = ExprStmtNode(Location(ctx), self.get_expr(ctx.expression()))
    def exitBlankStmt(self, ctx):
        self.map[ctx] = None
    def exitPrimaryExpr(self, ctx):
        self.map[ctx] = self.map[ctx.primary()]
    def exitMemberExpr(self, ctx):
        self.map[ctx] = MemberNode(self.get_expr(ctx.expression()))
    def exitArefExpr(self, ctx):
        self.map[ctx] = ArefNode(self.get_expr(ctx.expression(0),
                                self.get_expr(ctx.expression(1))))
    def exitExprssionList(self, ctx):
        exprs = []
        for x : ctx.expression():
            exprs.append(self.get_expr(x))
        self.map[ctx] = exprs

    def exitFuncallExpr(self, ctx):
        args = []
        if ctx.expressionList() is None:
            args = []
        else:
            args = self.map[ctx.expressionList()]
        self.map[ctx] = FuncallNode(self.get_expr(ctx.expression()), args)

    def exitNewExpr(self, ctx):
        self.map[ctx] = self.map[ctx.creator()]
    
    def exitSuffixExpr(self, ctx):
        op = None
        text = ctx.op.getText()
        if text == '++':
            op = UnaryOp.SUF_INC
        elif text == '--':
            op = UnaryOp.SUF_DEC
        else:
            raise InternalError('Invalid token ' + text)
        self.map[ctx] = SuffixOpNode(op, self,get_expr(ctx.expression()))

    def exitPrefixNode(self, ctx):
        op = None
        text = ctx.op.getText()
        if text == '+':
            op = UnaryOp.ADD
        elif text == '-':
            op = UnaryOp.MINUS
        elif text == '++'
            op = UnaryOp.PRE_INC
        elif text == '--'
            op = UnaryOp.PRE_DEC
        elif text == '-'
            op = UnaryOp.BIT_NOT
        elif text == '!'
            op = UnaryOp.LOGIC_NOT
        else:
            raise InternalError('Invalid token ' + text)
        self.map[ctx] = PrefixNode(op, self.get_expr(ctx.expression()))

    def exitBinaryExpr(self, ctx):
        op = None
        text = ctx.op.getText()
        if text == '*':
            op = BinrayOp.MUL
        elif text == '/':
            op = BinrayOp.DIV
        elif text == '%':
            op = BinrayOp.MOD
        elif text == '+':
            op = BinrayOp.ADD
        elif text == '-':
            op = BinrayOp.SUB
        elif text == '<<':
            op = BinrayOp.LSHIFT
        elif text == '>>':
            op = BinrayOp.RSHIFT
        elif text == '>':
            op = BinrayOp.GT
        elif text == '<':
            op = BinrayOp.LT
        elif text == '>=':
            op = BinrayOp.GE
        elif text == '<=':
            op = BinrayOp.LE
        elif text == '==':
            op = BinrayOp.EQ
        elif text == '!=':
            op = BinrayOp.NE
        elif text == '&':
            op = BinrayOp.BIT_ADD
        elif text == '^':
            op = BinrayOp.BIT_XOR
        elif text == '|':
            op = BinrayOp.BIT_OR
        else:
            raise InternalError('Invalid token ' + text)
        self.map[ctx] = BinaryOpNode(self.get_expr(ctx.expression(0),
                            op, self.get_expr(ctx.expression(1))))
    def exitLogicalAndExpr(self, ctx):
        self.map[ctx] = LogicalAndNode(self.get_expr(ctx.expression(0),
                            self.get_expr(ctx.expression(1))))
    
    def exitLogicalOrExpr(self, ctx):
        self.map[ctx] = LogicalOrNode(self.get_expr(ctx.expression(0),
                            self.get_expr(ctx.expression(1))))
    def exitAssignExpr(self, ctx):
        self.map[ctx] = AssignNode(self.get_expr(ctx.expression(0),
                            self.get_expr(ctx.expression(1))))
    def exitSubExpr(self, ctx):
        self.map[ctx] = self.map[ctx.expression()]
    def exitThisExpr(self, ctx):
        self.map[ctx] = VariableNode(Location(ctx), 'this')
    def exitVariableExpr(self, ctx):
        self.map[ctx] = VariableNode(Location(ctx.Identifier()),
                            ctx.Identifier().getText())
    def exitLiteralExpr(self, ctx):
        self.map[ctx] = self.map[ctx.Literal()]]
    def exitDecIntergerConst(self, ctx):
        self.map[ctx] = IntegerLiteralNode(Location(ctx), 
            int(ctx.DecimalInteger().getText()))
    def exitStringConst(self, ctx):
        value = ctx.StringLiteral().getText()
        value = value[1:len(value) - 1]
        map[ctx] = StringLiteralNode(Location(ctx), value)
    def exitBoolConst(self, ctx):
        map[ctx] = BoolLiteralNode(Locaation(ctx), 
            ctx.value.getText() == 'true')
    def exitNullConst(self, ctx):
        map[ctx] = VariableNode(Location(ctx), 'null')
    def exitArrayCreator(self, ctx):
        base_type = None
        if ctx.Identifier() != None:
            base_type = ClassType(ctx.Identifier().getText())
        else:
            base_type = self.map[ctx.primitiveType()]
        exprs = ctx.expression()
        dimension = (ctx.getChildCount() - 1 - len(exprs)) // 2
        type = ArrayType(base_type, dimension)
        expr_nodes = []
        for item in exprs:
            expr_nodes.append(self.get_expr(item))
        self.map[ctx] = CreatorNode(Location(ctx), type, expr_nodes, dimension)
    def exitErrorCreator(self, ctx):
        raise SemanticError(Location(ctx), 'Invalid creator expression')
    def exitNonArrayCretor(self, ctx):
        type = ClassType(ctx.Indentifier().getText())
        self.map[ctx] = CreatorNode(Location(ctx), type, None, 0)
    def get_stmt(self, ctx):
        if ctx == None:
            return None
        else:
            return self.map[ctx]
    def get_expr(self, ctx):
        if ctx == None:
            return None
        else:
            return self.map[ctx]
