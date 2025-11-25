from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import admin_required
import src as src

producers_bp = Blueprint('producers_bp', __name__)

@producers_bp.route('/producers')
def producers():
    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')
    return render_template('producers.html',
                           producers=producers.get_all())

@producers_bp.route('/producer_save', methods=['GET', 'POST'])
@admin_required
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
    return redirect(url_for('producers_bp.producers'))

@producers_bp.route('/producer_delete/<producer_id>', methods=['POST'])
@admin_required
def producer_delete(producer_id):
    producers = src.ProducerList()
    producers.read_from_csv('data/producers.csv')

    if producers.delete(int(producer_id)):
        flash("Виробник видалено!", "success")
    else:
        flash("Виробник не знайдено!", "warning")

    producers.write_to_csv('data/producers.csv')
    return redirect(url_for('producers_bp.producers'))