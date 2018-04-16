# Generated from Malic.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MalicParser import MalicParser
else:
    from MalicParser import MalicParser

# This class defines a complete generic visitor for a parse tree produced by MalicParser.

class MalicVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MalicParser#compilationUnit.
    def visitCompilationUnit(self, ctx:MalicParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#classDefinition.
    def visitClassDefinition(self, ctx:MalicParser.ClassDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:MalicParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#variableDefinition.
    def visitVariableDefinition(self, ctx:MalicParser.VariableDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#parameter.
    def visitParameter(self, ctx:MalicParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#primitiveType.
    def visitPrimitiveType(self, ctx:MalicParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#typeType.
    def visitTypeType(self, ctx:MalicParser.TypeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#block.
    def visitBlock(self, ctx:MalicParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#blockStmt.
    def visitBlockStmt(self, ctx:MalicParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#varDefStmt.
    def visitVarDefStmt(self, ctx:MalicParser.VarDefStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#ifStmt.
    def visitIfStmt(self, ctx:MalicParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#forStmt.
    def visitForStmt(self, ctx:MalicParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#whileStmt.
    def visitWhileStmt(self, ctx:MalicParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#returnStmt.
    def visitReturnStmt(self, ctx:MalicParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#breakStmt.
    def visitBreakStmt(self, ctx:MalicParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#continueStmt.
    def visitContinueStmt(self, ctx:MalicParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#exprStmt.
    def visitExprStmt(self, ctx:MalicParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#blankStmt.
    def visitBlankStmt(self, ctx:MalicParser.BlankStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#expressionList.
    def visitExpressionList(self, ctx:MalicParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#newExpr.
    def visitNewExpr(self, ctx:MalicParser.NewExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:MalicParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#prefixExpr.
    def visitPrefixExpr(self, ctx:MalicParser.PrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:MalicParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:MalicParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#funcallExpr.
    def visitFuncallExpr(self, ctx:MalicParser.FuncallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#memberExpr.
    def visitMemberExpr(self, ctx:MalicParser.MemberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#arefExpr.
    def visitArefExpr(self, ctx:MalicParser.ArefExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#suffixExpr.
    def visitSuffixExpr(self, ctx:MalicParser.SuffixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#binaryExpr.
    def visitBinaryExpr(self, ctx:MalicParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#assignExpr.
    def visitAssignExpr(self, ctx:MalicParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#subExpr.
    def visitSubExpr(self, ctx:MalicParser.SubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#thisExpr.
    def visitThisExpr(self, ctx:MalicParser.ThisExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#variableExpr.
    def visitVariableExpr(self, ctx:MalicParser.VariableExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#literalExpr.
    def visitLiteralExpr(self, ctx:MalicParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#DecIntegerConst.
    def visitDecIntegerConst(self, ctx:MalicParser.DecIntegerConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#StringConst.
    def visitStringConst(self, ctx:MalicParser.StringConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#boolConst.
    def visitBoolConst(self, ctx:MalicParser.BoolConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#nullConst.
    def visitNullConst(self, ctx:MalicParser.NullConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#errorCreator.
    def visitErrorCreator(self, ctx:MalicParser.ErrorCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#arrayCreator.
    def visitArrayCreator(self, ctx:MalicParser.ArrayCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MalicParser#nonarrayCreator.
    def visitNonarrayCreator(self, ctx:MalicParser.NonarrayCreatorContext):
        return self.visitChildren(ctx)



del MalicParser