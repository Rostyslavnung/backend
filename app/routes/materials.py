from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

materials_bp = Blueprint('materials_bp', __name__)

@materials_bp.route('/materials')
def materials():
    materials = src.MaterialList()
    materials.read_from_db()
    return render_template('materials.html',
                           materials=materials.get_all())

@materials_bp.route('/material_save', methods=['GET', 'POST'])
@admin_required
def material_save():
    form = request.form
    material_id = form.get('id')
    name = form.get('name')
    
    if material_id: 
        src.MaterialList.update_in_db(material_id, name)
    else:
        src.MaterialList.add_to_db(name)

    return redirect(url_for('materials_bp.materials'))

@materials_bp.route('/material_delete/<material_id>', methods=['POST'])
@admin_required
def material_delete(material_id):
    src.MaterialList.delete_from_db(material_id)
    return redirect(url_for('materials_bp.materials'))