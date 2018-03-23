from abc import ABC, abstractmethod

class Instruction(ABC):
    predecessor = None
    successor = None

    iin = None
    out = None

    use = None
    ddef = None

    all_ref = None
    live = None

    def __init__(self):
        self.predecessor = dict()
        self.successor = dict()
    @abstractmethod
    def replace_use(self, ffrom, to):
        pass
    
    @abstractmethod
    def replace_def(self, ffrom, to):
        pass

    def replace_all(self, ffrom, to):
        self.replace_use(ffrom, to)
        self.replace_def(ffrom, to)

    @property
    def use(self):
        if not self.use:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.use

    @property
    def ddef(self):
        if not self.ddef:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.ddef

    def init_def_and_use(self):
        self.use = dict()
        self.ddef = dict()
        self.all_ref = dict()
    
    @property
    def all_ref(self):
        if not self.all_ref:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.all_ref


    @abstractmethod
    def calc_def_and_use(self):
        pass
    
    @property
    def live(self):
        if not self.live:
            live = dict()
            for ref in self.iin:
                if ref.alias:
                    self.live.append(ref.alias)
                else:
                    self.live.append(ref)
            for ref in self.out:
                if ref.alias:
                    self.live.append(ref.alias)
                else:
                    self.live.apend(ref)

        return self.live 
