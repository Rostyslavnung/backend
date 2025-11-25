from .BaseList import BaseList
from .Kettle import Kettle
import csv
from database import get_connection

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

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM kettles
        """)

        rows = cur.fetchall()
        conn.close()

        return [Kettle(*row) for row in rows]

    def add(self, kettle):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO kettles (name, price, model_code, capacity, warranty_months,
                                 producer_id, kettle_type_id, color_id, material_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            kettle.name,
            kettle.price,
            kettle.model_code,
            kettle.capacity,
            kettle.warranty_months,
            kettle.producer_id,
            kettle.kettle_type_id,
            kettle.color_id,
            kettle.material_id
        ))

        conn.commit()
        conn.close()