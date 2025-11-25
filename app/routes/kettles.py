from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

kettles_bp = Blueprint('kettles_bp', __name__)

@kettles_bp.route('/')
def kettles():
    kettles = src.KettleList()
    kettles.read_from_csv('data/kettles.csv')

    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')

    types_list = src.KettleTypeList()
    types_list.read_from_csv('data/kettleTypes.csv')

    colors_list = src.ColorList()
    colors_list.read_from_csv('data/colors.csv')

    materials_list = src.MaterialList()
    materials_list.read_from_csv('data/materials.csv')

    producer_map = {p.id: p.name for p in producers.get_all()}
    types_map = {t.id: t.name for t in types_list.get_all()}
    colors_map = {c.id: c.name for c in colors_list.get_all()}
    materials_map = {m.id: m.name for m in materials_list.get_all()}

    q = request.args.get('q', '').strip().lower()
    brand = request.args.get('brand', '')
    sort = request.args.get('sort', 'name')

    all_k = []
    for k in kettles.get_all():
        d = k.to_dict()
        d["producer"] = producer_map.get(d["producer_id"], "Невідомий")
        d["type"] = types_map.get(d["kettle_type_id"], "Невідомий")
        d["color"] = colors_map.get(d["color_id"], "Невідомий")
        d["material"] = materials_map.get(d["material_id"], "Невідомий")
        all_k.append(d)

    if q:
        all_k = [k for k in all_k if q in (k.get('name') or '').lower()]
    if brand:
        all_k = [k for k in all_k if k.get('producer') == brand]

    if sort == 'price':
        all_k.sort(key=lambda x: float(x.get('price') or 0))
    else:
        all_k.sort(key=lambda x: (x.get('name') or '').lower())

    brands = [p.name for p in producers.get_all()]
    types = [t.name for t in types_list.get_all()]
    colors = [c.name for c in colors_list.get_all()]
    materials = [m.name for m in materials_list.get_all()]

    return render_template(
        'kettles.html',
        kettles=all_k,
        brands=brands,
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
    price = form.get('price')
    producer = form.get('producer')
    model = form.get('model')
    kettle_type_id = form.get('type')
    color_id = form.get('color')
    material_id = form.get('material')
    capacity = form.get('capacity')
    warranty_months = form.get('warranty_months')
    kettles = src.KettleList()
    kettles.read_from_csv('data/kettles.csv')

    if kettle_id: 
        for k in kettles.items:
            if str(k.id) == str(kettle_id):
                k._name = name
                k._price = price
                k._producer_id = producer
                k._model_code = model
                k._kettle_type_id = kettle_type_id
                k._color_id = color_id
                k._material_id = material_id
                k._capacity = capacity
                k._warranty_months = warranty_months
                break
        else:
            flash("Не знайдено чайник для редагування!", "warning")
    else:
        new_id = str(len(kettles.items) + 1)
        new_kettle = src.Kettle(
            id=new_id,
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
        kettles.add(new_kettle)

    kettles.write_to_csv('data/kettles.csv')
    flash("Зміни збережено!", "success")
    return redirect(url_for('kettles_bp.kettles'))

@kettles_bp.route('/kettle_delete/<kettle_id>', methods=['POST'])
@admin_required
def kettle_delete(kettle_id):
    kettles = src.KettleList()
    kettles.read_from_csv('data/kettles.csv')

    if kettles.delete(int(kettle_id)):
        flash("Чайник видалено!", "success")
    else:
        flash("Чайник не знайдено!", "warning")

    kettles.write_to_csv('data/kettles.csv')
    return redirect(url_for('kettles_bp.kettles'))