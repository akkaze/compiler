import logging

from compiler.options import *
from compiler.type import FunctionType, Type
from compiler.entity import Entity, ParameterEntity
class FunctionEntity(Entity):
    return_type = None
    params = None
    body = None
    scope = None
    
    is_constructor = False
    is_libfunction = False
    
    is_inlined = False
    calls = None

    begin_label_ir = None
    end_label_ir = None
    
    begin_label_ins = None
    end_label_ins = None
    
    irs = None
    bbs = None
    tmp_stack = None
    frame_size = 0
    local_variable_offset = 0

    reg_used = None
    all_reference = None
    
    asm_name = ''

    def __init__(self, loc, return_type, name, params, body):
        super(FunctionEntity, self).__init__(loc, FunctionType(name), name)
        self.params = params
        self.body = body
        self.return_type = return_type
        self.type.entity = self
        self.calls = []
        self.irs = []
        self.bbs = []
        self.tmp_stack = []
        self.reg_used = []
        self.all_reference = set()
    def add_thispointer(self, loc, entity):
        thispointer = ParameterEntity(loc, entity.type, 'this')
        self.params.insert(0, thispointer)
        return thispointer
    
    visited = dict()
    # check whether can be inlined
    def check_inlinable(self):
        global options
        if self.name == 'main':
            self.is_inlined = False
        else:
            self.visited = dict()
            self.is_inlined = not self.find_loop(self, self)
            stmt_size = self.stmt_size(body)
            if stmt_size > 0:      
                self.is_inlined = False
            if self.is_inlined and options.enable_function_inline and options.print_inline_info:
                    logging.info(name + ' is inlined')

    def check_self_inline(self):
        if self.depth >= 3:
            return False
        pow = 1
        for i in range(self.depth + 1):
            pow *= self.stmt_size
        return pow < 40
    
    def stmt_size(self, node):
        ct = 0
        if node == None:
            return 0
        if isinstance(node, BlockNode):
            for stmt_node in node.stmts():
                if isinstance(stmt_node, BlockNode):
                    ct += self.stmt_size(stmt_node)
                elif isinstance(stmt_node, ForNode):
                    ct += 3 + self.stmt_size(stmt_node.body)
                elif isinstance(stmt_node, IfNode):
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
        visited[called] = True
        for func in called.calls():
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
        self.calls.append(entity)
    def __str__(self):
        return 'function entity : ' + self.name
