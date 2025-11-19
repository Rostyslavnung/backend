import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user

from api.api import api
import src as src

load_dotenv()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(api, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return src.User.get(user_id)

@app.route('/ssr/kettles')
def kettles_ssr():
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
        'ssr_kettles.html',
        kettles=all_k,
        brands=brands,
        types=types,
        colors=colors,
        materials=materials,
        q=q,
        sort=sort
    )

@app.route('/ssr/kettle_save', methods=['GET', 'POST'])
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
    return redirect(url_for('kettles_ssr'))

@app.route('/ssr/kettle_delete/<kettle_id>', methods=['POST'])
def kettle_delete(kettle_id):
    kettles = src.KettleList()
    kettles.read_from_csv('data/kettles.csv')

    if kettles.delete(int(kettle_id)):
        flash("Чайник видалено!", "success")
    else:
        flash("Чайник не знайдено!", "warning")

    kettles.write_to_csv('data/kettles.csv')
    return redirect(url_for('kettles_ssr'))

@app.route('/ssr/kettle_types')
def types_ssr():
    kettle_types = src.KettleTypeList()
    kettle_types.read_from_csv('data/kettleTypes.csv')
    return render_template('ssr_kettle_types.html',
                           kettle_types=kettle_types.get_all())

@app.route('/ssr/kettle_type_save', methods=['GET', 'POST'])
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
    return redirect(url_for('types_ssr'))

@app.route('/ssr/type_delete/<type_id>', methods=['POST'])
def type_delete(type_id):
    types = src.KettleTypeList()
    types.read_from_csv('data/kettleTypes.csv')

    if types.delete(int(type_id)):
        flash("Тип видалено!", "success")
    else:
        flash("Тип не знайдено!", "warning")

    types.write_to_csv('data/kettleTypes.csv')
    return redirect(url_for('types_ssr'))

@app.route('/ssr/colors')
def colors_ssr():
    colors = src.ColorList()
    colors.read_from_csv('data/colors.csv')
    return render_template('ssr_colors.html',
                           colors=colors.get_all())

@app.route('/ssr/color_save', methods=['GET', 'POST'])
def color_save():
    form = request.form
    color_id = form.get('id')
    name = form.get('name')
    colors = src.ColorList()
    colors.read_from_csv('data/colors.csv')
    
    if color_id: 
        for c in colors.items:
            if str(c.id) == str(color_id):
                c.update(name=name)
                break
        else:
            flash("Не знайдено колір для редагування!", "warning")
    else:
        new_id = str(len(colors.items) + 1)
        new_color = src.Color(
            id=new_id,
            name=name
        )
        colors.add(new_color)

    colors.write_to_csv('data/colors.csv')
    flash("Зміни збережено!", "success")
    return redirect(url_for('colors_ssr'))

@app.route('/ssr/color_delete/<color_id>', methods=['POST'])
def color_delete(color_id):
    colors = src.ColorList()
    colors.read_from_csv('data/colors.csv')
    if colors.delete(int(color_id)):
        flash("Колір видалено!", "success")
    else:
        flash("Колір не знайдено!", "warning")

    colors.write_to_csv('data/colors.csv')
    return redirect(url_for('colors_ssr'))

@app.route('/ssr/materials')
def materials_ssr():
    materials = src.MaterialList()
    materials.read_from_csv('data/materials.csv')
    return render_template('ssr_materials.html',
                           materials=materials.get_all())

@app.route('/ssr/material_save', methods=['GET', 'POST'])
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
    return redirect(url_for('materials_ssr'))

@app.route('/ssr/material_delete/<material_id>', methods=['POST'])
def material_delete(material_id):
    materials = src.MaterialList()
    materials.read_from_csv('data/materials.csv')
    if materials.delete(int(material_id)):
        flash("Матеріал видалено!", "success")
    else:
        flash("Матеріал не знайдено!", "warning")

    materials.write_to_csv('data/materials.csv')
    return redirect(url_for('materials_ssr'))

@app.route('/ssr/producers')
def producers_ssr():
    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')
    return render_template('ssr_producers.html',
                           producers=producers.get_all())

@app.route('/ssr/producer_save', methods=['GET', 'POST'])
def producer_save():
    form = request.form
    producer_id = form.get('id')
    name = form.get('name')
    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')
    
    if producer_id: 
        for p in producers.items:
            if str(p.id) == str(producer_id):
                p.update(name=name)
                break
        else:
            flash("Не знайдено виробник для редагування!", "warning")
    else:
        new_id = str(len(producers.items) + 1)
        new_producer = src.Producer(
            id=new_id,
            name=name,

        )
        producers.add(new_producer)

    producers.write_to_csv('data/producers.csv')
    flash("Зміни збережено!", "success")
    return redirect(url_for('producers_ssr'))

@app.route('/ssr/producer_delete/<producer_id>', methods=['POST'])
def producer_delete(producer_id):
    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')

    if producers.delete(int(producer_id)):
        flash("Виробник видалено!", "success")
    else:
        flash("Виробник не знайдено!", "warning")

    producers.write_to_csv('data/producers.csv')
    return redirect(url_for('producers_ssr'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = src.LoginForm()
    if form.validate_on_submit():
        user = src.User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вхід успішний!', 'success')
            next_page = request.args.get('next')
            if not next_page:
                return abort(404)
            return redirect(next_page or url_for('index'))
        else:
            flash('Невірне ім’я користувача або пароль', 'danger')
    return render_template('login.html', form=form)