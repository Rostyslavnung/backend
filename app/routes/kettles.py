from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from app.decorators import admin_required
import src as src

kettles_bp = Blueprint('kettles_bp', __name__)

@kettles_bp.route('/')
def kettles():
    kettles = src.KettleList()

    q = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'name')

    kettles.read_from_db(q=q if q else None, sort=sort)

    producers = src.ProducerList()
    producers.read_from_db()

    types_list = src.KettleTypeList()
    types_list.read_from_db()

    colors_list = src.ColorList()
    colors_list.read_from_db()

    materials_list = src.MaterialList()
    materials_list.read_from_db()

    producer_map = {p.id: p.name for p in producers.get_all()}
    types_map = {t.id: t.name for t in types_list.get_all()}
    colors_map = {c.id: c.name for c in colors_list.get_all()}
    materials_map = {m.id: m.name for m in materials_list.get_all()}

    all_k = []
    for k in kettles.get_all():
        d = k.to_dict()
        d["producer_name"] = producer_map.get(d["producer_id"], "Невідомий")
        d["type_name"] = types_map.get(d["kettle_type_id"], "Невідомий")
        d["color_name"] = colors_map.get(d["color_id"], "Невідомий")
        d["material_name"] = materials_map.get(d["material_id"], "Невідомий")
        all_k.append(d)

    producers = producers.get_all()
    types = types_list.get_all()
    colors = colors_list.get_all()
    materials = materials_list.get_all()

    return render_template(
        'kettles.html',
        kettles=all_k,
        producers=producers,
        types=types,
        colors=colors,
        materials=materials,
        q=q,
        sort=sort
    )

@kettles_bp.route('/kettle_save', methods=['GET', 'POST'])
@admin_required
def kettle_save():
    form = request.form
    kettle_id = form.get('id')
    name = form.get('name')
    price = form.get('price') or None
    producer = form.get('producer')
    model = form.get('model')
    kettle_type_id = form.get('type')
    color_id = form.get('color')
    material_id = form.get('material')
    capacity = form.get('capacity') or None
    warranty_months = form.get('warranty_months') or None
    kettle = src.Kettle(
        id=int(kettle_id) if kettle_id else None,
        name=name,
        price=price,
        producer_id=producer,
        model_code=model,
        kettle_type_id=kettle_type_id,
        color_id=color_id,
        material_id=material_id,
        capacity=capacity,
        warranty_months=warranty_months,
    )

    if kettle_id: 
        try:
            src.KettleList.update_in_db(kettle)
            flash("Чайник успішно оновлено.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при оновленні чайника, чайник із такою назвою уже існує", "danger")
    else:
        try:
            src.KettleList.add_to_db(kettle)
            flash("Чайник успішно додано.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при додаванні чайника, чайник із такою назвою уже існує", "danger")

    return redirect(url_for('kettles_bp.kettles'))

@kettles_bp.route('/kettle_delete/<kettle_id>', methods=['POST'])
@admin_required
def kettle_delete(kettle_id):
    src.KettleList.delete_from_db(int(kettle_id))
    return redirect(url_for('kettles_bp.kettles'))