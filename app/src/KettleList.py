from app.src import BaseList, Kettle
import csv

class KettleList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 14:
                    kettle = Kettle(
                        int(row[0]),        # id
                        row[1],             # model
                        row[2],             # name
                        int(row[3]),       # producer_id
                        int(row[4]),       # color_id
                        int(row[5]),       # material_id
                        float(row[6]),     # power
                        float(row[7]),       # capacity
                        float(row[8]),     # price
                        float(row[9]),       # stock_quantity
                        float(row[10]),    # weight
                        float(row[11]),      # height
                        float(row[12]),      # width
                        float(row[13])       # depth
                    )
                    self.add(kettle)

    def get_as_xml(self):
        xml_items = [item.get_as_xml() for item in self._items]
        return "<kettles>\n" + "\n".join(xml_items) + "\n</kettles>"