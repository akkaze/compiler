import logging
from compiler.frontend.ast_visitor import ASTVisitor
from compiler.options import options
from compiler.ast import *
from compiler.entity import *
from compiler.entity.variable_entity import VariableEntity
from compiler.entity.function_entity import FunctionEntity
from compiler.ast.functiondef_node import FunctionDefNode
from compiler.ast.for_node import ForNode
from compiler.ast.while_node import WhileNode
from compiler.ast.if_node import IfNode
from compiler.ast.unaryop_node import UnaryOpNode
from compiler.typ.array_type import ArrayType
from compiler.typ.class_type import ClassType



class DependenceEdge(object):

    def __init__(self, base, rely):
        self.base = base
        self.rely = rely

    def __hash__(self):
        return hash(self.base) + hash(self.rely)

    def __eq__(self, other):
        return isinstance(other, DependenceEdge) and \
            self.base == other.base and \
            self.rely == other.rely


class OutputIrrelevantMaker(ASTVisitor):
    def __init__(self, ast):
        self.global_scope = ast.scope
        self.visited = set()
        self.global_variables = set()

        self.collect_set = None

        self.assign_dependence_stack = []
        self.control_dependence_stack = []

        self.current_function = None
        self.main_function = None

        self.side_effect = 0

        for name, entity in ast.scope.entities.items():
            if isinstance(entity, VariableEntity):
                self.global_variables.add(entity)
            if isinstance(entity, FunctionEntity) and \
                    entity.name == 'main':
                self.main_function = entity

    def propa_output_irrelevant(self, entity):
        if entity.is_output_irrelevant:
            return
        for rely in entity.dependence:
            edge = DependenceEdge(entity, rely)
            if not edge in self.visited:
                self.visited.add(edge)
                rely.is_output_irrelevant = False
                self.propa_output_irrelevant(rely)

    def visit_definitions(self, defs):
        all_entity = self.global_scope.gather_all()
        for entity in all_entity:
            entity.is_output_irrelevant = True

        self.global_scope.lookup('print').is_output_irrelevant = False
        self.global_scope.lookup('println').is_output_irrelevant = False
        self.main_function.is_output_irrelevant = False
        before = 0
        after = -1
        while before != after:
            for definition_node in defs:
                self.visit_definition(definition_node)
            before = after
            after = 0
            for entity in all_entity:
                self.propa_output_irrelevant(entity)
            for entity in all_entity:
                if not entity.is_output_irrelevant:
                    after += 1
        for definition_node in defs:
            self.visit_definition(definition_node)
        self.visited.clear()

        global options
        if options.print_irrelevant_mark_info:
            print('******** EDGE ********')
            for entity in all_entity:
                print(entity.name + ' :', end='')
                for rely in entity.dependence:
                    print('    ' + rely.name, end='')
                print('')
            print('******** RES  ********')
            for entity in all_entity:
                print(entity.name + ': ' + str(entity.is_output_irrelevant))

    def visit(self, node):
        if isinstance(node, ClassDefNode):
            self.visit_stmts(node.entity.member_funcs)
            self.visit_stmts(node.entity.member_vars)
            return
        elif isinstance(node, FunctionDefNode):
            self.current_function = node.entity
            for param in self.current_function.params:
                self.current_function.add_dependence(param)
            self.visit_stmt(self.current_function.body)
            self.current_function = self.main_function
            return
        elif isinstance(node, VariableDefNode):
            if node.entity.initializer:
                self.visit(AssignNode(VariableNode(node.entity,
                                                   node.location),
                                      node.entity.initializer))
            return
        elif isinstance(node, AssignNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                lhs = node.lhs
                if (isinstance(lhs.type, ArrayType) or isinstance(lhs.type, ClassType)) and not isinstance(node.rhs, CreatorNode):
                    self.begin_collect()
                    self.visit_expr(node.lhs)
                    self.visit_expr(node.rhs)
                    for entity in self.fetch_collect():
                        entity.is_output_irrelevant = False
                    if self.current_function:
                        self.current_function.is_output_irrelevant = False
                else:
                    backup_side_effect = self.side_effect
                    base = self.get_base_entity(lhs)
                    self.assign_dependence_stack.append(base)
                    self.visit_expr(node.lhs)
                    self.visit_expr(node.rhs)
                    self.assign_dependence_stack.pop()

                    if self.current_function and (base in self.global_variables):
                        base.add_dependence(self.current_function)
                    if base.is_output_irrelevant and self.side_effect == backup_side_effect:
                        node.is_output_irrelevant = True
                    else:
                        node.is_output_irrelevant = False
                    self.side_effect = backup_side_effect
            return
        elif isinstance(node, VariableNode):
            if self.is_in_collect_mode():
                self.collect_set.add(node.entity)
            else:
                entity = node.entity
                if self.current_function and (entity in self.global_variables):
                    self.current_function.add_dependence(entity)
                for base in self.assign_dependence_stack:
                    base.add_dependence(entity)
                for control in self.get_all_control_vars():
                    entity.add_dependence(control)
            return
        elif isinstance(node, FuncallNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                if not node.function_type.entity.is_output_irrelevant:
                    self.begin_collect()
                    self.visit_expr(node.expr)
                    self.visit_exprs(node.args)
                    for entity in self.fetch_collect():
                        entity.is_output_irrelevant = False
                    for entity in self.get_all_control_vars():
                        entity.is_output_irrelevant = False
                else:
                    self.visit_expr(node.expr)
                    self.visit_exprs(node.args)
            return
        elif isinstance(node, ReturnNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                if node.expr:
                    self.begin_collect()
                    self.visit_expr(node.expr)
                    for entity in self.fetch_collect():
                        self.current_function.add_dependence(entity)
                    for entity in self.get_all_control_vars():
                        self.current_function.add_dependence(entity)
            return
        elif isinstance(node, ForNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                self.begin_collect()
                if node.init:
                    self.visit_expr(node.init)
                if node.cond:
                    self.visit_expr(node.cond)
                if node.incr:
                    self.visit_expr(node.incr)

                control_vars = set()
                control_vars |= self.fetch_collect()
                self.control_dependence_stack.append(control_vars)

                if node.init:
                    self.visit_expr(node.init)
                if node.cond:
                    self.visit_expr(node.cond)
                if node.incr:
                    self.visit_expr(node.incr)
                if node.body:
                    self.visit_stmt(node.body)
                self.control_dependence_stack.pop()
                self.mark_node(node, control_vars)
            return
        elif isinstance(node, WhileNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                self.begin_collect()
                self.visit_expr(node.cond)
                control_vars = self.fetch_collect()
                self.control_dependence_stack.append(control_vars)
                self.visit_expr(node.cond)
                if node.body:
                    self.visit_stmt(node.body)
                self.control_dependence_stack.pop()
                self.mark_node(node, control_vars)
            return
        elif isinstance(node, IfNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                self.begin_collect()
                self.visit_expr(node.cond)
                control_vars = set()
                control_vars = self.fetch_collect()
                self.control_dependence_stack.append(control_vars)
                self.visit_expr(node.cond)
                if node.then_body:
                    self.visit_stmt(node.then_body)
                if node.else_body:
                    self.visit_stmt(node.else_body)
                self.control_dependence_stack.pop()
                self.mark_node(node, control_vars)
            return
        elif isinstance(node, PrefixOpNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                self.visit_expr(node.expr)
                if node.operator == UnaryOpNode.UnaryOp.PRE_DEC or node.operator == UnaryOpNode.UnaryOp.PRE_INC:
                    self.side_effect += 1
                return
        elif isinstance(node, SuffixOpNode):
            if self.is_in_collect_mode():
                super().visit(node)
            else:
                self.visit_expr(node.expr)
                if node.operator == UnaryOpNode.UnaryOp.SUF_DEC or node.operator == UnaryOpNode.UnaryOp.SUF_INC:
                    self.side_effect += 1
                return
        super().visit(node)

    def is_in_collect_mode(self):
        return self.collect_set != None

    def begin_collect(self):
        self.collect_set = set()

    def fetch_collect(self):
        ret = self.collect_set
        self.collect_set = None
        return ret

    def get_all_control_vars(self):
        ret = set()
        for entity_set in self.control_dependence_stack:
            ret |= entity_set
        return ret

    def get_base_entity(self, node):
        if isinstance(node, ArefNode):
            return self.get_base_entity(node.base_expr)
        elif isinstance(node, MemberNode):
            return self.get_base_entity(node.expr)
        elif isinstance(node, VariableNode):
            return node.entity

    def mark_node(self, node, control_vars):
        if len(control_vars) == 0:
            node.is_outut_irrelevant = False
        else:
            irrelevant = True
            for control_var in control_vars:
                if not control_var.is_output_irrelevant:
                    irrelevant = False
            node.is_output_irrelevant = irrelevant
