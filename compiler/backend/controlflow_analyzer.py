from compiler.ins import *
from compiler.backend import BasicBlock
from collections import deque
from compiler.options import *
import logging
import copy
global options
class ControlFlowAnalyzer:
    function_entities = None
    def __init__(self, emitter):
        self.function_entities = emitter.function_entities

    def build_controlflow(self):
        for function_entity in self.function_entities:
            if function_entity.is_inlined:
                continue
            self.build_basic_block(function_entity)
            self.build_controlflow_graph(function_entity)
            if options.enable_controlflow_optimization:
                self.optimize(function_entity)
            self.layout_basic_block(function_entity)
            if options.print_basic_blocks:
                self.print_self()

    ct = 0
    def build_basic_block(self, entity):
        bbs  = []

        bb = None
        for ins in entity.ins:
            if bb is None and not isinstance(ins, Label):
                label = Label('cfg_added_' + str(self.ct))
                self.ct += 1
                bb = BasicBlock(label)
                bb.ins.append(label)

            if isinstance(ins, Label):
                if bb:
                    bb.jump_to.append(ins)
                    bb.ins.append(Jmp(ins))
                    bbs.append(bb)
                bb = BasicBlock(ins)
                bb.ins.append(ins)
            else:
                bb.ins.append(ins)
                if isinstance(ins, Jmp):
                    bb.jump_to.append(ins.dest)
                    bbs.append(bb)
                    bb = None
                elif isinstance(ins, CJump):
                    bb.jump_to.append(ins.true_label)
                    bb.jump_to.append(ins.false_label)
                    bbs.append(bb)
                    bb = None

        if bb:
            bbs.append(bb)

        for bb in bbs:
            for label in bb.jump_to:
                bb.successor.append(label.basic_block)
                label.basic_block.predecessor.append(bb)
        entity.bbs = bbs
        entity.ins = None

    def build_controlflow_graph(self, entity):
        for bb in entity.bbs:
            ins = bb.ins
            for i in range(len(ins) - 1):
                ins[i].successor.append(ins[i + 1])
                ins[i + 1].predecessor.append(ins[i])
            
            first = ins[0]
            for pre in bb.predecessor:
                pre.ins[len(pre.ins) - 1].successor.append(first)
            last = ins[len(ins) - 1]
            for suc in bb.successor:
                suc.ins[0].predecessor.append(last)

    def optimize(self, entity):
        modified = True
        while(modified):
            modified = False
            now = None
            for bb in entity.bbs:
                if len(bb.successor) == 1 and \
                    len(bb.successor[0].predecessor) == 1:
                    now = bb
                    next_bb = now.successor[0]
                    if len(next_bb.successor):
                        modified = True
                        for next_next in next_bb.successor:
                            next_next.predecessor.remove(next_bb)
                            next_next.predecessor.append(now)
                            now.successor.append(next_next)
                        del next_bb.ins[0]
                        del now.ins[len(now.ins) - 1]
                        now.ins.extend(next_bb.ins)
                        entity.bbs.remove(next_bb)
                        now.successor.remove(next_bb)
                        break

            useless_basic_block = []
            for to_remove in entity.bbs:
                if len(to_remove.ins) < 2:
                    continue
                last = to_remove.ins[1]
                if len(to_remove.ins) == 2 and isinstance(last, Jmp):
                    backup = copy.deepycopy(to_remove.predecessor)
                    for pre in backup:
                        jump = pre.ins[len(pre.ins) - 1]
                        if isinstance(jump, Jmp):
                            modified = True
                            jump.dest = last.dest
                            pre.successor.remove(to_remove)
                            useless_basic_block.append(to_remove)
                            if len(to_remove.successor) == 1:
                                suc = to_remove.successor[0]
                                pre.successor.append(suc)
                                suc.predecessor.append(pre)
                        elif isinstance(jump, CJump):
                            modified = True
                            if jump.true_label == to_remove.label:
                                jump.true_label = last.dest
                            if jump.false_label == to_remove.label:
                                jump.false_label = last.dest
                            pre.successor.remove(to_remove)
                            useless_basic_block.append(to_remove)
                            if len(to_remove.successor) == 1:
                                suc = to_remove.successor[0]
                                pre.successor.append(suc)
                                suc.predecessor.append(pre)
                    if modified:
                        break
                for bb in entity.bbs:
                    if len(bb.predecessor) == 0 and \
                        bb.label != entity.begin_label_ins:
                        modified = True
                        useless_basic_block.append(bb)

                for bb in entity.bbs:
                    if len(bb.successor) == 2 and \
                        bb.successor[0] == bb.successor[1]:
                        logging.error('find redundant Cjump')

                for bb in useless_basic_block:
                    if bb in entity.bbs:
                        entity.bbs.remove(bb)

    def layout_basic_block(self, entity):
        bbs = entity.bbs
        queue = deque()
        queue.extend(bbs)
        new_bbs = []
        while len(queue):
            bb = queue.popleft()
            while bb != None and not bb.layouted:
                next_bb = None
                bb.layouted = True
                for suc in bb.successor:
                    if not suc.layouted:
                        last = bb.ins[len(bb.ins) - 1]
                        if isinstance(last, Jmp):
                            del bb.ins[len(bb.ins) - 1]
                        elif isinstance(last, CJump):
                            last.fall_through = suc.label
                        next_bb  = suc
                        break
                new_bbs.append(bb)
                bb = next_bb
        entity.bbs = new_bbs
        entity.ins = None

    def print_self(slef):
        for function_entity in self.function_entities:
            logging.error('====== ' + function_entity.name + ' ======')
            if function_entity.is_inlined:
                logging.erro('BE INLINED')
                continue
            for bb in function_entity.bbs:
                logging.error('---- b ---- jump to:')
                for label in bb.jump_to:
                    logging.error(' ' + label.name)
                logging.error()
                for ins in bb.ins:
                    logging.error(str(ins))
