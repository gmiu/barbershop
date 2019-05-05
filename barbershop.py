from app import create_app, db
from app.models import Barber, Service, Reservation


app = create_app()


@app.shell_context_processor
def make_shell_context():
    def admin():
        admin = Barber(username='admin', first_name='admin', last_name='admin')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

    return {'db': db,
            'Barber': Barber,
            'Service': Service,
            'Reservation': Reservation,
            'admin': admin}
