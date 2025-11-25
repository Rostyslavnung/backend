from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

colors_bp = Blueprint('colors_bp', __name__)


@colors_bp.route('/colors')
def colors():
    colors = src.ColorList()
    colors.read_from_csv('data/colors.csv')
    return render_template('colors.html',
                           colors=colors.get_all())

@colors_bp.route('/color_save', methods=['GET', 'POST'])
@admin_required
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
    return redirect(url_for('colors_bp.colors'))

@colors_bp.route('/color_delete/<color_id>', methods=['POST'])
@admin_required
def color_delete(color_id):
    colors = src.ColorList()
    colors.read_from_csv('data/colors.csv')
    if colors.delete(int(color_id)):
        flash("Колір видалено!", "success")
    else:
        flash("Колір не знайдено!", "warning")

    colors.write_to_csv('data/colors.csv')
    return redirect(url_for('colors_bp.colors'))