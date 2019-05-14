from flask import render_template
from app.email import send_email


def send_confirmation_email(reservation, barber, service):
    send_email('[Barbershop] Reservation confirmation {}'.format(
        reservation.reservation_time.strftime('%A, %b %d, %Y, %H:%M')),
               sender='no-reply@barbershop.com',
               recipients=[reservation.client_email],
               text_body=render_template('email/confirmation.txt',
                                         reservation=reservation, barber=barber, service=service),
               html_body=render_template('email/confirmation.html',
                                         reservation=reservation, barber=barber, service=service))
