class BasicBlock(object):
    predecessor = None
    successor = None
    label = None
    ins = None
    jump_to = None
    layouted = False
    
    use = None
    ddef = None
    
    live_in = None
    live_out = None
    
    def __init__(self, label):
        self.predecessor = []
        self.successor = []
        self.label = label
        self.label.basic_block = self

        self.ins = []
        self.jump_to = []

        self.use = dict()
        self.ddef = dict()
        self.live_in = dict()
        self.live_out = dict()
