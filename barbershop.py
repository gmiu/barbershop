from app import create_app, db
from app.models import Barber, Service, Reservation


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Barber': Barber,
            'Service': Service,
            'Reservation': Reservation}
