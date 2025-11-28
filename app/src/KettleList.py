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

    def read_from_db(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM kettles ORDER BY id")
        rows = cur.fetchall()

        self._items = [Kettle(id=row[0], model_code=row[1], name=row[2], producer_id=row[3], kettle_type_id=row[4], material_id=row[5], color_id=row[6], capacity=row[7], warranty_months=row[8], price=row[9]) for row in rows]

        cur.close()
        conn.close()

    @staticmethod
    def add_to_db(kettle):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO kettles (model_code, name, producer_id, kettle_type_id, material_id, color_id, capacity, warranty_months, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (kettle.model_code, kettle.name, kettle.producer_id, kettle.kettle_type_id, kettle.material_id, kettle.color_id, kettle.capacity, kettle.warranty_months, kettle.price)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def update_in_db(kettle):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE kettles SET model_code=%s, name=%s, producer_id=%s, kettle_type_id=%s, material_id=%s, color_id=%s, capacity=%s, warranty_months=%s, price=%s WHERE id=%s",
            (kettle.model_code, kettle.name, kettle.producer_id, kettle.kettle_type_id, kettle.material_id, kettle.color_id, kettle.capacity, kettle.warranty_months, kettle.price, kettle.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_from_db(kettle_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM kettles WHERE id=%s",
            (kettle_id,)
        )
        conn.commit()
        cur.close()
        conn.close()