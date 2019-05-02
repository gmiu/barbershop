from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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


@login.user_loader
def load_user(id):
    return Barber.query.get(int(id))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    price = db.Column(db.String(10))
    reservations = db.relationship('Reservation', backref='service', lazy='dynamic')

    def __repr__(self):
        return '<Service {}>'.format(self.name)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time)
    client_first_name = db.Column(db.String(20))
    client_last_name = db.Column(db.String(20))
    client_phone = db.Column(db.String(10), index=True)
    client_email = db.Column(db.String(50), index=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('barber.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Reservation {}>'.format(self.client_email)
