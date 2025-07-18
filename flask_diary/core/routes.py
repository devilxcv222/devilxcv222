from flask import Blueprint, render_template
from datetime import date

from .calendar_api import get_events

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    today = date.today()
    events = get_events(today)
    return render_template('index.html', events=events, today=today)
