from abc import ABC, abstractmethod

class AbstractRepository(ABC):   
    
    @abstractmethod
    async def get_objects():
        raise NotImplementedError   
    
    @abstractmethod
    async def insert_object():
        raise NotImplementedError
    
    @abstractmethod
    async def update_object():
        raise NotImplementedError