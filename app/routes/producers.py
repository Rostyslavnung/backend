from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

producers_bp = Blueprint('producers_bp', __name__)

@producers_bp.route('/producers')
def producers():
    producers = src.ProducerList()
    producers.read_from_db()
    return render_template('producers.html',
                           producers=producers.get_all())

@producers_bp.route('/producer_save', methods=['GET', 'POST'])
@admin_required
def producer_save():
    form = request.form
    producer_id = form.get('id')
    name = form.get('name')
    
    if producer_id: 
        src.ProducerList.update_in_db(producer_id, name)
    else:
        src.ProducerList.add_to_db(name)

    return redirect(url_for('producers_bp.producers'))

@producers_bp.route('/producer_delete/<producer_id>', methods=['POST'])
@admin_required
def producer_delete(producer_id):
    src.ProducerList.delete_from_db(producer_id)
    return redirect(url_for('producers_bp.producers'))