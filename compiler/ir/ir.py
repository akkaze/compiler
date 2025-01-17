from abc import ABC, abstractmethod

class IR(object):
    id = 0
    def __init__(self):
        self.id = IR.id
        IR.id += 1
     
    @abstractmethod
    def accept(emitter):
        pass
