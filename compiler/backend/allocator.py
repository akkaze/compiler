from compiler.ins import *
from compiler.ins.operand import *
from compiler.utils import *
from compiler.options import options
import logging

class Allocator:
    function_entities = None
    registers = None
    param_register_refs = None
    caller_save_reg_refs = None
    reg_config = None
    rax = None
    rbx = None
    rcx = None
    rdx = None
    rsi = None
    rdi = None
    rsp = None
    rbp = None
    rrax = None
    rrbx = None
    rrcx = None
    rrdx = None
    rrsi = None
    rrdi = None
    rrsp = None
    rrbp = None

    rr10 = None
    rr11 = None
    colors = None
    global_scope = None

    
    def __init__(self, emitter, register_config):
        self.function_entities = emitter.function_entities
        self.reg_config = register_config
        self.global_scope = emitter.global_scope    
        self.registers  = self.reg_config.registers
        self.rax = self.registers[0]
        self.rbx = self.registers[1]
        self.rcx = self.registers[2]
        self.rdx = self.registers[3]
        self.rsi = self.registers[4]
        self.rdi = self.registers[5]
        self.rbp = self.registers[6]
        self.rsp = self.registers[7]
        
        self.rrax = Reference(self.rax)
        self.rr10 = Reference(self.registers[10])
        self.rr11 = Reference(self.registers[11])

        self.param_register_refs = []
        for register in self.reg_config.param_registers:
            self.param_register_refs.append(Reference(register))

        self.rrdi = self.param_register_refs[0]
        self.rrsi = self.param_register_refs[1]
        self.rrdx = self.param_register_refs[2]
        self.rrcx = self.param_register_refs[3]

        self.precolored = set()
        self.precolored |= set(self.param_register_refs)
        self.precolored.add(self.rrax)
        self.precolored.add(self.rr10)
        self.precolored.add(self.rr11)

        for ref in self.precolored:
            ref.is_precolored = True
            ref.color = ref.reg

        self.caller_save_reg_refs = set()
        for ref in self.precolored:
            if not ref.reg.is_callee_save:
                self.caller_save_reg_refs.add(ref)
        self.colors = []
        self.colors.extend(self.reg_config.param_registers)
        self.colors.append(self.rax)
        self.colors.append(self.reg_config.registers[1])
        self.colors.append(self.reg_config.registers[10])
        self.colors.append(self.reg_config.registers[11])
        self.colors.append(self.reg_config.registers[12])
        self.colors.append(self.reg_config.registers[13])
        self.colors.append(self.reg_config.registers[14])
        self.colors.append(self.reg_config.registers[15])
        self.K = len(self.colors) 
    def allocate(self):
        for function_entity in self.function_entities:
            if function_entity.is_inlined:
                continue
            self.init(function_entity)
            self.load_precolored(function_entity)
            self.allocate_function(function_entity)

            all_ref = set()
            reg_used = set()

            for bb in function_entity.bbs:
                for ins in bb.ins:
                    self.replace_reg_for_ins(ins, all_ref, reg_used)

            function_entity.all_reference = all_ref
            reg_use_list = list(reg_used)
            function_entity.reg_used = reg_use_list

            if self.iter != 1:
                function_entity.reg_used.append(self.rbp)
            function_entity.local_variable_offset = self.local_offset

    def init(self, entity):
        # global
        self.edge_edge_map = dict()
        self.edge_set = set()
        self.simplified_edge = set()
        # node set
        self.simplify_worklist = set()
        self.initial = set()
        self.freeze_worklist = set()
        self.spill_worklist = set()
        self.spilled_nodes = set()
        self.coalesced_nodes = set()
        self.colored_nodes = set()
        self.select_worklist = set()
        self.select_stack = []

        # move set
        self.coalesced_moves = set()
        self.constrained_moves = set()
        self.frozen_moves = set()
        self.worklist_moves =  set()
        self.active_moves = set()
        self.init_liveness_analysis(entity)
        self.local_offset = 0

    edge_set = None
    simplified_edge = None
    K = 0
    local_offset = None

    precolored = None
    initial = None
    simplify_worklist = None
    freeze_worklist = None
    spill_worklist = None
    spilled_nodes = None
    coalesed_nodes = None
    colored_nodes = None
    select_worklist = None
    select_stack = None

    coalesed_moves = None
    constrained_moves = None
    frozen_moves = None
    worklist_moves = None
    active_moves = None

    iter = 0
    
    def allocate_function(self, entity):
        finish = False
        self.iter = 0
        while True:
            self.liveness_analysis(entity)
            self.build(entity)
            self.make_work_list()
            while True:
                if len(self.simplify_worklist) != 0:
                    self.simplify()
                elif len(self.worklist_moves) != 0:
                    self.coalesce()
                elif len(self.freeze_worklist) != 0:
                    self.freeze()
                elif len(self.spill_worklist) != 0:
                    self.select_spill()
                if len(self.simplify_worklist) == 0 and \
                    len(self.worklist_moves) == 0 and \
                    len(self.freeze_worklist) == 0 and \
                    len(self.spill_worklist) == 0:
                    break
            self.assign_colors(entity)
            finish = (len(self.spilled_nodes) == 0)
            self.rewrite_program(entity)
            self.iter += 1
            if finish:
                break
    
    sorted = None
    visited = None

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
        if options.print_global_allocation_info:
            logging.info('====== USE & DEF ======')
            for bb in entity.bbs:
                for ins in bb.ins:
                    log_str = '{0: >20}'.format(str(ins)) 
                    log_str += '     def: '
                    for ref in ins.ddef:
                        log_str += ' ' + str(ref)
                    log_str += '     use:'
                    for ref in ins.use:
                        log_str += ' ' + str(ref)
                    logging.info(log_str) 
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
                if self.iter == 0:
                    self.initial |= ins.all_ref
        modified = True
        # among blocks
        while modified:
            modified = False
            for bb in self.sorted:
                new_in = set()
                right = set(bb.live_out)
                right -= bb.ddef
                new_in |= bb.use
                new_in |= right

                new_out = set()
                for suc in bb.successor:
                    new_out |= suc.live_in
                if not (bb.live_in == new_in and \
                    bb.live_out == new_out):
                    modified = True
                bb.live_in = new_in
                bb.live_out = new_out
    def build(self, entity):
        self.simplified_edge.clear()
        self.edge_set.clear()
        self.initial -= self.precolored
        for ref in self.initial:
            ref.reset()
        for ref in self.precolored:
            ref.reset()
        # build inference graph
        for bb in entity.bbs:
            live = set(bb.live_out)
            
            for i in range(len(bb.ins) - 1, -1, -1):
                ins = bb.ins[i]
                for ref in live:
                    ref.ref_times += 1
                
                tmp = set(live) 
                ins.out = tmp
                if isinstance(ins, Move) and ins.is_ref_move:
                    live -= ins.use
                    for ref in ins.ddef:
                        ref.move_list.add(ins)
                    for ref in ins.use:
                        ref.move_list.add(ins)
                    self.worklist_moves.add(ins)
                live |= ins.ddef
                for d in ins.ddef:
                    for l in live:
                        self.add_edge(d, l)

                live -= ins.ddef
                live |= ins.use

                tmp = set(live)
                ins.iin = tmp

        if options.print_global_allocation_info:
            logging.info('====== IN & OUT ======')
            for bb in entity.bbs:
                for ins in bb.ins:
                    log_str = '{0: >20}'.format(str(ins))
                    log_str += '      in:'
                    for ref in ins.iin:
                        log_str += ' ' + str(ref)
                    log_str += '     out:'
                    for ref in ins.out:
                        log_str += ' ' + str(ref)
                    logging.info(log_str)
                logging.info('')
        
        if options.print_global_allocation_info:
            logging.info('===== EDGE =====')
            for u in self.initial:
                log_str = '{0: >10}'.format(u.name) + ':'
                for v in u.adj_list:
                    log_str += ' ' + v.name
                logging.info(log_str)
    def make_work_list(self):
        for ref in self.initial:
            if ref.degree >= self.K:
                self.spill_worklist.add(ref)
            elif self.is_move_related(ref):
                self.freeze_worklist.add(ref)
            else:
                self.simplify_worklist.add(ref)
    def simplify(self):
        ref = list(self.simplify_worklist)[0]
        self.move(ref, self.simplify_worklist, self.select_worklist)
        self.select_stack.append(ref)

        backup = ref.adj_list.copy()
        for adj in backup:
            self.simplified_edge.add(Allocator.Edge(adj, ref))
            self.simplified_edge.add(Allocator.Edge(ref, adj))
            self.delete_edge(ref, adj)
        
    def decrease_degree(self, ref):
        d = ref.degree
        ref.degree -= 1
        if d == self.K:
            self.enable_moves(ref)
            for adj in ref.adj_list:
                self.enable_moves(ref)
            if ref in self.spill_worklist:
                if self.is_move_related(ref):
                    self.move(ref, self.spill_worklist, \
                        self.freeze_worklist)
                else:
                    self.move(ref, self.spill_worklist, \
                        self.simplify_worklist)
    def is_move_related(self, ref):
        for ins in ref.move_list:
            if (ins in self.active_moves) or \
                (ins in self.worklist_moves):
                return True
        return False

    def enable_moves(self, ref):
        for move in ref.move_list:
            if move in self.active_moves:
                self.active_moves.remove(move)
                self.worklist_moves.add(move)

    def is_ok(self, u, v):
        for t in v.adj_list:
            if not (t.degree < self.K or (t in self.precolored) or \
                (self.get_edge(t, u) in self.edge_set)):
                return False
        return True

    def conservative(self, u, v):
        k = 0
        adjs = set()
        adjs |= u.adj_list
        adjs |= v.adj_list
        for ref in adjs:
            if ref.degree >= self.K:
                k += 1
        return k < self.K
    
    def get_alias(self, ref):
        if ref in self.coalesced_nodes:
            ref.alias = self.get_alias(ref.alias)
            return ref.alias
        else:
            return ref

    def add_worklist(self, ref):
        if ref not in self.precolored and not \
            self.is_move_related(ref) and \
            ref.degree < self.K:
            self.move(ref, self.freeze_worklist, \
                self.simplify_worklist)
    def combine(self, u, v):
        if v in self.freeze_worklist:
            self.move(v, self.freeze_worklist, self.coalesced_nodes)
        else:
            self.move(v, self.spill_worklist, self.coalesced_nodes)

        v.alias = u
        u.move_list |= v.move_list
        self.enable_moves(v)

        backup = v.adj_list.copy()
        for t in backup:
            self.delete_edge(t, v)
            self.add_edge(u, t)
            if t.degree >= self.K and (t in self.freeze_worklist):
                self.move(t, self.freeze_worklist, self.spill_worklist)
        if u.degree >= self.K and (u in self.freeze_worklist):
            self.move(u, self.freeze_worklist, self.spill_worklist)
    def coalesce(self):
        move =  list(self.worklist_moves)[0]
        x = self.get_alias(move.src)
        y = self.get_alias(move.dest)
        u = None
        v = None
        if y in self.precolored:
            u = y
            v = x
        else:
            u = x
            v = y
        self.worklist_moves.remove(move)
        if u == v:
            self.coalesced_moves.add(move)
            self.add_worklist(u)
        elif (v in self.precolored) or \
            (self.get_edge(u, v) in self.edge_set):
            self.constrained_moves.add(move)
            self.add_worklist(u)
            self.add_worklist(v)
        elif ((u in self.precolored) and self.is_ok (u, v) or \
            u not in self.precolored) and self.conservative(u, v):
            self.coalesced_moves.add(move)
            self.combine(u, v)
            self.add_worklist(u)
        else:
            self.active_moves.add(move)

    def freeze(self):
        u = self.freeze_worklist[0]
        self.move(self.freeze_worklist, \
            self.simplify_worklist)
        self.freeze_moves(u)

    def freeze_moves(self, u):
        for move in u.move_list:
            if (move in self.active_moves) or \
                (move in self.worklist_moves):
                v = None
                if self.get_alias(move.src) == \
                    self.get_alias(move.dest):
                    v = self.get_alias(move.src)
                else:
                    v = self.get_alias(move.dest)
                self.active_moves.remove(move)
                self.frozen_moves.add(move)
                is_empty = True
                for mov in v.move_list:
                    if (mov in self.active_moves) or \
                        (mov in self.worklist_moves):
                        is_empty = False
                        break
                if is_empty and (v in self.freeze_worklist):
                    self.move(v, self.freeze_worklist, \
                        self.simplify_worklist)

    protect = None
    def select_spill(self):
        to_spill = self.spill_worklist[0] 
        self.protect.add('i')
        self.protect.add('j')
        i = 1
        while (to_spill.name in self.protect) or \
            ('spill' in to_spill.name) and i < len(self.spill_worklist):
            to_spill = self.spill_worklist[i]
            i += 1
        self.move(to_spill, self.spill_worklist, self.simplify_worklist)
        self.freeze_moves(to_spill)

    def move(self, ref, ffrom, to):
        if ref in ffrom:
            if ref not in to:
                ffrom.remove(ref)
                to.add(ref)
            else:
                raise InternalError('already exist move ' + ref.name +\
                    ' from ' + str(ffrom) + ' to ' + str(to))
        else:
            raise InternalError('empty move ' + ref.name + \
                ' from ' + str(ffrom) + ' to ' + str(to))

    def assign_colors(self, entity):
        for edge in self.simplified_edge:
            self.add_edge(self.get_alias(edge.u), \
                self.get_alias(edge.v))
        ok_colors = []
        while len(self.select_stack) != 0:
            n = self.select_stack[-1]
            self.select_stack.pop()
            ok_colors.clear()
            for color in self.colors:
                ok_colors.append(color)

            for w in n.adj_list:
                w = self.get_alias(w)
                if (w in self.colored_nodes) or (w in self.precolored):
                    ok_colors.remove(w.color)
            if len(ok_colors) == 0:
                self.move(n, self.select_worklist, spilled_nodes)
                n.color = None
            else:
                color = ok_colors[0]
                self.move(n, self.select_worklist, self.colored_nodes)
                n.color = color
            for node in self.coalesced_nodes:
                node.color = self.get_alias(node).color

        if options.print_global_allocation_info:
            logging.info('=== Assign Result === ({} {})'\
                .format(entity.name, self.iter))
            log_str = 'colored :'
            for ref in self.colored_nodes:
                log_str += ' ' + ref.name + '(' + \
                    ref.color.name + ')'
            logging.info(log_str)
            log_str = 'coalesced :'
            for ref in self.coalesced_nodes:
                log_str += ' ' + ref.name + '(' + \
                    self.get_alias(ref).name + ')'
            logging.info(log_str)
            log_str = 'spilled :'
            for ref in self.spilled_nodes:
                log_str += ' ' + ref.name
            logging.info(log_str)

    spilled_counter = 0
    def rewrite_program(self, entity):
        new_temp = set()
        new_ins = []
        for ref in self.spilled_nodes:
            ref.is_spilled = True
            self.local_offset += options.REG_SIZE
            ref.set_offset(-self.local_offset, self.rbp)

        for ref in self.coalesced_nodes:
            self.get_alias(ref)

        stores = []
        for bb in entity.bbs:
            new_ins = []
            for ins in bb.ins:
                ins_use = ins.use
                ins_def = ins.ddef

                stores.clear()

                if not isinstance(ins, Label):
                    for use in ins_use:
                        if use.is_spilled:
                            if use in ins_deef:
                                tmp = Reference('spill_' + use.name + '_'\
                                    + str(self.spill_counter), \
                                    Reference.Type.UNKNOWN)
                                self.spill_counter += 1
                                new_temp.add(tmp)
                                new_ins.add(Move(tmp, Address(\
                                    self.rbp, None, 1, use.offset)))
                                ins.replace_all(use, tmp)
                                stores.append(Move(Address(\
                                    self.rbp, None, 1, use.offset)))
                            else:
                                if isinstance(ins, Move) and not \
                                    ins.dest.is_address and ins.src == use:
                                    ins = Move(ins.dest, Address(\
                                        self.rbp, None, 1, use.offset))
                                else:
                                    tmp = Reference('spill_' + use.name + '_'\
                                        + str(self.spill_counter), \
                                        Reference.Type.UNKNOWN)
                                    new_temp.add(tmp)
                                    new_ins.add(Move(tmp, Address(\
                                        self.rbp, None, 1, use.offset)))
                                    ins.replace_use(use, tmp)
                    for ddef in ins_def:
                        if ddef.is_spilled:
                            if ddef in ins_use:
                                pass
                            else:
                                if isinstance(ins, Move) or (not \
                                    ins.src.is_address and \
                                    move.ins.dest == ddef):
                                    ins = Move(Address(\
                                        self.rbp, None, 1, ddef.offset),
                                        ins.src)
                                else:
                                    tmp = Reference('spill_' + ddef.name + \
                                        '_' + str(self.spill_counter), \
                                        Reference.Type.UNKNOWN)
                                    new_temp.add(tmp)
                                    ins.replace_def(ddef, tmp)
                                    stores.append(Move(Address(\
                                        self.rbp, None, 1, ddef.offset)),
                                        tmp)
                for ref in ins.all_ref:
                    if ref in self.coalesced_nodes:
                        ins.replace_all(ref, self.get_alias(ref))
                ins.init_def_and_use()
                ins.calc_def_and_use()
                if isinstance(ins, Move) and ins.is_ref_move and \
                    ins.dest == ins.src:
                    pass
                else:
                    new_ins.append(ins)
                new_ins.extend(stores)
            bb.ins = new_ins

        for param in entity.params:
            if param.reference in self.coalesced_nodes:
                param.reference = self.get_alias(param.reference)
            if param.reference in self.colored_nodes:
                param.reference.register = param.reference.color
        if options.print_global_allocation_info:
            logging.info('===== REWRITE ======')
            for bb in entity.bbs:
                for ins in bb.ins:
                    logging.info(str(ins))
        self.select_stack.clear()
        self.select_worklist.clear()
        self.spilled_nodes.clear()
        self.initial.clear()
        self.initial |= self.colored_nodes
        self.initial |= self.coalesced_nodes
        self.initial |= new_temp
        self.colored_nodes.clear()
        self.coalesced_nodes.clear()
    def load_precolored(self, entity):
        for bb in entity.bbs:
            new_ins = []
            for raw in bb.ins:
                if isinstance(raw, Call):
                    param_reg_used = set()
                    ins = raw
                    push_ct = 0
                    i = 0
                    for operand in ins.operands:
                        if i < len(self.param_register_refs):
                            param_reg_used.add(\
                                self.param_register_refs[i])
                            new_ins.append(Move(\
                                self.param_register_refs[i], operand))
                        else:
                            if isinstance(operand, Immediate):
                                tmp = Reference('tmp_push', \
                                    Reference.Type.UNKNWON) 
                                new_ins.append(Move(tmp, operand))
                                operand = tmp
                            new_ins.append(Push(operand))
                            push_ct += 1
                        i += 1
                    new_call = Call(ins.entity, [])
                    new_call.caller_save = self.caller_save_reg_refs
                    new_call.used_parameter_register = param_reg_used
                    new_ins.append(new_call)
                    if push_ct > 0:
                        new_ins.append(Add(self.rbp, \
                            Immediate(self.push_ct * REG_SIZE)))
                    if ins.ret:
                        new_ins.append(Move(ins.ret, self.rrax))
                elif isinstance(raw, Div) or isinstance(raw, Mod):
                    new_ins.append(Move(self.rrax, raw.left))
                    new_ins.append(Move(self.rrdx, self.rdx))

                    right = raw.right
                    if isinstance(right, Immediate):
                        new_ins.append(Move(self.rrcx, right))
                        right = self.rrcx
                    elif isinstance(raw, Div):
                        new_ins.append(Div(self.rrax, right))
                        new_ins.append(Move(self.rrax, self.rax))
                        new_ins.append(Move(self.rrdx, self.rdx))
                        new_ins.append(Move(raw.left, self.rrax))
                    else:
                        new_ins.append(Mod(self.rrax, right))
                        new_ins.append(Mod(self.rrax, self.rax))
                        new_ins.append(Move(self.rrdx, self.rdx))
                        new_ins.append(Move(raw.left, self.rrdx))
                elif isinstance(raw, Return):
                    if raw.ret:
                        new_ins.append(Move(self.rrax, raw.ret))
                    new_ins.append(Return(None))
                elif isinstance(raw, Label):
                    if raw == entity.begin_label_ins:
                        i = 0
                        for param in entity.params:
                            if i < len(self.param_register_refs):
                                new_ins.append(Move(param.reference, \
                                    self.param_register_refs[i]))
                            else:
                                new_ins.append(Move(param.reference, \
                                    param.source))
                            i += 1
                    new_ins.append(raw)
                elif isinstance(raw, Sal) or isinstance(raw, Sar):
                    if isinstance(raw.right, Immediate):
                        new_ins.append(raw)
                    else:
                        new_ins.append(Move(self.rrcx, raw.right))
                        if isinstance(raw, Sal):
                            new_ins.append(Sal(raw.left, self.rrcx))
                        else:
                            new_ins.append(Sar(raw.left, self.rrcx))
                elif isinstance(raw, Cmp):
                    left = raw.left
                    right = raw.right
                    self.trans_compare(new_ins, raw, left, right)
                elif isinstance(raw, CJump) and raw.type != CJump.Type.BOOL:
                    left = raw.left
                    right = raw.right
                    self.trans_compare(new_ins, raw, left, right)
                else:
                    new_ins.append(raw)
            bb.ins = new_ins
    def trans_compare(self, new_ins, raw, left, right):
        if left.is_address and right.is_address:
            tmp = Reference('tmp_cmp', Reference.Type.UNKNWON)
            new_ins.append(Move(tmp, left))
            if isinstance(raw, Cmp):
                raw.left = tmp
                new_ins.append(raw)
                new_ins.append(Move(left, tmp))
            else:
                raw.left = tmp
                new_ins.append(raw)
        else:
            new_ins.append(raw)

    class Edge(object):
        u = None
        v = None
        def __init__(self, u, v):
            self.u = u
            self.v = v

        def __str__(self):
            return '(' + str(self.u) + ',' + str(self.v) + ')'

        def __hash__(self):
            return hash(self.u) + hash(self.v)

        def __eq__(self, o):
            return self.u == o.u and self.v == o.v

    def add_edge(self, u, v):
        if u == v:
            return
        edge = self.get_edge(u, v)
        if edge not in self.edge_set:
            self.edge_set.add(edge)
            self.edge_set.add(self.get_edge(v, u))
            if not u.is_precolored:
                u.adj_list.add(v)
                u.degree += 1
            if not v.is_precolored:
                v.adj_list.add(u)
                v.degree += 1

    def delete_edge(self, u, v):
        edge = self.get_edge(u, v)
        edge2 = self.get_edge(v, u)
        if edge not in self.edge_set or \
            edge2 not in self.edge_set:
            raise InternalError('delete edge error')
        self.edge_set.remove(edge)
        self.edge_set.remove(edge2)

        if edge not in self.edge_edge_map or \
            edge2 not in self.edge_edge_map:
            self.edge_edge_map.remove(edge)
            self.edge_edge_map.remove(edge2)
        if v in u.adj_list:
            u.adj_list.remove(v)
        if u in v.adj_list:
            v.adj_list.remove(u)
        self.decrease_degree(u)
        self.decrease_degree(v)

    edge_edge_map = None
    def get_edge(self, u, v):
        tmp_edge = Allocator.Edge(u, v)
        find = self.edge_edge_map.get(tmp_edge)
        if not find:
            self.edge_edge_map[tmp_edge] = tmp_edge
            return tmp_edge
        else:
            return find

    def replace_reg_for_ins(self, ins, all_ref, reg_used):
        for ref in ins.all_ref:
            all_ref.add(ref)
            if ref.color:
                ref.set_register(ref.color)
                reg_used.add(ref.color)
