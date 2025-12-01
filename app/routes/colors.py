from flask import Blueprint, flash, render_template, request, redirect, url_for
import psycopg2
from app.decorators import admin_required
import src as src

colors_bp = Blueprint('colors_bp', __name__)


@colors_bp.route('/colors')
def colors():
    colors = src.ColorList()
    colors.read_from_db()
    return render_template('colors.html',
                           colors=colors.get_all())

@colors_bp.route('/color_save', methods=['GET', 'POST'])
@admin_required
def color_save():
    form = request.form
    color_id = form.get('id')
    name = form.get('name')
    
    if color_id: 
        try:
            src.ColorList.update_in_db(color_id, name)
            flash("Колір успішно оновлено.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при оновленні кольору, колір із такою назвою уже існує", "danger")
    else:
        try:
            src.ColorList.add_to_db(name)
            flash("Колір успішно додано.", "success")
        except psycopg2.errors.UniqueViolation:
            flash(f"Помилка при додаванні кольору, колір із такою назвою уже існує", "danger")

    return redirect(url_for('colors_bp.colors'))

@colors_bp.route('/color_delete/<color_id>', methods=['POST'])
@admin_required
def color_delete(color_id):
    try:
        src.ColorList.delete_from_db(color_id)
    except psycopg2.errors.ForeignKeyViolation:
        flash("Неможливо видалити колір, бо існують чайники, що на нього посилаються.", "danger")

    return redirect(url_for('colors_bp.colors'))