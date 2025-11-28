from .BaseList import BaseList
from .KettleType import KettleType
from database import get_connection
import csv

class KettleTypeList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    kettle_type = KettleType(int(row[0]), row[1])
                    self.add(kettle_type)

    def get_as_xml(self):        
        xml_items = [item.get_as_xml() for item in self._items]
        return "<kettle_types>\n" + "\n".join(xml_items) + "\n</kettle_types>"
    
    def read_from_db(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM kettle_types ORDER BY id")
        rows = cur.fetchall()

        self._items = [KettleType(id=row[0], name=row[1]) for row in rows]

        cur.close()
        conn.close()


    @staticmethod
    def add_to_db(name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO kettle_types (name) VALUES (%s) RETURNING id",
            (name,)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def update_in_db(type_id, name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE kettle_types SET name=%s WHERE id=%s",
            (name, type_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_from_db(type_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM kettle_types WHERE id=%s",
            (type_id,)
        )
        conn.commit()
        cur.close()
        conn.close()