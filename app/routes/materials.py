from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
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
        try: 
            src.MaterialList.update_in_db(material_id, name)
            flash("Матеріал успішно оновлено.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при оновленні матеріалу, матеріал із такою назвою уже існує", "danger")
    else:
        try:
            src.MaterialList.add_to_db(name)
            flash("Матеріал успішно додано.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при додаванні матеріалу, матеріал із такою назвою уже існує", "danger")

    return redirect(url_for('materials_bp.materials'))

@materials_bp.route('/material_delete/<material_id>', methods=['POST'])
@admin_required
def material_delete(material_id):
    try:
        src.MaterialList.delete_from_db(material_id)
    except psycopg2.errors.ForeignKeyViolation:
        flash("Неможливо видалити матеріал, бо існують чайники, що на нього посилаються.", "danger")

    return redirect(url_for('materials_bp.materials'))