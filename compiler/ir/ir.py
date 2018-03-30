from abc import ABC, abstractmethod

class IR(object):
    @abstractmethod
    def accept(emitter):
        pass
