from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
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

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not current_user.check_password(old_password):
            flash("Старий пароль введено невірно", "danger")
        elif new_password != confirm_password:
            flash("Паролі не збігаються", "danger")
        else:
            current_user.set_password(new_password)
            flash("Пароль успішно змінено", "success")
            return redirect(url_for('kettles_bp.kettles'))

    return render_template("change_password.html")