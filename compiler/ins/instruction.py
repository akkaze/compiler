from abc import ABC, abstractmethod

class Instruction(ABC):
    id = 0
    def __init__(self):
        self.predecessor = []
        self.successor = []
        self.iin = set()
        self.out = set()
        self.m_use = set()
        self.m_ddef = set()
        self.m_all_ref = set()
        self.m_live = set()
        self.id = Instruction.id
        Instruction.id += 1
    
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
        if not self.m_all_ref:
            self.init_def_and_use()
            self.calc_def_and_use()
        return self.m_all_ref


    @abstractmethod
    def calc_def_and_use(self):
        pass
    
    @property
    def live(self):
        if not self.m_live:
            self.m_live = set()
            for ref in self.iin:
                if ref.alias:
                    self.m_live.add(ref.alias)
                else:
                    self.m_live.add(ref)
            for ref in self.out:
                if ref.alias:
                    self.m_live.add(ref.alias)
                else:
                    self.m_live.add(ref)

        return self.m_live 
