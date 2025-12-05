from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
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
        try:
            src.KettleTypeList.update_in_db(type_id, name)
            flash("Тип чайника успішно оновлено.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при оновленні типу чайника, тип чайника із такою назвою уже існує", "danger")
    else:
        try:
            src.KettleTypeList.add_to_db(name)
            flash("Тип чайника успішно додано.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при додаванні типу чайника, тип чайника із такою назвою уже існує", "danger")

    return redirect(url_for('types_bp.types'))

@types_bp.route('/type_delete/<type_id>', methods=['POST'])
@admin_required
def type_delete(type_id):
    try:
        src.KettleTypeList.delete_from_db(type_id)
    except psycopg2.errors.ForeignKeyViolation:
        flash("Неможливо видалити тип чайника, бо існують чайники, що на нього посилаються.", "danger")

    return redirect(url_for('types_bp.types'))