from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
import src as src

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    form = src.LoginForm()
    if form.validate_on_submit():
        user = src.User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вхід успішний!', 'success')
            return redirect(url_for('kettles_bp.kettles'))
        else:
            flash('Невірне ім’я користувача або пароль', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви успішно вийшли з акаунта!', 'info')
    return redirect(url_for('kettles_bp.kettles'))