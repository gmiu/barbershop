from app.barber import bp
from app.barber.forms import NewBarberForm, NewServiceForm
from app.models import Barber, Service
from app import db
from flask import render_template, redirect, flash, url_for


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    new_barber_form = NewBarberForm()
    if new_barber_form.validate_on_submit():
        barber = Barber(first_name=new_barber_form.first_name.data,
                        last_name=new_barber_form.last_name.data,
                        username=new_barber_form.username.data)
        barber.set_password(new_barber_form.password.data)
        db.session.add(barber)
        db.session.commit()
        flash('{} {} is now registered as a barber!'.format(new_barber_form.first_name.data,
                                                            new_barber_form.last_name.data))
        return redirect(url_for('barber.index'))

    new_service_form = NewServiceForm()
    if new_service_form.validate_on_submit():
        service = Service(name=new_service_form.name.data,
                          description=new_service_form.description.data,
                          duration=new_service_form.duration.data,
                          price=new_service_form.price.data)
        db.session.add(service)
        db.session.commit()
        flash('{} has been added!'.format(new_service_form.name.data))

    barbers = Barber.query.all()
    services = Service.query.all()


    return render_template('barber/index.html',
                           new_barber_form=new_barber_form,
                           new_service_form=new_service_form,
                           barbers=barbers,
                           services=services)


@bp.route('/delete/barber/<id>', methods=['GET', 'POST'])
def delete_barber(id):
    barber = Barber.query.filter_by(id=id).first()
    db.session.delete(barber)
    db.session.commit()
    return redirect(url_for('barber.index'))


@bp.route('/delete/service/<id>', methods=['GET', 'POST'])
def delete_service(id):
    service = Service.query.filter_by(id=id).first()
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('barber.index'))