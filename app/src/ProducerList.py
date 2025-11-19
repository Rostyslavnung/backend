from .BaseList import BaseList
from .Producer import Producer
import csv

class ProducerList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    producer = Producer(int(row[0]), row[1])
                    self.add(producer)

    def get_as_xml(self):
        xml_items = [item.get_as_xml() for item in self._items]
        return "<producers>\n" + "\n".join(xml_items) + "\n</producers>"