from app.auth_barber import bp
from app.auth_barber.forms import LoginForm
from app.models import Barber
from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('barber.index'))
    form = LoginForm()
    if form.validate_on_submit():
        barber = Barber.query.filter_by(username=form.username.data).first()
        if barber is None or not barber.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth_barber.login'))
        login_user(barber, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page) != '':
            next_page = url_for('barber.index')
        return redirect(next_page)
    return render_template('auth_barber/login.html', title='Barber Log In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

