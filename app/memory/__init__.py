from flask import Blueprint

bp = Blueprint('memory', __name__)

from app.memory import routes
