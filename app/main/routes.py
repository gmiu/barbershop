from app.main import bp
from flask import render_template, redirect, url_for
from app.models import Service, Barber
from app.main.forms import SelectService
from datetime import datetime, timedelta, date, time


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', title='Services', services=services)


@bp.route('/about')
def about():
    return render_template('about.html', title='About Us')


@bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    select_service_form = SelectService()
    services = Service.query.order_by(Service.price.desc()).all()
    barbers = Barber.query.filter(Barber.username != 'admin')
    select_service_form.services.choices = [(str(service), str(service)) for service in services]
    select_service_form.barbers.choices = [(str(barber), str(barber)) for barber in barbers]
    today = date.today()
    dates = [today + timedelta(days=i) for i in range(7)]
    select_service_form.date.choices = [(d, d.strftime('%A %Y/%m/%d')) for d in dates]
    if select_service_form.validate_on_submit():
        service = select_service_form.services.data
        barber = select_service_form.barbers.data
        return render_template('schedule.html', title='Schedule An Appointment',
                               select_service_form=select_service_form,
                               service=service, barber=barber)
    return render_template('schedule.html', title='Schedule An Appointment',
                           select_service_form=select_service_form)
