from app import db
from app.main import bp
from flask import render_template, redirect, url_for, request, flash
from app.models import Service, Barber, Reservation
from app.main.forms import ScheduleForm1, ScheduleForm2, ConfirmForm
from app.main.email import send_confirmation_email
from datetime import datetime, timedelta, date
from utils import create_hour


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
@bp.route('/schedule1', methods=['GET', 'POST'])
def schedule1():
    schedule_form = ScheduleForm1()

    services = Service.query.order_by(Service.price.desc()).all()
    barbers = Barber.query.filter(Barber.username != 'admin')
    end = datetime.strptime('{} 19:00'.format(date.today().strftime('%Y %m %d')), '%Y %m %d %H:%M')
    start = date.today() + timedelta(days=1) if datetime.now() > end else date.today()
    dates = [start + timedelta(days=i) for i in range(7)]

    schedule_form.services.choices = [(str(service), str(service)) for service in services]
    schedule_form.barbers.choices = [(str(barber), str(barber)) for barber in barbers]
    schedule_form.reservation_date.choices = [(d.strftime('%A %Y/%m/%d'), d.strftime('%A %Y/%m/%d')) for d in dates]

    if schedule_form.validate_on_submit():
        service = schedule_form.services.data
        barber_name = schedule_form.barbers.data
        reservation_date = schedule_form.reservation_date.data
        return redirect(url_for('main.schedule2', service=service, barber_name=barber_name,
                                reservation_date=reservation_date))
    return render_template('schedule1.html', title='Schedule An Appointment',
                           schedule_form=schedule_form)


@bp.route('/schedule2', methods=['GET', 'POST'])
def schedule2():
    service_full = request.args.get('service')
    service_name = service_full.split(' - ')[0]
    service = Service.query.filter_by(name=service_name).first()
    barber_name = request.args.get('barber_name').split(' ')
    barber = Barber.query.filter_by(first_name=barber_name[0]).filter_by(last_name=barber_name[1]).first()
    reservation_date = datetime.strptime(request.args.get('reservation_date'), '%A %Y/%m/%d').date()

    schedule_form = ScheduleForm2()
    hours = barber.get_hours(reservation_date, service.duration)
    schedule_form.hours.choices = [(h.strftime('%H:%M'), h.strftime('%H:%M')) for h in hours]

    if schedule_form.validate_on_submit():
        reservation_hour_str = schedule_form.hours.data
        first_name = schedule_form.first_name.data
        last_name = schedule_form.last_name.data
        phone = schedule_form.phone.data
        email = schedule_form.email.data

        reservation_hour = create_hour(reservation_hour_str, date=reservation_date)

        reservation = Reservation(reservation_date=reservation_date,
                                  reservation_time=reservation_hour,
                                  client_first_name=first_name,
                                  client_last_name=last_name,
                                  client_email=email,
                                  client_phone=phone,
                                  barber_id=barber.id,
                                  service_id=service.id)

        db.session.add(reservation)
        db.session.commit()

        return redirect(url_for('main.confirm', id=reservation.id))

    return render_template('schedule2.html', title='Schedule An Appointment',
                           schedule_form=schedule_form,
                           service=service, barber=barber, reservation_date=reservation_date)


@bp.route('/confirm/<id>', methods=['GET', 'POST'])
def confirm(id):
    reservation = Reservation.query.get(id)
    service = Service.query.get(reservation.service_id)
    barber = Barber.query.get(reservation.barber_id)

    confirm_form = ConfirmForm()
    if confirm_form.validate_on_submit():
        reservation.confirmed_status = True
        send_confirmation_email(reservation=reservation, barber=barber, service=service)
        db.session.commit()
        flash('Your reservation has been confirmed! An email with the confirmation has been sent to {}.'.format(reservation.client_email))
        return redirect(url_for('main.index'))

    return render_template('confirm_reservation.html', title='Confirm Reservation',
                           service=service, barber=barber, reservation=reservation, confirm_form=confirm_form)
