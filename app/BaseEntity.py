class BaseEntity:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id
    
    def _display(self):
        raise NotImplementedError("Subclasses must implement this method")