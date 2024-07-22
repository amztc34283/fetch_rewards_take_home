from typing import Optional

class DatastoreService:

    def __init__(self) -> None:
        raise Exception('DatastoreService can only be created using get_instance method.')
    
    """
    A static method that returns an instance of DatastoreService if it doesn't already exist, 
    creating it with an empty data dictionary if necessary.

    Returns:
        DatastoreService: The singleton_instance of DatastoreService.
    """
    @staticmethod
    def get_instance() -> 'DatastoreService':
        if not hasattr(DatastoreService, 'singleton_instance'):
            DatastoreService.singleton_instance = object.__new__(DatastoreService)
            DatastoreService.singleton_instance.data = dict()
        return DatastoreService.singleton_instance
    
    """
    Set the item for a given id in the datastore.

    Args:
        id (str): The unique identifier for the item.
        item (str): The item to be stored.

    Returns:
        None
        """
    async def set(self, id: str, item: str):
        self.singleton_instance.data[id] = item

    """
    Retrieves the item associated with the given ID from the datastore.

    Args:
        id (str): The unique identifier of the item to retrieve.

    Returns:
        Optional[str]: The item associated with the given ID, or None if not found.
    """
    async def get(self, id: str) -> Optional[str]:
        return self.singleton_instance.data.get(id, None)