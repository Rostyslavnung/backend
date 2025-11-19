from .BaseEntity import BaseEntity

class Kettle(BaseEntity):
    def __init__(self, id, model_code, name, 
                 producer_id, kettle_type_id, material_id, color_id, 
                 capacity, warranty_months, price):
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
                f"Warranty: {self._warranty_months} months, Price: ${self._price}")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def get_as_indexed_array(self):
        return [
            self.id,
            self._model_code,
            self._name,
            self._producer_id,
            self._kettle_type_id,
            self._material_id,
            self._color_id,
            self._capacity,
            self._warranty_months,
            self._price,
        ]
    
    def get_as_xml(self):
        return (f"<kettle>"
                f"<id>{self.id}</id>"
                f"<model_code>{self._model_code}</model_code>"
                f"<name>{self._name}</name>"
                f"<producer_id>{self._producer_id}</producer_id>"
                f"<kettle_type_id>{self._kettle_type_id}</kettle_type_id>"
                f"<material_id>{self._material_id}</material_id>"
                f"<color_id>{self._color_id}</color_id>"
                f"<capacity>{self._capacity}</capacity>"
                f"<warranty_months>{self._warranty_months}</warranty_months>"
                f"<price>{self._price}</price>"
                f"</kettle>")
    
    def to_dict(self):
        return {
            "id": self.id,
            "model_code": self._model_code,
            "name": self._name,
            "producer_id": self._producer_id,
            "kettle_type_id": self._kettle_type_id,
            "material_id": self._material_id,
            "color_id": self._color_id,
            "capacity": self._capacity,
            "warranty_months": self._warranty_months,
            "price": self._price,
        }