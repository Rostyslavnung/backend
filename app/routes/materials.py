from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

materials_bp = Blueprint('materials_bp', __name__)

@materials_bp.route('/materials')
def materials():
    materials = src.MaterialList()
    materials.read_from_csv('data/materials.csv')
    return render_template('materials.html',
                           materials=materials.get_all())

@materials_bp.route('/material_save', methods=['GET', 'POST'])
@admin_required
def material_save():
    form = request.form
    material_id = form.get('id')
    name = form.get('name')
    materials = src.MaterialList()
    materials.read_from_csv('data/materials.csv')
    
    if material_id: 
        for m in materials.items:
            if str(m.id) == str(material_id):
                m.update(name=name)
                break
        else:
            flash("Не знайдено матеріал для редагування!", "warning")
    else:
        new_id = str(len(materials.items) + 1)
        new_material = src.Material(
            id=new_id,
            name=name,

        )
        materials.add(new_material)

    materials.write_to_csv('data/materials.csv')
    flash("Зміни збережено!", "success")
    return redirect(url_for('materials_bp.materials'))

@materials_bp.route('/material_delete/<material_id>', methods=['POST'])
@admin_required
def material_delete(material_id):
    materials = src.MaterialList()
    materials.read_from_csv('data/materials.csv')
    if materials.delete(int(material_id)):
        flash("Матеріал видалено!", "success")
    else:
        flash("Матеріал не знайдено!", "warning")

    materials.write_to_csv('data/materials.csv')
    return redirect(url_for('materials_bp.materials'))