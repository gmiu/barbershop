from app import db
from datetime import datetime


class Barber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(7), index=True, unique=True)
    reservations = db.relationship('Reservation', backref='barber', lazy='dynamic')

    def __repr__(self):
        return '<Barber {} {}>'.format(self.first_name, self.last_name)


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
