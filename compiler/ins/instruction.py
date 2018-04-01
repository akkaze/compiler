from abc import ABC, abstractmethod

class Instruction(ABC):
    predecessor = None
    successor = None

    iin = None
    out = None

    m_use = None
    m_ddef = None

    m_all_ref = None
    live = None

    def __init__(self):
        self.predecessor = []
        self.successor = []
        self.iin = dict()
        self.out = dict()
    
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
        if not self.m_use:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.m_use

    @property
    def ddef(self):
        if not self.m_ddef:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.m_ddef
    
    def init_def_and_use(self):
        self.m_use = set()
        self.m_ddef = set()
        self.m_all_ref = set()
    
    @property
    def all_ref(self):
        if not self.m_all_reff:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.m_all_reff


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
