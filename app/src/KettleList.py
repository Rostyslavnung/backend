from app.src import BaseList, Kettle
import csv

class KettleList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 10:
                    kettle = Kettle(
                        int(row[0]),      # id
                        row[1],           # model_code
                        row[2],           # name
                        int(row[3]),      # producer_id
                        int(row[4]),      # kettle_type_id
                        int(row[5]),      # material_id
                        int(row[6]),      # color_id
                        float(row[7]),    # capacity
                        float(row[8]),    # warranty_months
                        float(row[9]),    # price
                    )
                    self.add(kettle)

    def get_as_xml(self):
        xml_items = [item.get_as_xml() for item in self._items]
        return "<kettles>\n" + "\n".join(xml_items) + "\n</kettles>"