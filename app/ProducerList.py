from app.BaseList import BaseList
from app.Producer import Producer
import csv

class ProducerList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    producer = Producer(int(row[0]), row[1])
                    self.add(producer)

