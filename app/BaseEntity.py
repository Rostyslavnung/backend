class BaseEntity:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id
    
    def _display(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_as_indexed_array(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_as_xml(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def to_dict(self):
        raise NotImplementedError("Subclasses must implement this method")