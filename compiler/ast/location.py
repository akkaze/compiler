from antlr4 import ParserRuleContext, Token
from antlr4.tree.Tree import TerminalNode

class Location:
    line = -1
    column = -1
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Token):
                self.line = args[0].line
                self.column = args[0].column
            elif isinstance(args[0], ParserRuleContext):
                token = args[0].start
                self.line = token.line
                self.column = token.column
            elif isinstance(args[0], TerminalNode):
                token = args[0].getSymbol()
                self.line = token.line
                self.column = token.column
            else:
                raise TypeError('unexpected type')
        else:
            self.line = args[0]
            self.column = args[1]

    def __str__(self):
        return 'line ' + str(self.line) + ':' + str(self.column) + ' '
