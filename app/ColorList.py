from app.BaseList import BaseList
from app.Color import Color
import csv

class ColorList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    color = Color(int(row[0]), row[1])
                    self.add(color)

    def get_as_xml(self):
        xml_items = [item.get_as_xml() for item in self._items]
        return "<colors>\n" + "\n".join(xml_items) + "\n</colors>"