from typing import Optional

class DatastoreService:

    def __init__(self) -> None:
        raise Exception('DatastoreService can only be created using get_instance method.')
    
    @staticmethod
    def get_instance() -> 'DatastoreService':
        if not hasattr(DatastoreService, 'singleton_instance'):
            DatastoreService.singleton_instance = object.__new__(DatastoreService)
            DatastoreService.singleton_instance.data = dict()
        return DatastoreService.singleton_instance
    
    async def set(self, id: str, item: str):
        self.singleton_instance.data[id] = item

    async def get(self, id: str) -> Optional[str]:
        return self.singleton_instance.data.get(id, None)