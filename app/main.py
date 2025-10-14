from flask import Flask, jsonify

from app.Producer import Producer
from app.KettleList import KettleList
from app.ProducerList import ProducerList
from app.kettle import Kettle

app = Flask(__name__)

kettle = Kettle(1, "X123", "SuperKettle", 101, 5, 3, 2, 1.5, 24, 49.99, 25, 1.2, 20, 15)

kettles = KettleList()
producers = ProducerList()

kettles.add(Kettle(1, "X123", "SuperKettle", 101, 5, 3, 2, 1.5, 24, 49.99, 25, 1.2, 20, 15))
kettles.add(Kettle(2, "A456", "QuickBoil", 102, 6, 4, 1, 2.0, 12, 39.99, 23, 1.1, 19, 14))

producers.add(Producer(101, "Philips"))
producers.add(Producer(102, "Bosch"))

@app.route('/kettles')
def get_all_kettles():
    return jsonify([str(k) for k in kettles.get_all()])

@app.route('/producers')
def get_all_producers():
    return jsonify([str(p) for p in producers.get_all()])