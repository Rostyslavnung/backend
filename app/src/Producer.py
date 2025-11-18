from app.src import BaseEntity

class Producer(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"Producer ID: {self.id}, Name: {self.__name}"
    
    @property
    def name(self):
        return self.__name

    def update(self, name=None):
        if name is not None:
            self.__name = name

    def get_as_indexed_array(self):
        return [self.id, self.__name]
    
    def get_as_xml(self):
        return f"<producer><id>{self.id}</id><name>{self.__name}</name></producer>"
    
    def to_dict(self):
        return {"id": self.id, "name": self.__name}