from app.src.Color import Color
from .BaseList import BaseList
from .Material import Material
from database import get_connection
import csv

class MaterialList(BaseList):
    def read_from_csv(self, filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    material = Material(int(row[0]), row[1])
                    self.add(material)

    def get_as_xml(self):
        xml_items = [item.get_as_xml() for item in self._items]
        return "<materials>\n" + "\n".join(xml_items) + "\n</materials>"
    
    def read_from_db(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM materials ORDER BY id")
        rows = cur.fetchall()

        self._items = [Material(id=row[0], name=row[1]) for row in rows]

        cur.close()
        conn.close()

    @staticmethod
    def add_to_db(name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO materials (name) VALUES (%s) RETURNING id",
            (name,)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

    @staticmethod
    def update_in_db(material_id, name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE materials SET name=%s WHERE id=%s",
            (name, material_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def delete_from_db(material_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM materials WHERE id=%s",
            (material_id,)
        )
        conn.commit()
        cur.close()
        conn.close()