# Generated from Malic.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MalicParser import MalicParser
else:
    from MalicParser import MalicParser

# This class defines a complete listener for a parse tree produced by MalicParser.
class MalicListener(ParseTreeListener):

    # Enter a parse tree produced by MalicParser#compilationUnit.
    def enterCompilationUnit(self, ctx:MalicParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by MalicParser#compilationUnit.
    def exitCompilationUnit(self, ctx:MalicParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by MalicParser#classDefinition.
    def enterClassDefinition(self, ctx:MalicParser.ClassDefinitionContext):
        pass

    # Exit a parse tree produced by MalicParser#classDefinition.
    def exitClassDefinition(self, ctx:MalicParser.ClassDefinitionContext):
        pass


    # Enter a parse tree produced by MalicParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:MalicParser.FunctionDefinitionContext):
        pass

    # Exit a parse tree produced by MalicParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:MalicParser.FunctionDefinitionContext):
        pass


    # Enter a parse tree produced by MalicParser#variableDefinition.
    def enterVariableDefinition(self, ctx:MalicParser.VariableDefinitionContext):
        pass

    # Exit a parse tree produced by MalicParser#variableDefinition.
    def exitVariableDefinition(self, ctx:MalicParser.VariableDefinitionContext):
        pass


    # Enter a parse tree produced by MalicParser#parameter.
    def enterParameter(self, ctx:MalicParser.ParameterContext):
        pass

    # Exit a parse tree produced by MalicParser#parameter.
    def exitParameter(self, ctx:MalicParser.ParameterContext):
        pass


    # Enter a parse tree produced by MalicParser#primitiveType.
    def enterPrimitiveType(self, ctx:MalicParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by MalicParser#primitiveType.
    def exitPrimitiveType(self, ctx:MalicParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by MalicParser#typeType.
    def enterTypeType(self, ctx:MalicParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by MalicParser#typeType.
    def exitTypeType(self, ctx:MalicParser.TypeTypeContext):
        pass


    # Enter a parse tree produced by MalicParser#block.
    def enterBlock(self, ctx:MalicParser.BlockContext):
        pass

    # Exit a parse tree produced by MalicParser#block.
    def exitBlock(self, ctx:MalicParser.BlockContext):
        pass


    # Enter a parse tree produced by MalicParser#blockStmt.
    def enterBlockStmt(self, ctx:MalicParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#blockStmt.
    def exitBlockStmt(self, ctx:MalicParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#varDefStmt.
    def enterVarDefStmt(self, ctx:MalicParser.VarDefStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#varDefStmt.
    def exitVarDefStmt(self, ctx:MalicParser.VarDefStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#ifStmt.
    def enterIfStmt(self, ctx:MalicParser.IfStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#ifStmt.
    def exitIfStmt(self, ctx:MalicParser.IfStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#forStmt.
    def enterForStmt(self, ctx:MalicParser.ForStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#forStmt.
    def exitForStmt(self, ctx:MalicParser.ForStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#whileStmt.
    def enterWhileStmt(self, ctx:MalicParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#whileStmt.
    def exitWhileStmt(self, ctx:MalicParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#returnStmt.
    def enterReturnStmt(self, ctx:MalicParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#returnStmt.
    def exitReturnStmt(self, ctx:MalicParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#breakStmt.
    def enterBreakStmt(self, ctx:MalicParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#breakStmt.
    def exitBreakStmt(self, ctx:MalicParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#continueStmt.
    def enterContinueStmt(self, ctx:MalicParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#continueStmt.
    def exitContinueStmt(self, ctx:MalicParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#exprStmt.
    def enterExprStmt(self, ctx:MalicParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#exprStmt.
    def exitExprStmt(self, ctx:MalicParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#blankStmt.
    def enterBlankStmt(self, ctx:MalicParser.BlankStmtContext):
        pass

    # Exit a parse tree produced by MalicParser#blankStmt.
    def exitBlankStmt(self, ctx:MalicParser.BlankStmtContext):
        pass


    # Enter a parse tree produced by MalicParser#expressionList.
    def enterExpressionList(self, ctx:MalicParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by MalicParser#expressionList.
    def exitExpressionList(self, ctx:MalicParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by MalicParser#newExpr.
    def enterNewExpr(self, ctx:MalicParser.NewExprContext):
        pass

    # Exit a parse tree produced by MalicParser#newExpr.
    def exitNewExpr(self, ctx:MalicParser.NewExprContext):
        pass


    # Enter a parse tree produced by MalicParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:MalicParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by MalicParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:MalicParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by MalicParser#prefixExpr.
    def enterPrefixExpr(self, ctx:MalicParser.PrefixExprContext):
        pass

    # Exit a parse tree produced by MalicParser#prefixExpr.
    def exitPrefixExpr(self, ctx:MalicParser.PrefixExprContext):
        pass


    # Enter a parse tree produced by MalicParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:MalicParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by MalicParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:MalicParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by MalicParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:MalicParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by MalicParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:MalicParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by MalicParser#funcallExpr.
    def enterFuncallExpr(self, ctx:MalicParser.FuncallExprContext):
        pass

    # Exit a parse tree produced by MalicParser#funcallExpr.
    def exitFuncallExpr(self, ctx:MalicParser.FuncallExprContext):
        pass


    # Enter a parse tree produced by MalicParser#memberExpr.
    def enterMemberExpr(self, ctx:MalicParser.MemberExprContext):
        pass

    # Exit a parse tree produced by MalicParser#memberExpr.
    def exitMemberExpr(self, ctx:MalicParser.MemberExprContext):
        pass


    # Enter a parse tree produced by MalicParser#arefExpr.
    def enterArefExpr(self, ctx:MalicParser.ArefExprContext):
        pass

    # Exit a parse tree produced by MalicParser#arefExpr.
    def exitArefExpr(self, ctx:MalicParser.ArefExprContext):
        pass


    # Enter a parse tree produced by MalicParser#suffixExpr.
    def enterSuffixExpr(self, ctx:MalicParser.SuffixExprContext):
        pass

    # Exit a parse tree produced by MalicParser#suffixExpr.
    def exitSuffixExpr(self, ctx:MalicParser.SuffixExprContext):
        pass


    # Enter a parse tree produced by MalicParser#binaryExpr.
    def enterBinaryExpr(self, ctx:MalicParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by MalicParser#binaryExpr.
    def exitBinaryExpr(self, ctx:MalicParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by MalicParser#assignExpr.
    def enterAssignExpr(self, ctx:MalicParser.AssignExprContext):
        pass

    # Exit a parse tree produced by MalicParser#assignExpr.
    def exitAssignExpr(self, ctx:MalicParser.AssignExprContext):
        pass


    # Enter a parse tree produced by MalicParser#subExpr.
    def enterSubExpr(self, ctx:MalicParser.SubExprContext):
        pass

    # Exit a parse tree produced by MalicParser#subExpr.
    def exitSubExpr(self, ctx:MalicParser.SubExprContext):
        pass


    # Enter a parse tree produced by MalicParser#thisExpr.
    def enterThisExpr(self, ctx:MalicParser.ThisExprContext):
        pass

    # Exit a parse tree produced by MalicParser#thisExpr.
    def exitThisExpr(self, ctx:MalicParser.ThisExprContext):
        pass


    # Enter a parse tree produced by MalicParser#variableExpr.
    def enterVariableExpr(self, ctx:MalicParser.VariableExprContext):
        pass

    # Exit a parse tree produced by MalicParser#variableExpr.
    def exitVariableExpr(self, ctx:MalicParser.VariableExprContext):
        pass


    # Enter a parse tree produced by MalicParser#literalExpr.
    def enterLiteralExpr(self, ctx:MalicParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by MalicParser#literalExpr.
    def exitLiteralExpr(self, ctx:MalicParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by MalicParser#DecIntegerConst.
    def enterDecIntegerConst(self, ctx:MalicParser.DecIntegerConstContext):
        pass

    # Exit a parse tree produced by MalicParser#DecIntegerConst.
    def exitDecIntegerConst(self, ctx:MalicParser.DecIntegerConstContext):
        pass


    # Enter a parse tree produced by MalicParser#StringConst.
    def enterStringConst(self, ctx:MalicParser.StringConstContext):
        pass

    # Exit a parse tree produced by MalicParser#StringConst.
    def exitStringConst(self, ctx:MalicParser.StringConstContext):
        pass


    # Enter a parse tree produced by MalicParser#boolConst.
    def enterBoolConst(self, ctx:MalicParser.BoolConstContext):
        pass

    # Exit a parse tree produced by MalicParser#boolConst.
    def exitBoolConst(self, ctx:MalicParser.BoolConstContext):
        pass


    # Enter a parse tree produced by MalicParser#nullConst.
    def enterNullConst(self, ctx:MalicParser.NullConstContext):
        pass

    # Exit a parse tree produced by MalicParser#nullConst.
    def exitNullConst(self, ctx:MalicParser.NullConstContext):
        pass


    # Enter a parse tree produced by MalicParser#errorCreator.
    def enterErrorCreator(self, ctx:MalicParser.ErrorCreatorContext):
        pass

    # Exit a parse tree produced by MalicParser#errorCreator.
    def exitErrorCreator(self, ctx:MalicParser.ErrorCreatorContext):
        pass


    # Enter a parse tree produced by MalicParser#arrayCreator.
    def enterArrayCreator(self, ctx:MalicParser.ArrayCreatorContext):
        pass

    # Exit a parse tree produced by MalicParser#arrayCreator.
    def exitArrayCreator(self, ctx:MalicParser.ArrayCreatorContext):
        pass


    # Enter a parse tree produced by MalicParser#nonarrayCreator.
    def enterNonarrayCreator(self, ctx:MalicParser.NonarrayCreatorContext):
        pass

    # Exit a parse tree produced by MalicParser#nonarrayCreator.
    def exitNonarrayCreator(self, ctx:MalicParser.NonarrayCreatorContext):
        pass


