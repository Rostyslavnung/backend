from flask import Blueprint, flash, render_template, request, redirect, url_for
from app.decorators import admin_required
import src as src

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users')
@admin_required
def users():
    users = src.UserList()
    users.read_from_db()
    return render_template('users.html',
                           users=users.get_all())

@users_bp.route('/user_save', methods=['GET', 'POST'])
@admin_required
def user_save():
    form = request.form
    user_id = form.get('id')
    username = form.get('username')
    is_admin = True if form.get('is_admin') == 'on' else False
    
    if user_id: 
        src.UserList.update_in_db(user_id, username, is_admin)
        flash("Користувача успішно оновлено.", "success")
    else:
        flash("Не знайдено користувача.", "danger")
    return redirect(url_for('users_bp.users'))

@users_bp.route('/user_delete/<user_id>', methods=['POST'])
@admin_required
def user_delete(user_id):
    src.UserList.delete_from_db(user_id)
    return redirect(url_for('users_bp.users'))