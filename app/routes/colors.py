from flask import Blueprint, render_template, request, redirect, url_for
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
        src.ColorList.update_in_db(color_id, name)
    else:
        src.ColorList.add_to_db(name)

    return redirect(url_for('colors_bp.colors'))

@colors_bp.route('/color_delete/<color_id>', methods=['POST'])
@admin_required
def color_delete(color_id):
    src.ColorList.delete_from_db(color_id)
    return redirect(url_for('colors_bp.colors'))