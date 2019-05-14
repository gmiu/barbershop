from app import create_app, db
from app.models import Barber, Service, Reservation
from datetime import datetime, timedelta, date
from utils import create_hour, hour_generator
from app.main.email import send_confirmation_email

app = create_app()


@app.shell_context_processor
def make_shell_context():
    def admin():
        admin = Barber(username='admin', first_name='admin', last_name='admin')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()

    def set_barbers():
        barbers = [
            {
                'first_name': 'Ionut',
                'last_name': 'Oarga',
                'username': 'oarga'
            },
            {
                'first_name': 'Iulian',
                'last_name': 'Ivascu',
                'username': 'ivascu'
            },
            {
                'first_name': 'Laurentiu',
                'last_name': 'Codrescu',
                'username': 'codrescu'
            },
            {
                'first_name': 'Louis',
                'last_name': 'Gauta',
                'username': 'gauta'
            },
            {
                'first_name': 'Marius',
                'last_name': 'Manole',
                'username': 'manole'
            },
            {
                'first_name': 'Razvan',
                'last_name': 'Chira',
                'username': 'chira'
            },
            {
                'first_name': 'Sabin',
                'last_name': 'Pasol',
                'username': 'pasol'
            }
        ]

        barber_objects = [Barber(first_name=barber['first_name'],
                                 last_name=barber['last_name'],
                                 username=barber['username']) for barber in barbers]

        for barber in barber_objects:
            barber.set_password(barber.username)

        for barber in barber_objects:
            db.session.add(barber)

        db.session.commit()

    def set_services():
        services = [
            {
                'description': 'tuns + spalat + uscat + aranjat + styling + masaj capilar',
                'duration': 40,
                'name': 'Premium Haircut',
                'price': 45
            },
            {
                'description': 'tuns + spalat + aranjat + styling + uscat + tuns barba + '
                               'contur barba + spalat barba + apa colonie + aranjat + creme '
                               '+ lotiuni + masaj capilar',
                'duration': 50,
                'name': 'Superior Experience',
                'price': 75
            },
            {
                'description': 'tuns + spalat + aranjat + styling + uscat + tuns barba + '
                               'contur barba + spalat barba + apa colonie + vopsit barba + '
                               'aranjat + creme + lotiuni + consiliere + masaj capilar',
                'duration': 60,
                'name': 'Ultimate Experience',
                'price': 85
            },
            {
                'description': 'tuns barba + contur barba + spalat barba + apa colonie + '
                               'creme',
                'duration': 20,
                'name': 'Executive Beard',
                'price': 35}
        ]

        service_objects = [Service(name=service['name'],
                                   description=service['description'],
                                   duration=service['duration'],
                                   price=service['price']) for service in services]

        for service in service_objects:
            db.session.add(service)

        db.session.commit()

    def create_reservation():
        datetime_format = '%Y %m %d %H:%M'
        res = Reservation()
        res.reservation_time = datetime.strptime(input('reservation_time({})='.format(datetime_format)),
                                                 datetime_format)
        res.reservation_date = res.reservation_time.date()
        res.client_first_name = input('client_first_name=')
        res.client_last_name = input('client_last_name=')
        res.client_phone = input('client_phone=')
        res.client_email = input('client_email=')
        res.barber_id = input('barber_id=')
        res.service_id = input('service_id=')
        db.session.add(res)
        db.session.commit()

    def right_intervals(hours, duration):
        intervals = int(duration / 10)
        for i in range(len(hours)):
            if hours[i] > (create_hour('20:00', hours[i].date()) - timedelta(minutes=duration)):
                break
            if i + intervals > len(hours):
                break
            works = True
            for j in range(intervals):
                if hours[i + j] != hours[i] + timedelta(minutes=10 * j):
                    works = False
                    break
            if works:
                print('\t', hours[i])


    return {'db': db,
            'Barber': Barber,
            'Service': Service,
            'Reservation': Reservation,
            'admin': admin,
            'add_barbers': set_barbers,
            'add_services': set_services,
            'new_res': create_reservation,
            'hour_generator': hour_generator,
            'hour': create_hour,
            'intervals': right_intervals,
            'date': date,
            'datetime': datetime,
            'timedelta': timedelta,
            'send_confirmation_email': send_confirmation_email}
