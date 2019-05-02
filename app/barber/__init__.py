from flask import Blueprint

bp = Blueprint('barber', __name__)

from app.barber import routes
