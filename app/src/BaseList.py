from .BaseEntity import BaseEntity

class BaseList:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add(self, item):
        if not isinstance(item, BaseEntity):
            raise TypeError("Item must be a subclass of BaseEntity")
        self._items.append(item)

    def get_by_id(self, id):
        for item in self._items:
            if item.id == id:
                return item
        return None

    def update(self, id, **kwargs):
        item = self.get_by_id(id)
        if item:
            item.update(**kwargs)
            return True
        return False

    def delete(self, id):
        item = self.get_by_id(id)
        if item:
            self._items.remove(item)
            return True
        return False

    def get_all(self):
        return self._items

    def __str__(self):
        return "\n".join(str(item) for item in self._items)
    
    def read_from_csv(self, file_path):
        raise NotImplementedError("Subclasses must implement this method")

    def write_to_csv(self, file_path):
        import csv
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in self._items:
                writer.writerow(item.get_as_indexed_array())

    def get_as_xml(self):
        raise NotImplementedError("Subclasses must implement this method")