from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

types_bp = Blueprint('types_bp', __name__)

@types_bp.route('/kettle_types')
def types():
    kettle_types = src.KettleTypeList()
    kettle_types.read_from_csv('data/kettleTypes.csv')
    return render_template('kettle_types.html',
                           kettle_types=kettle_types.get_all())

@types_bp.route('/kettle_type_save', methods=['GET', 'POST'])
@admin_required
def type_save():
    form = request.form
    type_id = form.get('id')
    name = form.get('name')
    types = src.KettleTypeList()
    types.read_from_csv('data/kettleTypes.csv')
    
    if type_id: 
        for t in types.items:
            if str(t.id) == str(type_id):
                t.update(name=name)
                break
        else:
            flash("Не знайдено тип для редагування!", "warning")
    else:
        new_id = str(len(types.items) + 1)
        new_type = src.KettleType(
            id=new_id,
            name=name,

        )
        types.add(new_type)

    types.write_to_csv('data/kettleTypes.csv')
    flash("Зміни збережено!", "success")
    return redirect(url_for('types_bp.types'))

@types_bp.route('/type_delete/<type_id>', methods=['POST'])
@admin_required
def type_delete(type_id):
    types = src.KettleTypeList()
    types.read_from_csv('data/kettleTypes.csv')

    if types.delete(int(type_id)):
        flash("Тип видалено!", "success")
    else:
        flash("Тип не знайдено!", "warning")

    types.write_to_csv('data/kettleTypes.csv')
    return redirect(url_for('types_bp.types'))