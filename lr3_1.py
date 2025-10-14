from flask import Flask, jsonify

app = Flask(__name__)

class BaseEntity:
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id
    
    def _display(self):
        raise NotImplementedError("Subclasses must implement this method")

class BaseList:
    def __init__(self):
        self._items = []

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

class KettleList(BaseList):
    pass

class ProducerList(BaseList):
    pass

class ColorList(BaseList):
    pass

class MaterialList(BaseList):
    pass

class KettleTypeList(BaseList):
    pass

class Kettle(BaseEntity):
    def __init__(self, id, model_code, name, 
                 producer_id, kettle_type_id, material_id, color_id, 
                 capacity, warranty_months, price, height, weight, length, width):
        super().__init__(id)
        self._model_code = model_code
        self._name = name
        self._producer_id = producer_id
        self._kettle_type_id = kettle_type_id
        self._material_id = material_id
        self._color_id = color_id
        self._capacity = capacity
        self._warranty_months = warranty_months
        self._price = price
        self._height = height
        self._weight = weight
        self._length = length
        self._width = width

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name can't be empty")
        self._name = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price can't be negative")
        self._price = value

    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, value):
        if value <= 0:
            raise ValueError("Capacity must be more than 0")
        self._capacity = value

    def __str__(self):
        return (f"Kettle ID: {self.id}, Model Code: {self._model_code}, Name: {self._name}, "
                f"Producer ID: {self._producer_id}, Kettle Type ID: {self._kettle_type_id}, "
                f"Material ID: {self._material_id}, Color ID: {self._color_id}, Capacity: {self._capacity}L, "
                f"Warranty: {self._warranty_months} months, Price: ${self._price}, "
                f"Dimensions (HxWxL): {self._height}x{self._width}x{self._length} cm, Weight: {self._weight} kg")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

class KettleType(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"KettleType ID: {self.id}, Name: {self.__name}"
    
    def update(self, name=None):
        if name is not None:
            self.__name = name

class Material(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"Material ID: {self.id}, Name: {self.__name}"
    
    def update(self, name=None):
        if name is not None:
            self.__name = name

class Color(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"Color ID: {self.id}, Name: {self.__name}"
    
    def update(self, name=None):
        if name is not None:
            self.__name = name

class Producer(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"Producer ID: {self.id}, Name: {self.__name}"
    
    def update(self, name=None):
        if name is not None:
            self.__name = name

kettle = Kettle(1, "X123", "SuperKettle", 101, 5, 3, 2, 1.5, 24, 49.99, 25, 1.2, 20, 15)

kettles = KettleList()
producers = ProducerList()

kettles.add(Kettle(1, "X123", "SuperKettle", 101, 5, 3, 2, 1.5, 24, 49.99, 25, 1.2, 20, 15))
kettles.add(Kettle(2, "A456", "QuickBoil", 102, 6, 4, 1, 2.0, 12, 39.99, 23, 1.1, 19, 14))

producers.add(Producer(101, "Philips"))
producers.add(Producer(102, "Bosch"))

@app.route('/kettles')
def get_all_kettles():
    return jsonify([str(k) for k in kettles.get_all()])

@app.route('/producers')
def get_all_producers():
    return jsonify([str(p) for p in producers.get_all()])
