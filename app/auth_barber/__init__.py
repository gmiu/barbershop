from flask import Blueprint

bp = Blueprint('auth_barber', __name__)

from app.auth_barber import routes
