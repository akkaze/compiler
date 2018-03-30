global options
class DataFlowAnalyzer:
    function_entities = None
    current_function = None
    
    def __init__(self, emitter):
        self.function_entities = emitter.function_entities
    
    def optimize(self):
        for function_entity in self.function_entities:
            if function_entity.is_inlined:
                continue
            self.current_function = function_entity
        if options.enable_common_expression_elimination:
            self.comm_expression_elimination(function_entity)
        if options.enable_constant_propagation:
            self.constant_propagation(function_entity)
            self.refresh_def_and_use(function_entity)
        if options.enable_dead_code_elimination:
            self.init_liveness_analysis(function_entity)
            for i in range(2):
                self.livenss_analysis(function_entity)
                for bb in function_entity.bbs:
                    self.dead_code_elimination(bb)
                self.refresh_def_and_use(function_entity)


    def refresh_def_and_use(self, entity):
        for bb in entity.bbs:
            for ins in bb.ins:
                ins.init_def_and_use()
                ins.calc_def_and_use()

    class Expression:
        name = ''
        left = None
        right = None

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

    copy_table = dict()
    expr_table = dict()
    def remove_key(self, to_remove):
        for left, right in self.expr_table.items():
            if right == to_remove:
                del self.expr_table[left]
                break
        del self.copy_table[to_remove]
        to_removes = []
        for left, right in self.copy_table.items():
            if right == to_remove:
                to_removes.append(left)
        for to_remove in to_removes:
            del self.copy_table[to_remove]
    tmp_ct = 0
    def put_expr(self, res, expr)
        self.remove_key(res)
        self.expr_table[expr] = res
    def put_copy(self, dest, src):
        self.remove_key(dest)
        self.copy_table[dest] = src
    def replace_copy(self, operand):
        for ffrom,to in self.copy_table.items():
            operand = operand.replace(ffrom, to)
        return operand
    def tansform_move(self, dest, src, to_add):
        copy = Reference('tmp_copy_' + str(self.tmp_ct), \
                Reference.Type.UNKNOWN)
        self.tmp_ct += 1
        self.put_copy(copy, src)
        self.put_copy(dest, src)
        to_add.append(Move(copy, dest))
        self.current_function.tmp_stack.append(copy)
    def transform_expr(self, dest, expr, to_add):
        copy = Reference('tmp_copy+' + str(self.tmp_ct), \
                Reference.Type.UNKNOWN)
        self.put_expr(copy, expr)
        self.put_copy(dest, copy)
        to_add.append(Move(copy_dest))
        self.current_function.tmp_stack.append(copy)
    dead_code_ct = 0
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
                    self.dead_count += 1
            else:
                new_ins.append(ins)
        bb.ins = new_ins
    def dfs_sort(self, bb):
        self.sorted.append(bb)
        self.visited.append(bb)
        for pre in bb.predecessor:
            if not pre in visited:
                self.dfs_sort(pre)

    def init_init_liveness_analysis(self, entity):
        self.sorted = []
        self.visited = dict()
        for i in range(len(entity.bbs)):
            pre = entity.bbs[i - 1]
            if not self.visited[pre]:
                self.dfs_sort(pre)
    def liveness_analysis(self,entity):
        for bb in entity.bbs:
            ddef = bb.ddef
            use = bb.use
            bb.live_in.clear()
            bb.live_out.clear()
            for ins in bb.ins:
                for ref in ins.use:
                    if not ref in ddef:
                        use.append(ref)
                for ref in ins.ddef:
                    ddef.append(ref)

            modified = True
            while modified:
                for bb in self.sorted:
                    new_in = set()
                    right = bb.live_out
                    for ddef in bb.ddef:
                        right.remove(ddef)
                    new_in |= bb.use
                    new_in |= right

                    new_out = set()
                    for suc in bb.successor:
                        new_out |= suc.live_in
                    if bb.live_in == new_in
            
    
