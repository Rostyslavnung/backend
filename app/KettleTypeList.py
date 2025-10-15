from app.BaseList import BaseList
from app.KettleType import KettleType
import csv

class KettleTypeList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    kettle_type = KettleType(int(row[0]), row[1])
                    self.add(kettle_type)