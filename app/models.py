from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from utils import hour_generator, create_hour


class Barber(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(7), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship('Reservation', backref='barber', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Barber {}>'.format(self.username)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_reservations_for_date(self, date):
        return self.reservations.filter(
            db.func.date(Reservation.reservation_date) == date).order_by(Reservation.reservation_time.asc())

    def calculate_busy_hours(self, date):
        def busy_hour_for_reservation(reservation):
            return hour_generator(reservation.reservation_time,
                                  reservation.reservation_time + timedelta(minutes=reservation.get_duration()))
        busy_hours = []
        for reservation in self.get_reservations_for_date(date):
            if reservation.confirmed_status:
                hour_gen = busy_hour_for_reservation(reservation)
                for h in hour_gen:
                    busy_hours.append(h)

        return busy_hours

    def get_hours(self, date, duration, start_str='10:00', end_str='20:00', not_before=15):
        start = create_hour(start_str, date)
        end = create_hour(end_str, date)

        hour = hour_generator(start, end)
        busy_hours = self.calculate_busy_hours(date)

        all_hours = [h for h in hour if h not in busy_hours]
        if date == datetime.today().date():
            past_hours = hour_generator(start, datetime.now() + timedelta(minutes=not_before))
            all_hours = [h for h in all_hours if h not in past_hours]

        intervals = int(duration / 10)
        free_hours = []

        for i in range(len(all_hours)):
            if all_hours[i] > (end - timedelta(minutes=duration)):
                break
            if i + intervals > len(all_hours):
                break
            works = True
            for j in range(intervals):
                if all_hours[i + j] != all_hours[i] + timedelta(minutes=10 * j):
                    works = False
                    break
            if works:
                free_hours.append(all_hours[i])

        return free_hours


@login.user_loader
def load_user(id):
    return Barber.query.get(int(id))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(300))
    duration = db.Column(db.Integer)
    price = db.Column(db.Integer)
    reservations = db.relationship('Reservation', backref='service', lazy='dynamic')

    def __repr__(self):
        return '{} - {} Minutes - {} RON'.format(self.name, str(self.duration), str(self.price))

    def __str__(self):
        return '{} - {} Minutes - {} RON'.format(self.name, str(self.duration), str(self.price))



class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_time = db.Column(db.DateTime, index=True)
    reservation_date = db.Column(db.Date, index=True)
    client_first_name = db.Column(db.String(20))
    client_last_name = db.Column(db.String(20))
    client_phone = db.Column(db.String(10), index=True)
    client_email = db.Column(db.String(50), index=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed_status = db.Column(db.Boolean, index=True, default=False)

    def get_duration(self):
        return Service.query.get(self.service_id).duration

    def get_service(self):
        return Service.query.get(self.service_id).name

    def get_barber(self):
        return Barber.query.get(self.barber_id).username

    def __repr__(self):
        return '<Reservation {} {} {} {} minutes>'.format(self.client_email,
                                                          self.reservation_time,
                                                          self.get_barber(),
                                                          self.get_duration())
