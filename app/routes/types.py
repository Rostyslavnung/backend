from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

types_bp = Blueprint('types_bp', __name__)

@types_bp.route('/kettle_types')
def types():
    kettle_types = src.KettleTypeList()
    kettle_types.read_from_db()
    return render_template('kettle_types.html',
                           kettle_types=kettle_types.get_all())

@types_bp.route('/kettle_type_save', methods=['GET', 'POST'])
@admin_required
def type_save():
    form = request.form
    type_id = form.get('id')
    name = form.get('name')
    
    if type_id: 
        src.KettleTypeList.update_in_db(type_id, name)
    else:
        src.KettleTypeList.add_to_db(name)

    return redirect(url_for('types_bp.types'))

@types_bp.route('/type_delete/<type_id>', methods=['POST'])
@admin_required
def type_delete(type_id):
    src.KettleTypeList.delete_from_db(type_id)
    return redirect(url_for('types_bp.types'))