from flask import (
    Blueprint, render_template
)
import os

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html',
                           title=os.environ.get('INDEX_TITLE') or "Grocery App")
