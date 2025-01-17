import logging

from compiler.options import *
from compiler.typ.function_type import FunctionType
from compiler.entity import entity
from compiler.entity.class_entity import ClassEntity
from compiler.entity.parameter_entity import ParameterEntity
from compiler.ast import block_node, for_node, if_node


class FunctionEntity(entity.Entity):

    def __init__(self, loc, return_type, name, params, body):
        super(FunctionEntity, self).__init__(loc, FunctionType(name), name)
        self.params = params
        for arg_idx, param in enumerate(self.params):
            param.func_entity = self
            param.arg_idx = arg_idx
        self.body = body
        self.return_type = return_type
        self.type.entity = self
        self.calls = set()
        self.irs = []
        self.bbs = []
        self.tmp_stack = []
        self.reg_used = []
        self.all_reference = set()
        self.is_constructor = False
        self.is_inlined = False
        self.is_libfunction = False
        self.m_stmt_size = 1

        self.visited = dict()

    def add_thispointer(self, loc, entity):
        assert isinstance(entity, ClassEntity)
        thispointer = ParameterEntity(loc, entity.type, 'this')
        self.params.insert(0, thispointer)
        return thispointer

    @property
    def asm_name(self):
        if self.m_asm_name:
            return self.m_asm_name
        else:
            return self.name

    @asm_name.setter
    def asm_name(self, name):
        self.m_asm_name = name
    # check whether can be inlined

    def check_inlinable(self):
        global options
        if self.name == 'main':
            self.is_inlined = False
        else:
            self.visited = dict()
            self.is_inlined = not self.find_loop(self, self)
            self.m_stmt_size = self.stmt_size(self.body)
            if self.m_stmt_size > 8:
                self.is_inlined = False
            if self.is_inlined and options.enable_function_inline and options.print_inline_info:
                logging.info(self.name + ' is inlined')

    def can_be_self_inline(self, depth):
        if depth >= 3:
            return False
        pow = 1
        for i in range(depth + 1):
            pow *= self.m_stmt_size
        return pow < 40

    def stmt_size(self, node):
        ct = 0
        if node == None:
            return 0
        if isinstance(node, block_node.BlockNode):
            for stmt_node in node.stmts:
                if isinstance(stmt_node, block_node.BlockNode):
                    ct += self.stmt_size(stmt_node)
                elif isinstance(stmt_node, for_node.ForNode):
                    ct += 3 + self.stmt_size(stmt_node.body)
                elif isinstance(stmt_node, if_node.IfNode):
                    ct += 1 + self.stmt_size(stmt_node.else_body)
                    + self.stmt_size(stmt_node.then_body)
                else:
                    ct += 1
        else:
            return 1
        return ct

    def find_loop(self, called, root):
        if called in self.visited:
            return called == root
        self.visited[called] = True
        for func in called.calls:
            if self.find_loop(func, root):
                return True
        return False

    # for locating local variables
    def all_local_variables(self):
        return self.scope.all_local_variables()

    def set_label_ir(self, begin, end):
        self.begin_label_ir = begin
        self.end_label_ir = end

    def set_label_ins(self, begin, end):
        self.begin_label_ins = begin
        self.end_label_ins = end

    def add_call(self, entity):
        self.calls.add(entity)

    def __str__(self):
        return 'function entity : ' + self.name
