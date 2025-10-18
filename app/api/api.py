from flask import jsonify, Blueprint
from app.KettleList import KettleList
from app.ProducerList import ProducerList
from app.KettleTypeList import KettleTypeList
from app.ColorList import ColorList
from app.MaterialList import MaterialList

api = Blueprint('api', __name__)
    
@api.route('/status')
def get_status():
    return jsonify({"status": "OK"})

@api.route('/getColorsJSON')
def get_colors_json():
    colors = ColorList()
    colors.read_from_csv('app/data/colors.csv')
    return jsonify({"colors": [c.to_dict() for c in colors.get_all()]})

@api.route('/getMaterialsJSON')
def get_materials_json():
    materials = MaterialList()
    materials.read_from_csv('app/data/materials.csv')
    return jsonify({"materials": [m.to_dict() for m in materials.get_all()]})

@api.route('/getProducersJSON')
def get_producers_json():
    producers = ProducerList()
    producers.read_from_csv('app/data/producers.csv')
    return jsonify({"producers": [p.to_dict() for p in producers.get_all()]})

@api.route('/getKettleTypesJSON')
def get_kettle_types_json():
    kettle_types = KettleTypeList()
    kettle_types.read_from_csv('app/data/kettle_types.csv')
    return jsonify({"kettle_types": [kt.to_dict() for kt in kettle_types.get_all()]})

@api.route('/getKettlesJSON')
def get_kettles_json():
    kettles = KettleList()
    kettles.read_from_csv('app/data/kettles.csv')
    return jsonify({"kettles": [k.to_dict() for k in kettles.get_all()]})

@api.route('/getKettlesXML')
def get_kettles_xml():
    kettles = KettleList()
    kettles.read_from_csv('app/data/kettles.csv')
    return kettles.get_as_xml()

@api.route('/getProducersXML')
def get_producers_xml():
    producers = ProducerList()
    producers.read_from_csv('app/data/producers.csv')
    return producers.get_as_xml()

@api.route('/getKettleTypesXML')
def get_kettle_types_xml():
    kettle_types = KettleTypeList()
    kettle_types.read_from_csv('app/data/kettle_types.csv')
    return kettle_types.get_as_xml()

@api.route('/getColorsXML')
def get_colors_xml():
    colors = ColorList()
    colors.read_from_csv('app/data/colors.csv')
    return colors.get_as_xml()

@api.route('/getMaterialsXML')
def get_materials_xml():
    materials = MaterialList()
    materials.read_from_csv('app/data/materials.csv')
    return materials.get_as_xml()