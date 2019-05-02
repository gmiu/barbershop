from app.barber import bp
from app.barber.forms import RegistrationForm
from app.models import Barber
from app import db
from flask import render_template, redirect, flash, url_for


@bp.route('/index')
def index():
    return render_template('barber/index.html')


@bp.route('/register_new_barber', methods=['GET', 'POST'])
def register_new_barber():
    form = RegistrationForm()
    if form.validate_on_submit():
        barber = Barber(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data)
        barber.set_password(form.password.data)
        db.session.add(barber)
        db.session.commit()
        flash('{} {} is now registered as a barber!'.format(form.first_name.data, form.last_name.data))
        return redirect(url_for('barber.index'))
    return render_template('barber/register_new_barber.html', title='Register', form=form)
