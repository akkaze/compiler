from compiler.ast import DefinitionNode, Location
from compiler.entity import *
from compiler.utils import SemanticError
from compiler.frontend.output_irrelevant_maker import OutputIrrelevantMaker
from compiler.frontend.symbol_resolver import SymbolResolver
from compiler.frontend.type_checker import TypeChecker
from compiler.ast.stringliteral_node import StringLiteralNode
from compiler.entity import scope


class AST(object):

    def __init__(self, definition_nodes, defined_class,
                 defined_function, defined_variable):
        self.definition_nodes = definition_nodes
        self.class_entities = defined_class
        self.function_entities = defined_function
        self.variable_entities = defined_variable
        self.scope = scope.Scope(True)

    def load_library(self, entities):
        for entity in entities:
            self.scope.insert(entity)

    def resolve_symbol(self):
        for class_entity in self.class_entities:
            self.scope.insert(class_entity)
        for function_entity in self.function_entities:
            self.scope.insert(function_entity)
        resolver = SymbolResolver(self.scope)
        resolver.visit_definitions(self.definition_nodes)

    def eliminate_output_irrelevant_node(self):
        if len(self.class_entities) != 0:
            return
        output_irrelevant_maker = OutputIrrelevantMaker(self)
        output_irrelevant_maker.visit_definitions(self.definition_nodes)

    def check_type(self):
        checker = TypeChecker(self.scope)
        checker.visit_definitions(self.definition_nodes)
        main_func = self.scope.lookup('main')
        if not main_func:
            raise SemanticError(Location(0, 0),
                                'main undefined')
        if not main_func.return_type.is_integer:
            raise SemanticError(Location(0, 0),
                                'main must return an integer')
