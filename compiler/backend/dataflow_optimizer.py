from compiler.ins import *
from compiler.ins.operand import *
from compiler.options import options

global options


class Expression:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def __hash__(self):
        hash_code = hash(self.name)
        if self.left:
            hash_code *= hash(self.left)
        if self.right:
            hash_code *= hash(self.right)
        return hash_code

    def __eq__(self, other):
        if isinstance(other, Expression):
            if not self.right:
                first = self.name == other.name and \
                    self.left == other.left and \
                    not other.right
            else:
                first = self.name == other.name and \
                    self.left == other.left and \
                    self.right == other.right
            return first
        return False


class DataFlowAnalyzer:
    def __init__(self, emitter):
        self.dead_code_ct = 0
        self.tmp_ct = 0
        self.copy_table = set()
        self.expr_table = set()
        self.function_entities = emitter.function_entities

        self.sorted = []
        self.visited = set()

    def optimize(self):
        for function_entity in self.function_entities:
            if function_entity.is_inlined:
                continue
            self.current_function = function_entity
            if options.enable_common_expression_elimination:
                self.common_subexpression_elimination(function_entity)
            if options.enable_constant_propagation:
                self.constant_propagation(function_entity)
                self.refresh_def_and_use(function_entity)
            if options.enable_deadcode_elimination:
                self.init_liveness_analysis(function_entity)
                for i in range(2):
                    self.liveness_analysis(function_entity)
                    for bb in function_entity.bbs:
                        self.dead_code_elimination(bb)
                    self.refresh_def_and_use(function_entity)

    def refresh_def_and_use(self, entity):
        for bb in entity.bbs:
            for ins in bb.ins:
                ins.init_def_and_use()
                ins.calc_def_and_use()

    def remove_key(self, to_remove):
        for left, right in self.expr_table.items():
            if right == to_remove:
                del self.expr_table[left]
                break
        if to_remove in self.copy_table:
            del self.copy_table[to_remove]
        to_removes = []
        for left, right in self.copy_table.items():
            if right == to_remove:
                to_removes.append(left)
        for to_remove in to_removes:
            del self.copy_table[to_remove]

    def put_expr(self, res, expr):
        self.remove_key(res)
        self.expr_table[expr] = res

    def put_copy(self, dest, src):
        self.remove_key(dest)
        self.copy_table[dest] = src

    def replace_copy(self, operand):
        for ffrom, to in self.copy_table.items():
            operand = operand.replace(ffrom, to)
        return operand
    # create a new copy reference and a instruction that copy dest into it

    def transform_move(self, dest, src, to_add):
        copy = Reference('tmp_copy_' + str(self.tmp_ct),
                         Reference.Type.UNKNOWN)
        self.tmp_ct += 1
        # src -> copy
        self.put_copy(copy, src)
        # src -> dest
        self.put_copy(dest, src)
        to_add.append(Move(copy, dest))
        self.current_function.tmp_stack.append(copy)

    def transform_expr(self, dest, expr, to_add):
        copy = Reference('tmp_copy_' + str(self.tmp_ct),
                         Reference.Type.UNKNOWN)
        self.tmp_ct += 1
        # expr -> copy
        self.put_expr(copy, expr)
        # copy -> dest
        self.put_copy(dest, copy)
        to_add.append(Move(copy, dest))
        self.current_function.tmp_stack.append(copy)

    def common_subexpression_elimination(self, entity):
        for bb in entity.bbs:
            self.expr_table = dict()
            self.copy_table = dict()
            new_ins = []
            for ins in bb.ins:
                to_add = []
                if isinstance(ins, Move):                   # store
                    if ins.dest.is_address:
                        self.expr_table.clear()
                        self.copy_table.clear()
                    elif ins.is_ref_move:                   # mov ref1, ref2
                        # if ref1 is already occur as source of some copy instruction
                        # replace it as the dest as this instruction
                        # then an extra reference can be saved
                        dest = ins.dest
                        src = ins.src
                        src = self.replace_copy(src)
                        # move ref2 into a copy reference
                        self.transform_move(dest, src, to_add)
                    else:                                   # load ref1, expr
                        src = self.replace_copy(ins.src)
                        dest = ins.dest
                        # create a expression on behalf of expr
                        expr_src = Expression('unary', src, None)
                        # lookup it in the expr table
                        res = self.expr_table.get(expr_src)
                        if not res:
                            # not found
                            # put it into the expr_table
                            self.transform_expr(dest, expr_src, to_add)
                        else:
                            # found, directly move previous copy reference into dest
                            ins = Move(dest, res)
                            self.transform_move(dest, res, to_add)
                elif isinstance(ins, Bin):
                    if ins.left.is_address:                 # add [ref1], ref2
                        self.expr_table.clear()
                        self.copy_table.clear()
                    else:                                   # add ref1, 12
                        dest = ins.left
                        src1 = self.replace_copy(dest)
                        src2 = self.replace_copy(ins.right)

                        expr = Expression(ins.name, src1, src2)
                        res = self.expr_table.get(expr)
                        if not res:
                            self.transform_expr(dest, expr, to_add)
                        else:
                            ins = Move(dest, res)
                            self.transform_move(dest, res, to_add)
                elif isinstance(ins, Lea): # the same as copy
                    dest = ins.dest
                    src = self.replace_copy(ins.addr)
                    expr_src = Expression('dis address', src, None)
                    res = self.expr_table.get(expr_src)
                    if not res:
                        self.transform_expr(dest, expr_src, to_add)
                    else:
                        ins = Move(dest, res)
                        self.transform_move(dest, res, to_add)
                else:
                    self.expr_table.clear()
                    self.copy_table.clear()
                new_ins.append(ins)
                new_ins.extend(to_add)
            bb.ins = new_ins

    def get_constant(self, operand):
        if not operand:
            return (False, None)
        is_constant = False
        value = 0
        if operand.is_const_int:
            is_constant = True
            value = operand.value
        else:
            if operand in self.constant_table:
                is_constant = True
                value = self.constant_table[operand]
            if isinstance(operand, Address):
                self.replace_address(operand)
        return (is_constant, value)

    def replace_address(self, addr):
        base = self.get_constant(addr.base)
        index = self.get_constant(addr.index)
        if index[0]:
            addr.add = addr.mul * index[1] + addr.add
            add.index = None

    def constant_propagation(self, entity):
        for bb in entity.bbs:
            self.constant_table = dict()
            new_ins = []
            for ins in bb.ins:
                if isinstance(ins, Move):
                    dest = ins.dest
                    src = ins.src
                    if not dest.is_address:
                        ret = self.get_constant(src)
                        if ret[0]:
                            self.constant_table[dest] = ret[1]
                            ins.src = Immediate(ret[1])
                        else:
                            if dest in self.constant_table:
                                del self.constant_table[dest]
                    new_ins.append(ins)
                elif isinstance(ins, Bin):
                    left = self.get_constant(ins.left)
                    right = self.get_constant(ins.right)
                    if left[0] and right[0]:
                        value = 0
                        if ins.name == 'sal':
                            value = left[1] << right[1]
                        elif ins.name == 'sar':
                            value = left[1] >> right[1]
                        elif ins.name == 'add':
                            value = left[1] + right[1]
                        elif ins.name == 'sub':
                            value = left[1] - right[1]
                        elif ins.name == 'and':
                            value = left[1] & right[1]
                        elif ins.name == 'imul':
                            value = left[1] * right[1]
                        elif ins.name == 'div':
                            value = int(left[1] / right[1])
                        elif ins.name == 'mod':
                            value = left[1] % right[1]
                        elif ins.name == 'xor':
                            value = left[1] ^ right[1]
                        elif ins.name == 'or':
                            value = left[1] | right[1]
                        else:
                            raise InternalError('invalid operator in constant propagation')
                        self.constant_table[ins.left] = value
                        new_ins.append(Move(ins.left, Immediate(value)))
                    else:
                        if left[0]:
                            del self.constant_table[ins.left]
                        new_ins.append(ins)
                elif isinstance(ins, Lea):
                    self.replace_address(ins.addr)
                    dest = self.get_constant(ins.dest)
                    if dest[0]:
                        self.constant_table.remove(ins.dest)
                    new_ins.append(ins)
                elif isinstance(ins, Label):
                    new_ins.append(ins)
                else:
                    self.constant_table.clear()
                    new_ins.append(ins)
            bb.ins = new_ins

    def dead_code_elimination(self, bb):
        new_ins = []
        for ins in bb.ins:
            if isinstance(ins, Bin) or isinstance(ins, Move):
                dead = False
                if len(ins.ddef) == 1:
                    dead = True
                    for ref in ins.ddef:
                        if ref in ins.out:
                            dead = False
                if not dead:
                    new_ins.append(ins)
                else:
                    self.dead_code_ct += 1
            else:
                new_ins.append(ins)
        bb.ins = new_ins

    def dfs_sort(self, bb):
        self.sorted.append(bb)
        self.visited.add(bb)
        for pre in bb.predecessor:
            if pre not in self.visited:
                self.dfs_sort(pre)

    def init_liveness_analysis(self, entity):
        self.sorted = []
        self.visited = set()
        for i in range(len(entity.bbs) - 1, -1, -1):
            pre = entity.bbs[i]
            if pre not in self.visited:
                self.dfs_sort(pre)

    def liveness_analysis(self, entity):
        for bb in entity.bbs:
            ddef = bb.ddef
            use = bb.use
            bb.live_in.clear()
            bb.live_out.clear()
            ddef.clear()
            use.clear()
            for ins in bb.ins:
                for ref in ins.use:
                    if ref not in ddef:
                        use.add(ref)
                for ref in ins.ddef:
                    ddef.add(ref)

        modified = True
        while modified:
            modified = False
            for bb in self.sorted:
                new_in = set()
                right = bb.live_out.copy()
                right -= bb.ddef
                new_in |= bb.use
                new_in |= right

                new_out = set()
                for suc in bb.successor:
                    new_out |= suc.live_in
                if not bb.live_in == new_in:
                    modified = True
                if not bb.live_out == new_out:
                    modified = True
                bb.live_in = new_in
                bb.live_out = new_out
        tmp = set()
        for bb in entity.bbs:
            live = bb.live_out.copy()
            for i in range(len(bb.ins) - 1, -1, -1):
                ins = bb.ins[i]
                tmp = live.copy()
                ins.out = tmp

                live -= ins.ddef
                live |= ins.use

                tmp = live.copy()
                ins.iin = tmp
