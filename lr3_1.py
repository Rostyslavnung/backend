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

class ElectricSpec(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"StoveType ID: {self.id}, Name: {self.__name}"
    
    def update(self, name=None):
        if name is not None:
            self.__name = name

class StoveSpec(BaseEntity):
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name

    def __str__(self):
        return f"StoveType ID: {self.id}, Name: {self.__name}"
    
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


@app.route('/')
def display_kettle():
    return str(kettle)

@app.route('/kettle')
def dkettle():
    kettle.update(price=44.99, color_id=4)
    return str(kettle)