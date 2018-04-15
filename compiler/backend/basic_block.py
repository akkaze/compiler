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

        self.use = set()
        self.ddef = set()
        self.live_in = set()
        self.live_out = set()
