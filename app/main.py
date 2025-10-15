from flask import Flask, jsonify

from app.KettleList import KettleList
from app.ProducerList import ProducerList
from app.KettleTypeList import KettleTypeList
from app.ColorList import ColorList
from app.MaterialList import MaterialList

app = Flask(__name__)

kettles = KettleList()
producers = ProducerList()
kettle_types = KettleTypeList()
colors = ColorList()
materials = MaterialList()

kettles.read_from_csv('app/data/kettles.csv')

producers.read_from_csv('app/data/producers.csv')

kettle_types.read_from_csv('app/data/kettleTypes.csv')

colors.read_from_csv('app/data/colors.csv')

materials.read_from_csv('app/data/materials.csv')

@app.route('/kettles')
def get_all_kettles():
    return jsonify([str(k) for k in kettles.get_all()])

@app.route('/producers')
def get_all_producers():
    return jsonify([str(p) for p in producers.get_all()])

@app.route('/kettle_types')
def get_all_kettle_types():
    return jsonify([str(kt) for kt in kettle_types.get_all()])

@app.route('/colors')
def get_all_colors():
    return jsonify([str(c) for c in colors.get_all()])

@app.route('/materials')
def get_all_materials():
    return jsonify([str(m) for m in materials.get_all()])