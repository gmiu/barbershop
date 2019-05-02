from app import db


class Barber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(7), index=True, unique=True)

    def __repr__(self):
        return '<Barber {}>'.format(self.username)
