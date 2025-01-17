from compiler.frontend.ast_visitor import ASTVisitor
from compiler.ast import *
from compiler.entity import *
from compiler.utils import *
from compiler.typ.class_type import ClassType
from compiler.typ.array_type import ArrayType
from compiler.typ.function_type import FunctionType
from compiler.typ.string_type import StringType
from compiler.entity.function_entity import FunctionEntity
from compiler.entity.class_entity import ClassEntity
from compiler.entity.member_entity import MemberEntity
from compiler.ast.block_node import BlockNode
from compiler.ast.functiondef_node import FunctionDefNode
from compiler.ast.stringliteral_node import StringLiteralNode
from compiler.entity.string_const_entity import StringConstEntity
from compiler.entity import scope


class SymbolResolver(ASTVisitor):

    def __init__(self, top_level_scope):
        self.stack = []
        self.top_level_scope = top_level_scope
        self.current_scope = top_level_scope
        self.stack.append(top_level_scope)
        self.current_class = None
        self.current_this = None
        self.first_block_in_function = False

    def enter_scope(self):
        self.current_scope = scope.Scope(self.current_scope)
        self.stack.append(self.current_scope)

    def exit_scope(self):
        self.stack.pop()
        self.current_scope = self.stack[-1]

    def enter_class(self, entity):
        self.current_class = entity
        self.enter_scope()
        entity.scope = self.current_scope

    def exit_class(self):
        self.exit_scope()
        self.current_class = None

    def resolve_type(self, type):
        if isinstance(type, ClassType):
            entity = self.current_scope.lookup(type.name)
            if not entity or not isinstance(entity, ClassEntity):
                return False
            type.entity = entity
        elif isinstance(type, FunctionType):
            entity = self.current_scope.lookup(type.name)
            if not entity or not isinstance(entity, FunctionEntity):
                return False
            type.entity = entity
        elif isinstance(type, ArrayType):
            return self.resolve_type(type.base_type)
        return True

    def visit(self, node):
        if isinstance(node, FunctionDefNode):
            entity = node.entity
            self.enter_scope()
            entity.scope = self.current_scope
            if not self.resolve_type(entity.return_type):
                raise SemanticError(
                    node.location, 'Cannot resolve symbol : ' + entity.return_type)
            if self.current_class:
                self.current_this = entity.add_thispointer(
                    node.location, self.current_class)
            for param in entity.params:
                self.current_scope.insert(param)
                if not self.resolve_type(param.type):
                    raise SemanticError(
                        node.location, 'Cannot resolve symbol : ' + str(param.type))
            self.first_block_in_function = True
            self.visit(entity.body)
            self.exit_scope()
            return
        elif isinstance(node, ClassDefNode):
            entity = node.entity
            self.enter_class(entity)
            for member_var in entity.member_vars:
                self.current_scope.insert(MemberEntity(member_var.entity))
            for member_func in entity.member_funcs:
                self.current_scope.insert(member_func.entity)
            self.visit_stmts(entity.member_vars)
            self.visit_stmts(entity.member_funcs)
            self.exit_class()
            return
        elif isinstance(node, VariableDefNode):
            entity = node.entity
            if not self.resolve_type(entity.type):
                raise SemanticError(node.location, 'Cannot resolve symbol : '
                                    + str(node.name))
            if not self.current_class or \
                    self.current_class.scope != self.current_scope:
                if entity.initializer:
                    self.visit_expr(entity.initializer)
                self.current_scope.insert(entity)
            return
        elif isinstance(node, StringLiteralNode):
            entity = self.top_level_scope.lookup_current_level(
                StringType.STRING_CONST_PREFIX + node.value)
            if not entity:
                entity = StringConstEntity(
                    node.location, StringType(), node.value, node)
                self.top_level_scope.insert(entity)
            node.entity = entity
            return
        elif isinstance(node, CreatorNode):
            if not self.resolve_type(node.type):
                raise SemanticError(
                    node.location, 'Cannot resolve symbol : ' + node.type)
            if node.exprs:
                self.visit_exprs(node.exprs)
            return
        elif isinstance(node, BlockNode):
            if self.first_block_in_function:
                self.first_block_in_function = False
                node.scope = self.current_scope
                self.visit_stmts(node.stmts)
            else:
                self.enter_scope()
                node.scope = self.current_scope
                self.visit_stmts(node.stmts)
                self.exit_scope()
            return
        elif isinstance(node, VariableNode):
            entity = self.current_scope.lookup(node.name)
            if not entity:
                raise SemanticError(
                    node.location, 'Cannot resolve symbol : ' + node.name)
            node.entity = entity
            if self.current_class and self.current_class.scope.lookup_current_level(node.name):
                node.this_pointer = self.current_this
            return
        super().visit(node)
