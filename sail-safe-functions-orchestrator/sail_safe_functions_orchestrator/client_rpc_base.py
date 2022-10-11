from abc import ABC, abstractmethod

class ClientRPCBase(ABC):
    
    @abstractmethod
    def call(self, safe_function_class, *safe_function_arguments):
        raise NotImplementedError()
